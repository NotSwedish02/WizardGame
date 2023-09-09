import pygame as py
from utils import *


py.init()
py.display.set_mode((10,10))

squaresmall = load("squareS")

bg = load("bg")
bg = py.transform.scale(bg, (800,800)).convert_alpha()

spellslotimg = load("spellslot",scale=1.5)

lightimg = load("light",scale=1)
    
orange_light = tint(lightimg, hex_to_rgb("#ff4914"))

blue_light = tint(lightimg, (100,100,255))

green_light = tint(lightimg, (100,255,100))


square = load("square")

staffimg = load("staff")

square_dead_icon = load("dead_enemy_icon")

hpframe = load("hpbarframe",scale=1.2)
hpframe = py.transform.rotate(hpframe,-90)

xpframe = load("xpbarframe",scale=1.2)
xpframe = py.transform.rotate(xpframe,-90)

chicken = load("chicken")

frament_sheet = load("fragments",scale=2)
fragments_imgs = []
for i in range(4):
    surf = py.Surface((64,64))
    surf.blit(frament_sheet,(-i*64,0))
    surf.set_colorkey((0,0,0))
    fragments_imgs.append(surf)

blader = load("blader")

blader_frames = []
for i in range(4):
    surf = py.Surface((48,48)).convert_alpha()
    surf.blit(blader,(-i*48,0))
    surf.set_colorkey((0,0,0))
    blader_frames.append(surf)


pekka = load("pekka",scale=2)

pekka_frames = []
for i in range(10):
    surf = py.Surface((128,128)).convert_alpha()
    surf.blit(pekka,(-i*128,0))
    surf.set_colorkey((0,0,0))
    pekka_frames.append(surf)

pekka_sword = load("pekka_blade_anim",scale=4)

pekka_sword_frames = []
for i in range(6):
    surf = py.Surface((256,256)).convert_alpha()
    surf.blit(pekka_sword,(-i*256,0))
    surf.set_colorkey((0,0,0))
    pekka_sword_frames.append(surf)

snake_head = load("snake_head")
snake_segment = load("snake_segment")
snake_tail = load("snake_tail")


py.quit()

