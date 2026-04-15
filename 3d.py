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
colors = [[[0, 42, 84, 126, 168, 210], [6, 48, 90, 132, 174, 216], [12, 54, 96, 138, 180, 222], [18, 60, 102, 144, 186, 228], [24, 66, 108, 150, 192, 234], [30, 72, 114, 156, 198, 240], [36, 78, 120, 162, 204, 246]], [[1, 43, 85, 127, 169, 211], [7, 49, 91, 133, 175, 217], [13, 55, 97, 139, 181, 223], [19, 61, 103, 145, 187, 229], [25, 67, 109, 151, 193, 235], [31, 73, 115, 157, 199, 241], [37, 79, 121, 163, 205, 247]], [[2, 44, 86, 128, 170, 212], [8, 50, 92, 134, 176, 218], [14, 56, 98, 140, 182, 224], [20, 62, 104, 146, 188, 230], [26, 68, 110, 152, 194, 236], [32, 74, 116, 158, 200, 242], [38, 80, 122, 164, 206, 248]], [[3, 45, 87, 129, 171, 213], [9, 51, 93, 135, 177, 219], [15, 57, 99, 141, 183, 225], [21, 63, 105, 147, 189, 231], [27, 69, 111, 153, 195, 237], [33, 75, 117, 159, 201, 243], [39, 81, 123, 165, 207, 249]], [[4, 46, 88, 130, 172, 214], [10, 52, 94, 136, 178, 220], [16, 58, 100, 142, 184, 226], [22, 64, 106, 148, 190, 232], [28, 70, 112, 154, 196, 238], [34, 76, 118, 160, 202, 244], [40, 82, 124, 166, 208, 250]], [[5, 47, 89, 131, 173, 215], [11, 53, 95, 137, 179, 221], [17, 59, 101, 143, 185, 227], [23, 65, 107, 149, 191, 233], [29, 71, 113, 155, 197, 239], [35, 77, 119, 161, 203, 245], [41, 83, 125, 167, 209, 251]]]

from colorutils import rgb_to_hsv
def frtr(I,II,III,IV,V,VI,fcol):
    col = (max(min(255,fcol[0]),0),max(min(255,fcol[1]),0),max(min(255,fcol[2]),0))
    hsv = col
    if rgb_to_hsv(col)[1] > 0.05:
        r = int((hsv[0]/255)*5)
        b = int((hsv[2]/255)*5)
        g = int((hsv[1]/255)*6)
        v1=0
        s1=0
        pyxel.tri(I,II,III,IV,V,VI,colors[int(r)][int(g)][int(b)])
        if not (r % 2 ==0 and g % 2 == 0 and b % 2 == 0):
            if r % 2 ==1:
                h1 = (int(r/2)+1)
            else:
                h1 = int(r/2)
            if b % 2 ==1:
                v1 = (int(b/2)+1)
            else:
                v1 = int(b/2)
            if g % 2 ==1:
                s1 = (int(g/2)+1)
            else:
                s1 = int(g/2)
            pyxel.dither(dist(((hsv[0]/255)*5,(hsv[2]/255)*5,(hsv[1]/255)*6),(r,b,g))/2)
            pyxel.tri(I,II,III,IV,V,VI,colors[h1][s1][v1])
            pyxel.dither(1)
    else:
        pyxel.dither(1)
        G = rgb_to_hsv(col)[2]*4
        pyxel.tri(I,II,III,IV,V,VI,252+int(G/2))
        if int(G) % 2 != 0:
            pyxel.dither(abs(G-int(G))/2)
            pyxel.tri(I,II,III,IV,V,VI,252+int(G/2)+1)


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
mesh("nut",2,0.2,0,0.3,(0,100,255))
mesh("nut",4,0,0,0.6,(255,0,255))
mesh("suzanne",-4,0,0,1,(200,100,0))
mesh("plane",0,-1,0,1,(80,0,130))
mesh("cone",0,0,5,0.3,(255,255,255))
mesh("cone",1,0,5,0.3,(0,0,0))
mesh("freak",0,0,-2,1,(0,255,0))



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
        self.col = ()
        #pyxel.colors.from_list([0x000000,0x2b335f,0x7e2072,0x19959c,0x8b4852,0x395c98,0xa9c1ff,0xeeeeee,0xd4186c,0xd38441,0xe9c35b,0xa3a3a3,0x70c6a9,0x7696de,0xff9798,0xedc7b0,0x555555,0x7b83af,0xce70c2,0x59e5ec,0xdb98a2,0x89ace8,0xf9f1ff,0xfffffff,0xf468bc,0xf3d491,0xf9f3ab,0xf3f3f3,0xc0f6f9,0xc6e6fe,0xffe7e8,0xfdf7f0])
        pyxel.colors.from_list([0x111600, 0x3b1500, 0x661400, 0x8f1200, 0xb91200, 0xe31100, 0x123a00, 0x3d3900, 0x673800, 0x903700, 0xbb3600, 0xe53500, 0x145e00, 0x3e5d00, 0x685c00, 0x925b00, 0xbc5a00, 0xe65900, 0x158300, 0x408100, 0x6a8000, 0x947f00, 0xbe7e00, 0xe77d00, 0x16a700, 0x41a600, 0x6ba500, 0x95a300, 0xbfa200, 0xe9a100, 0x18cb00, 0x42ca00, 0x6cc900, 0x97c800, 0xc1c700, 0xebc500, 0x19f000, 0x43ee00, 0x6eed00, 0x98ec00, 0xc2eb00, 0xedea00, 0x111615, 0x3b1515, 0x661415, 0x8f1215, 0xb91215, 0xe31115, 0x123a15, 0x3d3915, 0x673815, 0x903715, 0xbb3615, 0xe53515, 0x145e15, 0x3e5d15, 0x685c15, 0x925b15, 0xbc5a15, 0xe65915, 0x158315, 0x408115, 0x6a8015, 0x947f15, 0xbe7e15, 0xe77d15, 0x16a715, 0x41a615, 0x6ba515, 0x95a315, 0xbfa215, 0xe9a115, 0x18cb15, 0x42ca15, 0x6cc915, 0x97c815, 0xc1c715, 0xebc515, 0x19f015, 0x43ee15, 0x6eed15, 0x98ec15, 0xc2eb15, 0xedea15, 0x11163f, 0x3b153f, 0x66143f, 0x8f123f, 0xb9123f, 0xe3113f, 0x123a3f, 0x3d393f, 0x67383f, 0x90373f, 0xbb363f, 0xe5353f, 0x145e3f, 0x3e5d3f, 0x685c3f, 0x925b3f, 0xbc5a3f, 0xe6593f, 0x15833f, 0x40813f, 0x6a803f, 0x947f3f, 0xbe7e3f, 0xe77d3f, 0x16a73f, 0x41a63f, 0x6ba53f, 0x95a33f, 0xbfa23f, 0xe9a13f, 0x18cb3f, 0x42ca3f, 0x6cc93f, 0x97c83f, 0xc1c73f, 0xebc53f, 0x19f03f, 0x43ee3f, 0x6eed3f, 0x98ec3f, 0xc2eb3f, 0xedea3f, 0x11166a, 0x3b156a, 0x66146a, 0x8f126a, 0xb9126a, 0xe3116a, 0x123a6a, 0x3d396a, 0x67386a, 0x90376a, 0xbb366a, 0xe5356a, 0x145e6a, 0x3e5d6a, 0x685c6a, 0x925b6a, 0xbc5a6a, 0xe6596a, 0x15836a, 0x40816a, 0x6a806a, 0x947f6a, 0xbe7e6a, 0xe77d6a, 0x16a76a, 0x41a66a, 0x6ba56a, 0x95a36a, 0xbfa26a, 0xe9a16a, 0x18cb6a, 0x42ca6a, 0x6cc96a, 0x97c86a, 0xc1c76a, 0xebc56a, 0x19f06a, 0x43ee6a, 0x6eed6a, 0x98ec6a, 0xc2eb6a, 0xedea6a, 0x111694, 0x3b1594, 0x661494, 0x8f1294, 0xb91294, 0xe31194, 0x123a94, 0x3d3994, 0x673894, 0x903794, 0xbb3694, 0xe53594, 0x145e94, 0x3e5d94, 0x685c94, 0x925b94, 0xbc5a94, 0xe65994, 0x158394, 0x408194, 0x6a8094, 0x947f94, 0xbe7e94, 0xe77d94, 0x16a794, 0x41a694, 0x6ba594, 0x95a394, 0xbfa294, 0xe9a194, 0x18cb94, 0x42ca94, 0x6cc994, 0x97c894, 0xc1c794, 0xebc594, 0x19f094, 0x43ee94, 0x6eed94, 0x98ec94, 0xc2eb94, 0xedea94, 0x1116bf, 0x3b15bf, 0x6614bf, 0x8f12bf, 0xb912bf, 0xe311bf, 0x123abf, 0x3d39bf, 0x6738bf, 0x9037bf, 0xbb36bf, 0xe535bf, 0x145ebf, 0x3e5dbf, 0x685cbf, 0x925bbf, 0xbc5abf, 0xe659bf, 0x1583bf, 0x4081bf, 0x6a80bf, 0x947fbf, 0xbe7ebf, 0xe77dbf, 0x16a7bf, 0x41a6bf, 0x6ba5bf, 0x95a3bf, 0xbfa2bf, 0xe9a1bf, 0x18cbbf, 0x42cabf, 0x6cc9bf, 0x97c8bf, 0xc1c7bf, 0xebc5bf, 0x19f0bf, 0x43eebf, 0x6eedbf, 0x98ecbf, 0xc2ebbf, 0xedeabf,0x00000,0x888888,0xffffff])
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
                                (vertices[ind[0]][x],vertices[ind[0]][y],vertices[ind[0]][z]))) 
        self.tris.sort(key=lambda t: t[4], reverse=True)


        
    def draw(self):
        pyxel.cls(252) 
        pyxel.camera(-300,-300)
        pyxel.mouse(True)
        pyxel.line(300,-300,300,300,7)
        pyxel.dither(1)
        pyxel.text(-300,-280,str(int(1/(time()-self.tm))),colors[0][0][0])
        pyxel.text(-300,-290,str(self.cp),colors[0][0][0])
        self.tm = time()
        
        
        pyxel.text(-300,-300,str(len(self.tris)),colors[0][0][0])
        
        for tri in self.tris:
            self.dot = (lv @ tri[5])*-100
            pyxel.dither(1)
            #pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],tri[3])
            self.col = (tri[3][0]-self.dot,tri[3][1]-self.dot,tri[3][2]-self.dot)
            frtr(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],self.col)
            # if self.dot > 0:
            #     pyxel.dither(self.dot-0.1)
            #     pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],tri[3]+16)
            # if self.dot < 0:
            #     pyxel.dither(abs(self.dot))
            #     pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],0)

                
        

App()