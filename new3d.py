import os
from math import *
import pyxel  
from random import randint
from pyxel import KEY_W,KEY_S,KEY_D,KEY_A
from pyxel import KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN
import numpy as np
from time import time
import pymeshlab
import fpng

size = 256

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

def lerp(y, y_start, y_end, start_val, end_val):
    if y_start == y_end: return start_val
    return start_val + (end_val - start_val) * (y - y_start) / (y_end - y_start)

def drawTexturedTriangle(tri, img_bank=0):
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2), (u0, v0), (u1, v1), (u2, v2), depth, (nx0,ny0,nz0), (nx1,ny1,nz1), (nx2,ny2,nz2) ,materialdata = tri

    evilZ0,evilZ1,evilZ2 = 1/z0,1/z1,1/z2
    x0, y0 = x0 + 0.001, y0 + 0.001
    x1, y1 = x1 + 0.002, y1 + 0.002
    x2, y2 = x2 + 0.003, y2 + 0.003

    vertices = sorted([(x0, y0, u0, v0, evilZ0 ,nx0 ,ny0 ,nz0), (x1, y1, u1, v1, evilZ1 ,nx1 ,ny1 ,nz1), (x2, y2, u2, v2, evilZ2 ,nx2 ,ny2 ,nz2)], key=lambda v: v[1])
    (x0, y0, u0, v0, evilZ0 ,nx0 ,ny0 ,nz0), (x1, y1, u1, v1, evilZ1 ,nx1 ,ny1 ,nz1), (x2, y2, u2, v2, evilZ2 ,nx2 ,ny2 ,nz2) = vertices

    bigX = max([x0,x1,x2])
    weeX = min([x0,x1,x2])

    
    if int(y0) == int(y2): return

    pget = pyxel.images[img_bank].pget
    pset = pyxel.pset

    inv_y2_y0 = 1.0 / (y2 - y0) if (y2 - y0) != 0 else 0.0
    inv_y1_y0 = 1.0 / (y1 - y0) if (y1 - y0) != 0 else 0.0
    inv_y2_y1 = 1.0 / (y2 - y1) if (y2 - y1) != 0 else 0.0

    start_y = int(y0)
    end_y = int(y2) + 1

    if end_y - start_y > 1000 or start_y < -500 or end_y > 500:
        return

    for y in range(start_y, end_y):
        if -128 < y < 128:
            t_ac = (y - y0) * inv_y2_y0
            xa = x0 + (x2 - x0) * t_ac
            ua = u0 + (u2 - u0) * t_ac
            va = v0 + (v2 - v0) * t_ac
            za = evilZ0 + (evilZ2 - evilZ0) * t_ac

            if y < y1:
                t_ab = (y - y0) * inv_y1_y0
                xb = x0 + (x1 - x0) * t_ab
                ub = u0 + (u1 - u0) * t_ab
                vb = v0 + (v1 - v0) * t_ab
                zb = evilZ0 + (evilZ1 - evilZ0) * t_ab
            else:
                t_bc = (y - y1) * inv_y2_y1
                xb = x1 + (x2 - x1) * t_bc
                ub = u1 + (u2 - u1) * t_bc
                vb = v1 + (v2 - v1) * t_bc
                zb = evilZ1 + (evilZ2 - evilZ1) * t_bc

            if xa > xb:
                xa, xb = xb, xa
                ua, ub = ub, ua
                va, vb = vb, va
                za, zb = zb, za

            x_start, x_end = int(xa), int(xb)
            span_width = x_end - x_start
            if span_width <= 0 or span_width > 1000: continue
            
            u_step = (ub - ua) / span_width
            v_step = (vb - va) / span_width
            z_step = (zb - za) / span_width
            
            curr_u = ua
            curr_v = va
            curr_z = za

            for screen_x in range(x_start, x_end):
                if abs(curr_z) > 0.00001:
                    real_u = curr_u / curr_z
                    real_v = curr_v / curr_z
                else:
                    real_u, real_v = 0, 0
                if weeX < screen_x < bigX:
                    if -128 < screen_x < 128:
                        pyxel.dither(1)
                        # pset(screen_x, y, pyxel.clamp(pget(int(real_u), int(real_v))+(0*-43),0,254) )
                        pset(screen_x, y, pyxel.clamp(pget(int(real_u), int(real_v))+(0*-43),0,254) )

                curr_u += u_step
                curr_v += v_step
                curr_z += z_step

tris = []

pyxel.colors.from_list([0x080909, 0x093809, 0x086909, 0x099809, 0x08c609, 0x09ff09, 0x380808, 0x383808, 0x386708, 0x389808, 0x38c608, 0x38ff08, 0x670909, 0x693809, 0x676909, 0x699809, 0x67c609, 0x69ff09, 0x980808, 0x983808, 0x986708, 0x989808, 0x98c608, 0x98ff08, 0xc60909, 0xc63809, 0xc66909, 0xc69809, 0xc6c609, 0xc6ff09, 0xff0808, 0xff3808, 0xff6708, 0xff9808, 0xffc608, 0xffff08, 0x080938, 0x093838, 0x086938, 0x099838, 0x08c638, 0x09ff38, 0x380838, 0x383838, 0x386738, 0x389838, 0x38c638, 0x38ff38, 0x670938, 0x693838, 0x676938, 0x699838, 0x67c638, 0x69ff38, 0x980838, 0x983838, 0x986738, 0x989838, 0x98c638, 0x98ff38, 0xc60938, 0xc63838, 0xc66938, 0xc69838, 0xc6c638, 0xc6ff38, 0xff0838, 0xff3838, 0xff6738, 0xff9838, 0xffc638, 0xffff38, 0x080969, 0x093869, 0x086969, 0x099869, 0x08c669, 0x09ff69, 0x380867, 0x383867, 0x386767, 0x389867, 0x38c667, 0x38ff67, 0x670969, 0x693869, 0x676969, 0x699869, 0x67c669, 0x69ff69, 0x980867, 0x983867, 0x986767, 0x989867, 0x98c667, 0x98ff67, 0xc60969, 0xc63869, 0xc66969, 0xc69869, 0xc6c669, 0xc6ff69, 0xff0867, 0xff3867, 0xff6767, 0xff9867, 0xffc667, 0xffff67, 0x080998, 0x093898, 0x086998, 0x099898, 0x08c698, 0x09ff98, 0x380898, 0x383898, 0x386798, 0x389898, 0x38c698, 0x38ff98, 0x670998, 0x693898, 0x676998, 0x699898, 0x67c698, 0x69ff98, 0x980898, 0x983898, 0x986798, 0x989898, 0x98c698, 0x98ff98, 0xc60998, 0xc63898, 0xc66998, 0xc69898, 0xc6c698, 0xc6ff98, 0xff0898, 0xff3898, 0xff6798, 0xff9898, 0xffc698, 0xffff98, 0x0809c6, 0x0938c6, 0x0869c6, 0x0998c6, 0x08c6c6, 0x09ffc6, 0x3808c6, 0x3838c6, 0x3867c6, 0x3898c6, 0x38c6c6, 0x38ffc6, 0x6709c6, 0x6938c6, 0x6769c6, 0x6998c6, 0x67c6c6, 0x69ffc6, 0x9808c6, 0x9838c6, 0x9867c6, 0x9898c6, 0x98c6c6, 0x98ffc6, 0xc609c6, 0xc638c6, 0xc669c6, 0xc698c6, 0xc6c6c6, 0xc6ffc6, 0xff08c6, 0xff38c6, 0xff67c6, 0xff98c6, 0xffc6c6, 0xffffc6, 0x0809ff, 0x0938ff, 0x0869ff, 0x0998ff, 0x08c6ff, 0x09ffff, 0x3808ff, 0x3838ff, 0x3867ff, 0x3898ff, 0x38c6ff, 0x38ffff, 0x6709ff, 0x6938ff, 0x6769ff, 0x6998ff, 0x67c6ff, 0x69ffff, 0x9808ff, 0x9838ff, 0x9867ff, 0x9898ff, 0x98c6ff, 0x98ffff, 0xc609ff, 0xc638ff, 0xc669ff, 0xc698ff, 0xc6c6ff, 0xc6ffff, 0xff08ff, 0xff38ff, 0xff67ff, 0xff98ff, 0xffc6ff, 0xffffff])

textures = []
texturescount = 0

def loadmesh(File,X,Y,Z,Scale,Tex,Rot):
    global texturescount
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(str(os.path.relpath(__file__).replace("new3d.py","sceene/"+ File + ".obj")))
    mesh = ms.current_mesh()
    meshvert = mesh.vertex_matrix().tolist()
    meshind = mesh.face_matrix().tolist()
    ms.compute_normal_per_vertex()
    meshnormals = mesh.vertex_normal_matrix().tolist()
    
    if Tex != "none":
        meshuvs = mesh.wedge_tex_coord_matrix()
        pyxel.images[1].load(0, 0, str(os.path.relpath(__file__).replace("new3d.py","sceene/"+ Tex)))
        textures.append(pyxel.images[1])
        ct = texturescount
        texturescount += 1

    for fi, ind in enumerate(meshind):
        face = [list(meshvert[ind[0]]), list(meshvert[ind[1]]), list(meshvert[ind[2]])]
    
        for vert in face:
            vert[0] = vert[0] * Scale + X
            vert[1] = vert[1] * Scale + Y
            vert[2] = vert[2] * Scale + Z
            
        for i in range(3):
            uv = meshuvs[fi * 3 + i].tolist()
            uv[0] = uv[0] * 255
            uv[1] = uv[1] * 255 
            face.append(uv)
        for i in range(3):
            norm = meshnormals[ind[i]]
            face.append(norm)

        face.append((texturescount-1,0))

        tris.append(face)

loadmesh("freakycube",0,0,100,30,"cubetex.png",(0,0,0))

print(len(tris[0]))

def istorendertriangle(P0, P1, P2):
    if P0[2] < 1.0 or P1[2] < 1.0 or P2[2] < 1.0:
        return True
    val = (P1[0] - P0[0]) * (P2[1] - P0[1]) - (P1[1] - P0[1]) * (P2[0] - P0[0])
    return val < 0

speed = 40

class App:
    def __init__(self):
        pyxel.init(size, size,fps=120)
        self.tris = []
        self.tri = []
        self.dt = 0
        self.time = time()
        self.pos = [0,0,0]
        self.yaw = radians(0)
        self.pitch = radians(0)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.dt = time()-self.time
        self.time = time()

        if pyxel.btn(KEY_W):
            self.pos[2]-= sin(self.yaw+1.5708)*speed*self.dt
            self.pos[0]-= cos(self.yaw+1.5708)*speed*self.dt
        if pyxel.btn(KEY_S):
            self.pos[2]+= sin(self.yaw+1.5708)*speed*self.dt
            self.pos[0]+= cos(self.yaw+1.5708)*speed*self.dt
        if pyxel.btn(KEY_A):
            self.pos[2]-= sin(self.yaw)*speed*self.dt
            self.pos[0]-= cos(self.yaw)*speed*self.dt
        if pyxel.btn(KEY_D):
            self.pos[2]+= sin(self.yaw)*speed*self.dt
            self.pos[0]+= cos(self.yaw)*speed*self.dt
        if pyxel.btn(pyxel.KEY_SPACE):
            self.pos[1]+= speed*self.dt
        if pyxel.btn(pyxel.KEY_SHIFT):
            self.pos[1] -=speed*self.dt
        pyxel.warp_mouse(128,128)
        if pyxel.frame_count > 100:
            self.yaw += (pyxel.mouse_x-128)*self.dt/5
            self.pitch += (pyxel.mouse_y-128)*self.dt/5

        self.tris = []
        for t in tris:
            self.tri = t[0:3]
            depth = 0
            
            projected_verts = []
            projected_zs = []
            skip_triangle = False
            
            for prevert in self.tri:
                vert = [0,0,0]
                for i in range(3):
                    vert[i] = prevert[i] + self.pos[i]

                vert = rotate_z(rotate(vert, self.yaw), self.pitch)
                FOC = vert[2]
                
                if FOC < 1.0:
                    skip_triangle = True
                    break
                    
                depth += vert[2]
                projected_zs.append(FOC)
                projected_verts.append(((vert[0] / FOC) * -128, (vert[1] / FOC) * 128, vert[2]))
                
            if skip_triangle:
                continue

            if istorendertriangle(projected_verts[0], projected_verts[1], projected_verts[2]):
                continue

            temp_tri = []
            for pv in projected_verts:
                temp_tri.append(pv)
                
            for idx, uv in enumerate(t[3:6]):
                z = projected_zs[idx]
                temp_tri.append([uv[0] / z, uv[1] / z])
                
            temp_tri.append(depth/3)
            temp_tri.extend(t[6:9])
            temp_tri.append(t[-1])
            self.tris.append(temp_tri)
            
        self.tris.sort(key=lambda t: t[6], reverse=True)

    def draw(self):
        pyxel.cls(0)
        pyxel.camera(-128,-128)
        # drawTexturedTriangle([(-100,0,30),(100,0,30),(pyxel.mouse_x-128,pyxel.mouse_y-128,30),(0,0),(0,16),(16,16)])
        for trig in self.tris:
            print(len(trig))
            pyxel.images[0] = textures[trig[10][0]]
            drawTexturedTriangle(trig)
            # pyxel.trib(trig[0][0],trig[0][1],trig[1][0],trig[1][1],trig[2][0],trig[2][1],200)
        
App()