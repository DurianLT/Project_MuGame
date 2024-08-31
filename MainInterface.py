import pygame
import sys

# 初始化Pygame
pygame.init()

# 屏幕尺寸
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("音乐游戏")

# 颜色定义
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# 加载支持中文的字体
pixelFont24 = pygame.font.Font("font/HYPixel11pxJ-2.ttf", 24)

# 按钮类
class Button:
    def __init__(self, text, x, y, width, height, opacity=255):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.opacity = opacity

    def draw(self, screen):
        # 设置颜色的透明度
        color_with_opacity = (*self.color, self.opacity)
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill(color_with_opacity)
        screen.blit(surface, self.rect.topleft)

        text_surf = pixelFont24.render(self.text, True, WHITE)
        text_surf.set_alpha(self.opacity)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

# 主界面类
class MainScreen:
    def __init__(self):
        self.start_button = Button("开始游戏", screen_width - 150, screen_height - 200, 140, 40)
        self.editor_button = Button("写谱模式", screen_width - 150, screen_height - 150, 140, 40)
        self.settings_button = Button("设置", screen_width - 150, screen_height - 100, 140, 40)
        self.buttons = [self.start_button, self.editor_button, self.settings_button]

    def draw(self, screen):
        screen.fill(BLACK)  # 使用黑色背景代替背景图片
        title_surf = pixelFont24.render("音乐游戏", True, WHITE)
        screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 50))
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
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        self.button_width = 300
        self.button_height = 60
        self.level_buttons = []  # 存储关卡按钮实例

        # 返回按钮
        self.back_button = Button("返回", 20, 20, 100, 40)

    def draw(self, screen):
        screen.fill(BLACK)
        self.level_buttons.clear()  # 每次绘制前清空按钮列表

        # 绘制返回按钮
        self.back_button.draw(screen)

        # 绘制关卡选择按钮
        for i in range(len(self.levels)):
            # 计算每个按钮的y坐标，中心按钮在正中央，上下的按钮逐渐远离中心
            offset = i - self.current_index
            y = self.center_y + offset * (self.button_height + 10)
            opacity = max(50, 255 - abs(offset) * 100)  # 远离中心的按钮透明度降低

            button = Button(self.levels[i], self.center_x - self.button_width // 2, y, self.button_width, self.button_height, opacity)
            button.draw(screen)
            self.level_buttons.append(button)  # 存储按钮实例

    def scroll(self, direction):
        # direction: -1为向上滚动，1为向下滚动
        self.current_index = max(0, min(len(self.levels) - 1, self.current_index + direction))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event):
                return "main"  # 点击返回按钮返回主界面
            elif event.button == 4:  # 滚轮向上
                self.scroll(-1)
            elif event.button == 5:  # 滚轮向下
                self.scroll(1)
            else:
                for button in self.level_buttons:
                    if button.is_clicked(event):
                        print(f"选择了{button.text}关卡")  # 实现点击效果
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll(-1)
            elif event.key == pygame.K_DOWN:
                self.scroll(1)
        return None

# 初始化界面
main_screen = MainScreen()
level_select_screen = LevelSelectScreen()

# 当前界面状态
current_screen = "main"

# 主循环
running = True
while running:
    if current_screen == "main":
        main_screen.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen_switch = main_screen.handle_event(event)
            if screen_switch:
                current_screen = screen_switch

    elif current_screen == "level_select":
        level_select_screen.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen_switch = level_select_screen.handle_event(event)
            if screen_switch:
                current_screen = screen_switch

    pygame.display.flip()
    pygame.time.Clock().tick(30)
