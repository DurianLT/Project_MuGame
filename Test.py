import pygame
pygame.init()

# 创建一个简单的窗口
screen = pygame.display.set_mode((640, 480))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("A key was pressed")
            elif event.key == pygame.K_s:
                print("S key was pressed")
            elif event.key == pygame.K_k:
                print("K key was pressed")
            elif event.key == pygame.K_l:
                print("L key was pressed")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                print("A key was released")
            elif event.key == pygame.K_s:
                print("S key was released")
            elif event.key == pygame.K_k:
                print("K key was released")
            elif event.key == pygame.K_l:
                print("L key was released")

pygame.quit()
