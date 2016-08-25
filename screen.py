import ui
import numpy
import matplotlib.image as im
import io
import Image

class Screen(ui.View):
	def __init__(self,w,h):
		self.width=h
		self.height=w
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
		im.imsave(self.B,self.S.transpose([1,0,2])/255.,format='png')
		self.B.seek(0)
		self.set_needs_display()
	def blit(self,data,corner):
		self.S[corner[0]:(corner[0]+data.shape[0]), corner[1]:(corner[1]+data.shape[1]), :]=data
		self.updates_pending+=1
		self.update()
	@ui.in_background
	def update(self):
		#ui.Image.from_data(self.B.getvalue())
		self.updates_pending-=1
		if self.updates_pending>0:
			self.skip+=1
			if self.skip<5:
				return
		self.skip=0
		im.imsave(self.B,self.S.transpose([1,0,2])/255.,format='jpg')
		self.B.seek(0)
		self.set_needs_display()
	def draw(self):
		ui.Image.from_data(self.B.getvalue()).draw()

