# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:12:35 2017

@author: chemasmas
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 06:52:07 2017

@author: chemasmas
"""

import os, sys, inspect, Leap,time

leapController = Leap.Controller()
frame = Leap.Frame
manos = Leap.HandList

nombresDedos = [
    "pulgar","indice","medio","anular","menique"
    ]

nombresHuesos = [
    "metacarpo","proximal","medio","distal"    
    ]

def getHands():
    if(leapController.is_connected):
        frame = leapController.frame()
        manos = frame.hands
        if not manos.is_empty:
            return manos
        else:
            return Leap.HandList()
    else:
        print "Conectar El Leap Motion"
        return None
        
def imprimirHueso(hueso):
    #print("\t"+nombresHuesos[hueso.type])
    #print("\t"+str(hueso.length))
    base  = hueso.basis #Base ortogonal al dedo
    inicio = hueso.prev_joint
    fin = hueso.next_joint
    
    #print(base)
    #HUESOS De la mano
    #print("\t"+str(inicio))
    #print("\t"+str(fin))
    #return [inicio.to_tuple(),fin.to_tuple()]
    return [inicio,fin]
    
def imprimirDedo(dedo):
    #print(nombresDedos[dedo.type])
    res = []
    for i in range(4):
        #print(nombresHuesos[i])
        hueso = dedo.bone(i)
        arr = imprimirHueso(hueso)
        #print(arr)
        ##res.append(arr)
        res.extend(arr)
        #print(dedo.bone(i))
    return res


#Retorna una lista de todas las articulaciones y el centro de la mano
def imprimirMano(mano):
    base = mano.basis #Base de la mano, provee de la martriz de tranformacion
    posicion = mano.palm_position # coordenada 
    distancia = posicion.magnitude #distancia linea recta, centropalama de  la mano al snsor
    dedos = mano.fingers
    res =[posicion]
    #if(centro)
    for dedo in dedos:
        arr = imprimirDedo(dedo)
        ##res.append(arr)
        res.extend(arr)
        
    #print("-"*10)
    return res

def estructuraMano(mano):
    posicion = mano.palm_position # coordenada 
    dedos = mano.fingers
    res =[posicion]
    for dedo in dedos:
        arr = estructuraDedo(dedo)
        res.append(arr)        
    return res

def estructuraDedo(dedo):
    res = []
    for i in range(4):
        hueso = dedo.bone(i)
        arr = estructuraHueso(hueso)
        res.append(arr)
    return res
    
def estructuraHueso(hueso):
    base  = hueso.basis #Base ortogonal al dedo
    inicio = hueso.prev_joint
    fin = hueso.next_joint
    return [inicio,fin]

def crearArchivo(nombre = "test.txt"):
    
    try:
        os.stat("archivos")
    except:
        os.mkdir("archivos")
        
    archivo = open("archivos/"+nombre,"w")
    return archivo;
    



def main():
    #nombre  = str(raw_input("Nombre archivo: "))
    nombre  = ""
    xyz = crearArchivo("xyz"+nombre+".txt")
    xy = crearArchivo("xy"+nombre+".txt")
    xz = crearArchivo("xz"+nombre+".txt")
    
    centro = crearArchivo("centro"+nombre+".txt")
    pulgar = crearArchivo("pulgar"+nombre+".txt")
    indice = crearArchivo("indice"+nombre+".txt")
    medio = crearArchivo("medio"+nombre+".txt")
    anular = crearArchivo("anular"+nombre+".txt")
    pinky = crearArchivo("pinky"+nombre+".txt")
    cnt = 0
    while(cnt < 10):
        manos = getHands()
        if not manos == None:
            for mano in manos:
                #dedosExt(mano)
            
                arr = imprimirMano(mano)
                estructura = estructuraMano(mano)
            
                #print(str(estructura))            
                xyz.write(flatArr(mapToXYZ(arr),3))
                xyz.write("\n")
                
                xy.write(flatArr(mapToXY(arr)))
                xy.write("\n")
                
                xz.write(flatArr(mapToXZ(arr)))
                xz.write("\n")
            
                xyz.flush()
                xy.flush()
                xz.flush()
                
                dim = ["x","z"]
                centro.write(toDim(estructura[0],dim))
                centro.flush()
                #dedo pulgar
                for i in estructura[1]:
                    pulgar.write(toDim(i[0],dim))
                    pulgar.write(toDim(i[1],dim))
                pulgar.flush()
                
                #dedo indice
                for i in estructura[2]:
                    indice.write(toDim(i[0],dim))
                    indice.write(toDim(i[1],dim))
                indice.flush()
                
                #dedo medio
                for i in estructura[3]:
                    medio.write(toDim(i[0],dim))
                    medio.write(toDim(i[1],dim))
                medio.flush()
                
                #dedo indice
                for i in estructura[4]:
                    anular.write(toDim(i[0],dim))
                    anular.write(toDim(i[1],dim))
                anular.flush()
                
                #dedo indice
                for i in estructura[5]:
                    pinky.write(toDim(i[0],dim))
                    pinky.write(toDim(i[1],dim))
                pinky.flush()
                
            cnt = cnt +1        
        time.sleep(1)
    print("Terminado")


def toDim(vector, dim = ["x","y"]):
    res = ""
    if "x" in dim:
        res = res + str(vector.x) + "\t"
    if "y" in dim:
        res = res + str(vector.y) + "\t"
    if "z" in dim:
        res = res + str(vector.z) + "\t"
    res = res + "\n"
    return res

def mapToXYZ(arr):
    res =  []
    for t in arr:
        res.extend([t.x,t.y,t.z])
        #print(str(t.x))
    return res
    
def mapToXY(arr):
    res =  []
    for t in arr:
        res.extend([t.x,t.y])
        #print(str(t.x))
    return res

def mapToXZ(arr):
    res =  []
    for t in arr:
        res.extend([t.x,t.z])
        #print(str(t.x))
    return res
    
def flatArr(arr,dim = 2):
    res = ""
    cnt = 0
    for i in arr:
        if cnt % dim == 0:
            res = res + "\n"
        res = res + str(i) + "\t"
        cnt = cnt +1 
    
    return res

if __name__ == "__main__":
    main()



