from scene import *
from random import uniform, random
import sound

class Letter(LabelNode):
	def __init__(self,**kwargs):
		LabelNode.__init__(self,**kwargs)
		
	def is_touched(self,bound,x,y):
		#determine if a letter has been touched		
		left_bound = self.position.x - bound
		right_bound = self.position.x + bound
		upper_bound = self.position.y + bound
		bottom_bound = self.position.y - bound
		if left_bound <= x and x <= right_bound and bottom_bound <= y and y <= upper_bound:
			return True
		return False
		
class Man(ShapeNode):
	def __init__(self,**kwargs):
		ShapeNode.__init__(self,**kwargs)
		self.width = 7
		#build head
		head_shape = ui.Path.oval(0,0,100,100)
		head_shape.line_width = self.width
		head = ShapeNode(head_shape,fill_color='clear',stroke_color='white',parent=self,position=(0,150))
		#build body
		body_shape = ui.Path.rect(0,0,self.width,200)
		body = ShapeNode(body_shape,fill_color='white',stroke_color='clear',parent=self,position=(0,100))
		body.anchor_point = (0.5,1)
		#build arms
		left_arm_shape = self.make_limb(-50,100)
		left_arm = ShapeNode(left_arm_shape,stroke_color='white',parent=self,position=(0,50))
		left_arm.anchor_point = (1,1)
		right_arm_shape = self.make_limb(50,100)
		right_arm = ShapeNode(right_arm_shape,stroke_color='white',parent=self,position=(0,50))
		right_arm.anchor_point = (-1,1)
		#build legs
		left_leg_shape = self.make_limb(-50,150)
		left_leg = ShapeNode(left_leg_shape,stroke_color='white',parent=self,position=(0,-95))
		left_leg.anchor_point = (1,1)
		right_leg_shape = self.make_limb(50,150)
		right_leg = ShapeNode(right_leg_shape,stroke_color='white',parent=self,position=(0,-95))
		right_leg.anchor_point = (-1,1)
		
	def make_limb(self,endX,endY):
		limb = ui.Path()
		limb.line_width = self.width
		limb.move_to(0,0)
		limb.line_to(endX,endY)
		limb.close()
		return limb

class Hangman(Scene):
	
	def setup(self):
		self.font_family = 'Helvetica'
		self.font_size = 40
		self.background_color = "#208041"
		self.background = Node(parent=self)
		self.letters = []
		self.place_letters()
		man_space = ui.Path.rect(0,0,150,450)
		self.man = Man(path=man_space,fill_color='clear',stroke_color='white',parent=self,position=(self.size.w/2,self.size.h/2))
		
	def place_letters(self):
		#place all of the letters in the alphabet
		keyspace = "abcdefghijklmnopqrstuvwxyz"
		for i, char in enumerate(keyspace):
			y = self.size.h - self.font_size * 3
			margin = self.font_size * 1.5
			available_space = self.size.w - margin 
			gap = available_space / len(keyspace)
			x = margin + gap*i
			letter = Letter(text=char, font=(self.font_family,self.font_size), position=(x,y))
			self.letters.append(letter)
			self.background.add_child(letter)
			
	def touch_began(self, touch):
		#listen for touch events on letters
		#if any of the letters are touched, replace them with a dot
		for let in self.letters:
			if let.is_touched(self.font_size / 2,touch.location.x,touch.location.y):
				self.letters.remove(let)
				let.run_action(Action.remove())
				temp = SpriteNode('plf:LaserPurpleDot',position=let.position,parent=self)
		
run(Hangman())
