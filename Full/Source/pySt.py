import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os
import json
import time

#Settings
with open("assets/options.json", "r") as f:
    opt = eval(f.read())
screen_size = width, height = opt["screen_size"]
fps = opt["fps"]
player_opt = opt["player_opt"]
bullet_opt = opt["bullet_opt"]
enemy_opt = opt["enemy_opt"]
enemy_per_second = enemy_opt["enemy_per_second"]
enemy_rate = fps / enemy_per_second
full_time = opt["time_mode"]["full_time"]
rate_mode_opt = opt["rate_mode"]

def load_png(name):
    '''加载图像并返回图像对象'''
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print("无法加载图片:", fullname)
        raise SystemExit(message)
    return image, image.get_rect()


class PhysicalObj(pygame.sprite.Sprite):
    '''
    class PhysicalObj
    用于存放Enemy和Bullet
    其实就是封装了一些常用操作的Sprite...
    '''

    #初始化
    def __init__(self, image_path, pos=(0, 0), v=(0, 0), a=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(image_path)
        self.set_pos(pos)
        self.v = v 
        self.a = a 
        self.bounce_times = 0

    #设置对象位置
    #这里的位置是图像rect中心位置
    def set_pos(self, pos):
        self.rect.center = pos

    def set_v(self, v):
        self.v = v

    def set_a(self, a):
        self.a = a

    #将对象blit在on_surface上
    def blit_on(self, on_surface):
        on_surface.blit(self.image, (self.rect.centerx, self.rect.centery)) 

    def move(self, dx):
        self.rect.move_ip(dx[0], dx[1])

    #由加速度计算速度
    def v_add(self, a):
        v = self.v
        self.v = v[0] + a[0], v[1] + a[1]

    #全物理计算
    def update(self):
        self.v_add(self.a)
        self.move(self.v)
        out_dead = self.try_out_dead() 
        if out_dead and player.alive:
            if is_bullet:
                player.get_score(bullet_opt["kill_score"])
            else:
                player.get_score(enemy_opt["kill_score"])

    def try_out_dead(self):
        if self.if_out_dead():
            self.kill()
            return True
        else:
            return False

    def if_out_dead(self):
        pos = self.rect.center
        if pos[0] < 0 or pos[1] < 0 or pos[0] > width or pos[1] > height:
            return True 
        else: 
            return False


class BouncyObj(PhysicalObj):
    """
    弹性Obj
    就是为了做反弹子弹
    """
    #初始化
    def __init__(self, image_path, pos=(0, 0), v=(0, 0), a=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(image_path)
        self.set_pos(pos)
        self.v = v 
        self.a = a 
        self.bounce_times = 0

    #反弹检测
    def try_bounce(self):
        pos = self.rect.center 
        #左右
        if pos[0] < 0 or pos[0] > width:
            self.v = -self.v[0], self.v[1]
            self.bounce_times += 1
        #上下
        if pos[1] < 0 or pos[1] > height:
            self.v = self.v[0], -self.v[1]
            self.bounce_times += 1

    def update(self):
        self.v_add(self.a)
        self.move(self.v)
        self.try_bounce()

class Enemy(PhysicalObj):
    """
    敌人类
    PhysicalObj的拓展，出屏扣分
    """
    def update(self, player):
        self.v_add(self.a)
        self.move(self.v)
        out_dead = self.try_out_dead() 
        if out_dead and player.alive:
            player.get_score(enemy_opt["kill_score"])
            player.shot -= 1

class Bullet(PhysicalObj):
    """
    普通子弹类
    PhysicalObj的拓展，出屏扣分
    """
    def update(self, player):
        self.v_add(self.a)
        self.move(self.v)
        out_dead = self.try_out_dead() 
        if out_dead and player.alive:
            player.get_score(bullet_opt["kill_score"])

class BouncyBullet(Bullet):
    def try_bounce(self, player):
        pos = self.rect.center 
        #左右
        if pos[0] < 0 or pos[0] > width:
            self.v = -self.v[0], self.v[1]
            self.bounce_times += 1
        #下
        if pos[1] > height:
            self.v = self.v[0], -self.v[1]
            self.bounce_times += 1
        if pos[1] < 0:
            self.kill()

    def update(self, player):
        self.v_add(self.a)
        self.move(self.v)
        self.try_bounce(player)



class Player(PhysicalObj):
    '''
    可移动对象
    差不多就是玩家...
    重要的是可以发射子弹！
    '''

    def __init__(self, image_path, pos=(0, 0), v=(0, 0), a=(0, 0), gamemode="0"):
        PhysicalObj.__init__(self, image_path, pos, v, a)
        self.z_cd, self.x_cd = 0, 0
        self.cds = {self.z_cd, self.x_cd}   
        self.score = player_opt["init_score"]     #计分板在这里！
        self.alive = True
        self.max = 0
        self.gamemode = gamemode
        #下面是rate_mode
        self.shot = 0
        self.generated = 0
        self.shot_rate = 1


    def update(self):
        PhysicalObj.update(self)
        self.cd_run()
        self.if_score_dead()


    #射击
    def shoot(self, bullet_image, bullet_list):
        if self.z_cd == 0:
            bullet_list.add( Bullet(bullet_image, pos=self.rect.midtop, v=(0, -5)) )
            self.z_cd = player_opt["z_cd"]

    def x_shoot(self, bullet_image, bullet_list):
        if self.x_cd == 0:
            bullet_list.add(
                Bullet(bullet_image, pos=self.rect.midtop, v=(0, -5)), 
                Bullet(bullet_image, pos=self.rect.midtop, v=(-4, -3)), 
                Bullet(bullet_image, pos=self.rect.midtop, v=(4, -3)), 
                Bullet(bullet_image, pos=self.rect.midtop, v=(-2, -4)), 
                Bullet(bullet_image, pos=self.rect.midtop, v=(2, -4)), 
                Bullet(bullet_image, pos=self.rect.midtop, v=(5, 0)), 
                Bullet(bullet_image, pos=self.rect.midtop, v=(-5, 0)), 
                )
            self.x_cd = player_opt["x_cd"]

    def cd_run(self):
        if self.z_cd > 0: self.z_cd -= 1
        if self.x_cd > 0: self.x_cd -= 1

    def get_score(self, num):
        self.score += num

    def get_shot_rate(self):
        self.shot_rate = self.shot / self.generated
        return self.shot_rate

    def if_score_dead(self):
        if self.score <= 0:
            self.alive = False

    def save_score(self, saving):
        with open("assets/ScoreRecord.txt", "a+") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f": {self.gamemode}: {saving}\n")

class PlayerOfBounce(Player):
    def shoot(self, bullet_image, bullet_list):
        if self.z_cd == 0:
            bullet_list.add(
                BouncyBullet(bullet_image, pos=self.rect.midtop, v=(-4, -3)),
                BouncyBullet(bullet_image, pos=self.rect.midtop, v=(4, -3))
            )


