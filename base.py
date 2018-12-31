import cv2
import numpy as np
import cv2


### all in camera frame for simplicy

red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)
random = (55, 68, 129)

colors = [red, blue, green, random]

class Camera():
	def __init__(self, depth=30):
		self.depth = depth
		img = np.zeros((500, 500, 3))
		img = img.astype('uint8') + 255
		self.img = img
		cv2.circle(self.img, (250, 250), 3, (124, 97, 756), -1)
		

	def proj(self, pt):
		x = float(pt[0]) / float(pt[2]) * self.depth
		y = float(pt[1]) / float(pt[2]) * self.depth
		return (-int(x)+250, -int(y)+250)
	
	def render_pt(self, pt, color):
		cv2.circle(self.img, pt, 5, color, -1)

	def render_poly(self, pts, color):
		pts.append(pts[0])
		index =0
		for i in range(len(pts)-1):
			cv2.line(self.img, pts[i], pts[i+1], colors[i], 2)
			index += 1

	def view(self, duration):
		cv2.imshow('view', self.img)
		key = cv2.waitKey(duration)
		return key

	def rotX(self, theta, pt):
		M = np.array([[1, 0, 0], 
					  [0, np.cos(theta), -np.sin(theta)], 
					  [0, np.sin(theta), np.cos(theta)]])
		pt_rot = M.dot(np.asarray(pt).reshape((3, 1)))
		return pt_rot

	def rotY(self, theta, pt):
		M = np.array([[np.cos(theta), 0, np.sin(theta)], 
					  [0, 1, 0], 
					  [-np.sin(theta), 0, np.cos(theta)]])
		pt_rot = M.dot(np.asarray(pt).reshape((3, 1)))
		return pt_rot.astype('int')

	def refresh(self):
		self.img[:, :, :] = 255
		cv2.circle(self.img, (250, 250), 3, (124, 97, 756), -1)
	

cam = Camera(depth=5)

Pt1 = [1000.0, 1000.0, 200.0]
Pt2 = [1000.0, -1000.0, 200.0]
Pt3 = [-1000.0, -1000.0, 200.0]
Pt4 = [-1000.0, 1000.0, 200.0]
shape = [Pt1, Pt2, Pt3, Pt4]



Ytheta = 0
Xtheta = 0

while True:
	pts = []
	index = 0
	for pt in shape:
		pt = cam.rotY( Ytheta* np.pi/180, pt)
		pt = cam.rotX( Xtheta* np.pi/180, pt)
		pt = cam.proj(pt)
		pts.append(pt)
	cam.render_poly(pts, red)

	key = cam.view(1)
	if key == 84:
		Xtheta -=1
		print('up')
	if key == 82:
		Xtheta +=1
		print('down')
	if key == 83:
		Ytheta +=1
		print('left')
	if key == 81:
		Ytheta -=1
		print('right')
	cam.refresh()
	





		



