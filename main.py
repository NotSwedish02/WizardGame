import pygame as py
import math 
from random import randint as rint
from utils import *
from images import * 

from enemy_classes import *


py.init()
py.font.init()

font = py.font.Font("Kenney Mini.ttf")
smallfont = py.font.Font("Kenney Mini.ttf",12)

display = py.display.set_mode((800,600))

screen = py.Surface((800,600))

fps = 80
delta = 1/fps




class Player():
    def __init__(self,x,y):

        #Movement

        self.pos = py.Vector2(x,y)
        self.keys = {
            py.K_w: py.Vector2(0,-1),
            py.K_a: py.Vector2(-1,0),
            py.K_s: py.Vector2(0,1),
            py.K_d: py.Vector2(1,0)
        }

        self.velocity = py.Vector2(0,0)
        self.force = py.Vector2(0,0)

        #Animation

        self.speed = 5 * delta
        self.spritesheet = load("mage1")
        self.spritesheet2 = load("mage2")
        self.spritesheet3 = load("mage3")

        self.frames = []
        for i in range(8):
            surf = py.Surface((32,32))
            surf.blit(self.spritesheet,(-i*32,0))
            surf.set_colorkey((0,0,0))
            self.frames.append(surf)

        self.frames2 = []
        for i in range(8):
            surf = py.Surface((32,32))
            surf.blit(self.spritesheet2,(-i*32,0))
            surf.set_colorkey((0,0,0))
            self.frames2.append(surf)

        self.frames3 = []
        for i in range(8):
            surf = py.Surface((32,32))
            surf.blit(self.spritesheet3,(-i*32,0))
            surf.set_colorkey((0,0,0))
            self.frames3.append(surf)


        self.current_frames = self.frames

        self.flip_h = False
        self.frame = 0
        self.timer = 0
        self.frame_no = 4
        self.framerate = 10

        #Spells

        self.spell_list = []
        self.spell_list.append(all_spells[rint(0,len(all_spells)-1)]) 
        self.cast_queue = []

        self.cast_queue_pos = py.Vector2(220,520)

        for i in range(5):
            self.cast_queue.append(self.spell_list[rint(0,len(self.spell_list)-1)])

        self.cast_timer = 2
        self.cast_time = 2

        self.spell_functions = {
            "FireRing": fire_ring,
            "Thunder": thunder,
            "Dart": throw_darts,
            "Blast": blast,
            "Chicken": chicken_spell,
            "Ignite": ignite
        }

        self.spell_prediction = {
            "FireRing": fire_prediction,
            "Thunder": thunder_prediction,
            "Dart": dart_prediction,
            "Blast": blast_prediction,
            "Chicken": chicken_prediction,
            "Ignite": ignite_prediction
        }

        self.spell_levels = {
            "FireRing": 1,
            "Thunder": 1,
            "Dart": 1,
            "Blast": 1,
            "Chicken": 1,
            "Ignite": 1
        }

        self.xp = 100
        self.level = 0

        self.xp_pos =  py.Vector2(50,50)

        #UI

        self.spell_bar_pos = py.Vector2(720,20)
        self.spell_images = {
            "Dart": load("darticon",scale=1.5),
            "FireRing": load("ringfireicon",scale=1.5),
            "Thunder": load("thundericon",scale=1.5),
            "Blast": load("fireblasticon",scale=1.5),
            "Chicken": load("chickenicon",scale=1.5),
            "Ignite": load("igniteicon",scale=1.5),

        }

        self.cast_queue_moving = 0
        self.last_added = ""

        #Hp

        self.hp = 100
        self.hp_pos = py.Vector2(20,50)
        self.jiggle_timer = 0

        #Staff
        self.staff = staffimg

        #Options
        self.picking_option = False
        self.possible_spells = []

        self.xp_steps = {
            0: 50,
            1: 75,
            2: 100,
            3: 150,
            4: 300,
            5: 400,
            6: 400,
            7: 400,
            8: 450,
            9: 450,
            10: 700
        }
        for i in range(90):
            self.xp_steps[i+11] = 2000
        
        self.dmg_modifier = 1

    def barrier(self, screen):
        py.draw.circle(screen, (100,0,0), (400,300) - cam, 600, 3)
        if (self.pos - py.Vector2(400,300)).length() > 600:
            self.hp -= 5 * delta
    
    def draw(self):

        self.timer += delta
        if self.timer > 1/self.framerate:
            self.timer = 0
            self.frame += 1
            if self.frame >= self.frame_no:
                self.frame = 0

        if self.flip_h:
            img = self.current_frames[self.frame+4]
        else:
            img = self.current_frames[self.frame]
            
      
        screen.blit(img, self.pos-py.Vector2(16,16) - cam)

        if self.cast_timer <= self.cast_time * .7:
            coming_spell = self.cast_queue[0]
            coming_spell_level = self.spell_levels[coming_spell]
            self.spell_prediction[coming_spell](coming_spell_level)

        #Staff
        vec = self.pos - py.mouse.get_pos() - cam
        mouse_ag = -math.atan2(vec.y, vec.x)/math.pi*180 + 135
        staff = py.transform.rotate(self.staff, mouse_ag)
        staff.set_colorkey((0,0,0))
        screen.blit(staff, self.pos-py.Vector2(1,1)*staff.get_width()/2-vec*0.8-cam)

        for enemy in enemies:
            if enemy.weight == 1:
                if (enemy.pos - (self.pos-vec*0.8-vec.normalize()*15)).length() < 20+enemy.size/2:
                    enemy.take_dmg(5)
                    enemy.velocity -= vec.normalize() * 3 
                    create_light(enemy.pos,lightimg,lights,scale=3)

        #py.draw.circle(screen, (100,100,200), self.pos-vec*0.4-vec.normalize()*15, 20)

    def render_UI(self):

        for i in range(8):
            screen.blit(spellslotimg, self.spell_bar_pos + py.Vector2(0,i*63))

        idx = 0
        for i in self.spell_list:
            pos = self.spell_bar_pos + py.Vector2(0,idx*63) + py.Vector2(6,6)
            screen.blit(self.spell_images[i], pos)
            txt = smallfont.render("Lvl. " + str(self.spell_levels[i]), True, (0,0,0))
            screen.blit(txt, pos + py.Vector2(0,35))
            idx += 1

        if self.cast_queue_moving > 0:
            self.cast_queue_moving -= delta
            

        idx = 0
        for i in self.cast_queue:
            pos = self.cast_queue_pos + py.Vector2(-idx*63,0) + py.Vector2(-self.cast_queue_moving,0) * 63 / .2
            screen.blit(spellslotimg, pos)
            screen.blit(self.spell_images[i], pos + py.Vector2(6,6))
            idx += 1
        
        #Level
        txt = font.render("Level. " + str(self.level),True,(0,0,0))
        screen.blit(txt,(10,0))
        #Hp
        hpsurf = py.Surface((50,200))
        hpsurf.set_colorkey((0,0,0))
        points = [py.Vector2(10,120-self.hp) + py.Vector2(i,math.sin((i+self.jiggle_timer)/18*math.pi*2) * 2.5) for i in range(18)]
        points.append(py.Vector2(25,120-self.hp + 2.5))
        points.append(py.Vector2(10,120-self.hp + 2.5))

        py.draw.polygon(hpsurf, (200,0,0), points)
        self.jiggle_timer += delta * 20

        py.draw.rect(hpsurf, (200,0,0), (py.Vector2(10,120-self.hp), (18,self.hp-10)))

        hpsurf.blit(hpframe,(0,0))
        screen.blit(hpsurf, self.hp_pos)

        #XP

        xp_show_value = self.xp/self.xp_steps[self.level]*100
        XPsurf = py.Surface((50,200))
        XPsurf.set_colorkey((0,0,0))
        points = [py.Vector2(10,110-xp_show_value) + py.Vector2(i,math.sin((i+self.jiggle_timer)/18*math.pi*2) * 2.5) for i in range(18)]
        points.append(py.Vector2(25,110-xp_show_value + 2.5))
        points.append(py.Vector2(10,110-xp_show_value + 2.5))

        py.draw.polygon(XPsurf, (55,55,200), points)
        self.jiggle_timer += delta * 20

        py.draw.rect(XPsurf, (55,55,200), (py.Vector2(10,110-xp_show_value), (18,xp_show_value-10)))

        XPsurf.blit(xpframe,(0,0))
        screen.blit(XPsurf, self.xp_pos)

        #Kills
        screen.blit(square_dead_icon, (20,20))
        global enemies_killed
        txt = font.render(str(enemies_killed), False, (0,0,0))
        screen.blit(txt,(50,20))

    def level_up(self):
        if self.xp >= self.xp_steps[self.level]:
            self.xp -= self.xp_steps[self.level]
            self.level += 1

            if self.level == 10:
                self.current_frames = self.frames2
                self.dmg_modifier = 1.5
                self.speed = 7 * delta
                self.cast_time = 1.5

            if self.level == 20:
                self.current_frames = self.frames3
                self.dmg_modifier = 2
                self.speed = 10 * delta
                self.cast_time = .8

            self.possible_spells = []
            for i in range(3):
                choice = all_spells[rint(0,len(all_spells)-1)]
                count = 0
                while choice in self.possible_spells and count < 5:
                    count += 1
                    choice = all_spells[rint(0,len(all_spells)-1)]

                self.possible_spells.append(choice)

            global paused
            global screenshot
            paused = True
            screenshot = screen.copy()

            self.picking_option = True

    def skill_menu(self,click):
        py.draw.rect(screen, (21, 21, 21), (400-250,300-150,500,300))

        for i in range(3):

            spell = self.possible_spells[i]

            new_spell = False
            if spell not in self.spell_list:
                new_spell = True

            choice_surf = py.Surface((200,80))
            if new_spell:
                choice_surf.fill((55,55,85))
            else:
                choice_surf.fill((85,125,85))


            hovering_over = False
            
            mox, moy = py.mouse.get_pos()
            if abs(mox - (250)) < 100 and abs(moy - (190 + 100*i)) < 40:
                if new_spell:
                    choice_surf.fill((155,155,185))
                else:
                    choice_surf.fill((185,225,185))
                hovering_over = True

        
            spellimg = all_spell_icons[spell]
            choice_surf.blit(spellimg, (10,10))

            if new_spell:
                txt = font.render("New spell!", True, (255,255,255))
            else:
                txt = font.render("Level up!", True, (255,255,255))

            choice_surf.blit(txt, (70,20))

            screen.blit(choice_surf, (400-250 + 10,300-150 + 10 + 100*i))

                
            if hovering_over and click:
                if spell not in self.spell_list:
                    self.spell_list.append(spell)
                else:
                    self.spell_levels[spell] += 1
                global paused
                paused  = False

                self.picking_option = False

    def cast(self):
        self.cast_timer -= delta
        if self.cast_timer <= 0:
            self.cast_timer = self.cast_time
            self.cast_queue_moving = .2

            coming_spell = self.cast_queue[0]
            self.spell_functions[coming_spell]()

            del self.cast_queue[0]

            spell = self.spell_list[rint(0,len(self.spell_list)-1)]
            while spell == self.last_added and len(self.spell_list) > 1:
                spell = self.spell_list[rint(0,len(self.spell_list)-1)]
            self.cast_queue.append(spell)
            self.last_added = spell

    def move(self):

        
        try:
            self.velocity += self.force.normalize()
        except:
            pass
        self.pos += self.velocity * self.speed

        self.velocity -= self.velocity * 0.9 * delta * 5

    def input(self,key,is_pressed):
        if self.hp > 0:
            if key in self.keys.keys():
                if is_pressed:
                    self.force += self.keys[key]
                    self.flip_h = sign(-self.force.x)
                else:
                    self.force -= self.keys[key]
            if key == py.K_p and is_pressed:
                global paused
                global screenshot
                paused = not paused
                screenshot = screen.copy()
        else:
            if key == py.K_r:
                global run
                run = False
                self.force *= 0
                game()

    def take_dmg(self,dmg):
        self.hp -= dmg
        self.white_time = .2



#Spell objects
class Thunder():
    def __init__(self,pos,lvl):
        self.pos = pos
        self.points = []
        self.change_timer = 0
        self.lifetime = .6
        self.dmg = 4 + lvl * 1

    def draw(self):
        if self.change_timer <= 0:
            self.points = [self.pos]
            for i in range(9):
                p = self.pos + py.Vector2(0,-100) * i
                p += py.Vector2(rint(-50,50), rint(-20,20))
                self.points.append(p)
            self.change_timer = rint(2,8) * .01

        self.change_timer -= delta
        self.lifetime -= delta
            
        for i in range(len(self.points)-2):
            py.draw.line(screen, (255,255,255), self.points[i]-cam, self.points[i+1]-cam, i*2+3)
        create_light(player.pos,lightimg,lights,scale=rint(2,10))

    def damage(self):
        for i in enemies:
            if py.Vector2(i.pos - player.pos).length() < 80:
                i.take_dmg(self.dmg)

class Spawner():
    def __init__(self,pos, awake_point):
        self.pos = pos
        self.frame = 0
        self.frame_timer = 0
        self.framerate = 10

        self.frames = []
        self.spritesheet = load("spawner")

        for i in range(4):
            surf = py.Surface((64,64))
            surf.blit(self.spritesheet,(-i*64,0))
            surf.set_colorkey((0,0,0))
            self.frames.append(surf)

        self.spawn_timer = 2
        self.spawnrate = .5

        self.awake = False
        self.awake_point = awake_point

        self.idle_frame_no = rint(0,3)

    def draw(self):
        self.frame_timer += delta
        if self.frame_timer > 1/self.framerate:
            self.frame_timer = 0
            self.frame += 1
            if self.frame > len(self.frames)-1:
                self.frame = 0

        screen.blit(self.frames[self.frame], self.pos - py.Vector2(32,32) - cam)

    def spawn(self):
        self.spawn_timer += delta

        if self.spawn_timer > 1/self.spawnrate and len(enemies) < 75:
            self.spawn_timer = 0
            if self.spawnrate < 1:
                self.spawnrate += .01

            rand_no = rint(0,200)
            if rand_no == 0: #.5% chance of pekka
                enemy = Pekka(self.pos.copy(),game_vars)
                enemies.append(enemy)
            elif rand_no == 1: #.5% chance of snake
                enemy = Snake(self.pos.copy(),game_vars)
                enemies.append(enemy)
            elif rand_no <= 40: #20% chance of square
                enemy = Square(self.pos.copy(),game_vars)
                enemies.append(enemy)
            elif rand_no <= 100: #30% chance of blader
                enemy = BladeGuy(self.pos.copy(),game_vars)
                enemies.append(enemy)
            else: #48% chance of small square
                enemy = SquareSmall(self.pos.copy(),game_vars)
                enemies.append(enemy)

    def draw_idle(self):
        screen.blit(self.frames[self.idle_frame_no], self.pos - py.Vector2(32,32) - cam)

class Dart():
    def __init__(self,pos,target,lvl):
        self.pos = pos
        self.target = target
        self.velocity = py.Vector2(1,1).rotate(rint(0,360)/180*math.pi) * 100 * delta
        self.kill_switch = False
        self.dmg = 10+lvl*6

    def draw(self):
        points = [self.pos - cam]
        points.append(self.pos - self.velocity - cam)
        points.append(self.pos - self.velocity*5 + self.velocity.rotate(math.pi*.5)*.4 - cam)
        points.append(self.pos - self.velocity*5 - self.velocity.rotate(math.pi*.5)*.4 - cam)

        py.draw.polygon(screen, (255,255,255), points)

        create_particles(self.pos.copy(), py.Vector2(1,1).rotate(rint(0,360)/180*math.pi) * 20 * delta, particles,
                            size=rint(2,10), type_="square")
    
    def move(self):
        self.velocity -= self.velocity * .9 * 2 * delta
        self.velocity += (self.target.pos - self.pos).normalize() * 70 * delta

        self.pos += self.velocity

    def hit(self):
        if (self.target.pos - self.pos).length() < self.target.size/2:
            self.target.take_dmg(self.dmg)
            self.kill_switch = True

class Blast():
    def __init__(self,lvl):
        self.pos = player.pos
        self.time = 1
        self.vec = None
        self.width = 25+5*lvl
        self.dmg = .25 + .25*lvl

    def draw(self):

        self.vec = py.mouse.get_pos() + cam - self.pos
       
        color = change_rgb_val(hex_to_rgb("#ff4914"),rint(-10,10)*0.01,0,0)
        for i in range(1):
            create_particles(self.pos.copy(), self.vec.normalize().rotate(rint(-5,5)) * rint(2000,3000) * delta,particles, color=color, size=rint(10,30), type_="square", angle=rint(0,360)/180*math.pi)
        self.time -= delta

    def hit(self):
        for enemy in enemies:
            #y = mx + b
        
            m = (self.pos.y - (self.pos.y + self.vec.y))/(self.pos.x - (self.pos.x + self.vec.x))
            b = self.pos.y - self.pos.x * m
            if m != 0:
                m2 = -1/m
                b2 = enemy.pos.y - enemy.pos.x * m2

                
                x = (b2- b) / (m - m2)
                y = m*x + b

                if (py.Vector2(x,y) - enemy.pos).length() < self.width:
                    enemy.take_dmg(self.dmg)

class Fragment():
    def __init__(self,pos,velocity,img_no,exception_):
        self.pos = pos
        self.velocity = velocity
        self.img = fragments_imgs[img_no]
        self.kill_switch = False
        self.exception_ = exception_

        self.time = 2

    def draw(self):
        screen.blit(self.img, self.pos - py.Vector2(32,32) - cam)
        pos = self.pos
        vec = py.Vector2(1,1)

        if rint(0,1) == 0:
            for i in range(1):
                color = change_rgb_val((200,55,155),rint(-10,10)*0.01,0,0)
                create_particles(pos.copy(), vec.rotate(rint(0,360)) * rint(50,300) * delta,particles, color=color, size=rint(2,5), type_="square", angle=rint(0,360)/180*math.pi)
        

    def move(self):
        self.pos += self.velocity

    def hit(self):
        self.time -= delta
        if self.time <= 0:
            self.kill_switch = True
        for enemy in enemies:
            if enemy != self.exception_:
                if abs(self.pos.x - enemy.pos.x) < 16 and abs(self.pos.y - enemy.pos.y) < 16:
                    self.kill_switch = True
                    enemy.take_dmg(15)



def test_spell():
    for i in range(10):
        ag = rint(0,360)/180*math.pi
        mod = rint(5,50) * delta
        create_particles(player.pos.copy(), py.Vector2(math.cos(ag),particles, math.sin(ag)) * mod)

def fire_ring():

    lvl = player.spell_levels["FireRing"]

    for i in range(50):
        ag = rint(0,360)/180*math.pi
        mod = rint(125,170) * delta
        radius = rint(40,60)
        create_particles(
            player.pos.copy() + py.Vector2(math.cos(ag), math.sin(ag)) * radius,
            py.Vector2(math.cos(ag), math.sin(ag)) * mod + py.Vector2(0,rint(-150,-40) * delta),
            particles,
            size = rint(2,13),
            color = change_rgb_val(hex_to_rgb("#ff4914"),rint(-8,8)*.01,0,0),
            type_ = "square",
            angle = rint(0,360)/180*math.pi
        )
    create_light(player.pos,orange_light,lights, scale=10)

    for i in enemies:
        if py.Vector2(i.pos - player.pos).length() < 120 + 10*lvl:
            i.take_dmg(40+5*lvl)

def thunder():
    thunder = Thunder(player.pos, player.spell_levels["Thunder"])
    thunder_list.append(thunder)
    
def throw_darts():
    lvl = player.spell_levels["Dart"]
    if len(enemies) > 0:
        for i in range(11+4*lvl):
            target = enemies[rint(0,len(enemies)-1)]
            dart = Dart(player.pos.copy(), target, lvl)
            darts.append(dart)

def blast():
    lvl = player.spell_levels["Blast"]
    blast_ = Blast(lvl)
    blasts.append(blast_)

def chicken_spell():
    lvl = player.spell_levels["Chicken"]

    create_light(player.pos,green_light,lights,scale=20)

    temp_chickens = []
    for i in enemies:
        if py.Vector2(i.pos - player.pos).length() < 70 + 10*lvl:
            i.hp = "chicken"
            chic = Chicken(i.pos,game_vars)
            temp_chickens.append(chic)

    to_remove = []
    for i in enemies:
        if isinstance(i.hp, str):
            to_remove.append(i)
    
    for i in to_remove:
        enemies.remove(i)
            
    for chic in temp_chickens:
        enemies.append(chic)

def ignite():
    lvl = player.spell_levels["Ignite"]

    possible_enemies = enemies.copy()
    for i in range(1 + int(lvl/2)):
        closest_dist = 10000
        closest = None
        for enemy in possible_enemies:
            dist = (enemy.pos - player.pos).length()

            if dist < closest_dist:
                closest_dist = dist
                closest = enemy

        closest.take_dmg(200)
        possible_enemies.remove(closest)

        if closest.hp <= 0:
            for i in range(5):
                frag = Fragment(closest.pos.copy(), py.Vector2(1,0).rotate(i/4*360+rint(-45,45)) * 300 * delta,i%4,closest)
                fragments.append(frag)
    
    

def area_prediction(radius,pos):
    for i in range(36):
        py.draw.arc(screen,(0,0,0), (pos.x-radius/2-cam.x, pos.y-radius/2-cam.y, radius, radius), i/36*math.pi*2, 0.1+i/36*math.pi*2,3)

def fire_prediction(lvl):
    area_prediction(120+10*lvl, player.pos)

def thunder_prediction(lvl):
    area_prediction(80, player.pos)

def dart_prediction(lvl):
    pass

def blast_prediction(lvl):
    vec = py.mouse.get_pos() - player.pos + cam
    width = (25 + 5*lvl)/2
    for i in range(100):
        py.draw.line(screen, (0,0,0), player.pos - cam + vec.normalize().rotate(90) * width + vec.normalize() * i * 20,
                      player.pos - cam + vec.normalize().rotate(90) * width  + vec.normalize() * (i * 20 + 10),3)
        py.draw.line(screen, (0,0,0), player.pos - cam + vec.normalize().rotate(-90) * width  + vec.normalize() * i * 20,
                      player.pos - cam + vec.normalize().rotate(-90) * width  + vec.normalize() * (i * 20 + 10),3)

def chicken_prediction(lvl):
    area_prediction(70+10*lvl, player.pos)

def ignite_prediction(lvl):

    lvl = player.spell_levels["Ignite"]

    possible_enemies = enemies.copy()
    for i in range(1 + int(lvl/2)):
        closest_dist = 10000
        closest = None
        for enemy in possible_enemies:
            dist = (enemy.pos - player.pos).length()

            if dist < closest_dist:
                closest_dist = dist
                closest = enemy
        if closest in possible_enemies:
            possible_enemies.remove(closest)

        area_prediction(40, closest.pos)



def game():

    global player
    global enemies
    global lights
    global particles
    global thunder_list
    global run
    global darts
    global blasts
    global damage_dealt_last_delta
    global enemies_killed
    global paused
    global screenshot
    global all_spells
    global all_spell_icons
    global fragments
    global cam
    global game_vars


    cam = py.Vector2(0,0)

    all_spells = ["Dart", "FireRing", "Thunder", "Blast", "Chicken", "Ignite"]
    all_spell_icons = {
            "Dart": load("darticon",scale=1.5),
            "FireRing": load("ringfireicon",scale=1.5),
            "Thunder": load("thundericon",scale=1.5),
            "Blast": load("fireblasticon",scale=1.5),
            "Chicken": load("chickenicon",scale=1.5),
            "Ignite": load("igniteicon",scale=1.5),

        }
        
    enemies_killed = 0

    player = Player(400,300)


    darts = []

    enemies = []

    spawners = []

    for i in range(9):
        spawner = Spawner(player.pos.copy() + py.Vector2(1,0).rotate(i/9*360) * 150, i*2)
        spawners.append(spawner)

    thunder_list = []

    particles = []


    lights = []

    blasts = []

    fragments = []

  
    paused = False

 
    screenshot = None
    damage_dealt_last_delta = 0

    game_vars = player, screen, cam, particles
    
    clock = py.time.Clock()

    click = False

    run = True
    while run:

        screen.fill(hex_to_rgb("#89a1bb"))
        screen.blit(bg,(-cam.x%400,-cam.y%300) - py.Vector2(400,300))
        screen.blit(bg,(-cam.x%400,-cam.y%300) - py.Vector2(0,300))
        screen.blit(bg,(-cam.x%400,-cam.y%300) - py.Vector2(400,0))
        screen.blit(bg,(-cam.x%400,-cam.y%300) - py.Vector2(0,0))

        #print(damage_dealt_last_delta/delta)
        damage_dealt_last_delta = 0
        
   

        

        if paused:
            screen.blit(screenshot,(0,0))

            if player.picking_option:
                player.skill_menu(click)
        else:
            #move camera
            vec = (player.pos - cam - py.Vector2(400,300))
            if vec.length() > 5:
                cam += vec * delta * 5

            
            for spawner in spawners:
                if spawner.awake:
                    spawner.draw()
                    spawner.spawn()
                else:
                    spawner.draw_idle()
                    if player.level >= spawner.awake_point:
                        spawner.awake = True

            for blast_ in blasts:
                blast_.draw()
                blast_.hit()
                if not blast_.time > 0:
                    blasts.remove(blast_)
            
        

            for enemy in enemies:
                enemy.move()
                enemy.draw()
                enemy.attack()
                #enemy.death_effect()

              
                if enemy.hp <= 0:
                    enemy.death_effect()
                    enemies.remove(enemy)
                    enemies_killed += 1

            for enemy in enemies:
                for other_enemy in enemies:
                    if enemy != other_enemy:
                        vec = py.Vector2(enemy.pos - other_enemy.pos)
                        if vec.length() != 0:
                            if vec.length() < (enemy.size + other_enemy.size/2):
                                enemy.pos += vec.normalize()/enemy.weight
                                other_enemy.pos -= vec.normalize()/other_enemy.weight


            for p in particles:

                if p[5] == "circle":
                    py.draw.circle(screen, p[4], p[0] - cam, p[3])
                if p[5] == "square":
                    points = [p[0] - cam + p[3]*py.Vector2(math.cos((i+p[6])/4*math.pi*2), math.sin((i+p[6])/4*math.pi*2)) for i in range(4)]
                    py.draw.polygon(screen, p[4], points)

                p[0] += p[1]
                p[2] -= delta

                if p[3] <= 0:
                    particles.remove(p)

                p[3] -= 10 * delta

            for fragment_ in fragments:
                fragment_.draw()
                fragment_.hit()
                fragment_.move()


                if fragment_.kill_switch:
                    fragments.remove(fragment_)

            for light in lights:
                img = py.transform.scale(light[4], py.Vector2(32,32) * light[3])
                screen.blit(img, light[0] - cam - py.Vector2(32,32) * light[3] / 2)


                if light[2]:
                    light[3] -= delta * 100
                    light[3] = max(light[3],0)

                light[1] -= delta
                if not light[1] > 0:
                    lights.remove(light)

            for thunder_ in thunder_list:

                thunder_.draw()
                thunder_.damage()

                if thunder_.lifetime <= 0:
                    thunder_list.remove(thunder_)
                
            for dart in darts:
                dart.draw()
                dart.move()
                dart.hit()

                if dart.kill_switch:
                    darts.remove(dart)

    
            if player.hp > 0:
                player.barrier(screen)
                player.move()
                player.draw()
                player.render_UI()
                player.cast()
                player.level_up()
        


        display.blit(screen,(0,0))

    
        

        click = False
        for e in py.event.get():
            if e.type == py.QUIT:
                run = False
            if e.type == py.KEYDOWN:
                player.input(e.key, True)
            if e.type == py.KEYUP:
                player.input(e.key, False)
            if e.type == py.MOUSEBUTTONDOWN:
                click = True
        py.display.set_caption(str(clock.get_fps()))
        clock.tick(fps)
        py.display.update()


game()
