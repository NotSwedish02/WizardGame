import pygame as py
import math
from PIL import ImageColor
import colorsys




def hex_to_rgb(color):
    return ImageColor.getcolor(color, "RGB")

def change_rgb_val(color,h_change,s_change,v_change):
    r,g,b = color
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    h += h_change
    s += s_change
    v += v_change

    if h > 255:
        h = h - 1
    if h < 0:
        h = h + 1

    return colorsys.hsv_to_rgb(h,s,v)


def load(name,scale=1):
    img = py.image.load("images/" + name + ".png").convert_alpha()
    img.set_colorkey((0,0,0))
    img = py.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
    return img

def sign(x):
    if x >= 0:
        return True
    else:
        return False
    
def tint(surf, tint_color):

    surf = surf.copy()
    surf.fill((0, 0, 0, 255), None, py.BLEND_RGBA_MULT)
    surf.fill(tint_color[0:3] + (0,), None, py.BLEND_RGBA_ADD)
    return surf

def create_particles(pos, init_velocity, particles, time=1, size=1, color="#ffffff", type_="circle", angle=0):
        if color is str:
            color = hex_to_rgb(color)

        p = [pos, init_velocity, time, size, color, type_, angle]
        particles.append(p)

def create_light(pos,img,lights,time=1,fade=True,scale=1):
    light_ = [pos,time,fade,scale,img]
    lights.append(light_)



    
