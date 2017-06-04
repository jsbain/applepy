import ui
import numpy
import matplotlib.image as im
import io
import Image
import threading

class Screen(ui.View):
	def __init__(self,w,h):
		self.width=w
		self.height=h
		self.S=numpy.zeros((w,h,3))
		self.B=io.BytesIO()
		ui.Image.from_data(self.B.getvalue())
		im.imsave(self.B,self.S,format='jpg')
		self.B.seek(0)
		self.set_needs_display()
		self.updates_pending=0
		self.skip=0
	def set_data(self,S):
		self.S=S
		#ui.Image.from_data(self.B.getvalue())
		im.imsave(self.B,self.S.transpose([1,0,2])/255.,format='jpg')
		self.B.seek(0)
		self.set_needs_display()
	def blit(self,data,corner):
		#print(data[1,1,2])
		try:
			self.S[corner[0]:(corner[0]+data.shape[0]), corner[1]:(corner[1]+data.shape[1]), :]=data
			if not self.updates_pending:
					self.updates_pending+=1
					self.update()
		except:
			pass
	@ui.in_background
	def update(self):
		self.updates_pending =0
		im.imsave(self.B,self.S.transpose([1,0,2])/255.,format='jpg')
		self.B.seek(0)
		self.set_needs_display()
	def draw(self):
		if not self.on_screen:
			raise KeyboardInterrupt()
		ui.Image.from_data(self.B.getvalue()).draw()


if __name__=='__main__':
	import time
	w=300
	h=w
	s=Screen(w,h)

	d=numpy.zeros((w*h,3))
	d[:,0]=128+128*numpy.sin(w*7*numpy.linspace(0,6.28,w*h))
	d[:,1]=128+128*numpy.sin(3/4+w*4.1*numpy.linspace(0,6.28,w*h))
	d[:,2]=128+128*numpy.sin(3+1.7*numpy.linspace(0,6.28,w*h))
	#d=d.reshape(3,w*h).transpose()
	s.set_data(d.reshape(w,h,3))
	s.present('sheet')
	time.sleep(1)
	pixel=255*numpy.ones((5,5,3))
	def runloop():
		for r in range(0,h,5):
			for c in range(0,w,5):
				s.blit(pixel,[c,r])
			#time.sleep(0.1)
		time.sleep(2)
		s.set_data(	numpy.zeros((w,h,3)))
		#s.update()
	import threading
	threading.Thread(target=runloop).start()

