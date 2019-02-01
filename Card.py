from tkinter import *
import tkinter.font
from PIL import ImageTk, Image

import math

class Card:
	def __init__(self, canvas, master, controller, name, status, card_posX, card_posY):
		self.canvas = canvas
		self.master = master
		self.name = name
		self.status = status
		self.prev_status = None
		self.controller = controller
		if self.controller == 1:
			self.enemy = 2
		else:
			self.enemy = 1
		self.drawn_elements = []
		self.highlights = []
		self.font_size = self.master.font_size
		self.large_font_size = self.master.large_font_size
		self.board_width = self.master.board_width
		self.board_height = self.master.board_height
		if "Display" in self.status:
			self.face_up = True
			self.font_size = 26#int(math.ceil(self.master.font_size*2.5))
			self.card_width = self.master.card_width*2.5
			self.card_height = self.master.card_height*2.5
		else:
			self.face_up = False
			self.card_width = self.master.card_width
			self.card_height = self.master.card_height

		self.mana_width = self.card_width/10
		self.mana_height = self.card_height/15
		self.mana_buffer = self.card_width/30
		self.pixel_x = self.card_width/100
		self.pixel_y = self.card_height/150

		self.selected_size = 0
		self.can_attack = False
		self.card_effect = None
		self.countered = False
		self.readable_effect = []
		self.effect_targets = []
		self.type = "Unit"
		self.token = False
		self.construct = False
		self.attack = None
		self.defense = None
		self.card_img = None
		self.ez_stat_display = False

		self.zone_discount = None
		self.zone_color = None
		self.zone_number = None

		#keywords
		self.undermine = False
		self.alacrity = False
		self.covert = False
		self.piercing = False
		self.healtouch = False
		self.arrival = False
		self.into_play = False
		self.afterdeath = False
		self.discard = False
		self.mill = False
		self.procure = False
		self.consume = False
		self.stake = False
		self.aura = False
		self.aura_status = None
		self.staked_zone = None
		self.activatable = False
		self.prep = False
		self.prep_type = None

		#effect commands
		self.activated_commands = []
		self.activated_condition = "False"
		self.arrival_commands = []
		self.arrival_condition = "True"
		self.into_play_commands = []
		self.into_play_condition = "True"
		self.afterdeath_commands = []
		self.afterdeath_condition = "True"
		self.aura_commands = []
		self.aura_condition = "True"
		self.ondraw_effects = []
		self.ondraw_condition = "True"
		self.resolve_commands = []
		self.resolve_condition = "True"
		self.resolve_arrival_commands = []
		self.resolve_arrival_condition = "True"
		self.resolve_afterdeath_commands = []
		self.resolve_afterdeath_condition = "True"
		self.prep_commands = []
		self.prep_condition = "True"
		self.prep_activated_commands = []
		self.prep_activated_condition = "True"

		self.follow_up_commands = []
		self.follow_up_condition = "True"

		self.base_card_cost = [0, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()
		self.base_effect_cost = [0, 0, 0, 0, 0]
		self.effect_cost = self.base_effect_cost.copy()
		self.inputs = []
		self.iterations = 0

		self.activated_repeats = 0
		self.arrival_repeats = 0
		self.into_play_repeats = 0
		self.aura_repeats = 0
		self.afterdeath_repeats = 0
		self.discard_repeats = 0
		self.mill_repeats = 0
		self.prep_repeats = 0
		self.prep_activated_repeats = 0
		self.follow_up_repeats = 0

		self.attack_targets = self.master.get_list("Board", self.enemy)
		self.effect_counters = 0

		self.select_color = 'red'
		self.attack_text = None
		self.defense_text = None

		self.x1 = card_posX
		self.y1 = card_posY#self.board_height-card_posY
		self.x2 = card_posX+self.card_width
		self.y2 = card_posY+self.card_height#(self.board_height-card_posY)+self.card_height
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='white'))
		if "Empty" not in self.status and "Alive" not in self.status and "Button" not in self.status and "Open" not in self.status:
			eval('self.' + name + '()')
		if self.status == "Display" and self.card_effect is not None:
			text_boxY = (self.pixel_y*4)+len(self.readable_effect)*(self.pixel_y*12)
			self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y2, self.x2, self.y2+text_boxY, outline='black', fill='white'))
			if self.activatable and self.type == "Unit":
				self.draw_cost(self.effect_cost, True)
			buffer_y = 0
			buffer_x = (self.base_max_length - self.first_max_length)*self.pixel_x*10/3
			index = 1
			for line in self.readable_effect:
				self.drawn_elements.append(self.canvas.create_text(self.x1+(self.pixel_x*4)+buffer_x, self.y2+(self.pixel_y*4)+buffer_y, anchor=NW, font=("Consolas", int(self.font_size/3*2)), text=line))

				if buffer_x == (self.base_max_length - self.second_max_length)*self.pixel_x*10/3:
					buffer_x = 0
				if buffer_x == (self.base_max_length - self.first_max_length)*self.pixel_x*10/3:
					buffer_x = (self.base_max_length - self.second_max_length)*self.pixel_x*10/3
				
				buffer_y = (self.pixel_y*12)*index
				index += 1


	def stickman(self):
		self.drawn_name = "Stickman"
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='white'))	
		# self.card_cost = [['red', 0], ['blue', 1], ['green', 0], ['yellow', 0], ['colorless', 0]]
		self.primary_color = 1
		self.base_card_cost = [0, 1, 0, 0, 1]
		self.card_cost = self.base_card_cost.copy()
		self.base_attack = 2
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		if self.face_up:
			self.draw_cost(self.card_cost, False)
			self.draw_atk_def()

			head_x1 = self.card_width/3 + self.x1
			head_y1 = self.y1 + self.card_height/10
			head_x2 = head_x1 + self.card_width/3
			head_y2 = head_y1 + self.card_width/3
			self.drawn_elements.append(self.canvas.create_oval(head_x1, head_y1, head_x2, head_y2, fill='blue'))

			body_x1 = (head_x1+head_x2)/2 - self.card_width/30
			body_y1 = head_y2
			body_x2 = (head_x1+head_x2)/2 + self.card_width/30
			body_y2 = head_y2 + self.card_height/3
			self.drawn_elements.append(self.canvas.create_rectangle(body_x1, body_y1, body_x2, body_y2, outline='', fill='blue'))

			arm1_x0 = body_x1
			arm1_y0 = body_y1 + self.card_height/30
			arm1_x1 = arm1_x0
			arm1_y1 = arm1_y0 + (self.card_height/30)
			arm1_x2 = arm1_x0 - self.card_width/4
			arm1_y2 = body_y2
			arm1_x3 = arm1_x2 - self.card_height/30
			arm1_y3 = arm1_y2
			self.drawn_elements.append(self.canvas.create_polygon(arm1_x0, arm1_y0, arm1_x1, arm1_y1, arm1_x2, arm1_y2, arm1_x3, arm1_y3, fill='blue'))

			arm2_x0 = body_x2
			arm2_y0 = body_y1 + self.card_height/30
			arm2_x1 = arm2_x0
			arm2_y1 = arm1_y0 + (self.card_height/30)
			arm2_x2 = arm2_x0 + self.card_width/4
			arm2_y2 = body_y2
			arm2_x3 = arm2_x2 + self.card_height/30
			arm2_y3 = arm2_y2
			self.drawn_elements.append(self.canvas.create_polygon(arm2_x0, arm2_y0, arm2_x1, arm2_y1, arm2_x2, arm2_y2, arm2_x3, arm2_y3, fill='blue'))

			leg1_x0 = body_x1
			leg1_y0 = body_y2 - (self.card_height/30)
			leg1_x1 = leg1_x0
			leg1_y1 = leg1_y0 + (self.card_height/30)
			leg1_x2 = leg1_x0 - self.card_width/4
			leg1_y2 = body_y2 + self.card_height/3
			leg1_x3 = leg1_x2 - self.card_height/30
			leg1_y3 = leg1_y2
			self.drawn_elements.append(self.canvas.create_polygon(leg1_x0, leg1_y0, leg1_x1, leg1_y1, leg1_x2, leg1_y2, leg1_x3, leg1_y3, fill='blue'))

			leg2_x0 = body_x2
			leg2_y0 = body_y2 - (self.card_height/30)
			leg2_x1 = leg2_x0
			leg2_y1 = leg1_y0 + (self.card_height/30)
			leg2_x2 = leg2_x0 + self.card_width/4
			leg2_y2 = body_y2 + self.card_height/3
			leg2_x3 = leg2_x2 + self.card_height/30
			leg2_y3 = leg2_y2
			self.drawn_elements.append(self.canvas.create_polygon(leg2_x0, leg2_y0, leg2_x1, leg2_y1, leg2_x2, leg2_y2, leg2_x3, leg2_y3, fill='blue'))

	def redstickman(self):
		self.drawn_name = "Red Stickman"
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='white'))	
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 2]
		self.card_cost = self.base_card_cost.copy()
		self.base_attack = 3
		self.base_defense = 3
		self.attack = self.base_attack
		self.defense = self.base_defense

		if self.face_up:
			self.draw_cost(self.card_cost, False)
			self.draw_atk_def()

			head_x1 = self.card_width/3 + self.x1
			head_y1 = self.y1 + self.card_height/10
			head_x2 = head_x1 + self.card_width/3
			head_y2 = head_y1 + self.card_width/3
			self.drawn_elements.append(self.canvas.create_oval(head_x1, head_y1, head_x2, head_y2, fill='red'))

			body_x1 = (head_x1+head_x2)/2 - self.card_width/30
			body_y1 = head_y2
			body_x2 = (head_x1+head_x2)/2 + self.card_width/30
			body_y2 = head_y2 + self.card_height/3
			self.drawn_elements.append(self.canvas.create_rectangle(body_x1, body_y1, body_x2, body_y2, outline='', fill='red'))

			arm1_x0 = body_x1
			arm1_y0 = body_y1 + self.card_height/30
			arm1_x1 = arm1_x0
			arm1_y1 = arm1_y0 + (self.card_height/30)
			arm1_x2 = arm1_x0 - self.card_width/4
			arm1_y2 = body_y2
			arm1_x3 = arm1_x2 - self.card_height/30
			arm1_y3 = arm1_y2
			self.drawn_elements.append(self.canvas.create_polygon(arm1_x0, arm1_y0, arm1_x1, arm1_y1, arm1_x2, arm1_y2, arm1_x3, arm1_y3, fill='red'))

			arm2_x0 = body_x2
			arm2_y0 = body_y1 + self.card_height/30
			arm2_x1 = arm2_x0
			arm2_y1 = arm1_y0 + (self.card_height/30)
			arm2_x2 = arm2_x0 + self.card_width/4
			arm2_y2 = body_y2
			arm2_x3 = arm2_x2 + self.card_height/30
			arm2_y3 = arm2_y2
			self.drawn_elements.append(self.canvas.create_polygon(arm2_x0, arm2_y0, arm2_x1, arm2_y1, arm2_x2, arm2_y2, arm2_x3, arm2_y3, fill='red'))

			leg1_x0 = body_x1
			leg1_y0 = body_y2 - (self.card_height/30)
			leg1_x1 = leg1_x0
			leg1_y1 = leg1_y0 + (self.card_height/30)
			leg1_x2 = leg1_x0 - self.card_width/4
			leg1_y2 = body_y2 + self.card_height/3
			leg1_x3 = leg1_x2 - self.card_height/30
			leg1_y3 = leg1_y2
			self.drawn_elements.append(self.canvas.create_polygon(leg1_x0, leg1_y0, leg1_x1, leg1_y1, leg1_x2, leg1_y2, leg1_x3, leg1_y3, fill='red'))

			leg2_x0 = body_x2
			leg2_y0 = body_y2 - (self.card_height/30)
			leg2_x1 = leg2_x0
			leg2_y1 = leg1_y0 + (self.card_height/30)
			leg2_x2 = leg2_x0 + self.card_width/4
			leg2_y2 = body_y2 + self.card_height/3
			leg2_x3 = leg2_x2 + self.card_height/30
			leg2_y3 = leg2_y2
			self.drawn_elements.append(self.canvas.create_polygon(leg2_x0, leg2_y0, leg2_x1, leg2_y1, leg2_x2, leg2_y2, leg2_x3, leg2_y3, fill='red'))

	def pineapple(self):
		self.drawn_name = "Pineapple"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/pineappleS.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 0, 0, 3, 1]
		self.card_cost = self.base_card_cost.copy()
		
		self.base_attack = 6
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Destroy an enemy unit."
		self.activated_condition = "'Zone' in card.status and self.get_list('Board', card.enemy) is not None"
		self.activated_commands = ["secondary_targets[0].move('Disc'+str(secondary_targets[0].controller))"]#, "self.deselect_card()"]
		self.activatable = True
		self.base_effect_cost = [0, 0, 0, 1, 1]
		self.effect_cost = self.base_effect_cost.copy()
		self.make_readable_text(self.card_effect)
		self.effect_targets = self.master.get_list("Board", self.enemy) #self.master.enemy_list

		# if self.face_up:
		self.redraw_card()
			# self.draw_cost(self.card_cost, False)
			# self.draw_atk_def()
			
			# self.drawn_elements.append(self.canvas.create_image(self.x1+1, self.y1+self.mana_height+(self.mana_buffer*3), image=self.card_img, anchor=NW))

	def flytrap(self):
		self.drawn_name = "Flytrap"
		# self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='white'))	
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 2, 0, 2]
		self.card_cost = self.base_card_cost.copy()
		
		self.base_attack = 4
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Consume"
		self.make_readable_text(self.card_effect)
		self.consume = True

		# if self.face_up:
		self.redraw_card()

	def angry_rabbit(self):
		self.drawn_name = "Angry Rabbit"
		# self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='white'))	
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/angry_rabbit.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()
		
		self.base_attack = 2
		self.base_defense = 0
		self.attack = self.base_attack
		self.defense = self.base_defense

		# if self.face_up:
		self.redraw_card()
			# self.draw_cost(self.card_cost, False)
			# self.draw_atk_def()
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		# self.drawn_elements.append(self.canvas.create_image(self.x1+1, self.y1+self.mana_height+(self.mana_buffer*3), image=self.card_img, anchor=NW))

	def slithery_snake(self):
		self.drawn_name = "Slithery Snake"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/slithery_snake.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 1
		self.base_card_cost = [1, 0, 0, 0, 2]
		self.card_cost = self.base_card_cost.copy()
		
		self.base_attack = 1
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Swap this Unit's stats."
		self.activated_condition = "'Zone' in card.status"
		self.activated_commands = ["card.swap_stats()"]
		self.activatable = True
		self.base_effect_cost = [0, 0, 0, 0, 1]
		self.effect_cost = self.base_effect_cost.copy()
		self.make_readable_text(self.card_effect)
		self.effect_targets = [self]

		self.redraw_card()

	def fast_rabbit(self):
		self.drawn_name = "Fast Rabbit"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/fast_rabbit.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [2, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()
		
		self.base_attack = 2
		self.base_defense = 0
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "Alacrity"
		self.make_readable_text(self.card_effect)
		
		self.alacrity = True
		self.can_attack = True

		self.redraw_card()
			# self.draw_cost(self.card_cost, False)
			# self.draw_atk_def()
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		# self.drawn_elements.append(self.canvas.create_image(self.x1+1, self.y1+self.mana_height+(self.mana_buffer*3), image=self.card_img, anchor=NW))

	def cantrip(self):
		self.drawn_name = "Cantrip"
		self.type = "Spell"
		
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()
		
		self.card_effect = "Draw a 1 cost Unit from your deck."
		self.make_readable_text(self.card_effect)
		self.activated_condition = "'Hand' in card.status and self.card_group(card.procure_pool, card.procure_types, card.procure_names, card.procure_colors, card.procure_mana_totals, []) != []"
		self.activated_commands = ["card.secondary_select(self.card_group(card.procure_pool, card.procure_types, card.procure_names, card.procure_colors, card.procure_mana_totals, []))", "self.draw_specific_card(card.inputs.pop())"]
		# self.resolve_commands = ["self.move('Disc'+str(self.controller))", "self.master.deselect_card()", "self.master.draw(target)"]
		# self.master.card_group(self.master.get_list('Board', self.controller), '', '', 'Green', range(0, 30)), 'Defense', 1)
		self.activatable = True
		self.base_effect_cost = self.card_cost
		self.effect_cost = self.base_effect_cost.copy()
		self.effect_targets = [self.master.get_list("Deck_Zone", self.controller)]
		self.procure = True
		self.procure_pool = self.master.get_list("Deck", self.controller)
		self.procure_types = ["Unit"]
		self.procure_names = []
		self.procure_colors = []
		self.procure_mana_totals = [1]

		self.redraw_card()

	def drill_mole(self):
		self.drawn_name = "Drill Mole"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/drill_mole.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 1, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Undermine"
		self.make_readable_text(self.card_effect)
		self.undermine = True
		
		self.redraw_card()

	def ramparoo(self):
		self.drawn_name = "Ramparoo"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 2, 0, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 2
		self.base_defense = 2
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Gain 1 Green Mana at the end of this turn."
		self.make_readable_text(self.card_effect)
		self.arrival_commands = ["self.end_of_turn_effects.append('self.curr_mana_list[2].adjust_max_amount(1)')", "self.end_of_turn_effects.append('self.curr_mana_list[2].adjust_amount(1)')"]
		self.arrival = True
		
		self.redraw_card()

	def ramparee(self):
		self.drawn_name = "Ramparee"
		self.type = "Spell"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 1, 0, 1]
		self.card_cost = self.base_card_cost.copy()
		
		self.card_effect = "Gain 1 Green Mana at the end of this turn."
		self.make_readable_text(self.card_effect)
		self.activated_condition = "'Hand' in card.status"
		self.activated_commands = ["self.end_of_turn_effects.append('self.curr_mana_list[2].adjust_max_amount(1)')", "self.end_of_turn_effects.append('self.curr_mana_list[2].adjust_amount(1)')"]
		# self.effect_commands.append("card.move('Disc'+str(card.controller))")
		# self.effect_commands.append("self.master.deselect_card()")
		# self.effect_commands.append("self.master.display_hand()")
		self.activatable = True
		self.base_effect_cost = self.card_cost
		self.effect_cost = self.base_effect_cost.copy()
		self.effect_targets = [self]
		
		self.redraw_card()

	def failure_to_launch(self): #failure to lunch? counter consume lul
		self.drawn_name = "Failure to Launch"
		self.type = "Spell"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [2, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()
		
		self.card_effect = "Prep: When your opponent plays a Unit, counter it."
		self.make_readable_text(self.card_effect)
		self.prep_activated_condition = "'Disc' not in secondary_targets[0].status"
		self.prep_activated_commands = ["secondary_targets[0].move('Disc'+str(secondary_targets[0].controller))", "secondary_targets[0].countered = True"]#, "self.deselect_card()", "self.display_hand()"]
		# self.effect_commands = ["self.master.end_of_turn_effects.append('self.curr_mana_list[1].max_amount+=1')"]
		# self.effect_commands.append("self.master.end_of_turn_effects.append('self.curr_mana_list[1].set_amount(self.curr_mana_list[1].amount+1)')")
		# self.effect_commands.append("self.discard()")

		# self.effect_commands.append("self.master.display_hand()")
		self.activatable = True
		self.prep = True
		self.prep_type = "cast_card"+str(self.enemy)
		self.base_effect_cost = self.card_cost
		self.effect_cost = self.base_effect_cost.copy()
		self.effect_targets = [self]
		
		self.redraw_card()

	def unexpected_sacrifice(self):
		self.drawn_name = "Unexpected Sacrifice"
		self.type = "Spell"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [2, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()
		
		self.card_effect = "Prep: When an ally minion dies, draw 2 cards."
		self.make_readable_text(self.card_effect)
		self.prep_activated_commands = ["self.draw_from_deck(self.enemy,2)"]
		self.activatable = True
		self.prep = True
		self.prep_type = "unit_death"+str(self.controller)
		self.base_effect_cost = self.card_cost
		self.effect_cost = self.base_effect_cost.copy()
		self.effect_targets = [self]
		
		self.redraw_card()

	def sturdy_roots(self):
		self.drawn_name = "Sturdy Roots"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/sturdy_roots.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 2, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 3
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Stake: Units placed on the staked zone cost 1 less colorless mana."
		self.make_readable_text(self.card_effect)
		self.arrival_condition = "len(self.open_zones(self.curr_zone_list)) > 0"
		self.arrival_commands = ["card.secondary_select(card.stake_targets)", "card.inputs[0].add_zone_effect([0,0,0,0,-1])", "card.staked_zone=(card.inputs.pop())"]
		# self.resolve_arrival_commands = ["target.zone_discount=[0,0,0,0,-1]", "target.zone_color=self.get_color(2)", "target.redraw_card()", "self.staked_zone=target", "self.master.deselect_card()"]
		self.afterdeath_commands = ["card.staked_zone.zone_discount=None", "card.staked_zone.delete()", "card.staked_zone.redraw_card()", "card.staked_zone=None"]
		self.arrival = True
		self.stake = True
		self.afterdeath = True
		# self.effect_commands = ["card.discard()", "self.draw_from_deck(self.enemy,2)"]
		self.base_effect_cost = self.card_cost
		self.effect_cost = self.base_effect_cost.copy()
		# self.effect_targets = self.master.get_list("Zone", self.controller) #self.master.curr_zone_list
		self.stake_targets = self.master.get_list("Zone", self.controller)
		
		self.redraw_card()

	def fungo(self):
		self.drawn_name = "Fungo"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 0
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Afterdeath: Deal 2 damage to the enemy hero."
		self.make_readable_text(self.card_effect)
		self.afterdeath_commands = ["self.adjust_health(card.enemy, -2)"]
		self.afterdeath = True
		
		self.redraw_card()

	def big_leech(self):
		self.drawn_name = "Big Leech"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [2, 0, 0, 0, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 4
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Lose 3 health."
		self.make_readable_text(self.card_effect)
		self.arrival_commands = ["self.adjust_health(card.controller, -3)"]
		self.arrival = True
		
		self.redraw_card()

	def dakter(self):
		self.drawn_name = "Dakter"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 2]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 2
		self.base_defense = 3
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Gain 3 health."
		self.make_readable_text(self.card_effect)
		self.arrival_commands = ["self.adjust_health(card.controller, 3)"]
		self.arrival = True
		
		self.redraw_card()

	def poison_peddler(self):
		self.drawn_name = "Poison Peddler"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/poison_peddler.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 2]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 2
		self.base_defense = 2
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Lose 2 health. Reduce target enemy unit's defense by 2."
		self.make_readable_text(self.card_effect)
		# self.arrival_condition = "self.enemy_board_list"
		self.arrival_commands = ["self.adjust_health(card.controller, -2)", "card.follow_up_commands = card.arrival_follow_up_commands"]
		self.follow_up_condition = "self.enemy_board_list"
		self.arrival_follow_up_commands = ["card.secondary_select(card.arrival_targets)", "card.inputs[0].adjust_stats('Defense', -2)", "card.inputs.pop().redraw_card()"]
		# self.resolve_commands = ["target.adjust_stats('Defense', -2)", "target.redraw_card()", "self.master.deselect_card()"]
		self.arrival = True
		self.arrival_targets = self.master.get_list("Board", self.enemy)

		self.redraw_card()

	def mushrumi(self):
		self.drawn_name = "Mushrumi"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/venus_flytrap.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 0, 0, 0, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 2
		self.base_defense = 2
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Aura: Whenever an ally unit dies, deal 1 damage to the enemy hero and gain 1 health."
		self.make_readable_text(self.card_effect)
		self.aura_condition = "('Zone' in card.status) and (secondary_targets[0].controller == card.controller)"
		self.aura_commands = ["self.adjust_health(card.enemy, -1)", "self.adjust_health(card.controller, 1)"]
		# self.afterdeath_condition = "not self.countered"
		# self.afterdeath_commands = ["self.aura_cards.remove(card)"]
		# self.afterdeath = True
		self.aura = True
		self.aura_type = "unit_death"+str(self.controller)
		self.aura_status = "Zone"
		
		self.redraw_card()

	def cherry(self):
		self.drawn_name = "Cherry"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/poison_peddler.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 0, 0, 1, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 0
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Summon a 1/0 Cherry Twin."
		self.make_readable_text(self.card_effect)
		self.arrival_condition = "len(self.open_zones(self.curr_zone_list)) > 0"
		self.arrival_commands = ["card.secondary_select(card.arrival_targets)", "self.summon_token(card.name, card.inputs.pop())"]
		# self.resolve_arrival_commands = ["self.summon_tokens(card.name, card.inputs)", "self.deselect_card()"]
		self.arrival = True
		self.arrival_targets = self.master.get_list("Zone", self.controller)
		self.arrival_repeats = 0

		self.redraw_card()

	def frail_wanderer(self):
		self.drawn_name = "Frail Wanderer"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/frail_wanderer.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 2, 0, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 4
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "When this card is discarded, summon it and give it Alacrity."
		self.make_readable_text(self.card_effect)
		self.discard_condition = "len(self.open_zones(self.curr_zone_list)) > 0"
		# self.discard_commands = ["self.select_card(card, 'Blue')", "card.secondary_select(card.discard_targets)", "card.alacrity = True", "card.can_attack = True", "card.move(card.inputs.pop().name)", "self.select_previous()"]
		self.discard_commands = ["self.select_card(card, 'Blue')", "card.alacrity = True", "card.can_attack = True", "card.move(random.choice(self.open_zones(self.get_list('Zone', card.controller))).name)", "self.select_previous()"]

		# self.discard_commands = ["self.current_effect = 'effect'", "self.master.deselect_card()", "self.master.select_card(self)", "self.secondary_select()"]
		# self.resolve_commands = ["self.face_up = True", "self.alacrity = True", "self.can_attack = True", "self.move(target.name)", "self.master.deselect_card()", "self.select_color='red'", "self.master.select_card(self)"]
		self.discard = True
		self.discard_targets = self.master.get_list("Zone", self.controller)

		self.redraw_card()

	def scrap_cycler(self):
		self.drawn_name = "Scrap Cycler"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/scrap_cycler2.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 1, 1, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 2
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Draw a card, then discard a card."
		self.make_readable_text(self.card_effect)
		self.arrival_commands = ["self.draw_from_deck(card.controller, 1)", "card.secondary_select(card.arrival_targets)", "card.inputs[0].move('Disc'+str(card.inputs.pop().controller))"] #"self.forced_discard(self.curr_hand_list)"]
		# self.resolve_commands = ["self.face_up = True", "self.move_to_zone(target.name)", "self.master.deselect_card()"]
		self.arrival = True
		self.arrival_targets = self.master.get_list("Hand", self.controller)
		# self.effect_targets = self.master.get_list("Hand", self.controller)

		self.redraw_card()

	def stalk_harvester(self):
		self.drawn_name = "Stalk Harvester"
		self.type = "Spell"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/stalk_harvester.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 0, 0, 1, 0]
		self.card_cost = self.base_card_cost.copy()
		
		self.card_effect = "Prep: At the end of your opponents turn, spend all your Green mana and draw a card for each mana spent."
		self.make_readable_text(self.card_effect)
		self.prep_condition = "self.curr_mana_list[2].amount > 0"
		self.prep_activated_commands = ["self.draw_from_deck(self.enemy, self.enemy_mana_list[2].amount)", "self.enemy_mana_list[2].set_amount(0)"]
		self.activatable = True
		self.prep = True
		self.prep_type = "end_of_turn"+str(self.enemy)
		self.base_effect_cost = self.card_cost
		self.effect_cost = self.base_effect_cost.copy()
		self.effect_targets = [self]


		self.redraw_card()

	def grave_disguiser(self):
		self.drawn_name = "Grave Disguiser"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/poison_peddler.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 4, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 2
		self.base_defense = 3
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Arrival: Place a Unit from your graveyard on the bottom of your deck. It costs 0 Mana."
		self.make_readable_text(self.card_effect)
		self.arrival_condition = "self.curr_discard_list"
		self.arrival_commands = ["card.secondary_select(card.arrival_targets)", "card.inputs[0].move('Deck'+str(card.controller))", "self.move_to_bottom(self.curr_deck_list, card.inputs[0])", "card.inputs[0].card_cost = [0,0,0,0,0]", "card.inputs[0].arrival = True"]
		self.resolve_arrival_commands = ["target.status = 'Disc'+str(target.controller)", "target.move('Deck'+str(target.controller))", "target.card_cost = [0,0,0,0,0]", "target.arrival = True"]
		# self.resolve_commands.append("self.master.displayed_stack.remove(target)")
		# self.resolve_commands.append("self.master.put_down_stack()")
		self.resolve_arrival_commands.append("target.arrival_commands.append('self.master.draw_from_deck(self.controller, 1)')")
		self.resolve_arrival_commands.append("self.master.deselect_card()")
		self.arrival = True
		self.procure = True
		# self.procure_pool = self.master.curr_discard_list ########CHANGE THIS TO USE MASTER.GET_LIST
		self.arrival_targets = self.master.get_list("Disc", self.controller)
		# self.procure_pool = self.master.get_list("Disc", self.controller)
		# self.procure_type = ["Unit"]
		# self.procure_mana = range(0, 10)
		# self.procure_color = [0, 1, 2, 3]

		self.redraw_card()

	def swarm_head(self):
		self.drawn_name = "Swarm Head"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/creepy_head.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 1
		self.base_card_cost = [0, 2, 0, 0, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "Alacrity. Afterdeath: Summon a Swarm Head from your deck."
		self.make_readable_text(self.card_effect)
		self.afterdeath_condition = "self.get_card_from_list(self.get_list('Deck', card.controller), card.name)"
		self.afterdeath_commands = ["self.get_card_from_list(self.get_list('Deck', card.controller), card.name).move(card.prev_status)"]


		self.alacrity = True
		self.can_attack = True
		self.afterdeath = True

		
		
		self.redraw_card()

	def friendly_scarecrow(self):
		self.drawn_name = "Friendly Scarecrow"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/friendly_scarecrow.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 0, 0, 1, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 2
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Aura: Friendly Green Units have +1 Defense."
		self.make_readable_text(self.card_effect)
		self.arrival_condition = "self.card_group(self.curr_board_list, [], [], [2], [], [])"
		self.arrival_commands = ["self.mass_adjust_stats(self.card_group(self.get_list('Board', card.controller), [], [], [2], [], []), 'Defense', 1)"]
		self.aura_condition = "(secondary_targets[0].card_cost[2] > 0) and secondary_targets[0].controller == card.controller"
		self.aura_commands = ["secondary_targets[0].adjust_stats('Defense', 1)"]
		self.afterdeath_commands = ["self.mass_adjust_stats(self.card_group(self.get_list('Board', card.controller), [], [], [2], [], []), 'Defense', 1)"]

		self.arrival = True
		self.afterdeath = True
		self.aura = True
		self.aura_type = "unit_into_play"+str(self.controller)
		self.aura_status = "Zone"
		
		self.redraw_card()

	def xeno_seer(self):
		self.drawn_name = "Xeno Seer"
		
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/xeno_seer.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 1
		self.base_card_cost = [0, 2, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 0
		self.base_defense = 3
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Move a Blue card in your deck that costs 3 or less total mana to the top of your deck." #maybe put it on the top of the deck instead? ok ;)
		self.activated_condition = "'Zone' in card.status and self.card_group(self.get_list('Deck', card.controller), [], [], card.procure_color, card.procure_mana, [])"
		self.activated_commands = ["card.secondary_select(self.card_group(self.get_list('Deck', card.controller), [], [], card.procure_color, card.procure_mana, []))", "self.move_to_top(self.get_list('Deck', card.controller), card.inputs.pop())"]
		# self.resolve_commands = ["self.master.deselect_card()", "self.master.move_to_top(self.master.get_list('Deck', self.controller), target)"]
		self.activatable = True
		self.base_effect_cost = [0, 3, 0, 0, 0]
		self.effect_cost = self.base_effect_cost.copy()
		self.make_readable_text(self.card_effect)
		self.effect_targets = [self.master.get_list("Deck_Zone", self.controller)]
		self.procure = True
		self.procure_pool = self.master.curr_deck_list
		self.procure_type = ["Unit", "Spell"]
		self.procure_mana = [0, 1, 2, 3]
		self.procure_color = [1]

		self.redraw_card()

	def xeno_controller(self):
		self.drawn_name = "Xeno Controller"
		
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/xeno_controller.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 1
		self.base_card_cost = [0, 2, 0, 0, 2]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 2
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense
		
		self.card_effect = "Take control of an Enemy Unit that costs 3 or less total mana."
		self.activated_condition = "'Zone' in card.status and self.card_group(self.get_list('Board', card.enemy), [], [], [], [0, 1, 2, 3], []) and card.refresh_effect_targets()"
		self.activated_commands = ["card.inputs.append(secondary_targets[0])", "card.secondary_select(self.open_zones(self.get_list('Zone', card.controller)))", "card.inputs[0].change_controller()", "card.inputs[0].move(card.inputs[1].name)", "card.inputs = []"]
		# self.arrival_commands = ["self.current_effect = 'arrival'", "self.stake_select()"]
		# self.resolve_arrival_commands = ["target.zone_discount=[0,0,0,0,-1]", "target.zone_color=self.get_color(2)", "target.redraw_card()", "self.staked_zone=target", "self.master.deselect_card()"]
		# self.effect_condition = "self.staked_zone.status is not 'Full'"
		# self.effect_commands = ["self.current_effect = 'effect'", "self.secondary_select()"]
		# self.resolve_commands = ["target.move(self.staked_zone.name)", "self.master.deselect_card()"]
		# self.afterdeath_commands = ["self.current_effect = 'afterdeath'", "self.staked_zone.zone_discount=None", "self.staked_zone.zone_color=None", "self.staked_zone.delete()", "self.staked_zone.redraw_card()", "self.staked_zone=None"]
		self.activatable = True
		# self.arrival = True
		# self.stake = True
		# self.afterdeath = True
		self.base_effect_cost = [0, 3, 0, 0, 0]
		self.effect_cost = self.base_effect_cost.copy()
		self.make_readable_text(self.card_effect)
		self.effect_targets = self.master.card_group(self.master.get_list('Board', self.enemy), [], [], [], [0, 1, 2, 3], [])
		self.eval_effect_targets = "self.master.card_group(self.master.get_list('Board', self.enemy), [], [], [], [0, 1, 2, 3], [])"
		self.stake_targets = self.master.get_list("Zone", self.controller)
		# self.procure = True
		# self.procure_pool = self.master.curr_deck_list
		# self.procure_type = ["Unit", "Spell"]
		# self.procure_mana = [0, 1, 2, 3]
		# self.procure_color = [1]

		self.redraw_card()

	def fossil_fuel_factory(self):
		self.drawn_name = "Fossil Fuel Factory"
		self.construct = True
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/fossil_fuel_factory.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 0, 0, 2, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 0
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "At then end of your turn, move all Green Units in your graveyard to the Event Horizon and create a 1/1 Robot for each."
		self.make_readable_text(self.card_effect)
		self.aura_condition = "'Zone' in card.status and self.card_group(self.curr_discard_list, ['Unit'], [], [2], [], [])"
		self.aura_commands = ["self.select_card(card, 'Blue')", "card.follow_up_repeats = min(len(self.open_zones(self.get_list('Zone', card.controller))), len(self.card_group(self.get_list('Disc', card.controller), ['Unit'], [], [2], [], [])))", "card.follow_up_commands = card.aura_follow_up_commands.copy()"]
		self.aura_follow_up_commands = ["self.curr_discard_list.remove(self.card_group(self.curr_discard_list, ['Unit'], [], [2], [], [])[0])", "self.update_discards()", "card.secondary_select(self.open_zones(self.get_list('Zone', card.controller)))", "self.summon_token('robot_token', card.inputs.pop())"]

		# self.aura_commands = ["card.current_effect = 'aura'", "self.deselect_card()", "self.select_card(card)", "card.multi_select(eval(card.inputs))", "self.curr_discard_list = list(set(self.get_list('Disc', card.controller))-set(self.card_group(self.get_list('Disc', card.controller), '', '', ['Red', 'Blue', 'Green', 'Yellow'], range(0, 30))))", "self.update_discards()"]
		# self.aura_condition = "self.card_group(self.get_list('Disc', card.controller), '', '', ['Red', 'Blue', 'Green', 'Yellow'], range(0, 30))"
		# self.resolve_aura_commands = ["self.master.summon_token('robot_token', target)", "self.master.triggers -= 1"]
		# self.afterdeath_commands = ["self.aura_cards.remove(card)"]

		# self.inputs = "len(self.card_group(self.get_list('Disc', card.controller), '', '', ['Red', 'Blue', 'Green', 'Yellow'], range(0, 30)))"
		self.aura = True
		self.aura_type = "end_of_turn"+str(self.controller)
		self.aura_status = "Zone"

		self.effect_targets = self.master.get_list("Zone", self.controller)
		
		self.redraw_card()

	def robot_token(self):
		self.drawn_name = "Robot"
		self.token = True
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/robot_token.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 0, 0, 1, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		# self.card_effect = ""
		# self.make_readable_text(self.card_effect)
		
		self.redraw_card()

	def regenerating_ooze(self):
		self.drawn_name = "Regenerating Ooze"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/poison_peddler.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 4, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 3
		self.base_defense = 3
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "Afterdeath: Summon 0/0 Oozelings equal to this card's attack."
		self.make_readable_text(self.card_effect)
		# self.into_play_commands = ["card.follow_up_repeats = card.attack-1"]
		self.afterdeath_commands = ["self.summon_token('oozeling', self.get_zone_from_status(card.prev_status))", "card.follow_up_repeats = min(card.attack-1, len(self.open_zones(self.get_list('Zone', card.controller))))", "card.follow_up_commands = card.afterdeath_follow_up_commands"]
		self.follow_up_condition = "card.attack > 1 and 'Disc' in card.status and self.open_zones(self.get_list('Zone', card.controller))"
		self.afterdeath_follow_up_commands = ["self.summon_token('oozeling', random.choice(self.open_zones(self.get_list('Zone', card.controller))))"]
		# self.into_play = True
		self.afterdeath = True

		# self.follow_up_repeats = self.attack-1
		
		self.redraw_card()

	def oozeling(self):
		self.drawn_name = "Oozeling"
		self.token = True
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/poison_peddler.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 0, 1, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 0
		self.base_defense = 0
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "Destroy all ally Oozelings and resummon Regenerating Ooze in an Oozeling's place."
		self.activated_condition = "self.get_card_from_list(self.curr_discard_list, 'regenerating_ooze') and card.refresh_effect_targets()"
		self.activated_commands = ["card.inputs = [self.get_card_from_list(self.curr_discard_list, 'regenerating_ooze'), secondary_targets[0].status]", "card.inputs[0].can_attack = False", "card.inputs[0].attack = len(self.card_group(self.curr_board_list, [], [card.name], [], [], []))", "card.inputs[0].defense = len(self.card_group(self.curr_board_list, [], [card.name], [], [], []))", "self.remove_tokens(self.card_group(self.curr_board_list, [], [card.name], [], [], []))", "card.inputs[0].move(card.inputs[1])", "self.select_card(card.inputs[0], 'Red')"]
		self.activatable = True

		self.base_effect_cost = [0, 0, 0, 0, 1]
		self.effect_cost = self.base_effect_cost.copy()
		self.make_readable_text(self.card_effect)

		self.effect_targets = self.master.card_group(self.master.curr_board_list, [], [self.name], [], [], [])
		self.eval_effect_targets = "self.master.card_group(self.master.curr_board_list, [], [self.name], [], [], [])"
		
		self.redraw_card()

	def hazardous_algae(self):
		self.drawn_name = "Hazardous Algae"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/hazardous_algae.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 0
		self.base_card_cost = [1, 1, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "After attacking an enemy, deal 4 damage to the enemy hero."
		self.aura_condition = "card == secondary_targets[0]"
		self.aura_commands = ["self.adjust_health(card.enemy, -4)"]

		self.aura = True
		self.aura_type = "attack_any"+str(self.controller)
		self.aura_status = "Zone"

		self.make_readable_text(self.card_effect)
		
		self.redraw_card()

	def contaminated_algae(self):
		self.drawn_name = "Contaminated Algae"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/contaminated_algae.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 1
		self.base_card_cost = [0, 1, 0, 0, 1]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "After attacking an enemy, summon an Algae from your deck."
		self.aura_condition = "card == secondary_targets[0] and (self.card_group(self.curr_deck_list, [], ['algae'], [], [], []) is not [])"
		self.aura_commands = ["card.secondary_select(self.card_group(self.curr_deck_list, [], ['algae'], [], [], []))", "card.secondary_select(self.open_zones(self.curr_zone_list))", "card.inputs[0].move(card.inputs[1].name)", "card.inputs = []"]

		self.aura = True
		self.aura_type = "attack_any"+str(self.controller)
		self.aura_status = "Zone"

		self.make_readable_text(self.card_effect)
		
		self.redraw_card()

	def spreading_algae(self):
		self.drawn_name = "Spreading Algae"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/spreading_algae.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 2
		self.base_card_cost = [0, 1, 1, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "After attacking an enemy, summon a Spreading Algae"
		self.aura_condition = "card == secondary_targets[0] and self.open_zones(self.curr_zone_list) != []"
		self.aura_commands = ["card.secondary_select(self.open_zones(self.curr_zone_list))", "self.summon_token(card.name, card.inputs.pop())"]

		self.aura = True
		self.aura_type = "attack_any"+str(self.controller)
		self.aura_status = "Zone"

		self.make_readable_text(self.card_effect)
		
		self.redraw_card()

	def corrosive_algae(self):
		self.drawn_name = "Corrosive Algae"
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/corrosive_algae.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 3
		self.base_card_cost = [0, 1, 0, 1, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 1
		self.base_defense = 1
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "After attacking an enemy, reduce its defense to 0."
		self.aura_condition = "card == secondary_targets[0] and 'Zone' in secondary_targets[1].status"
		self.aura_commands = ["secondary_targets[1].adjust_stats('defense', secondary_targets[1].defense * -1)"]

		self.aura = True
		self.aura_type = "attack_unit"+str(self.controller)
		self.aura_status = "Zone"

		self.make_readable_text(self.card_effect)
		
		self.redraw_card()

	def rainbow_pond(self):
		self.drawn_name = "Rainbow Pond"
		self.construct = True
		self.card_img = ImageTk.PhotoImage(Image.open('./Main/rainbow_pond.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 4
		self.base_card_cost = [1, 1, 1, 1, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 0
		self.base_defense = 4
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "Whenever you play a Unit with a unique Primary Color, draw a card."
		self.make_readable_text(self.card_effect)
		self.aura_condition = "'Zone' in card.status and len(self.card_group(self.curr_board_list, [], [], [], [], [secondary_targets[0].primary_color])) < 1"
		self.aura_commands = ["self.draw_from_deck(card.controller, 1)"]

		self.aura = True
		self.aura_type = "unit_play_from_hand"+str(self.controller)
		self.aura_status = "Zone"

		self.effect_targets = self.master.get_list("Zone", self.controller)
		
		self.redraw_card()

	def bait_taker(self):
		self.drawn_name = "Bait Taker"
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/rainbow_pond.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 1
		self.base_card_cost = [0, 3, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 4
		self.base_defense = 2
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = "After discarding 3 cards, summon this Unit from your Deck or Hand"
		self.make_readable_text(self.card_effect)
		self.aura_condition = "('Hand' in card.status or 'Deck' in card.status)"
		self.aura_commands = ["card.follow_up_commands = card.aura_follow_up_commands.copy()"]
		self.follow_up_condition = "card.effect_counters == 3"
		self.aura_follow_up_commands = ["card.move(random.choice(self.open_zones(self.get_list('Zone', card.controller))).name)"]
		

		self.aura = True
		self.aura_type = "card_discard"+str(self.controller)
		self.aura_status = ["Hand", "Deck"]

		self.effect_targets = self.master.get_list("Zone", self.controller)
		
		self.redraw_card()

	def template(self):
		self.drawn_name = ""
		# self.card_img = ImageTk.PhotoImage(Image.open('./Main/poison_peddler.png').resize((int(self.card_width),int((self.card_height/3)*2)), Image.ANTIALIAS))
		self.primary_color = 4
		self.base_card_cost = [0, 0, 0, 0, 0]
		self.card_cost = self.base_card_cost.copy()

		self.base_attack = 0
		self.base_defense = 0
		self.attack = self.base_attack
		self.defense = self.base_defense

		self.card_effect = ""
		self.make_readable_text(self.card_effect)
		
		self.redraw_card()

	def refresh_effect_targets(self):
		self.effect_targets = eval(self.eval_effect_targets)
		return True

	def make_readable_text(self, text):
		self.readable_effect = []
		curr_length = 0
		curr_word = ""
		curr_line = ""
		self.base_max_length = 25
		self.first_max_length = self.base_max_length
		self.second_max_length = self.base_max_length
		if self.type == "Unit" and self.effect_cost is not None:
			total_colors = 0
			for x in range(0,5):
				if self.effect_cost[x] > 0:
					self.first_max_length -= 4
					total_colors += 1

				if self.effect_cost[x] > 2 and x != 4:
					self.first_max_length -=4

				if self.effect_cost[x] > 1 and x != 4:
					self.second_max_length = self.base_max_length - 4*(total_colors)

		max_length = self.first_max_length
		for char in text:
			if char == " ":
				curr_line += curr_word
				curr_line += " "
				curr_word = ""
				curr_length += 1
			else:
				curr_word += char
				curr_length += 1

			if curr_length > max_length:
				self.readable_effect.append(curr_line)
				curr_line = ""
				curr_length = len(curr_word)

				if max_length == self.second_max_length:
					max_length = self.base_max_length
				if max_length == self.first_max_length:
					max_length = self.second_max_length

		curr_line += curr_word
		if curr_line:
			self.readable_effect.append(curr_line)
			
	def redraw_card(self):
		self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='white'))	

		if "Zone" in self.name:
			if self.zone_discount is not None:
				discount_amount = 0
				for mana_discount in self.zone_discount:
					if mana_discount != 0:
						discount_amount = mana_discount
						break
				self.zone_number = self.canvas.create_text(self.x1+(self.card_width/2), self.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=discount_amount)
				self.drawn_elements.append(self.zone_number)
			if self.status == "Full":
				for card in (self.master.board_list1 + self.master.board_list2):
					if card.status == self.name:
						card.redraw_card()
		else:
			if self.face_up:
				self.drawn_elements.append(self.canvas.create_line(self.x1, self.y1+self.pixel_y*20-1, self.x2, self.y1+self.mana_height+(self.mana_buffer*3)-1))
				self.drawn_elements.append(self.canvas.create_line(self.x1, self.y2-self.pixel_y*30, self.x2, self.y2-self.pixel_y*30))
				if self.attack is not None and self.defense is not None:
					self.draw_atk_def()
				if self.card_img is not None:
					self.drawn_elements.append(self.canvas.create_image(self.x1+1, self.y1+self.mana_height+(self.mana_buffer*3), image=self.card_img, anchor=NW))

				self.draw_cost(self.card_cost, False)
				font_size = int(math.ceil(self.font_size*12/10))
				if len(self.drawn_name) > 13:
					font_size -= 1
					if "Display" in self.status:
						font_size -= 3
				if len(self.drawn_name) > 15:
					font_size -= 1
					if "Display" in self.status:
						font_size -= 3
				if len(self.drawn_name) > 18:
					font_size -= 2
					if "Display" in self.status:
						font_size -= 3
				font = tkinter.font.Font(family="Consolas", size=font_size, weight="bold")
				self.drawn_elements.append(self.canvas.create_text(self.x1+(self.pixel_x*4), self.y1+(self.pixel_y*10), anchor=W, font=font, text=self.drawn_name, activefill=self.get_color(self.primary_color)))
			self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill=None))

	def update_dimensions(self, new_width, new_height):
		self.card_width = new_width
		self.card_height = new_height
		self.x2 = self.x1+self.card_width
		self.y2 = self.y1+self.card_height
		self.redraw_card()

	def draw_cost(self, cost, description):
		base_posY = self.y2-self.mana_buffer-(self.mana_height*2)-(self.pixel_y*3)
		if description:
			base_posY = self.y2+self.pixel_y*2.5
		mana_posX = self.x1+(self.mana_buffer)+self.mana_width#+(self.pixel_x*1)
		mana_posY = base_posY
		num = 0
		for value in cost[:-1]:
			if value == 5:
				mana_posX += self.mana_width + self.mana_buffer
				self.drawn_elements.append(self.canvas.create_oval(mana_posX, mana_posY, mana_posX-self.mana_width*2-self.mana_buffer, mana_posY+self.mana_height*2+self.mana_buffer, outline='black', fill=self.get_color(num)))
				mana_posX += (self.mana_width + self.mana_buffer)
			else:
				for i in range(0, value):
					self.drawn_elements.append(self.canvas.create_oval(mana_posX-self.mana_width, mana_posY+self.mana_height, mana_posX, mana_posY, outline='black', fill=self.get_color(num)))
					if i == 1 or i == value-1:
						mana_posX += self.mana_width + self.mana_buffer
						mana_posY = base_posY
					else:
						mana_posY += self.mana_buffer + self.mana_height - self.pixel_y*1
			num += 1
		if cost[4] != 0:
			self.drawn_elements.append(self.canvas.create_oval(mana_posX-self.mana_width, mana_posY+self.mana_height, mana_posX, mana_posY, outline='black', fill="White"))
			self.drawn_elements.append(self.canvas.create_text(mana_posX-(self.mana_width/2)+self.pixel_x*0.5, mana_posY+(self.mana_height/2), font=("Consolas", self.font_size), text=cost[4]))

	def get_color(self, num):
		if num == 0:
			return "#E34234"
		if num == 1:
			return "#3F00FF"
		if num == 2:
			return "#355E3B"
		if num == 3:
			return "#FDEE00"
		if num == 4:
			return "Black"

	# def card_colors(self):
	# 	colors = []
	# 	if self.card_cost[0] > 0:
	# 		colors.append("Red")
	# 	if self.card_cost[1] > 0:
	# 		colors.append("Blue")
	# 	if self.card_cost[2] > 0:
	# 		colors.append("Green")
	# 	if self.card_cost[3] > 0:
	# 		colors.append("Yellow")
	# 	return colors

	def draw_atk_def(self):
		self.drawn_elements.append(self.canvas.create_line(self.x2-self.pixel_x*30, self.y2, self.x2-self.pixel_x*30, self.y2-self.pixel_y*30))
		self.drawn_elements.append(self.canvas.create_line(self.x2-self.pixel_x*30, self.y2, self.x2, self.y2-self.pixel_y*30))
		# self.drawn_elements.append(self.canvas.create_line(self.x2, self.y2, self.x2-self.pixel_x*30, self.y2-self.pixel_y*30))

		# attack_posX = self.x1+(self.pixel_x*100/3) +(self.pixel_x*3)
		# defense_posX = self.x2 - (self.pixel_x*100/3) + (self.pixel_x*100/6)
		attack_posX = self.x2-self.pixel_x*21
		attack_posY = self.y2-self.pixel_y*21
		defense_posX = self.x2-self.pixel_x*9
		defense_posY = self.y2-self.pixel_y*9
		# stat_posY = self.y2 - (self.pixel_y*11)

		if self.attack_text is not None and self.defense_text is not None:
			self.canvas.delete(self.attack_text)
			self.canvas.delete(self.defense_text)

		self.attack_text = self.canvas.create_text(attack_posX, attack_posY, font=("Consolas", self.font_size), text=self.attack)
		self.drawn_elements.append(self.attack_text)

		self.defense_text = self.canvas.create_text(defense_posX, defense_posY, font=("Consolas", self.font_size), text=self.defense)
		self.drawn_elements.append(self.defense_text)

		# self.attack_img = ImageTk.PhotoImage(Image.open('./Main/attack.png').resize((int(self.card_width/5),int((self.card_height/15)*2)), Image.ANTIALIAS))
		# self.drawn_elements.append(self.canvas.create_image(self.x1+(self.card_width/40), self.y2-((self.card_height/15)*2), image=self.attack_img, anchor=NW))

		# self.defense_img = ImageTk.PhotoImage(Image.open('./Main/defense.png').resize((int(self.card_width/5),int((self.card_height/15)*2)), Image.ANTIALIAS))
		# self.drawn_elements.append(self.canvas.create_image(self.x1+(self.pixel_x*50), self.y2-((self.card_height/15)*2), image=self.defense_img, anchor=NW))

	def display_ez_stat(self, stat_value):
		self.ez_stat_display = True
		self.ez_stat_box_element = self.canvas.create_rectangle(self.x2-self.pixel_x*30, self.y2, self.x2, self.y2-self.pixel_y*30, fill='white')
		self.ez_stat_element = self.canvas.create_text(self.x2-self.pixel_x*15, self.y2-self.pixel_y*15, font=("Consolas", self.font_size*2), text=stat_value)

	def adjust_stats(self, stat, value):
		if stat == "Attack":
			self.attack += value
			if self.attack < 0:
				self.attack = 0
		else:
			self.defense += value
			if self.defense < 0:
				self.defense = 0
		self.redraw_card()

	def adjust_mana(self, mana_change):
		for x in range(0, 4):
			self.card_cost[x] += mana_change[x]

	def add_zone_effect(self, discount):
		self.zone_discount = discount
		self.redraw_card()

	def attack_card(self, card):
		self.master.resume_master = "self.main_phase()"
		if self.attack > card.defense:
			self.attack_card_trigger(card)
			card.move("Disc"+str(card.controller))
			while(self.master.resolving_effect):
				continue
		elif self.attack == card.defense:
			self.attack_card_trigger(card)
			self.move("Disc"+str(self.controller))
			while(self.master.resolving_effect):
				continue
			card.move("Disc"+str(card.controller))
			while(self.master.resolving_effect):
				continue
		elif self.attack < card.defense:
			self.attack_card_trigger(card)
			self.move("Disc"+str(self.controller))
			while(self.master.resolving_effect):
				continue

	def attack_card_trigger(self, card):
		if self.master.trigger_dict["attack_unit"+str(self.controller)] is not []:
			self.master.effect_trigger([self, card], "attack_unit"+str(self.controller))

	def change_controller(self):
		if "Hand" in self.status:
			self.master.get_list("Hand", self.controller).remove(self)
			self.master.get_list("Hand", self.enemy).append(self)
		elif "Deck" in self.status:
			self.master.get_list("Deck", self.controller).remove(self)
			self.master.get_list("Deck", self.enemy).append(self)
		elif "Disc" in self.status:
			self.master.get_list("Disc", self.controller).remove(self)
			self.master.get_list("Disc", self.enemy).append(self)
		elif "Zone" in self.status:
			for zone in self.master.get_list("Zone", self.controller):
				if zone.name == self.status:
					zone.status = "Open"
					break
			self.master.get_list("Board", self.controller).remove(self)
			self.master.get_list("Board", self.enemy).append(self)
		self.attack_targets = self.master.get_list("Board", self.enemy)
		old_controller = self.controller
		self.controller = self.enemy
		self.enemy = old_controller

	def effect_requirements(self):
		if self.type == "Unit" and self.activatable and "Zone" in self.status:
			return True
		elif self.type == "Spell":
			return True
		return False

	def secondary_select(self, targets):
		self.master.user_input = True
		self.select_color = "Blue"
		for target in targets:
			if not ("Zone" in target.name and target.status == "Full"):
				self.master.add_secondary_highlight(target, "Blue")
		if "Disc" in targets[0].status or "Deck" in targets[0].status:
			self.master.display_stack(targets, targets[0].status)
		self.master.player_status = "pick_card"

	def total_mana_cost(self):
		total_cost = 0
		for mana_cost in self.card_cost:
			total_cost += mana_cost
		return total_cost

	def swap_stats(self):
		old_atk = self.attack
		self.attack = self.defense
		self.defense = old_atk
		self.redraw_card()

	def enough_mana(self, mana_list, effect_cost):
		total_mana = 0
		total_cost = 0
		for mana_pool in mana_list:
			total_mana += mana_pool.amount
		for mana_cost in effect_cost:
			total_cost += mana_cost
		if total_mana >= total_cost:
			return True
		return False

	def move(self, status):
		self.prev_status = self.status
		self.status = status
		if self.prev_status != self.status:
			if "Zone" in self.prev_status:
				self.master.get_list("Board", self.controller).remove(self)
				self.master.get_zone_by_name(self.prev_status).status = "Open"
			elif "Hand" in self.prev_status:
				self.master.get_list("Hand", self.controller).remove(self)
				self.master.display_hand()
			elif "Disc" in self.prev_status:
				self.master.get_list("Disc", self.controller).remove(self)
				self.master.update_discards()
			elif "Deck" in self.prev_status:
				self.master.get_list("Deck", self.controller).remove(self)
				self.master.update_decks()
		

		if self.aura and self.prev_status[:4] not in self.aura_status and self.status[:4] in self.aura_status:
			self.master.add_aura_card(self)
		elif self.aura and self.prev_status[:4] in self.aura_status and self.status[:4] not in self.aura_status:
			self.master.remove_aura_card(self)

		if "Zone" in status:
			self.master.get_list("Board", self.controller).append(self)
			self.face_up = True
			self.move_to_zone(status)
			if "Hand" in self.prev_status and not self.countered:
				if self.arrival:
					self.master.add_to_stack(self, "arrival", [])
					# self.master.trigger_card_effect(self, "arrival", [])
				if self.master.trigger_dict["unit_play_from_hand"+str(self.controller)] is not []:
					self.master.effect_trigger([self], "unit_play_from_hand"+str(self.controller))
			if self.master.trigger_dict["unit_into_play"+str(self.controller)] is not []:
				self.master.effect_trigger([self], "unit_into_play"+str(self.controller))
		elif "Disc" in status:
			if self.token:
				self.master.get_list("Card", self.controller).remove(self)
				self.delete()
			else:
				self.master.get_list("Disc", self.controller).append(self)
				if self.into_play and not self.countered:
					self.master.add_to_stack(self, "into_play", [])
					# self.master.trigger_card_effect(self, "into_play", [])
				self.face_up = False
				self.move_to_discard(status)
				if "Zone" in self.prev_status and not self.countered:
					if self.afterdeath:
						self.master.add_to_stack(self, "afterdeath", [])
						# self.master.trigger_card_effect(self, "afterdeath", [])
					if self.master.trigger_dict["unit_death"+str(self.controller)] is not []:
						self.master.effect_trigger([self], "unit_death"+str(self.controller))
				if "Hand" in self.prev_status and self.type != "Spell":
					if self.discard:
						self.master.add_to_stack(self, "discard", [])
						# self.master.trigger_card_effect(self, "discard", [])
					if self.master.trigger_dict["card_discard"+str(self.controller)] is not []:
						self.master.effect_trigger([self], "card_discard"+str(self.controller))
				if "Deck" in self.prev_status:
					if self.mill:
						self.master.add_to_stack(self, "mill", [])
						# self.master.trigger_card_effect(self, "mill", [])
					if self.master.trigger_dict["card_mill"+str(self.controller)] is not []:
						self.master.effect_trigger([self], "card_mill"+str(self.controller))
		elif "Deck" in status:
			self.master.get_list("Deck", self.controller).append(self)
			self.move_to_deck(status)
			self.face_up = False
		self.countered = False

	def specific_move(self, status, face_up, x1, y1, x2, y2):
		self.prev_status = self.status
		self.status = status
		self.delete()
		self.face_up = face_up
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		# self.drawn_elements.append(self.canvas.create_rectangle(x1, y1, x2, y2, outline='black'))
		self.redraw_card()

	def move_to_zone(self, zone_name):
		self.delete()
		zone = self.master.get_zone_by_name(zone_name)
		zone.status = "Full"
		self.x1 = zone.x1
		self.x2 = zone.x2
		self.y1 = zone.y1
		self.y2 = zone.y2

		# self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black'))
		self.redraw_card()

	def move_to_discard(self, discard):
		self.delete()
		disc_zone = self.master.get_list("Discard_Zone", self.controller)
		self.x1 = disc_zone.x1
		self.x2 = disc_zone.x2
		self.y1 = disc_zone.y1
		self.y2 = disc_zone.y2
		# self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black'))
		self.redraw_card()
		self.master.update_discards()
		# if self.type == "Unit":
		# 	self.attack = self.base_attack
		# 	self.defense = self.base_defense
		# self.card_cost = self.base_card_cost
		# self.effect_cost = self.base_effect_cost

	def move_to_deck(self, deck):
		self.delete()
		deck_zone = self.master.get_list("Deck_Zone", self.controller)
		self.x1 = deck_zone.x1
		self.x2 = deck_zone.x2
		self.y1 = deck_zone.y1
		self.y2 = deck_zone.y2
		# self.drawn_elements.append(self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black'))
		self.redraw_card()
		self.master.update_decks()

	def select(self):
		if len(self.highlights) > 3:
			self.canvas.delete(self.highlights.pop(3))
			self.canvas.delete(self.highlights.pop(0))

		self.highlights.append(self.canvas.create_rectangle(self.x1-self.selected_size,self.y1-self.selected_size,self.x2+self.selected_size,self.y2+self.selected_size,outline=self.select_color))
		self.highlights.append(self.canvas.create_rectangle(self.x1-self.selected_size,self.y1-self.selected_size,self.x2+self.selected_size,self.y2+self.selected_size,outline=self.select_color))

		if self.selected_size > 8:
			self.selected_size = 0

	def deselect(self):
		self.selected_size = 0
		for line in self.highlights:
			self.canvas.delete(line)
		self.highlights = []
		if self.ez_stat_display:
			self.canvas.delete(self.ez_stat_box_element)
			self.canvas.delete(self.ez_stat_element)
			self.ez_stat_display = False
		# for x in range(0, len(self.highlights)):
		# 	self.canvas.delete(self.highlights.pop())

	def delete(self):
		for element in self.drawn_elements:
			self.canvas.delete(element)
		if self.ez_stat_display:
			self.canvas.delete(self.ez_stat_box_element)
			self.canvas.delete(self.ez_stat_element)
			self.ez_stat_display = False

#coding notes
#check more card effects to see if it works with the "while/continue" system
#revert the while/continue system but keep the stack, use restart_from_interupt

#game design ideas:
#attack/defense
#everything has piercing? probably not
#attacking a monster calculates your monsters attack - their defense
#attack defense and health?? attacking leaves a minion with less defense?? this could b very cool ;)

#GAME MECHANICS:
#each player starts out with a celestial body that is loosely associated with each color
#red: meteor? eh
#blue: moon
#green: planet
#yellow: star/sun
#upgrade them somehow... maybe if you:
#have enough mana of a certain color
#draw a specific type of card
#opt out of draw phase
#cap on each type of mana? special effect when reaching cap?
#have other type of card that can exist in the card zones, cant attack/defend basically an enchantment. maybe taking hero damage lowers its health?


#CARD IDEAS:
#keywords:
#consume: can destroy and allied unit for mana when paying mana costs (gray, purple)
#stake/claim land: pick a unit zone to apply some sort of standing buff
#undermine?: if your enemy only has units with defense higher than your attack, you can attack directly 
#arrival?: on play
#afterlife?: on death trigger
#alacrity?: charge
#modular: merge on top of another unit to combine stats and keywords,when host unit dies stacked unit is left behind
#covert: can attack over units
#procure: tutor a card from deck
#prep: can be casted at the end of your turn to trigger on your opponents turn
#piercing: any leftover damage is dealt to opp. life ()
#healtouch: any damage dealt healed
#Early Bird: If your borange mana is less than X then trigger effect
#Goad: Opponent's units must attack this creature if they are attacking
#Supergoad: Opponent's unit's must attack

#color identity
#4 base archetypes	orange (blue)			purple (green)		yellow (yellow)		gray (red)
#aggressive/tempo:	earlygame powerspike	evasive				swarming			burn/suicide (card disadvantage)
#midrange/value:	versatile effects		ramp/big units		midgame powerspike	life cost	
#control:			countering				blocking the board	removal				lifegain
#combo:				tutor effects			graveyard manip		tribal				self-destruction

# borange: (blue?)
# Angry Rabbit: B: 3/0
# slithery snake: 2B: 1/4: 1 mana: swap attack and defense
# failure_to_launch: BB: prep: when your opponent plays a unit, counter it
# cantrip: 0: procure: a 1 cost unit
# Slippy: 6BB: 4/4: counter your opponents first unit or spell every turn
# FAST RABBIT 1B: 2/2 alacrity
# Wormgetter: B: 1/1 Early Bird 3: gain +1/+1
# Mudscamp: 2B: 2/3 Undermine Early Bird 5: Gain +1/+0
# Candrip: 1B: 1/1 arrival: Draw a Card. Early Bird 3: Gain +1,+1, Discard a Card
# Prep School: 1B: 2/2 Prep: summon this unit
# Preparations: 3: Choose One- Prep: Draw a Card at the end of your opponents turn or Prep: When an oppponent plays a spell counter it, or Prep: When an opponent attacks a
# unit you control that unit gets +3/+3

# purple: (green?)
# mole:P:1/1: undermine
# happy turtle:P:0/2
# turmor too: 2P: 2/2: arrival: add one purple mana to your pool at the end of your turn
# tumor: 1P: add one purple mana to your pool at the end of your turn
# big turtle: 1PP: 1/6
# creepy mole: 1P: 1/3: summon a unit from your graveyard that costs 1 or less
# big ol dragon: 5PP: 6/4: covert
# Earthworm: 2P: 2/3 Undermine, when this unit deals damage to an opponent draw a card
# flytrap: 3PP: 4/4 Consume: add a card from your graveyard to your hand
# double-headed flytrap: 4P: 3/3 Consume: destroy target unit with less or equal base defense than the unit consumed

# yellow: (yellow?)
# cherry: Y: 1/0: arrival: create 1/0
# hawk: 2Y: 2/2: alacrity, arrival: lower a units block by 1
# stinky toad: 2Y 1/1: arrival: destroy an enemy unit with 2 or less defense
# open the breach: 3Y: set your opponents units block to 0 for the rest of this turn
# valiant bumblebee: 1YY: 2/1: other yellow units have +1/+1
# hive mind: 3YYY: summon 1/1 modulars in each of your zones
# Honeycomb: Y: 1/1: modular
# Hive Bond: 1Y: mana add 2 Honeycombs to your hand
# Splitter: 2YY: 2/2 afterlife: Put a Honeycomb in two target Zone
# Harvester: 1Y: 1/1 modular, healtouch
# : 1YY: destroy target unit
# Beekeeper: 1YY: 1/1 modular, arrival: If you stack this card, draw a card for each unit with modular in this stack
# Spring: 1YY: Add 3 Honeycombs to your hand
# 1Y: 1/1 afterlife: Create a 1/1

# gray: (red?)
# fungo: G: 2/0: afterlife: deal 2 damage to enemy
# big leech: 2G: 4/4: arrival: lose 3 life
# dakter: 2G 3/3: arrival: gain 3 life
# mushrümi: 2G: 2/2: whenever a unit you control dies, deal 1 damage to your enemy and gain 1 life
# drain life: XGG: deal X damage to your opponent, gain X life
# Swolshrüm G: 3/3: Arrival: lose 5 life
# STink Beeeeetle: 3G: 2/2 Arrival: Choose a player. All players life total be come the same as that player
# Poison Peddler: 1G: 2/2: Arrival: reduce target units defense by 1. Lose 2 life
# Burn ems: 2G: Deal 5 damage to target player or unit
# Unexpected Sacrifice: GG: Prep: When a unit you control dies, draw 2 cards.

# NEUTRAL:
# Dumpster Diver: 3: 1/3 2:Draw a card
# 1: Prep: Draw a Card at the end of your opponents turn
# 2: 1/3

# HYBRID
# 1YG: Destroy target unit, gain life equal to its defense


#whenever you play a minion of a specfic cost, gain benefit

#gain temporary mana equal to the amount of mana you have spent this turn

#have a hand size limit (adjustable by card effect?) where you are forced to discard of your choice when you have too many cards on your turn
#then you can have synergy cards that proc off of being discarded, so you can self mill

#check old archetypes from other games for inspiration: crystal beasts?, plants?

#pay X colored mana, destroy a unit that costs exactly that amount

#card that tutors a NON synergy/archetypal card

#something that allows units to attack units in your opponents hand?

#win condition when reaching a certain life total?

#lose one card zone every turn after your deck is empty

#card thats mana cost is equal to number of cards in your opponents hand, attack and defense are double that

#card that costs all 4 colors, and gets a different trigger effects based on when you play units with different primary colors

#cryogenics, prep: when an ally unit dies, return them to the zone they were in after some amount turns

#card you cast using opponents mana?? combined with cards that lock your opponents mana so they cant be used on their turn

#exalting 'something': card name

#algae crew:
#contaminated algae: After battling an enemy, give all ally Units +1 Attack.
#hazardous algae: After battling an enemy, deal 2 damage to the enemy hero.
#corrosize algae: After battling an enemy, reduce its defense to 0.
#spreading algae: After battling an enemy, summon another Spreading Algae in the closest zone.

#THEMATIC IDEAS

#sci fi
#red: suns/stars, fire, magma
	#inhabitants: humanoid faction, elementals

#blue: deep space, water/ice from planets/comets
	#inhabitants: mysterious humanoid faction, aliens

#green: natural life, plants/animals, death?
	#inhabitants: plant/animal life

#yellow: light, electricity/machines?
	#inhabitants: robots





