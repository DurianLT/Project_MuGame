import pygame
import sys
import time
import os

# 初始化Pygame
pygame.init()

# 可设置内容
FPS = 60  # 帧数
WIDTH, HEIGHT = 800, 600  # 屏幕尺寸
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project_MuGame")
note_speed = 300

# 颜色定义
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSLUCENT_BLACK = (0, 0, 0, 128)  # 半透明黑色

# 加载支持中文的字体
pixelFont24 = pygame.font.Font("font/HYPixel11pxJ-2.ttf", 24)

# 初始化时钟
clock = pygame.time.Clock()

##################################################################################################################################
# 功能类
##################################################################################################################################

# 按钮类 Button
class Button:
    def __init__(self, text, x, y, width, height, color, opacity=255):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.opacity = opacity

    def draw(self, screen):
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill((*self.color, self.opacity))
        screen.blit(surface, self.rect.topleft)

        text_surf = pixelFont24.render(self.text, True, WHITE)
        text_surf.set_alpha(self.opacity)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

# 键盘按钮类 KeyButton
class KeyButton:
    def __init__(self, key, lane, x, y, width, height):
        self.key = key
        self.lane = lane
        self.rect = pygame.Rect(x, y, width, height)
        self.is_pressed = False
        self.color_default = WHITE
        self.color_pressed = GRAY

    def draw(self, screen):
        color = self.color_pressed if self.is_pressed else self.color_default
        pygame.draw.rect(screen, color, self.rect)

        key_surf = pixelFont24.render(self.key, True, BLACK)
        key_rect = key_surf.get_rect(center=self.rect.center)
        screen.blit(key_surf, key_rect)

    def press(self):
        self.is_pressed = True

    def release(self):
        self.is_pressed = False

##################################################################################################################################
# 精灵类
##################################################################################################################################

class Note:
    def __init__(self, lane, color, start_time, end_time):
        self.lane = lane  # 滑道（0-3）
        self.color = color
        self.start_time = start_time
        self.end_time = end_time
        self.speed = note_speed  # 垂直速度（像素/秒）

        # 根据 start_time 和 end_time 计算音符的初始 y 位置和高度
        self.height = self.speed * ((self.end_time - self.start_time) / 1000)  # Note的高度
        self.y = -(self.speed*end_time/1000-550)

        self.width = WIDTH // 4 - 10  # Note的宽度

    def update(self, delta_time):
        # 更新y坐标，随时间下降
        self.y += self.speed * delta_time

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.lane * WIDTH // 4 + WIDTH // 8 - self.width // 2, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y > HEIGHT

    def is_on_judgment_line(self):
        return HEIGHT - 50 <= self.y + self.height <= HEIGHT - 40

##################################################################################################################################
# 界面类
##################################################################################################################################

# 主界面类
class MainScreen:
    def __init__(self):
        self.start_button = Button("开始游戏", WIDTH - 150, HEIGHT - 200, 140, 40, GRAY)
        self.editor_button = Button("写谱模式", WIDTH - 150, HEIGHT - 150, 140, 40, GRAY)
        self.settings_button = Button("设置", WIDTH - 150, HEIGHT - 100, 140, 40, GRAY)

        self.buttons = [self.start_button, self.editor_button, self.settings_button]

    def draw(self, screen):
        screen.fill(BLACK)
        title_surf = pixelFont24.render("音乐游戏", True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event):
                return "level_select"
            elif self.editor_button.is_clicked(event):
                return "editor"
            elif self.settings_button.is_clicked(event):
                return "settings"
        return None

# 关卡选择界面类
class LevelSelectScreen:
    def __init__(self):
        self.levels = ["新手教程", "Rush E"]
        self.current_index = 0
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.button_width = 300
        self.button_height = 60
        self.level_buttons = []
        self.back_button = Button("返回", 20, 20, 100, 40, GRAY)

    def draw(self, screen):
        screen.fill(BLACK)
        self.level_buttons.clear()
        self.back_button.draw(screen)
        for i in range(len(self.levels)):
            offset = i - self.current_index
            y = self.center_y + offset * (self.button_height + 10)
            opacity = max(50, 255 - abs(offset) * 100)
            button = Button(self.levels[i], self.center_x - self.button_width // 2, y, self.button_width, self.button_height, GRAY, opacity)
            button.draw(screen)
            self.level_buttons.append(button)

    def scroll(self, direction):
        self.current_index = max(0, min(len(self.levels) - 1, self.current_index + direction))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event):
                return "main"
            elif event.button == 4:
                self.scroll(-1)
            elif event.button == 5:
                self.scroll(1)
            else:
                for button in self.level_buttons:
                    if button.is_clicked(event):
                        return "game", button.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll(-1)
            elif event.key == pygame.K_DOWN:
                self.scroll(1)
        return None

# 游戏界面类
class GameScreen:
    def __init__(self, level_name):
        self.level_name = level_name
        self.start_time = time.time()
        self.total_paused_time = 0  # 总暂停时间
        self.paused_time = 0  # 当前暂停开始时间
        self.paused = False
        self.notes = []  # 用于存储生成的note
        self.judgment_line_y = HEIGHT - 50
        self.score = 0

        self.key_buttons = {
            pygame.K_a: KeyButton("A", 0, WIDTH // 8 - 50, HEIGHT - 40, 100, 40),
            pygame.K_s: KeyButton("S", 1, WIDTH // 8 * 3 - 50, HEIGHT - 40, 100, 40),
            pygame.K_k: KeyButton("K", 2, WIDTH // 8 * 5 - 50, HEIGHT - 40, 100, 40),
            pygame.K_l: KeyButton("L", 3, WIDTH // 8 * 7 - 50, HEIGHT - 40, 100, 40)
        }

        # 生成测试数据
        self.load_level_data()

        # 暂停菜单
        self.pause_menu = {
            "continue": Button("继续", WIDTH // 2 - 150, HEIGHT // 2 - 60, 140, 40, GRAY),
            "return": Button("返回", WIDTH // 2 - 150, HEIGHT // 2, 140, 40, GRAY),
            "settings": Button("设置", WIDTH // 2 - 150, HEIGHT // 2 + 60, 140, 40, GRAY)
        }

    def calculate_score(self, key):
        for note in self.notes:
            if note.is_on_judgment_line() and note.lane == self.key_buttons[key].lane:
                distance = abs(note.y + note.height - self.judgment_line_y)
                if distance < 10:  # Perfect
                    self.score += 100
                    print("Perfect!")
                elif distance < 20:  # Great
                    self.score += 50
                    print("Great!")
                elif distance < 30:  # Bad
                    self.score += 10
                    print("Bad!")
                self.notes.remove(note)
                return
        print("Miss!")


    # 修正后的时间解析方法
    def parse_time(self, time_str):
        # 拆分分钟、秒、毫秒
        minutes, seconds, milliseconds = map(int, time_str.split(":"))
        
        # 返回时间的总毫秒数
        return (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    
    def load_level_data(self):
        level_file = f"levels/{self.level_name}.txt"
        with open(level_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        level_name = lines[0].strip()
        music_path = lines[1].strip()
        note_data = lines[3:]  # 跳过第三行空行
        
        # 解析音符数据
        for line in note_data:
            parts = line.strip().split()
            note_type = parts[0]
            lane = int(parts[1])
            start_time = self.parse_time(parts[2])
            end_time = self.parse_time(parts[3])

            print(f"解析到音符 {line.strip()} 滑道 {lane} 开始时间 {start_time} 结束时间 {end_time}")

            color = BLUE if note_type == "NOTE" else BLUE if note_type == "HOLD" else YELLOW  # 根据类型选择颜色
            # 使用绝对时间（相对于游戏开始时间）
            self.notes.append(Note(lane, color, start_time, end_time))


    def format_time(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time * 1000) % 1000)
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

    def update_notes(self, delta_time):
        if not self.paused:
            for note in self.notes:
                note.update(delta_time)
                if note.is_off_screen():
                    self.notes.remove(note)
                elif note.is_on_judgment_line():
                    # 处理到达判定线的note
                    print(f"Note on lane {note.lane} reached the judgment line")

    def draw(self, screen):
        screen.fill(BLACK)
        # 绘制音符
        for note in self.notes:
            note.draw(screen)
        # Draw key buttons
        for key_button in self.key_buttons.values():
            key_button.draw(screen)

        # 绘制滑道分界线
        for i in range(1, 5):
            pygame.draw.line(screen, WHITE, (i * WIDTH // 4, 0), (i * WIDTH // 4, HEIGHT-50), 2)

        # 绘制判定线
        pygame.draw.line(screen, WHITE, (0, self.judgment_line_y), (WIDTH, self.judgment_line_y), 5)

        # 绘制屏幕边界和信息
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))  # 顶部空白区域

        # 计算显示时间
        if self.paused:
            elapsed_time = self.paused_time - self.start_time - self.total_paused_time
        else:
            elapsed_time = time.time() - self.start_time - self.total_paused_time

        time_surf = pixelFont24.render(f"关卡时间: {self.format_time(elapsed_time)}", True, WHITE)
        screen.blit(time_surf, (WIDTH - time_surf.get_width() - 10, 10))

        # 显示分数（示例）
        score_surf = pixelFont24.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_surf, (WIDTH - score_surf.get_width() - 10, 30))


        # 显示暂停按钮
        pause_button = Button("暂停", 10, 10, 100, 40, GRAY)
        pause_button.draw(screen)

        if self.paused:
            # 半透明覆盖层
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(TRANSLUCENT_BLACK)
            screen.blit(overlay, (0, 0))

            # 暂停菜单按钮
            for key, button in self.pause_menu.items():
                button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_buttons:
                self.key_buttons[event.key].press()
                self.calculate_score(event.key)
                print(f"Key {pygame.key.name(event.key).upper()} pressed")  # 打印按下的按键

        elif event.type == pygame.KEYUP:
            if event.key in self.key_buttons:
                self.key_buttons[event.key].release()
                print(f"Key {pygame.key.name(event.key).upper()} released")  # 打印松开的按键
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.paused:
                if self.pause_menu["return"].is_clicked(event):
                    return "level_select"
                elif self.pause_menu["continue"].is_clicked(event):
                    self.paused = False
                    self.total_paused_time += time.time() - self.paused_time
                elif self.pause_menu["settings"].is_clicked(event):
                    return "settings"
            else:
                if event.button == 1:
                    # 检查暂停按钮
                    pause_button = Button("暂停", 10, 10, 100, 40, GRAY)
                    if pause_button.is_clicked(event):
                        self.paused = True
                        self.paused_time = time.time()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # 按下 P 键暂停
                if self.paused:
                    self.paused = False
                    self.total_paused_time += time.time() - self.paused_time
                else:
                    self.paused = True
                    self.paused_time = time.time()
        return None

##################################################################################################################################
# 游戏主循环
##################################################################################################################################

main_screen = MainScreen()
level_select_screen = LevelSelectScreen()
game_screen = None
current_screen = "main"

running = True
while running:
    delta_time = clock.tick(FPS) / 1000  # 时间差，单位为秒

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # 根据当前界面处理事件
        if current_screen == "main":
            screen_switch = main_screen.handle_event(event)
            if screen_switch:
                current_screen = screen_switch

        elif current_screen == "level_select":
            result = level_select_screen.handle_event(event)
            if result:
                if isinstance(result, tuple):
                    current_screen, level_name = result
                    game_screen = GameScreen(level_name)
                else:
                    current_screen = result

        elif current_screen == "game":
            result = game_screen.handle_event(event)
            if result:
                current_screen = result

    # 更新并绘制当前屏幕
    if current_screen == "main":
        main_screen.draw(screen)

    elif current_screen == "level_select":
        level_select_screen.draw(screen)

    elif current_screen == "game":
        if not game_screen.paused:
            game_screen.update_notes(delta_time)
        game_screen.draw(screen)

    pygame.display.flip()

pygame.quit()

