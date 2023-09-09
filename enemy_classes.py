import pygame as py
import math 
from random import randint as rint
from utils import *
from images import * 

delta = 1/80




class Enemy():
    def __init__(self,pos,game_vars):
        self.pos = pos
        self.hp = 100
        self.speed = 50 * delta
        self.vec = py.Vector2(0,0)
        self.white_time = 0
        self.size = 20
        self.dmg = 10

        self.velocity = py.Vector2(0,0)

        self.xp_amount = 5

        self.player, self.screen, self.cam, self.particles = game_vars

        self.weight = 1

    def take_dmg(self,dmg):

        self.hp -= dmg * self.player.dmg_modifier
        self.white_time = .2

        if not self.hp > 0:
            self.player.xp += self.xp_amount

    def attack(self):
        if (self.pos - self.player.pos).length() < self.size/2:
            self.hp = 0
            self.player.take_dmg(self.dmg)
    
    def debug_draw(self):
        py.draw.circle(self.screen,(21,21,21), self.pos, 5)

    def move(self):
        self.vec = self.player.pos - self.pos
        self.pos += self.vec.normalize() * self.speed

        self.velocity -= self.velocity * .9 * delta * 5
        self.pos += self.velocity

    def death_effect(self):
        for i in range(8):
            create_particles(self.pos.copy(),
                             py.Vector2(1,1).rotate(rint(0,360)) * rint(50,250) * delta + py.Vector2(0,-125*delta),
                             self.particles,
                             size=rint(5,20),
                             color="#000000")

class Square(Enemy):
    def __init__(self,pos,game_vars):
        Enemy.__init__(self,pos,game_vars)
        self.hp = 200
        self.speed = 50 * delta
        self.img = square
        self.size = 20
        self.dmg = 40

        self.xp_amount = 20

    def draw(self):
        img = py.transform.rotate(self.img, -math.atan2(self.vec.y, self.vec.x)/math.pi*180)

        if self.white_time > 0:
            self.white_time -= delta
            img = tint(img, (255,255,255))

        img.set_colorkey((0,0,0))
        self.screen.blit(img, self.pos - py.Vector2(1,1) * img.get_width()/2 - self.cam)

class SquareSmall(Square):
    def __init__(self,pos,game_vars):
        Enemy.__init__(self,pos,game_vars)
        self.hp = 110
        self.speed = rint(50,70) * delta
        self.img = squaresmall
        self.size = 10

class Chicken(Enemy):
    def __init__(self,pos,game_vars):
        Enemy.__init__(self,pos,game_vars)
        self.hp = 1
        self.pos = pos
        self.wing_open_timer = 0
        self.wings_open_for = 0
        self.imgs = []
        for i in range(2):
            surf = py.Surface((32,32))
            surf.blit(chicken,(-i*32,0))
            surf.set_colorkey((0,0,0))
            self.imgs.append(surf)
        self.xp_amount = 5

        self.direction = py.Vector2(1,1).rotate(rint(0,360)) * 3
        
    def draw(self):

        self.wing_open_timer -= delta
        if self.wing_open_timer <= 0:
            self.wing_open_timer = rint(3,10)
            self.wings_open_for = rint(0,20) * 0.1
            self.direction = py.Vector2(1,1).rotate(rint(0,360)) * 3

        img = self.imgs[0]
        if self.wings_open_for > 0:
            self.wings_open_for -= delta
            img = self.imgs[1]

        self.screen.blit(img, self.pos - py.Vector2(16,16) - self.cam)

    def move(self):
        self.pos += self.direction * delta

    def attack(self):
        pass

    def take_dmg(self,dmg):
        self.hp -= dmg * self.player.dmg_modifier

        if not self.hp > 0:
            self.player.xp += self.xp_amount

class BladeGuy(Enemy):
    def __init__(self,pos,game_vars):
        Enemy.__init__(self,pos,game_vars)
        self.hp = 70
        self.speed = rint(80,100) * delta
        self.xp_amount = 15
        self.dmg = 30
        self.frames = blader_frames

        self.frame = 0
        self.timer = 0
        self.frame_no = 4
        self.framerate = 40

    def draw(self):
        self.timer += delta
        if self.timer > 1/self.framerate:
            self.timer = 0
            self.frame += 1
            if self.frame >= self.frame_no:
                self.frame = 0
            
        img = self.frames[self.frame]

        if self.white_time > 0:
            self.white_time -= delta
            img = tint(img, (255,255,255))


        self.screen.blit(img, self.pos-py.Vector2(16,16)-self.cam)

class Pekka(Enemy):
    def __init__(self,pos,game_vars):
        Enemy.__init__(self,pos,game_vars)
        self.hp = 500
        self.speed = 60 * delta
        self.size = 64
        self.dmg = 70

        self.xp_amount = 100

        self.frames = pekka_frames
        self.sword_frames = pekka_sword_frames

        self.frame = 0
        self.timer = 0
        self.frame_no = 4
        self.framerate = 10

        self.attack_frame = 0
        self.attack_timer = 0
        self.attack_rate = .5

        self.no_attack_timer = 0

        self.weight = 20

    def draw(self):
        self.timer += delta
        if self.timer > 1/self.framerate:
            self.timer = 0
            self.frame += 1
            if self.frame >= self.frame_no:
                self.frame = 0
            
        img = self.frames[self.frame]

        if self.vec.x > 0:
            img = py.transform.flip(img,1,0).convert_alpha()

        if self.white_time > 0:
            self.white_time -= delta
            img = tint(img, (255,255,255))


        self.screen.blit(img, self.pos-py.Vector2(1,1)*self.size-self.cam)
        
            
    def attack(self):
        self.attack_timer += delta
        if self.attack_timer > 1/self.attack_rate and self.attack_frame == 0:
            self.attack_timer = 0
            self.attack_frame = 1

        if self.timer > 1/self.framerate-delta and self.attack_frame != 0:
            self.attack_frame += 1
            if self.attack_frame > len(self.sword_frames)-1:
                self.attack_frame = 0

            if self.no_attack_timer <= 0:
                if abs(self.pos.x - self.player.pos.x) < self.size * 2:
                    if abs(self.pos.y - self.player.pos.y) < self.size:
                        self.player.take_dmg(self.dmg)
                        self.no_attack_timer = .5
            else:
                self.no_attack_timer -= delta

        img = self.sword_frames[self.attack_frame]
        if self.vec.x > 0:
            img = py.transform.flip(img,1,0).convert_alpha()

        self.screen.blit(img, self.pos-py.Vector2(1,1)*self.size*2-self.cam)

class Snake(Enemy):
    def __init__(self,pos,game_vars):
        Enemy.__init__(self,pos,game_vars)
        self.hp = 1000
        self.speed = rint(80,100) * delta
        self.xp_amount = 500
        self.dmg = 30
        self.headimg = snake_head
        self.segmentimg = snake_segment
        self.tailimg = snake_tail

        self.rotation = 0

        self.segments = []
        for i in range(9):
            segment = [self.pos + py.Vector2(-20*i), 0]
            self.segments.append(segment)
        self.no_dmg_time = 0
        self.tail_attack = False
        self.tail_inactive = 0

    def draw(self):

        head = py.transform.rotate(self.headimg, self.rotation)
       
        if self.white_time > 0:
            self.white_time -= delta
            head = tint(head, (255,255,255))

        head.set_colorkey((0,0,0))
        self.screen.blit(head, self.pos - py.Vector2(1,1)*head.get_width()/2 - self.cam)

        idx = 0
        for i in self.segments:
            if idx == len(self.segments)-1:
                segment = py.transform.rotate(self.tailimg, i[1])

            else:
                segment = py.transform.rotate(self.segmentimg, i[1])

            if self.white_time > 0:
                segment = tint(segment, (255,255,255))

            segment.set_colorkey((0,0,0))
            self.screen.blit(segment, i[0] - py.Vector2(1,1)*segment.get_width()/2 - self.cam)
            idx += 1

    def attack(self):

        if self.no_dmg_time > 0:
            self.no_dmg_time -= delta

        self.tail_attack = False

        tail = self.segments[len(self.segments)-1]

        if self.tail_inactive > 0:
            self.tail_inactive -= delta

        distance = (tail[0] - self.player.pos).length()
        if distance < 150 and not self.tail_inactive > 0:
            tail[0] -= (tail[0] - self.player.pos) * delta * 2
            self.tail_attack = True
            if distance < 40:
                self.player.take_dmg(self.dmg)
                self.tail_inactive = 5
        else:
            distance = (self.pos - self.player.pos).length()
            if distance < 250:
                self.speed = 100 * delta
            else:
                self.speed = 60 * delta
            
        
        if distance < self.size/2 and self.no_dmg_time <= 0:
            self.player.take_dmg(self.dmg)
            self.no_dmg_time = .5
    
    def move(self):

        if self.tail_attack:

            tail = self.segments[len(self.segments)-1]

            vec = self.player.pos - tail[0]
            tail[1] = -math.atan2(vec.y, vec.x)/math.pi*180+180


            idx = 0
            for i in self.segments:
                if idx == 0:
                    vec = (self.pos- i[0])
                    self.pos -= vec * delta * 2
                if i != tail:
                    vec = (self.segments[idx+1][0] - i[0])
                    i[0] += vec * delta * 2
                    i[1] = -math.atan2(vec.y, vec.x)/math.pi*180

                idx += 1

        else:
            vec = self.player.pos - self.pos
            self.rotation = -math.atan2(vec.y, vec.x)/math.pi*180

            self.pos += vec.normalize() * self.speed

            idx = 0
            for i in self.segments:
                if idx == 0:
                    vec = (self.pos- i[0])
                    i[0] += vec * delta * 2
                else:
                    vec = (self.segments[idx-1][0] - i[0])
                    i[0] += vec * delta * 2
                idx += 1

                i[1] = -math.atan2(vec.y, vec.x)/math.pi*180

        self.velocity -= self.velocity * .9 * delta * 5
        self.pos += self.velocity


