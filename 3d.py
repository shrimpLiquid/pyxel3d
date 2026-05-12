import os
from math import *
import pyxel  
from random import randint
from pyxel import KEY_W,KEY_S,KEY_D,KEY_A
from pyxel import KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN
import numpy as np
import stl_reader
from time import time
from stl import mesh as besh

size = 600




def rotate_z(point, angle):
    px, py, pz = point  
    qx = py * cos(angle) - pz * sin(angle)
    qy = py * sin(angle) + pz * cos(angle)
    return px, qx, qy
def rotate(point, angle):
    px, py, pz = point
    qx = px * cos(angle) + pz * sin(angle)
    qz = -px * sin(angle) + pz * cos(angle)
    return qx, py, qz

x= 0
y= 1
z= 2
prevertices = []
indices = []
length = 0
colors = [[[0, 36, 72, 108, 144, 180], [6, 42, 78, 114, 150, 186], [12, 48, 84, 120, 156, 192], [18, 54, 90, 126, 162, 198], [24, 60, 96, 132, 168, 204], [30, 66, 102, 138, 174, 210]], [[1, 37, 73, 109, 145, 181], [7, 43, 79, 115, 151, 187], [13, 49, 85, 121, 157, 193], [19, 55, 91, 127, 163, 199], [25, 61, 97, 133, 169, 205], [31, 67, 103, 139, 175, 211]], [[2, 38, 74, 110, 146, 182], [8, 44, 80, 116, 152, 188], [14, 50, 86, 122, 158, 194], [20, 56, 92, 128, 164, 200], [26, 62, 98, 134, 170, 206], [32, 68, 104, 140, 176, 212]], [[3, 39, 75, 111, 147, 183], [9, 45, 81, 117, 153, 189], [15, 51, 87, 123, 159, 195], [21, 57, 93, 129, 165, 201], [27, 63, 99, 135, 171, 207], [33, 69, 105, 141, 177, 213]], [[4, 40, 76, 112, 148, 184], [10, 46, 82, 118, 154, 190], [16, 52, 88, 124, 160, 196], [22, 58, 94, 130, 166, 202], [28, 64, 100, 136, 172, 208], [34, 70, 106, 142, 178, 214]], [[5, 41, 77, 113, 149, 185], [11, 47, 83, 119, 155, 191], [17, 53, 89, 125, 161, 197], [23, 59, 95, 131, 167, 203], [29, 65, 101, 137, 173, 209], [35, 71, 107, 143, 179, 215]]]

from colorutils import rgb_to_hsv
def frtr(I,II,III,IV,V,VI,fcol):
    col = (max(min(255,fcol[0]),0),max(min(255,fcol[1]),0),max(min(255,fcol[2]),0))
    hsv = col
    g = int((hsv[0]/255)*5)
    r = int((hsv[1]/255)*5)
    b = int((hsv[2]/255)*5)
    v1=0
    s1=0
    pyxel.tri(I,II,III,IV,V,VI,colors[int(r)][int(g)][int(b)])


def sideofline(A, B, P):
    val = ((B[x] - A[x]) * (P[y] - A[y]) - (B[y] - A[y]) * (P[x] - A[x]))
    if val > 0:
        return 1
    elif val < 0:
        return -1
    return 0

def triangle(P0, P1, P2):
    if P0[z] < 0.1 or P1[z] < 0.1 or P2[z] < 0.1:
        return False
    val = (P1[x] - P0[x]) * (P2[y] - P0[y]) - (P1[y] - P0[y]) * (P2[x] - P0[x])
    
    return val < 0

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
mesh("nut",2,0.2,0,0.3,(0,100,255))
mesh("nut",4,0,0,0.6,(255,0,255))
mesh("suzanne",-4,0,0,1,(200,100,0))
mesh("plane",0,-1,0,1,(80,0,130))
mesh("cone",0,0,5,0.3,(255,255,255))
mesh("ball",0,0,-2,1,(0,255,0))
mesh("S&C",5,0,6,1,(0,100,255))




lv = np.array([0.25, -0.5, 1])
slop= 1.6*size
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
        pyxel.init(size, size)
        self.points = []
        self.tris = []
        self.c = 8
        self.cp = [0,0,0]
        self.trf = []
        self.yaw = radians(90)
        self.pitch = radians(0)
        self.dot = 0
        self.tm = 0
        self.col = ()
        #pyxel.colors.from_list([0x000000,0x2b335f,0x7e2072,0x19959c,0x8b4852,0x395c98,0xa9c1ff,0xeeeeee,0xd4186c,0xd38441,0xe9c35b,0xa3a3a3,0x70c6a9,0x7696de,0xff9798,0xedc7b0,0x555555,0x7b83af,0xce70c2,0x59e5ec,0xdb98a2,0x89ace8,0xf9f1ff,0xfffffff,0xf468bc,0xf3d491,0xf9f3ab,0xf3f3f3,0xc0f6f9,0xc6e6fe,0xffe7e8,0xfdf7f0])
        pyxel.colors.from_list([0x080909, 0x093809, 0x086909, 0x099809, 0x08c609, 0x09ff09, 0x380808, 0x383808, 0x386708, 0x389808, 0x38c608, 0x38ff08, 0x670909, 0x693809, 0x676909, 0x699809, 0x67c609, 0x69ff09, 0x980808, 0x983808, 0x986708, 0x989808, 0x98c608, 0x98ff08, 0xc60909, 0xc63809, 0xc66909, 0xc69809, 0xc6c609, 0xc6ff09, 0xff0808, 0xff3808, 0xff6708, 0xff9808, 0xffc608, 0xffff08, 0x080938, 0x093838, 0x086938, 0x099838, 0x08c638, 0x09ff38, 0x380838, 0x383838, 0x386738, 0x389838, 0x38c638, 0x38ff38, 0x670938, 0x693838, 0x676938, 0x699838, 0x67c638, 0x69ff38, 0x980838, 0x983838, 0x986738, 0x989838, 0x98c638, 0x98ff38, 0xc60938, 0xc63838, 0xc66938, 0xc69838, 0xc6c638, 0xc6ff38, 0xff0838, 0xff3838, 0xff6738, 0xff9838, 0xffc638, 0xffff38, 0x080969, 0x093869, 0x086969, 0x099869, 0x08c669, 0x09ff69, 0x380867, 0x383867, 0x386767, 0x389867, 0x38c667, 0x38ff67, 0x670969, 0x693869, 0x676969, 0x699869, 0x67c669, 0x69ff69, 0x980867, 0x983867, 0x986767, 0x989867, 0x98c667, 0x98ff67, 0xc60969, 0xc63869, 0xc66969, 0xc69869, 0xc6c669, 0xc6ff69, 0xff0867, 0xff3867, 0xff6767, 0xff9867, 0xffc667, 0xffff67, 0x080998, 0x093898, 0x086998, 0x099898, 0x08c698, 0x09ff98, 0x380898, 0x383898, 0x386798, 0x389898, 0x38c698, 0x38ff98, 0x670998, 0x693898, 0x676998, 0x699898, 0x67c698, 0x69ff98, 0x980898, 0x983898, 0x986798, 0x989898, 0x98c698, 0x98ff98, 0xc60998, 0xc63898, 0xc66998, 0xc69898, 0xc6c698, 0xc6ff98, 0xff0898, 0xff3898, 0xff6798, 0xff9898, 0xffc698, 0xffff98, 0x0809c6, 0x0938c6, 0x0869c6, 0x0998c6, 0x08c6c6, 0x09ffc6, 0x3808c6, 0x3838c6, 0x3867c6, 0x3898c6, 0x38c6c6, 0x38ffc6, 0x6709c6, 0x6938c6, 0x6769c6, 0x6998c6, 0x67c6c6, 0x69ffc6, 0x9808c6, 0x9838c6, 0x9867c6, 0x9898c6, 0x98c6c6, 0x98ffc6, 0xc609c6, 0xc638c6, 0xc669c6, 0xc698c6, 0xc6c6c6, 0xc6ffc6, 0xff08c6, 0xff38c6, 0xff67c6, 0xff98c6, 0xffc6c6, 0xffffc6, 0x0809ff, 0x0938ff, 0x0869ff, 0x0998ff, 0x08c6ff, 0x09ffff, 0x3808ff, 0x3838ff, 0x3867ff, 0x3898ff, 0x38c6ff, 0x38ffff, 0x6709ff, 0x6938ff, 0x6769ff, 0x6998ff, 0x67c6ff, 0x69ffff, 0x9808ff, 0x9838ff, 0x9867ff, 0x9898ff, 0x98c6ff, 0x98ffff, 0xc609ff, 0xc638ff, 0xc669ff, 0xc698ff, 0xc6c6ff, 0xc6ffff, 0xff08ff, 0xff38ff, 0xff67ff, 0xff98ff, 0xffc6ff, 0xffffff])
        pyxel.run(self.update, self.draw)
        

    def update(self):
        print(self.pitch,self.yaw)
        if pyxel.frame_count >20:
            self.yaw += (((pyxel.mouse_x-int(size/2)))/-100)*(600/size)
            self.pitch += (((pyxel.mouse_y-int(size/2)))/-100)*(600/size)
        pyxel.warp_mouse(int(size/2),int(size/2))
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
                                int((self.points[ind[2]][z]+self.points[ind[1]][z]+self.points[ind[0]][z])/3),
                                nval[i],
                                (vertices[ind[0]][x],vertices[ind[0]][y],vertices[ind[0]][z]))) 
        self.tris.sort(key=lambda t: t[4], reverse=True)


        
    def draw(self):
        pyxel.cls(colors[0][0][0]) 
        pyxel.camera(-(size/2),-(size/2))
        pyxel.line((size/2),-(size/2),(size/2),(size/2),7)
        pyxel.dither(1)
        

        self.tm = time()
        
        
        
        for tri in self.tris:
            self.dot = (lv @ tri[5])*-100
            pyxel.dither(1)
            self.col = (tri[3][0]-self.dot,tri[3][1]-self.dot,tri[3][2]-self.dot)
            #self.col = ((tri[5][x]+1)*127,(tri[5][y]+1)*127,(tri[5][z]+1)*127)
            frtr(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],self.col)
            # pyxel.trib(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],0)
        
        
        
        
        pyxel.text(-(size/2),-280,str(int(1/(time()-self.tm))),colors[5][5][5])
        pyxel.text(-(size/2),-290,str(self.cp),colors[5][5][5])
        pyxel.text(-(size/2),-(size/2),str(len(self.tris)),colors[5][5][5])
        

App()