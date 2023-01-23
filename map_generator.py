import opensimplex as sp
import json
import random

def save_map_vals(n):
        d = {}
        for y,row in enumerate(n):
            for x,col in enumerate(row):
                d[str((x,y))] = col
        with open("base_tile_values.json","w") as file:
            json.dump(d,file,indent=2)

def load_map_vals(file):

    def jsonKeys2int(x):
        if isinstance(x, dict):
                return {eval(k):v for k,v in x.items()}
        return x
    
    map_vals = {}
    with open(file) as file:
        map_vals = json.load(file,object_hook=jsonKeys2int)
    return map_vals

def map_value_generator(seed):
        '''random map value generator using opensimplex module, returns a 2d list of floats'''
        r = seed
        print(f"seed: {r}")
        sp.seed(r)
        n = []
        for y in range(250):
            o = []
            for x in range(400):
                o.append(sp.noise2(x*0.2,y*0.2))
            n.append(o)
        return n

def _smooth_noise(l):
        '''function used to smooth out noise values of a list l by checking
            with the values of the tiles around it. If a type of tile is in greater count make the current tile into that tile.
            This function returns a list of float values'''
        for y,row in enumerate(l):
            for x,col in enumerate(row):
                high_ground = 0
                grass = 0
                sand = 0
                water = 0
                deep_water = 0
                if x == len(row)-1 and y == len(l)-1:
                    neighb = [l[y][x-1],l[y-1][x],l[y-1][x-1]]
                elif x == len(row)-1:
                    neighb = [l[y][x-1],l[y+1][x],l[y-1][x],l[y-1][x-1],l[y+1][x-1]]
                elif y == len(l)-1:
                    neighb = [l[y][x+1],l[y][x-1],l[y-1][x],l[y-1][x-1],l[y-1][x+1]]
                else:
                    neighb = [l[y][x+1],l[y][x-1],l[y+1][x],l[y-1][x],l[y+1][x+1],l[y-1][x-1],l[y-1][x+1],l[y+1][x-1]]
                for i in neighb:
                    if i >= 0.5: high_ground += 1
                    elif i>=0.1 and i<=0.5: grass += 1
                    elif i>=-0.1 and i<=0.1: sand += 1
                    elif i>=-0.3 and i<=-0.1: water += 1
                    elif i<=-0.3: deep_water += 1
                if high_ground == max(high_ground,grass,sand,water,deep_water): l[y][x] = 0.51
                elif grass == max(high_ground,grass,sand,water,deep_water): l[y][x] = 0.2
                elif sand == max(high_ground,grass,sand,water,deep_water): l[y][x] = 0.0
                elif water == max(high_ground,grass,sand,water,deep_water): l[y][x] = -0.2
                elif deep_water == max(high_ground,grass,sand,water,deep_water): l[y][x] = -0.31
        return l

#self.map_value_generator(1234)
    #_smooth_noise()
map_val =_smooth_noise(map_value_generator(1234))
save_map_vals(map_val)
