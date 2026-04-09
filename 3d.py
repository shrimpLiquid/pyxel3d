import os
from math import *
import pyxel  
from random import randint
import cmath
from pyxel import KEY_W,KEY_S,KEY_D,KEY_A
from pyxel import KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN
import numpy as np
import stl_reader
from time import time
from stl import mesh as besh






def rotate_z(point, angle):
    px, py, pz = point  
    qx = py * cmath.cos(angle) - pz * cmath.sin(angle)
    qy = py * cmath.sin(angle) + pz * cmath.cos(angle)
    return px, qx, qy
def rotate(point, angle):
    px, py, pz = point
    qx = px * cmath.cos(angle) + pz * cmath.sin(angle)
    qz = -px * cmath.sin(angle) + pz * cmath.cos(angle)
    return qx, py, qz

x= 0
y= 1
z= 2
prevertices = []
indices = []
length = 0

def sideofline(A, B, P):
    val = ((B[x] - A[x]) * (P[y] - A[y]) - (B[y] - A[y]) * (P[x] - A[x]))
    if val > 0:
        return 1
    elif val < 0:
        return -1
    return 0

def triangle(P0, P1, P2):
    n = 0
    for N in [P0[z],P1[z],P2[z]]:
        if N < 0:
            n+=1
    if n > 2:
        return False
    n = 0
    for N in [P0[x],P0[y],P1[x],P1[y],P2[x],P2[y]]:
        if N < -400 or N > 600:
            n+=1
    if n > 2:
        return False
    val = (P1[x] - P0[x]) * (P2[y] - P0[y]) - (P1[y] - P0[y]) * (P2[x] - P0[x])
    if val < 0:
        return True
    return False

def normalize_3d_vector(v):
    magnitude = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    
    if magnitude == 0:
        return [0, 0, 0]
    
    return [v[0] / magnitude, v[1] / magnitude, v[2] / magnitude]

def mesh(file, X, Y, Z, S,color):
    global modelcount
    global nval
    meshvert, meshind, = stl_reader.read(str(os.path.relpath(__file__).replace("3d.py", file + ".stl")))
    mehse = besh.Mesh.from_file(str(os.path.relpath(__file__).replace("3d.py", file + ".stl")))
    normals = mehse.normals
    for N in normals:
        nval.append(normalize_3d_vector(N))

    start_idx = len(prevertices)
    for P in meshvert:
        prevertices.append([P[0] * S + X, P[2] * S + Y, P[1] * S + Z])
    meshind = meshind.tolist()
    for I in meshind:
        I[0] += start_idx
        I[1] += start_idx
        I[2] += start_idx
        I.append(color)
        indices.append(I)
    modelcount += 1
modelcount = 0
nval = []
mesh("nut",2,0.2,0,0.3,1)
mesh("nut",4,0,0,0.6,8)
mesh("suzanne",-4,0,0,1,4)
mesh("plane",0,-1,0,1,2)
mesh("cone",0,0,5,0.3,7)
mesh("cone",1,0,5,0.3,0)
mesh("freak",0,0,-2,1,6)



lv = np.array([0.447214, -0.894427, 0])
slop= 1000
speed = 0.1
def project(pos):
    FOC = 1
    DIZ = (FOC+float(pos[z]))
    if DIZ <= 0.1: 
        DIZ = 0.1
    return([(float(pos[x]))/DIZ*slop,
       (float((pos[y]*-1)))/DIZ*slop,
            float(pos[z])])
class App:
    def __init__(self):
        pyxel.init(600, 600)
        self.points = []
        self.tris = []
        self.c = 8
        self.cp = [0,0,0]
        self.trf = []
        self.yaw = -21474832.540000007
        self.pitch = -21474827.75000000
        self.dot = 0
        self.tm = 0
        pyxel.run(self.update, self.draw)
        

    def update(self):
        print(self.pitch,self.yaw)
        if pyxel.frame_count >20:
            self.yaw += (((pyxel.mouse_x-300))/-100)
            self.pitch += (((pyxel.mouse_y-300))/-100)
        pyxel.warp_mouse(300,300)
        if pyxel.btn(KEY_W):
            self.cp[2]+= sin(self.yaw+1.5708)*speed
            self.cp[0]+= cos(self.yaw+1.5708)*speed
        if pyxel.btn(KEY_S):
            self.cp[2]-= sin(self.yaw+1.5708)*speed
            self.cp[0]-= cos(self.yaw+1.5708)*speed
        if pyxel.btn(KEY_A):
            self.cp[2]-= sin(self.yaw)*speed
            self.cp[0]-= cos(self.yaw)*speed
        if pyxel.btn(KEY_D):
            self.cp[2]+= sin(self.yaw)*speed
            self.cp[0]+= cos(self.yaw)*speed
        if pyxel.btn(pyxel.KEY_SPACE):
            self.cp[1]+= speed
        if pyxel.btn(pyxel.KEY_SHIFT):
            self.cp[1] -=speed
        
        
        vertices = []
        for vert in prevertices:
            self.trf = [vert[0] - self.cp[0], 
                        vert[1] - self.cp[1], 
                        vert[2] - self.cp[2]] 
            self.trf = rotate(self.trf,(self.yaw))
            self.trf = rotate_z(self.trf,self.pitch)
            vertices.append(self.trf)
        self.points.clear()
        self.tris.clear()
        for vert in vertices:
            self.points.append(project(vert))
        
        for i, ind in enumerate(indices):
            self.c = 8
            self.center = (((self.points[ind[0]][x]+self.points[ind[1]][x]+self.points[ind[2]][x])/3),(self.points[ind[0]][y]+self.points[ind[1]][y]+self.points[ind[2]][y])/3)
            if triangle(self.points[ind[0]],self.points[ind[1]],self.points[ind[2]]):
                self.tris.append(((self.points[ind[0]][x],self.points[ind[0]][y]),
                                (self.points[ind[1]][x],self.points[ind[1]][y]),
                                (self.points[ind[2]][x],self.points[ind[2]][y]),
                                ind[3],
                                int(self.points[ind[2]][z]),
                                nval[i],
                                (np.array(normalize_3d_vector([(prevertices[ind[0]][x]+prevertices[ind[1]][x]+prevertices[ind[2]][x])/3,(prevertices[ind[0]][y]+prevertices[ind[1]][y]+prevertices[ind[2]][y])/3,(prevertices[ind[0]][z]+prevertices[ind[1]][z]+prevertices[ind[2]][z])/3])) @ nval[i]))) 
        self.tris.sort(key=lambda t: t[4], reverse=True)


        
    def draw(self):
        pyxel.cls(0) 
        pyxel.camera(-300,-300)
        pyxel.mouse(True)
        pyxel.line(300,-300,300,300,7)
        pyxel.dither(1)
        pyxel.text(-300,-280,str(int(1/(time()-self.tm))),7)
        self.tm = time()
        pyxel.colors.from_list([0x000000,0x2b335f,0x7e2072,0x19959c,0x8b4852,0x395c98,0xa9c1ff,0xeeeeee,0xd4186c,0xd38441,0xe9c35b,0xa3a3a3,0x70c6a9,0x7696de,0xff9798,0xedc7b0,0x555555,0x7b83af,0xce70c2,0x59e5ec,0xdb98a2,0x89ace8,0xf9f1ff,0xfffffff,0xf468bc,0xf3d491,0xf9f3ab,0xf3f3f3,0xc0f6f9,0xc6e6fe,0xffe7e8,0xfdf7f0])
        pyxel.text(-300,-300,str(len(self.tris)),7)
        
        for tri in self.tris:
            self.dot = (lv @ tri[5])/2
            self.dot = 
            pyxel.dither(1)
            pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],tri[3])
            if self.dot > 0:
                pyxel.dither(self.dot-0.1)
                pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],tri[3]+16)
            if self.dot < 0:
                pyxel.dither(abs(self.dot))
                pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],0)

                
        

App()
