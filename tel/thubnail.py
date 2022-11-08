
import appuifw
import e32
import graphics
import key_codes
import os
class FlickrS60Error(Exception): pass
class FlickrS60Thumb:
	def __init__(self, path):
		self.path = unicode(path)
		self.listFile = []
		self.ldivx = 0
		self.ldivy = 0
		self.lock = e32.Ao_lock()
		self.canvas = None
		self.img = graphics.Image.new((176, 144))
		self.img_tmp = graphics.Image.new((42, 36))
		self.x, self.y = 0, 0
		self.p = 0
		self.pages = 0
		self.currpages = 0
		self.mpath = 0
	def OnRun(self):
		appuifw.app.exit_key_handler = self.lock.signal
	
		self._createList()
		
		self.canvas = appuifw.Canvas(redraw_callback=self.OnUpdate)
		appuifw.app.body = self.canvas
		self.canvas.bind(key_codes.EKeyRightArrow, lambda: self.move(1, 0))
		self.canvas.bind(key_codes.EKeyLeftArrow, lambda: self.move(-1, 0))
		self.canvas.bind(key_codes.EKeyUpArrow, lambda: self.move(0, -1))
		self.canvas.bind(key_codes.EKeyDownArrow, lambda: self.move(0, 1))
		self.canvas.bind(key_codes.EKeySelect, self.IMG)
		self._drawIMG()
		
		self.lock.wait()
	def OnUpdate(self, rect):
		self.canvas.blit(self.img)
		self.canvas.rectangle([(self.p+(42*self.x), 36*self.y), (self.p+(42*self.x)+42, (36*self.y)+36)], width=2, outline=0x123456)
	def move(self, x, y):
		self.x = (self.x+x)%4
		self.y = (self.y+y)
		if x == 1: self.p = (self.p+2)%8
		if x == -1: self.p = (self.p-2)%8
		if self.y == 4:
			if self.currpages < self.pages-1:
				self.y = 0
				self.currpages += 1
				self._drawIMG(start=self.currpages)
			else:
				self.y = 3
			
		if self.y == -1:
			if self.currpages > 0:
				self.y = 3
				self.currpages -= 1
				self._drawIMG(start=self.currpages)
			else:
				self.y = 0
	
		self.mpath = (4*self.y + self.x)+(16*self.currpages)
		
		self.OnUpdate(None)
	
	def IMG(self):
		try:
			m = self.listFile[self.mpath].replace('_PalbTN\\', '')
			appuifw.Content_handler().open(m)
		except:
			pass
		
	def _drawIMG(self, start=0):
		self.img.clear(0xffffff)
		z = 0
		
		for id in range(start*16, (start+1)*16):
			j, i = divmod(id-(start*16), 4)
			try:
				self.img_tmp.load(self.listFile[id])
				self.img.blit(self.img_tmp, target=(z+(42*i)+(z+1), 36*j))
				z = (z+1)%4
			except:
				break
		self.OnUpdate(None)
	def _createList(self):
		try:
			for id in os.listdir(self.path):
				self.listFile.append(self.path + id)
			self.ldivx, self.ldivy = divmod(len(self.listFile), 16)
			self.pages = self.ldivx
			if self.ldivy <> 0: self.pages += 1
		except:
			raise FlickrS60Error('Errore nella creazione della lista.')
if __name__ == '__main__':
#	FlickrS60Thumb('E:\\Images\\_PalbTN\\').OnRun()
	FlickrS60Thumb('c:\\data\\download\\').OnRun()
