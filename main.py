# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 06:52:07 2017

@author: chemasmas
"""

import os, sys, inspect, Leap,time
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

bandera = True
#Vectores Base
x = Leap.Vector(1,0,0)
y = Leap.Vector(0,1,0)
z = Leap.Vector(0,0,1)


def paint_axis(axis):
    axis.set_xbound(-200,200)
    axis.set_ybound(-200,200)
    axis.set_zbound(-200,200)
    axis.plot([-200,200] , [0,0] , [0,0] , 'r',label = "x") #x
    axis.plot([0,0] , [-200,200] , [0,0] , 'b',label = "y") #z
    axis.plot([0,0] , [0,0] , [-200,200] , 'g',label = "z") #y
    axis.set_xlabel("X")
    axis.set_ylabel("Z")
    axis.set_zlabel("Y")
    
def paint_point(axis, x, y ,z):
    #para adaptarnos al eje del leap z e y cambian de pos
    axis.scatter(x,-z,y,'z',20,'c')
     
def paint_line(axis,x0,x1,y0,y1,z0,z1):
    axis.plot([x0,x1],[-z0,-z1],[y0,y1],'c')
    
def paint_basis(axis,item):
    basis = item.basis
    origen = basis.origin
    xvector = basis.x_basis
    yvector = basis.y_basis
    zvector = basis.z_basis
    print str(item)

def handle_close(evt):
    global bandera
    bandera = False
    print('Closed Figure!')
    
    
def proyDedoXY(dedo):
    metacarpo = dedo.bone(0)
    proximal = dedo.bone(1)
    intermedio = dedo.bone(2)
    distal = dedo.bone(3)
    
    #metacarpo.next_joint Posicion de la articulacion cercana a la punta
    #metacarpo.prev_joint    
    
    
#vista Frontal
def proyManoXY(mano):
    #Vectores
    direccion = mano.direction;
    posPalma = mano.palm_position
    normPalma = mano.palm_normal
    dedos = mano.fingers
    pulgar = dedos[0] #Pulgar
    indice = dedos[1] #Indice
    medio = dedos[2] #Medio
    anular = dedos[3] #Anular
    menique = dedos[4] #Menique
    
    #componentes en x (flotantes)
    xDireccion = direccion.dot(x)
    xPosPalma = posPalma.dot(x)
    xNormPalma = normPalma.dot(x)
    
 
    #componentes en y
    yDireccion = direccion.dot(y)
    yPosPalma = posPalma.dot(y)
    yNormPalma = normPalma.dot(y)
    
    proyeccion = {}
    proyeccion["direccion"] = Leap.Vector(xDireccion,yDireccion,0)
    proyeccion["normal"] = Leap.Vector(xNormPalma,yNormPalma,0)

    #Impresiones
    #print("Datos Originales");
    #print(direccion.to_tuple())   
    #print(normPalma.to_tuple())
    
    #print("Proyeccion a XY")
    #print(proyeccion["direccion"].to_tuple())
    #print(proyeccion["normal"].to_tuple())
    return proyeccion()

def main():
    print("inicio")
    controller = Leap.Controller()
    #fig = plt.figure()
    #fig.canvas.mpl_connect('close_event', handle_close)
    #ax = fig.add_subplot(111, projection='3d')
    #plt.ion()
    
    
    #paint_axis(ax)
    #while bandera:
    while (True):
        frame = controller.frame()
        hands = frame.hands
        if not hands.is_empty:
            for hand in hands:
                ##Vectores utiles 
                proyManoXY(hand)
                
                #print str(hand.palm_position)
                #print str(hand.basis)
                
                #xpalm = hand.palm_position.x
                #ypalm = hand.palm_position.y
                #zpalm = hand.palm_position.z
                
                #print(str(frame))
                #paint_point(ax,xpalm,ypalm,zpalm)
                #paint_line(ax,0,xpalm,0,ypalm,0,zpalm)
                #paint_basis(ax,hand)
                #ax.scatter([xpalm],[ypalm],[zpalm],'z',20,'b')
                #ax.plot([0,xpalm],[0,ypalm],[0,zpalm],'b')
                
                #print str(hand.basis)
        #plt.pause(0.001)
        time.sleep(1)
 #   while (controller.is_service_connected()) :
  #      ax.clear()  
   #     origen = Leap.Vector()
    #    xaxis = Leap.Vector().x_axis
     #   yaxis = Leap.Vector().y_axis
      #  zaxis = Leap.Vector().z_axis
#
 #       ax.plot([0,100] , [0,0] , [0,0] , 'r')
  #      ax.plot([0,0] , [0,100] , [0,0] , 'r')
   #     ax.plot([0,0] , [0,0] , [0,100] , 'r')
#
        #plt.show()	
  #      time.sleep(1)
        

if __name__ == "__main__":
    main()

