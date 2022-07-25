from pySt import *

def main():
    pygame.init()
    init_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Test")

    #背景
    background = pygame.Surface(screen_size).convert()
    background.fill((64, 64, 64))
    screen.blit(background, (0, 0))

    a = BouncyObj("Bullet1.png", pos=(100, 100), v=(4, 0), a=(0, 0.2))
    A = pygame.sprite.Group(a)

    quit = False

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            #退出
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == 27:
                    pygame.quit()
                    quit = True

        if quit:
            break

        A.update()
        A.draw(screen)

        pygame.display.update()
        init_clock.tick_busy_loop(fps)

if __name__ == '__main__':
    main()
