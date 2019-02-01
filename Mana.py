from tkinter import *

class Mana:
	def __init__(self, canvas, master, color, controller, amount, max_amount, board_width, board_height, mana_width, mana_height, mana_posX, mana_posY, mana_cap):
		self.canvas = canvas
		self.master = master
		self.color = color
		self.color_code = None
		self.num = None
		self.controller = controller
		self.amount = amount
		self.mana_cap = mana_cap
		self.max_amount = max_amount
		self.drawn_elements = []
		self.mana_width = mana_width
		self.mana_height = mana_height
		self.selected_size = 0
		self.selected = False
		self.select_color = "red"
		self.highlights = []
		self.x1 = mana_posX
		self.x1_full = self.x1-(self.master.pixel_x*35)
		self.y1 = board_height-mana_posY
		self.x2 = mana_posX+self.mana_width
		self.y2 = (board_height-mana_posY)+self.mana_height
		if color == "red":
			self.num = 0
		if color == "blue":
			self.num = 1
		if color == "green":
			self.num = 2
		if color == "yellow":
			self.num = 3
		if color != "colorless":
			eval('self.' + color + '()')
			self.display_max()
			self.display_amount()

	def red(self):
		self.color_code = "#E34234" #vermillion
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill=self.color_code))
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1_full, self.y1, self.x1, self.y2, outline='black'))
		self.drawn_elements.append(self.canvas.create_line(self.x1_full, self.y1-(self.y1-self.y2)/2, self.x1, self.y1-(self.y1-self.y2)/2))

	def blue(self):
		self.color_code = "#3F00FF" #indigo
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill=self.color_code))
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1_full, self.y1, self.x1, self.y2, outline='black'))
		self.drawn_elements.append(self.canvas.create_line(self.x1_full, self.y1-(self.y1-self.y2)/2, self.x1, self.y1-(self.y1-self.y2)/2))

	def green(self):
		self.color_code = "#355E3B" #hunter green
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill=self.color_code))
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1_full, self.y1, self.x1, self.y2, outline='black'))
		self.drawn_elements.append(self.canvas.create_line(self.x1_full, self.y1-(self.y1-self.y2)/2, self.x1, self.y1-(self.y1-self.y2)/2))

	def yellow(self):
		self.color_code = "#FDEE00" #aureolin
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill=self.color_code))
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1_full, self.y1, self.x1, self.y2, outline='black'))
		self.drawn_elements.append(self.canvas.create_line(self.x1_full, self.y1-(self.y1-self.y2)/2, self.x1, self.y1-(self.y1-self.y2)/2))

	def display_max(self):
		self.max_element = self.canvas.create_text(self.x1-(self.master.pixel_x*35/2), self.y1+(self.mana_height/4), font=("Consolas", 12), text=self.max_amount, activefill=self.color_code)

	def display_amount(self):
		self.amount_element = self.canvas.create_text(self.x1-(self.master.pixel_x*35/2), self.y1+(self.mana_height*3/4), font=("Consolas", 12), text=self.amount, activefill=self.color_code)

	def set_max_amount(self, new_amount):
		self.max_amount = new_amount
		if self.max_amount > self.mana_cap:
			self.max_amount = self.mana_cap
		self.canvas.delete(self.max_element)
		self.display_max()

	def adjust_max_amount(self, value):
		self.set_max_amount(self.max_amount+value)

	def set_amount(self, new_amount):
		self.amount = new_amount
		self.canvas.delete(self.amount_element)
		self.display_amount()

	def adjust_amount(self, value):
		self.set_amount(self.amount+value)

	def select(self):
		if len(self.highlights) > 3:
			self.canvas.delete(self.highlights.pop(3))
			self.canvas.delete(self.highlights.pop(0))

		self.highlights.append(self.canvas.create_rectangle(self.x1-(self.master.pixel_x*35)-self.selected_size, self.y1-self.selected_size, self.x2+self.selected_size, self.y2+self.selected_size, outline=self.color_code))
		self.highlights.append(self.canvas.create_rectangle(self.x1-(self.master.pixel_x*35)-self.selected_size, self.y1-self.selected_size, self.x2+self.selected_size, self.y2+self.selected_size, outline=self.color_code))

		if self.selected_size > 8:
			self.selected_size = 0

	def deselect(self):
		self.selected = False
		self.selected_size = 0
		for x in range(0, len(self.highlights)):
			self.canvas.delete(self.highlights.pop())

	def delete(self):
		for element in self.drawn_elements:
			self.canvas.delete(element)