from scene import *
from random import choice
from dict import dict
import sound

class Letter(LabelNode):
	def __init__(self,**kwargs):
		LabelNode.__init__(self,**kwargs)
		
	def is_touched(self,x,y):
		#determine if a letter has been touched
		bound = self.font[1] / 2
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
		#possibly make body part sizes functions of man_space...
		self.width = 7
		self.start_color = 'white'
		self.start_alpha = 0.1
		self.end_alpha = 1
		#build head
		head_shape = ui.Path.oval(0,0,100,100)
		head_shape.line_width = self.width
		headY = self.size.h/2
		head = ShapeNode(head_shape,fill_color='clear',stroke_color=self.start_color,parent=self,position=(0,headY),alpha=self.start_alpha)
		head.anchor_point = (0.5,1)
		#build body
		body_shape = ui.Path.rect(0,0,self.width,200)
		bodyY = headY - 100
		body = ShapeNode(body_shape,fill_color=self.start_color,parent=self,position=(0,bodyY),alpha=self.start_alpha)
		body.anchor_point = (0.5,1)
		#build arms
		armY = bodyY - 50
		left_arm = self.make_limb(0,armY,-50,100)
		right_arm = self.make_limb(0,armY,50,100)
		#build legs
		legY = headY - 295
		left_leg = self.make_limb(0,legY,-50,150)
		right_leg = self.make_limb(0,legY,50,150)
		#guesses system
		self.parts = [head, body, left_arm, right_arm, left_leg, right_leg]
		self.incorrect_guesses = 0
		
	def make_limb(self,x,y,changeX,changeY):
		#set anchor point in the top left or top right corner
		anchorX = -1
		if changeX < 0:
			anchorX = 1
		#draw limb
		limb_shape = ui.Path()
		limb_shape.line_width = self.width
		limb_shape.move_to(0,0)
		limb_shape.line_to(changeX,changeY)
		limb_shape.close()
		#make shape node and add anchor point
		limb = ShapeNode(limb_shape,stroke_color=self.start_color,parent=self,position=(x,y),alpha=self.start_alpha)
		limb.anchor_point = (anchorX,1)
		return limb
		
	def add_part(self):
		if self.incorrect_guesses in range(len(self.parts)):
			self.parts[self.incorrect_guesses].alpha = self.end_alpha
			self.incorrect_guesses+=1

class Hangman(Scene):
	
	def setup(self):
		#font
		self.font_family = 'Helvetica'
		self.font_size = 40
		#setup background
		self.background_color = "#208041"
		#place letters
		self.letters = []
		self.place_letters()
		#place man
		man_space = ui.Path.rect(0,0,150,450)
		self.man = Man(path=man_space,fill_color='clear',parent=self,position=(self.size.w/2,self.size.h/2))
		#place noose...
		#choose a random word and fill the answer with blanks
		dict_array = dict.split('\n')
		self.word = choice(dict_array)
		blanks = ""
		for letter in self.word:
			blanks += "_ "
		blanks = blanks[:-1]
		self.answer = LabelNode(blanks,font=(self.font_family,self.font_size),position=(self.size.w/2,200),parent=self)
		self.game_state = LabelNode("",font=(self.font_family,self.font_size),position=(self.size.w/2,100),parent=self)
		
	def place_letters(self):
		#place all of the letters in the alphabet
		keyspace = "abcdefghijklmnopqrstuvwxyz"
		for i, char in enumerate(keyspace):
			y = self.size.h - self.font_size * 3
			margin = self.font_size * 1.5
			available_space = self.size.w - margin 
			gap = available_space / len(keyspace)
			x = margin + gap*i
			letter = Letter(text=char, font=(self.font_family,self.font_size),position=(x,y),parent=self)
			self.letters.append(letter)
			
	def touch_began(self, touch):
		#listen for touch events on letters
		#if any of the letters are touched, replace them with a dot
		if self.man.incorrect_guesses < 6:
			for let in self.letters:
				if let.is_touched(touch.location.x,touch.location.y):
					self.guess_letter(let.text)
					self.letters.remove(let)
					let.run_action(Action.remove())
					temp = SpriteNode('plf:LaserPurpleDot',position=let.position,parent=self)
				
	def replace_character(self,string,new_string,index):
		#thow error if the index is not within the bounds of the string
		if index not in range(len(string)):
			raise ValueError("index outside given string")
		else:
			return string[:index] + new_string + string[index+1:]
				
	def guess_letter(self,let):
		#replace blank with letter if it is right
		#else take away a life
		found = False
		for index, right_letter in enumerate(self.word):
			if let == right_letter:
				found = True
				blanks = self.replace_character(self.answer.text,let,2*index)
				self.answer.text = blanks
		if not found:
			self.man.add_part()	
		#after the guess, check the state of the game
		self.check_state()
			
	def check_state(self):
		if self.man.incorrect_guesses > 5:
			self.game_state.text = f'Game Over: the words was {self.word}'
		if self.answer.text.find('_') < 0:
			self.game_state.text = 'Nice!'
			
run(Hangman())
