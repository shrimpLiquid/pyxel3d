a = []
b = []
c = []

ind = []
for i in range(6):
	b = []
	for j in range(7):
		c = []
		for k in range(6):
			c.append(())
		b.append(c)
	a.append(b)
	ind.append(b)
    
from PIL import Image
from colorutils import rgb_to_hex as rth , rgb_to_hsv
import colorutils


for B in range(6):
    for G in range(7):
        for R in range(6):
            im = Image.open("pyxel3d/cols.png")
            cole = im.getpixel((R+(B*6),G))
            cole = (cole[0], cole[1], cole[2])
            a[R][G][B] = cole 
            #print("cols/" + filenames[h] + "   " + str(cole) + "    " + str((h, s, v)) + "      " + str(a[h][s][v]))
# print(a)

cl = []
numb = 0
for B in range(6):
	for G in range(7):
		for R in range(6):
			cl.append(rth(a[R][G][B]).replace("#","0x"))
			ind[R][G][B] = numb
			numb+=1

print(ind)
print(cl)

"""
colors2 = {}
for r in range(256):
	for g in range(256):
		for b in range(256):
			hsv = rgb_to_hsv((r,g,b))
			colors2[(r,g,b)] = ind[int((hsv[0]/360)*7)][int(hsv[1]*5)][int(hsv[2]*5)]
			print((r,g,b))
print(colors2)

#ksjfcbdsyxjbytvweiudtv8idyvti baugdiufvȳi iguiv̄cibubcuh̄iohihiǵugÚGuḡUIgdbcukfus


colors2 = {}"""
def rgb_to_hsv(rgb):
    """
    Convert an RGB color representation to an HSV color representation.

    (r, g, b) :: r -> [0, 255]
                 g -> [0, 255]
                 b -> [0, 255]

    :param rgb: A tuple of three numeric values corresponding to the red, green, and blue value.
    :return: HSV representation of the input RGB value.
    :rtype: tuple
    """
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    _min = min(r, g, b)
    _max = max(r, g, b)
    v = _max
    delta = _max - _min

    if _max == 0:
        return 0, 0, v

    s = delta / _max

    if delta == 0:
        delta = 1

    if r == _max:
        h = 60 * (((g - b) / delta) % 6)

    elif g == _max:
        h = 60 * (((b - r) / delta) + 2)

    else:
        h = 60 * (((r - g) / delta) + 4)

    return round(h, 3), round(s, 3), round(v, 3)

"""txt = open("output.txt","a")
txt.write("shrimp?")
txt.close()

ind = (((0, 1, 2, 3, 4, 5), (6, 7, 8, 9, 10, 11), (12, 13, 14, 15, 16, 17), (18, 19, 20, 21, 22, 23), (24, 25, 26, 27, 28, 29), (30, 31, 32, 33, 34, 35)), ((36, 37, 38, 39, 40, 41), (42, 43, 44, 45, 46, 47), (48, 49, 50, 51, 52, 53), (54, 55, 56, 57, 58, 59), (60, 61, 62, 63, 64, 65), (66, 67, 68, 69, 70, 71)), ((72, 73, 74, 75, 76, 77), (78, 79, 80, 81, 82, 83), (84, 85, 86, 87, 88, 89), (90, 91, 92, 93, 94, 95), (96, 97, 98, 99, 100, 101), (102, 103, 104, 105, 106, 107)), ((108, 109, 110, 111, 112, 113), (114, 115, 116, 117, 118, 119), (120, 121, 122, 123, 124, 125), (126, 127, 128, 129, 130, 131), (132, 133, 134, 135, 136, 137), (138, 139, 140, 141, 142, 143)), ((144, 145, 146, 147, 148, 149), (150, 151, 152, 153, 154, 155), (156, 157, 158, 159, 160, 161), (162, 163, 164, 165, 166, 167), (168, 169, 170, 171, 172, 173), (174, 175, 176, 177, 178, 179)), ((180, 181, 182, 183, 184, 185), (186, 187, 188, 189, 190, 191), (192, 193, 194, 195, 196, 197), (198, 199, 200, 201, 202, 203), (204, 205, 206, 207, 208, 209), (210, 211, 212, 213, 214, 215)), ((216, 217, 218, 219, 220, 221), (222, 223, 224, 225, 226, 227), (228, 229, 230, 231, 232, 233), (234, 235, 236, 237, 238, 239), (240, 241, 242, 243, 244, 245), (246, 247, 248, 249, 250, 251)))
for r in range(256):
	txt = open("output.txt","a")
	for g in range(256):
		for b in range(256):
			hsv = rgb_to_hsv((r,g,b))
			txt.write("("+str(r,g,b)+"):"+str(ind[int((hsv[0]/360)*7)][int(hsv[1]*5)][int(hsv[2]*5)])+",")
	txt.close()
"""