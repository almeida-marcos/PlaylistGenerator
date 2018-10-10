
class Qnode:
	
	def __init__(self, left, right, bottom, top):
		self.tl = None
		self.tr = None
		self.bl = None
		self.br = None
		self.IDs = []

		self.left = left
		self.right = right
		self.bottom = bottom
		self.top = top
		self.cols = 1
		self.count = 0
	
	def Divide(self, size):

		if self.right - self.left > size or self.top - self.bottom > size:
			
			mx = self.left + (self.right - self.left)/2.0
			my = self.bottom + (self.top - self.bottom)/2.0
			
			self.tl = Qnode(self.left, mx, my, self.top)
			self.tl.Divide(size)

			self.tr = Qnode(mx, self.right, my, self.top)
			self.tr.Divide(size)

			self.bl = Qnode(self.left, mx, self.bottom, my)
			self.bl.Divide(size)

			self.br = Qnode(mx, self.right, self.bottom, my)
			self.br.Divide(size)

			self.cols = 2*self.tl.cols

	def Insert(self, x, y, id):
		
		if self.tl == None:
			self.IDs.append(id)

		else:

			mx = self.left + (self.right - self.left)/2.0
			my = self.bottom + (self.top - self.bottom)/2.0

			if x <= mx and y >= my:
				self.tl.Insert(x,y,id)
			elif x > mx and y >= my:
				self.tr.Insert(x,y,id)
			elif x <= mx and y < my:
				self.bl.Insert(x,y,id)
			else:
				self.br.Insert(x,y,id)

	def RetrieveCellIDs(self, x, y):

		if self.tl == None:
			return self.IDs

		mx = self.left + (self.right - self.left)/2.0
		my = self.bottom + (self.top - self.bottom)/2.0

		if x <= mx and y >= my:
			return self.tl.RetrieveCellIDs(x,y)
		elif x > mx and y >= my:
			return self.tr.RetrieveCellIDs(x,y)
		elif x <= mx and y < my:
			return self.bl.RetrieveCellIDs(x,y)
		else:
			return self.br.RetrieveCellIDs(x,y)

class Qtree:

	def __init__(self, left, right, bottom, top):
		self.root = Qnode(left, right, bottom, top)

	def Divide(self, size):
		self.root.Divide(size)

	def Insert(self, x, y, id):
		self.root.Insert(x,y,id)

	def RetrieveCellIDs(self, x, y):
		return self.root.RetrieveCellIDs(x, y)

	
