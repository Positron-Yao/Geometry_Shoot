from pySt import *

def infinite_mode():
    #初始化
    pygame.init()
    init_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Test")

    #背景
    background = pygame.Surface(screen_size).convert()
    background.fill((64, 64, 64))
    screen.blit(background, (0, 0))

    #Enemy
    enemy_list = pygame.sprite.Group()

    #Bullet
    bullet_list = pygame.sprite.Group()
    
    #Player
    player = Player(player_opt["image"], pos=(width/2, height-8), gamemode="无尽模式")
    left, right = False, False

    player_list = pygame.sprite.Group(player)

    #时间管理
    time0 = 0
    ts = 0

    #文字
    font1 = pygame.font.Font(None, 48)
    font2 = pygame.font.Font("assets/LiShu.ttf", 24)
    over_text1 = font1.render(f"Game Over", True, (200, 200, 200))
    over_text2 = font2.render(f"纪录已保存", True, (200, 200, 200))

    quit = False

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            #退出
            if event.type == QUIT:
                player.save_score(f"\n\tScore: {player.max}")
                pygame.quit()
                quit = True

            if event.type == KEYDOWN:
                if event.key == 27:
                    player.save_score(f"\n\tScore: {player.max}")
                    pygame.quit()
                    quit = True

                #运动控制
                left = event.key == K_LEFT
                right = event.key == K_RIGHT
                #射击
                if event.unicode == "z":
                    player.shoot(bullet_opt["image"], bullet_list)
                if event.unicode == "x":
                    player.x_shoot(bullet_opt["image"], bullet_list)
            if event.type == KEYUP:
                #运动控制
                if event.key == K_LEFT:
                    left = False
                if event.key == K_RIGHT:
                    right = False

        if quit:
            break

    #玩家事件部分
        #移动操作
        if left:
            player.v = -5, 0
        elif right:
            player.v = 5, 0
        else:
            player.v = 0, 0

        if player.rect.center[0] <= 15 and player.v[0] < 0: player.v = (0, 0)
        if player.rect.center[0] >= width - 15 and player.v[0] > 0: player.v = (0, 0)

        if player.alive:
            player_list.update()
            player_list.draw(screen)
        else:
            screen.blit(over_text1, (width/2-100, height/2))
            screen.blit(over_text2, (width/2-70, height/2 + 30))


    #随机生成敌人
        if time0 // enemy_rate > ts:
            ts = time0 // enemy_rate
            enemy_list.add( Enemy(enemy_opt["image"], pos=(randint(20, width - 20), 20), v=(0, enemy_opt["v"])) )

    #自动事件部分 - 敌人&子弹的run和blit
        enemy_list.update(player)
        enemy_list.draw(screen)
        bullet_list.update(player)
        bullet_list.draw(screen)

    #碰撞检测
        cld_eb = pygame.sprite.groupcollide(enemy_list, bullet_list, 1, 1)
        cld_ep = pygame.sprite.groupcollide(enemy_list, player_list, 1, 0)

    #计分板
        if cld_eb:      #敌人与子弹碰撞
            player.get_score(player_opt["each_score"])
        if cld_ep:      #敌人与玩家碰撞
            player.get_score(enemy_opt["collide_score"])
        screen.blit(font1.render(f"Score: {player.score}", True, (200, 200, 200)), (10, 10))
        if player.max < player.score:
            player.max = player.score

    #帧更新部分
        pygame.display.update()
        init_clock.tick_busy_loop(fps)
        time0 += 1
        
def time_mode():
    #初始化
    pygame.init()
    init_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Test")

    #背景
    background = pygame.Surface(screen_size).convert()
    background.fill((64, 64, 64))
    screen.blit(background, (0, 0))

    #Enemy
    enemy_list = pygame.sprite.Group()

    #Bullet
    bullet_list = pygame.sprite.Group()
    
    #Player
    player = Player("Player1.png", pos=(width/2, height-8), gamemode="限时赛")
    left, right = False, False

    player_list = pygame.sprite.Group(player)

    #时间管理
    time0 = 0
    ts = -1

    #文字
    font1 = pygame.font.Font(None, 48)
    font2 = pygame.font.Font("assets/LiShu.ttf", 24)
    over_text1 = font1.render(f"Game Over", True, (200, 200, 200))
    over_text2 = font2.render(f"纪录已保存", True, (200, 200, 200))

    quit = False

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            #退出
            if event.type == QUIT:
                player.save_score(f"\n\tScore: {player.max}")
                pygame.quit()
                quit = True

            if event.type == KEYDOWN:
                if event.key == 27:
                    player.save_score(f"\n\tScore: {player.max}")
                    pygame.quit()
                    quit = True

                #运动控制
                left = event.key == K_LEFT
                right = event.key == K_RIGHT
                #射击
                if event.unicode == "z":
                    player.shoot(bullet_opt["image"], bullet_list)
                if event.unicode == "x":
                    player.x_shoot(bullet_opt["image"], bullet_list)
            if event.type == KEYUP:
                #运动控制
                if event.key == K_LEFT:
                    left = False
                if event.key == K_RIGHT:
                    right = False

        if quit:
            break

    #玩家事件部分
        #移动操作
        if left:
            player.v = -5, 0
        elif right:
            player.v = 5, 0
        else:
            player.v = 0, 0

        if player.rect.center[0] <= 15 and player.v[0] < 0: player.v = (0, 0)
        if player.rect.center[0] >= width - 15 and player.v[0] > 0: player.v = (0, 0)

        if player.alive:
            player_list.update()
            player_list.draw(screen)
        else:
            screen.blit(over_text1, (width/2-100, height/2))
            screen.blit(over_text2, (width/2-70, height/2 + 30))


    #随机生成敌人
        if time0 // enemy_rate > ts:
            ts = time0 // enemy_rate
            enemy_list.add( Enemy(enemy_opt["image"], pos=(randint(20, width - 20), 20), v=(0, enemy_opt["v"])) )

    #自动事件部分 - 敌人&子弹的run和blit
        enemy_list.update(player)
        enemy_list.draw(screen)
        bullet_list.update(player)
        bullet_list.draw(screen)

    #碰撞检测
        cld_eb = pygame.sprite.groupcollide(enemy_list, bullet_list, 1, 1)
        cld_ep = pygame.sprite.groupcollide(enemy_list, player_list, 1, 0)


    #计分板
        if cld_eb:      #敌人与子弹碰撞
            player.get_score(player_opt["each_score"])
        if cld_ep:      #敌人与玩家碰撞
            player.get_score(enemy_opt["collide_score"])
    #显示分数
        screen.blit(font1.render(f"Score: {player.score}", True, (200, 200, 200)), (10, 10))
        #记录最高分
        if player.max < player.score:
            player.max = player.score

    #限时部分
        if time0 // fps < full_time:
            screen.blit(font1.render(f"Time: {round(full_time - time0 / fps, 2)}", True, (200, 200, 200)), (width-200, 10))
        else:
            player.alive = False


    #帧更新部分
        pygame.display.update()
        init_clock.tick_busy_loop(fps)
        time0 += 1

def rate_mode():
    #初始化
    pygame.init()
    init_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Test")

    #背景
    background = pygame.Surface(screen_size).convert()
    background.fill((64, 64, 64))
    screen.blit(background, (0, 0))

    #Enemy
    enemy_list = pygame.sprite.Group()

    #Bullet
    bullet_list = pygame.sprite.Group()
    
    #Player
    player = PlayerOfBounce("Player1.png", pos=(width/2, height-8), gamemode="物理皇帝")
    left, right = False, False

    player_list = pygame.sprite.Group(player)

    #时间管理
    time0 = 0
    enemy_time_run = -1
    shoot_time_run = -1

    #文字
    font1 = pygame.font.Font(None, 48)
    font2 = pygame.font.Font("assets/LiShu.ttf", 24)
    over_text1 = font1.render(f"Game Over", True, (200, 200, 200))
    over_text2 = font2.render(f"纪录已保存", True, (200, 200, 200))

    quit = False

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            #退出
            if event.type == QUIT:
                player.save_score(f"\n\tScore: {player.max}  Hit Rate: {round(100 * player.get_shot_rate(), 2)}%")
                pygame.quit()
                quit = True

            if event.type == KEYDOWN:
                if event.key == 27:
                    player.save_score(f"\n\tScore: {player.max}  Hit Rate: {round(100 * player.get_shot_rate(), 2)}%")
                    pygame.quit()
                    quit = True

                #运动控制
                left = event.key == K_LEFT
                right = event.key == K_RIGHT
            if event.type == KEYUP:
                #运动控制
                if event.key == K_LEFT:
                    left = False
                if event.key == K_RIGHT:
                    right = False

        if quit:
            break

    #玩家事件部分
        #移动操作
        if left:
            player.v = -5, 0
        elif right:
            player.v = 5, 0
        else:
            player.v = 0, 0

        if player.rect.center[0] <= 15 and player.v[0] < 0: player.v = (0, 0)
        if player.rect.center[0] >= width - 15 and player.v[0] > 0: player.v = (0, 0)

        if player.alive:
            player_list.update()
            player_list.draw(screen)
        else:
            screen.blit(over_text1, (width/2-100, height/2))
            screen.blit(over_text2, (width/2-70, height/2 + 30))


    #随机生成敌人 & 发射子弹
        if time0 // enemy_rate > enemy_time_run:
            enemy_time_run = time0 // enemy_rate
            enemy_list.add( Enemy(enemy_opt["image"], pos=(randint(20, width - 20), 20), v=(0, enemy_opt["v"])) )
            player.generated += 1
            player.shot += 1
        if time0 // (fps / rate_mode_opt["shoot_per_second"]) > shoot_time_run:
            shoot_time_run = time0 // (fps / rate_mode_opt["shoot_per_second"])
            player.shoot(bullet_opt["image"], bullet_list)

    #自动事件部分 - 敌人&子弹的run和blit
        enemy_list.update(player)
        enemy_list.draw(screen)
        bullet_list.update(player)
        bullet_list.draw(screen)

    #碰撞检测
        cld_eb = pygame.sprite.groupcollide(enemy_list, bullet_list, 1, 1)
        cld_ep = pygame.sprite.groupcollide(enemy_list, player_list, 1, 0)


    #计分板
        if cld_eb:      #敌人与子弹碰撞
            player.get_score(player_opt["each_score"])
        if cld_ep:      #敌人与玩家碰撞
            player.get_score(enemy_opt["collide_score"])
    #显示分数
        screen.blit(font1.render(f"Score: {player.score}", True, (200, 200, 200)), (10, 10))
    #显示击破率
        screen.blit(font1.render(f"Hit Rate: {round(100 * player.get_shot_rate(), 2)}%", True, (200, 200, 200)), (10, 55))
    #记录最高分
        if player.max < player.score:
            player.max = player.score

    #显示时间
        screen.blit(font1.render(f"Time: {round(time0 / fps, 2)}", True, (200, 200, 200)), (width-200, 10))


    #帧更新部分
        pygame.display.update()
        init_clock.tick_busy_loop(fps)
        time0 += 1


if __name__ == '__main__':
    choose_text = """请选择模式：
1. 无尽模式
2. 限时赛
3. 物理皇帝
>>> """
    while True:
        try:
            choose = int(input(choose_text))
            if choose == 1:
                infinite_mode()
            elif choose == 2:
                time_mode()
            elif choose == 3:
                bouncy_mode()
        except ValueError:
            print("\n滚你妈，好好输！\n")