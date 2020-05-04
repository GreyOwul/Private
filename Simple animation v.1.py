# -*- coding: utf-8 -*-
"""
Created on Sat May  2 07:34:32 2020

@author: seand

https://www.youtube.com/watch?v=Pl4Hp8qwwes
How to pickle

"""

import math, numpy, pickle
width=1280 #Width and height MUST be 16:9  (Easily tweakable?)
height=720

Period = 2 #(seconds)
FPS = 30 #Frames per Second

light_x=8 #Light's position in space.
light_y=4.5
light_z=9
brightness=100000 #scalar multiplier which is roughly analogous to how many watts the light is rated at.
min_Intensity=11 #describes the minimum brightness a pixel on the spehere will be coloured (min_Intensity,min_Intensity,min_Intensity)
light = (light_x,light_y,light_z,brightness)

d_pix_proj=9

r=13  #sphere radius and position in space
a=17
b=0
c=27


def Distance_From_Sphere_Surface(x,y,z,a,b,c,r): #Takes position in space (x,y,z) and returns the distance of that point to the surafce of a sphere cenred at (a,b,c) of radius (r)
    distance=abs(((x-a)**2+(y-b)**2+(z-c)**2)**(1/2)-r)
    return distance


def Light_Intensity(light,min_Intensity,x,y,z,a,b,c): #Given a pixel corresponds to a point, what is the value of the pixel?
    Normal_Vector_Surface = numpy.array([x-a,y-b,z-c]) #Vector Going normal (away) from the surface of the sphere at the point
    Light_To_Surface_Vector = numpy.array([x-light_x,y-light_y,z-light_z]) #Vector Going from the light source to the point
    Dot_Product = numpy.dot(Normal_Vector_Surface,Light_To_Surface_Vector)
    
    if Dot_Product >= 0:
        return (min_Intensity,min_Intensity,min_Intensity)
    
    if Dot_Product < 0:
        Normal_Vector_Surface_Length = ((x-a)**2+(y-b)**2+(z-c)**2)**(1/2)
        Light_To_Surface_Vector_Length = ((x-light_x)**2+(y-light_y)**2+(z-light_z)**2)**(1/2)  
        Cosine_Ratio = Dot_Product/(Normal_Vector_Surface_Length*Light_To_Surface_Vector_Length)
        distance=((x-light[0])**2+(y-light[1])**2+(z-light[2])**2)**(1/2)
        Intensity=int(light[4]*Cosine_Ratio/((distance**2)*4*math.pi))
        
        if Intensity <= min_Intensity:
            return (min_Intensity,min_Intensity,min_Intensity)
        
        return (Intensity,Intensity,Intensity)


for frame in range(0, (FPS*Period/2), 1):
    a=math.cos(frame*2*math.pi/(FPS*Period))*17   #This describes the movement of the sphere in the x direction 
    Image_Array = numpy.full((height,width,3),0)
    
    for v_pix in range(1,(height+1)*2,2):
        for h_pix in range (1,(width+1)*2,2):    
            h_pix_proj=((-8)+h_pix*(width*2))/1000
            v_pix_proj=((-4.5)+v_pix*(height*2))/1000
            
            for t in range(13950,40150,50):      
                x=h_pix_proj*(t/(d_pix_proj))
                y=v_pix_proj*(t/(d_pix_proj))
                z=t/1000
                
                if Distance_From_Sphere_Surface(x,y,z,a,b,c,r) <= 0.025:
                    pix=Light_Intensity(light,x,y,z,a,b,c)
                    Image_Array[v_pix-1,h_pix-1]=pix
                    break
                
    with open(f"{width},{height},{Period},{FPS},{light_x},{light_y},{light_z},{brightness},{min_Intensity},{r},{a},{b},{c},{frame}.pkl","wb") as pickle_file:
        pickle.dump(Image_Array, pickle_file)
    
    
                
            
                    
                    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
