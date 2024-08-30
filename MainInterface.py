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
BLUE = (0, 0, 255)
BLACK = (0,0,0)

# 加载支持中文的字体
font = pygame.font.Font("font\msyh.ttf", 24)

# 按钮类
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return self.rect.collidepoint(event.pos)

# 创建主界面按钮
start_button = Button("开始游戏", screen_width - 150, screen_height - 200, 140, 40)
editor_button = Button("写谱模式", screen_width - 150, screen_height - 150, 140, 40)
settings_button = Button("设置", screen_width - 150, screen_height - 100, 140, 40)

buttons = [start_button, editor_button, settings_button]

# 主循环
running = True
while running:
    screen.fill(BLACK)  # 暂时使用蓝色背景代替背景图片

    # 绘制游戏名称
    title_surf = font.render("音乐游戏", True, WHITE)
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 50))

    # 绘制按钮
    for button in buttons:
        button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event):
                print("开始游戏按钮被点击")
                # 实现动画效果及切换到关卡选择
                # TODO: 添加动画和关卡选择界面
            elif editor_button.is_clicked(event):
                print("写谱模式按钮被点击")
                # 切换到写谱工具界面
                # TODO: 添加写谱工具界面
            elif settings_button.is_clicked(event):
                print("设置按钮被点击")
                # 切换到设置界面
                # TODO: 添加设置界面

    pygame.display.flip()
    pygame.time.Clock().tick(30)
