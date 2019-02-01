from tkinter import *
import tkinter.font
from PIL import ImageTk, Image
import os, random, time, math, socket

from Card import Card
from Mana import Mana
import connection

class Board:
	def __init__(self, master, board_width, board_height):
		self.total_card_list = []
		self.card_list1 = []
		self.hero_zone1 = None
		self.health1 = 25
		self.health_number1 = None
		self.card_list2 = []
		self.hero_zone2 = None
		self.health2 = 25
		self.health_number2 = None
		self.zone_list1 = []
		self.curr_zone_list = self.zone_list1
		self.zone_list2 = []
		self.enemy_zone_list = self.zone_list2
		self.deck_list1 = []
		self.curr_deck_list = self.deck_list1
		self.deck_zone1 = None
		self.deck_list2 = []
		self.enemy_deck_list = self.deck_list2
		self.deck_zone2 = None
		self.board_list1 = []
		self.curr_board_list = self.board_list1
		self.board_list2 = []
		self.enemy_board_list = self.board_list2
		self.hand_list1 = []
		self.hand_list2 = []
		self.discard_list1 = []
		self.curr_discard_list = self.discard_list1
		self.discard_zone1 = None
		self.discard_number1 = None
		self.discard_list2 = []
		self.enemy_discard_list = self.discard_list2
		self.discard_zone2 = None
		self.discard_number2 = None
		self.deck_number1 = None
		self.deck_number2 = None
		self.mana_list1 = []
		self.mana_list2 = []
		self.prep_mana_list = []
		self.board_width = board_width
		self.board_height = board_height
		self.pixel_x = board_width/1600
		self.pixel_y = board_height/900
		self.card_width = self.pixel_x*100
		self.card_height = self.pixel_y*150
		self.mana_width = self.pixel_x*60#self.card_width
		self.mana_height = self.mana_width
		self.mana_buffer = self.pixel_x*(53+(1/3))
		self.selected_card = None
		self.secondary_targets = []
		self.effect_target_self = False
		self.end_of_turn_effects = []
		self.play_trigger_effects = []
		self.possible_prep = []
		self.prepped_cards = []
		self.aura_cards = []
		self.chained_tokens = []
		self.iterations = 0
		self.triggers = 0
		self.stack = []
		self.resolving_effect = False
		self.user_input = False
		self.aura_triggers = []
		self.start_from_interupt = None
		self.trigger_type = None
		self.displayed_card = None
		self.displayed_stack = []
		self.simple_display = False
		self.deck_size = 30
		self.mana_cap = 5
		self.player_turn = 1
		self.player_status = "add_mana"
		self.highlights = []
		self.font_size = int(self.card_width/10)
		self.large_font_size = int(self.card_width/10*8)
		self.keywords = ["Undermine", "Alacrity", "Covert", "Piercing", "Healtouch", "Arrival", "Afterdeath", "Discard", "Mill", "Procure", "Consume", "Stake", "Aura", "Prep"]

		# MY_SERVER_HOST = socket.gethostbyname(socket.gethostname())
		# print(MY_SERVER_HOST)
		# MY_SERVER_PORT = 6463
		# OTHER_HOST = '10.0.1.25'
		# OTHER_PORT = 22885

		# if MY_SERVER_HOST > OTHER_HOST:
		# 	self.player = 1
		# 	self.enemy = 2
		# else:
		# 	self.player = 2
		# 	self.enemy = 1



		self.master = master
		master.title("Card Game")

		self.canvas = Canvas(master, width=self.board_width, height=self.board_height)
		self.canvas.pack()

		self.populate_buttons()
		self.populate_zones()
		self.populate_mana()
		self.decks = open("Decks",'r')
		self.deck_name1 = "test_cards"
		self.deck_name2 = "GY"
		self.populate_decks()
		self.create_trigger_dict()
		# print(list(set([1,2,3])-set([1])))
		
		self.decks.close()
		
		self.update_healths()
		self.update_decks()
		self.update_discards()
		self.start_turn()
		self.draw_from_deck(1, 4)
		self.draw_from_deck(2, 4)

		# self.greet_button = Button(master, text="Greet", command=self.greet)
		# self.greet_button.pack()

		# self.close_button = Button(master, text="Close", command=master.quit)
		# self.close_button.pack()

		# buf_x = 10
		# buf_y = 0
		# #Trebuchet MS, Orator, Bitmap
		# for name in sorted(tkinter.font.families()):
		# 	print(name)
		# 	# self.canvas.create_text(buf_x, buf_y, anchor=NW, font=(name, 20), text='test')
		# 	self.canvas.create_text(buf_x, buf_y, anchor=NW, font=(name, 20), text=name)
		# 	buf_x += 80
		# 	if buf_x > 1500:
		# 		buf_x = 10
		# 		buf_y += 50

		def m1(event):
			if (self.end_turn_button.x2 > event.x > self.end_turn_button.x1) and (self.end_turn_button.y2 > event.y > self.end_turn_button.y1) and self.player_status != "add_mana" and self.player_status != "forced_discard":
				self.end_turn_start()

			self.clicked_card = None
			for card in self.card_list1 + self.card_list2:
				if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1):
					self.clicked_card = card
					break

			self.clicked_mana = None
			if self.clicked_card == None:
				for mana in self.mana_list1 + self.mana_list2:
					if (mana.x2 > event.x > mana.x1_full) and (mana.y2 > event.y > mana.y1):
						self.clicked_mana = mana
						break

			if self.displayed_stack == [] and self.player_status != "prep_cards" and self.player_status != "use_mana" and not self.user_input:
				# for card in (self.board_list1 + self.board_list2 + self.curr_hand_list):
				if self.clicked_card in self.board_list1 + self.board_list2 + self.curr_hand_list and self.clicked_card not in self.secondary_targets and (self.clicked_card != self.selected_card or self.clicked_card.activatable):
					# if card not in self.secondary_targets:
					# 	if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1) and (card != self.selected_card or card.activatable):
					self.select_card(card, "Red")
							# if self.selected_card is not None:
							# 	if not (card in self.curr_board_list and self.selected_card.consume and self.selected_card in self.curr_hand_list):
							# 		# self.deselect_card()
							# 		# card.select_color = "Red"
							# 		self.select_card(card, "Red")
							# else:
							# 	# card.select_color = "Red"
							# 	self.select_card(card, "Red")

			elif self.player_status != "pick_card" and self.player_status != "forced_discard":
				if self.clicked_card in self.displayed_stack and (self.clicked_card != self.selected_card or self.clicked_card.activatable):
				# for card in self.displayed_stack:
					if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1) and (card != self.selected_card or card.activatable):
						# if self.selected_card is not None:
						# 	self.deselect_card()
						# card.select_color = "Red"
						self.select_card(card, "Red")



			if self.player_status == "add_mana":
				if self.clicked_mana in self.curr_mana_list and self.clicked_mana.max_amount < self.mana_cap:
				# for mana_pool in self.curr_mana_list:
				# 	if (mana_pool.x2 > event.x > mana_pool.x1_full) and (mana_pool.y2 > event.y > mana_pool.y1) and mana_pool.max_amount < self.mana_cap:
					for mana_reset in self.curr_mana_list:
						if mana_reset.max_amount < self.mana_cap:
							mana_reset.deselect()
							self.highlights.remove(mana_reset)
					self.clicked_mana.adjust_max_amount(1)
					self.clicked_mana.set_amount(self.clicked_mana.max_amount)
					self.player_status = "main_phase"
					self.resume_master = "self.main_phase()"
					if len(self.curr_hand_list) > 7:
						self.forced_discard(self.curr_hand_list)
					# break

			if self.player_status == "main_phase":
				if self.selected_card is not None:
					if self.secondary_targets == []:
						if self.selected_card.status == ("Hand"+str(self.player_turn)) and self.selected_card.type == "Unit" and self.enough_mana(self.curr_mana_list, self.selected_card.card_cost):
							for zone in self.curr_zone_list:
								if zone.status is not "Full" or self.selected_card.consume:
									self.add_secondary_highlight(zone, "Red")
						if ("Zone"+str(self.player_turn)) in self.selected_card.status and self.selected_card.can_attack and not self.selected_card.construct:
							self.get_attack_targets()

					for target in self.secondary_targets:
						if (target.x2 > event.x > target.x1) and (target.y2 > event.y > target.y1) and self.selected_card.select_color == "Red":
							if "Hero" not in target.name:
								if ("Zone"+str(self.player_turn)) in self.selected_card.status and self.selected_card.can_attack:
									if self.trigger_dict["attack_any"+str(self.selected_card.controller)] is not []:
										self.effect_trigger([self.selected_card], "attack_any"+str(self.selected_card.controller))
									self.selected_card.attack_card(target)
									self.selected_card.can_attack = False
							elif ("Zone"+str(self.player_turn)) in self.selected_card.status and self.selected_card.can_attack:
								if self.trigger_dict["attack_any"+str(self.selected_card.controller)] is not []:
									self.effect_trigger([self.selected_card], "attack_any"+str(self.selected_card.controller))
								if self.trigger_dict["attack_hero"+str(self.selected_card.controller)] is not []:
										self.effect_trigger([self.selected_card], "attack_hero"+str(self.selected_card.controller))
								self.adjust_health(self.enemy, -1*self.selected_card.attack)
								self.selected_card.can_attack = False

							if self.selected_card.status == ("Hand"+str(self.player_turn)):
								current_card_cost = self.selected_card.card_cost
								if self.selected_card.consume:
									for card in self.curr_board_list:
										if card.status == target.name:
											current_card_cost[4] -= math.ceil(card.total_mana_cost()/2)
											if current_card_cost[4] < 0:
												current_card_cost[4] = 0
											card.move(self.get_list("Disc", card.controller))

								if target.zone_discount is not None:
									for x in range(0, 5):
										current_card_cost[x] += target.zone_discount[x]
										if current_card_cost[x] < 0:
											current_card_cost[x] = 0

								if self.enough_mana(self.curr_mana_list, current_card_cost):

									for zone in self.secondary_targets:
										if zone != target:
											zone.deselect()
											self.highlights.remove(zone)
									self.secondary_targets = [target]

									self.player_status = "use_mana"
									self.queued_move = "self.play_card_from_hand(self.selected_card, self.secondary_targets[0])"
									self.spend_mana(self.curr_mana_list, current_card_cost)
							break
									


			if self.player_status != "use_mana" and self.player_status != "pick_card" and self.player_status != "prep_cards" and self.player_status != "forced_discard":
				if self.selected_card is not None:
					if self.selected_card != self.clicked_card:
					# if not ((self.selected_card.x2 > event.x > self.selected_card.x1) and (self.selected_card.y2 > event.y > self.selected_card.y1)):
						self.deselect_card()

				if self.displayed_stack == []:
					if (self.discard_zone1.x2 > event.x > self.discard_zone1.x1) and (self.discard_zone1.y2 > event.y > self.discard_zone1.y1):
						if self.discard_list1:
							self.display_stack(self.discard_list1, "Disc1")

					elif (self.discard_zone2.x2 > event.x > self.discard_zone2.x1) and (self.discard_zone2.y2 > event.y > self.discard_zone2.y1):
						if self.discard_list2:
							self.display_stack(self.discard_list2, "Disc2")

					if (self.curr_deck_zone.x2 > event.x > self.curr_deck_zone.x1) and (self.curr_deck_zone.y2 > event.y > self.curr_deck_zone.y1):
						if self.curr_deck_list:
							self.display_stack(self.curr_deck_list, ("Deck"+str(self.player_turn)))
				else:
					if not ((self.display_stack_bg.x2 > event.x > self.display_stack_bg.x1) and (self.display_stack_bg.y2 > event.y > self.display_stack_bg.y1)):
						self.put_down_stack()
						


			if self.player_status == "use_mana":
				if self.clicked_mana in self.curr_mana_list:
				# for mana_pool in self.curr_mana_list:
				# 	if (mana_pool.x2 > event.x > mana_pool.x1) and (mana_pool.y2 > event.y > mana_pool.y1):
					if self.clicked_mana.amount > 0:
						self.clicked_mana.adjust_amount(-1)
						if self.clicked_mana.amount == 0:
							self.clicked_mana.deselect()
							self.highlights.remove(self.clicked_mana)
						self.pick_mana -= 1
						remaining_mana_color = None
						for open_mana in self.curr_mana_list:
							if open_mana.amount >= self.pick_mana:
								if remaining_mana_color == None:
									remaining_mana_color = open_mana
								else:
									remaining_mana_color = None
									break
						if remaining_mana_color is not None:
							remaining_mana_color.adjust_amount(-1*self.pick_mana)
							self.pick_mana = 0

						
						if self.pick_mana == 0:
							for mana_reset in self.curr_mana_list:
								if mana_reset in self.highlights:
									mana_reset.deselect()
									self.highlights.remove(mana_reset)
							self.player_status = "main_phase"
							eval(self.queued_move)
							self.queued_move = None
							# break


		def m2(event):
			self.clicked_card = None
			for card in self.card_list1 + self.card_list2:
				if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1):
					self.clicked_card = card
					break

			if self.player_status == "main_phase":
				if self.clicked_card in self.curr_card_list and eval(self.clicked_card.activated_condition) and self.enough_mana(self.curr_mana_list, self.clicked_card.effect_cost):
				# for card in self.curr_card_list:
				# 	if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1) and eval(card.activated_condition) and self.enough_mana(self.curr_mana_list, card.effect_cost):
					# card.select_color = "Blue"
					# if self.selected_card is not None:
					# 	self.deselect_card()
					self.select_card(self.clicked_card, "Blue")
					if self.clicked_card in self.clicked_card.effect_targets:
						if self.effect_target_self == True:
							self.effect_target_self = False
						else:
							self.effect_target_self = True
						self.clicked_card.select_color = "Blue"
						self.secondary_targets.append(self.clicked_card)
					else:
						self.effect_target_self = False
					for target in self.clicked_card.effect_targets:
						if target != self.clicked_card:
							self.add_secondary_highlight(target, "Blue")
						# else:
						# 	self.effect_target_self = True
						# 	self.secondary_targets.append(target)
						# target.select_color = "Blue"
						# self.highlights.append(target)
						# self.secondary_targets.append(target)

				if self.selected_card is not None:
					if self.secondary_targets is not None and not self.effect_target_self:
						for card in self.secondary_targets:
							if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1):# and card != self.selected_card:
								if self.enough_mana(self.curr_mana_list, self.selected_card.effect_cost):

									for target in self.secondary_targets:
										if target != card and target != self.selected_card:
											target.deselect()
											self.highlights.remove(target)

									self.secondary_targets = [card]

									self.player_status = "use_mana"
									self.resume_master = "self.main_phase()"
									self.queued_move = "self.add_to_stack(self.selected_card, 'activated', self.secondary_targets)"
									# self.queued_move = "self.trigger_card_effect(self.selected_card, 'activated', self.secondary_targets)"
									self.spend_mana(self.curr_mana_list, self.selected_card.effect_cost)
									break
									# break

			# if self.player_status != "use_mana" and self.player_status != "pick_card" and self.player_status != "forced_discard":
			# 	if self.selected_card is not None:
			# 		if self.selected_card is not self.clicked_card:
			# 		# if not ((self.selected_card.x2 > event.x > self.selected_card.x1) and (self.selected_card.y2 > event.y > self.selected_card.y1)):
			# 			self.deselect_card()

			if self.player_status == "pick_card" or self.player_status == "forced_discard":
				for target in self.secondary_targets:
					if (target.x2 > event.x > target.x1) and (target.y2 > event.y > target.y1):
						if self.player_status == "forced_discard":
							for card in self.secondary_targets:
								card.deselect()
								self.highlights.remove(card)
							self.secondary_targets = []
							self.player_status = "main_phase"
							target.move("Disc"+str(self.player_turn))
							while(self.resolving_effect):
								continue
							# self.display_hand()

						elif self.selected_card is not None:
							if self.displayed_stack:
								# self.displayed_stack.remove(target)
								self.put_down_stack()
							self.selected_card.inputs.append(target)
							self.user_input = False
							self.selected_card.select_color = "Red"
							self.selected_card.iterations += 1
							self.deselect_secondaries()
							self.iterate_card_effect(self.selected_card, [])
							# self.player_status = "main_phase"
							# self.selected_card.multi_select(self.iterations-1)

						# elif self.displayed_stack:
						# 	self.displayed_stack.remove(target)
						# 	self.put_down_stack()
						# 	self.player_status = "main_phase"

						

						
						break

			if self.player_status == "prep_cards":
				if self.clicked_card in self.possible_prep and self.clicked_card not in self.prepped_cards:
				# for card in self.possible_prep:
				# 	if (card.x2 > event.x > card.x1) and (card.y2 > event.y > card.y1) and card not in self.prepped_cards:
					if self.enough_mana(self.curr_mana_list, self.clicked_card.effect_cost):
						self.add_prep_card(self.clicked_card)
						print(self.prepped_cards)
						# self.prepped_cards.append(card)
						self.possible_prep.remove(self.clicked_card)
						self.highlights.remove(self.clicked_card)
						card.deselect()
						self.add_to_stack(self.clicked_card, "prep", [])
						# self.trigger_card_effect(self.clicked_card, "prep", [])
						# if not self.possible_prep:
						# 	self.end_turn_stuff()


		self.canvas.bind("<Button-1>", m1)
		self.canvas.bind("<Button-2>", m2)


		# def ip_value(ip):
		#     # """ ip_value returns ip-string as integer """
		#     return int(''.join([x.rjust(3, '0') for x in ip.split('.')]))

		# server = connection.Server(MY_SERVER_HOST, MY_SERVER_PORT) 

		# def data_transfer():
		# 	me_data = self.make_data()
		# 	connection.send(me_data, OTHER_HOST, OTHER_PORT) # the send code

		# 	enemy_data = server.receive() # the receive code
		    
		# 	enemy.rect.centerx = int(enemy_data[:4])
		# 	enemy.rect.centery = int(enemy_data[4:])

		def game_tick():
			tick_count = 0
			while(True):
				# data_transfer()
				time.sleep(0.01)
				tick_count += 1
				if tick_count%8 == 0:
					for item in self.highlights:
						item.selected_size += self.pixel_x*2
						item.select()

				if self.stack and not self.resolving_effect:
					self.resolving_effect = True
					effect = self.stack.pop()
					print("popping")
					self.trigger_card_effect(effect[0], effect[1], effect[2])


				master.update()

		game_tick()

		master.mainloop()

	def make_data(self):
		datax = str(self.deck_size).rjust(4, '0')
		# datay = str(self.rect.centery).rjust(4, '0')
		return datax# + datay

	def greet(self):
		print("The light shall burn you!")

	def end_turn_start(self):
		if self.player_status == "prep_cards":
			self.end_turn()
		else:
			for effect in self.end_of_turn_effects:
				exec(effect)
			self.end_of_turn_effects = []
			# self.resume_master = "self.end_turn_start_prep()"
			if self.trigger_dict["end_of_turn"+str(self.player_turn)] is not []:
				if self.effect_trigger([], "end_of_turn"+str(self.player_turn)):
					print("eh")
					self.start_from_interupt = "self.end_turn_start_prep()"
					# self.end_turn_start_prep()
				else:
					self.end_turn_start_prep()
			else:
				self.end_turn_start_prep()



			# self.end_turn_start_prep()
			# if not self.user_input:
			# 	self.end_turn_start_prep()
		

	def end_turn_start_prep(self):
		while(self.stack):
			continue
		if self.player_status == "prep_cards" and not self.user_input:
			self.end_turn()
		else:
			self.deselect_card()
			self.end_turn_prep()

	def end_turn_prep(self):
		self.resume_master = "None"
		for card in self.prepped_cards:
			self.trigger_dict[card.prep_type].remove(card)
		self.prepped_cards = []
		self.possible_prep = []
		any_prep = False
		for card in self.curr_hand_list:
			if card.prep:
				if self.enough_mana(self.curr_mana_list, card.effect_cost) and eval(card.prep_condition):
					any_prep = True
					# self.resume_master = "self.prep_done_check()"
					self.player_status = "prep_cards"
					card.select_color = "Blue"
					self.highlights.append(card)
					self.possible_prep.append(card)
		if not any_prep:
			self.end_turn()

	def prep_done_check(self):
		if not self.possible_prep:
			self.user_input = False
			self.end_turn()

	# def end_turn_stuff(self):#INCORPERATE THIS TOO
	# 	for effect in self.end_of_turn_effects:
	# 		exec(effect)
	# 	self.end_of_turn_effects = []
	# 	self.effect_trigger(None, "end_of_turn"+str(self.player_turn))
	# 	if not self.aura_triggers:
	# 		self.end_turn()

	# def end_trigger(self):
	# 	if self.triggers == 0:
	# 		eval(self.)

	def end_turn(self):
		# if self.player_status != "prep_cards":
		# 	for effect in self.end_of_turn_effects:
		# 		exec(effect)
		# 	self.end_of_turn_effects = []
		# 	self.effect_trigger(None, "end_of_turn"+str(self.player_turn))

		# any_prep = False
		# for card in self.curr_hand_list:
		# 	if card.prep:
		# 		if self.enough_mana(self.curr_mana_list, card.effect_cost):
		# 			any_prep = True
		# 			break
		# if self.player_status != "prep_cards" and any_prep:
		# 	# if self.selected_card is not None:
		# 	self.deselect_card()
		# 	self.prepped_cards = []
		# 	self.possible_prep = []
		# 	self.prep_mana_list = self.curr_mana_list
		# 	self.player_status = "prep_cards"
		# 	for card in self.curr_hand_list:
		# 		if card.prep:
		# 			if self.enough_mana(self.curr_mana_list, card.effect_cost):
		# 				card.select_color = "Blue"
		# 				self.highlights.append(card)
		# 				self.possible_prep.append(card)
		# else:
		for card in self.possible_prep:
			self.highlights.remove(card)
			card.deselect()
		self.possible_prep = []
		if self.player_turn == 1:
			self.player_turn = 2
		else:
			self.player_turn = 1
		self.player_status = "add_mana"
		# if self.iterations == 0:
		self.start_turn()

	def start_turn(self):
		self.prev_selected_card = None
		if self.player_turn == 1:
			self.curr_player = 1
			self.enemy = 2

			self.curr_card_list = self.card_list1
			self.enemy_card_list = self.card_list2

			self.curr_mana_list = self.mana_list1
			self.enemy_mana_list = self.mana_list2

			self.curr_hero_zone = self.hero_zone1
			self.enemy_hero_zone = self.hero_zone2

			self.curr_health = self.health1
			self.enemy_health = self.health2

			self.curr_board_list = self.board_list1
			self.enemy_board_list = self.board_list2

			self.curr_zone_list = self.zone_list1
			self.enemy_zone_list = self.zone_list2

			self.curr_hand_list = self.hand_list1
			self.enemy_hand_list = self.hand_list2

			self.curr_deck_list = self.deck_list1
			self.enemy_deck_list = self.deck_list2

			self.curr_deck_zone = self.deck_zone1
			self.enemy_deck_zone = self.deck_zone2

			self.curr_discard_list = self.discard_list1
			self.enemy_discard_list = self.discard_list2
		else:
			self.curr_player = 2
			self.enemy = 1

			self.curr_card_list = self.card_list2
			self.enemy_card_list = self.card_list1

			self.curr_mana_list = self.mana_list2
			self.enemy_mana_list = self.mana_list1

			self.curr_hero_zone = self.hero_zone2
			self.enemy_hero_zone = self.hero_zone1

			self.curr_health = self.health2
			self.enemy_health = self.health1

			self.curr_board_list = self.board_list2
			self.enemy_board_list = self.board_list1

			self.curr_zone_list = self.zone_list2
			self.enemy_zone_list = self.zone_list1

			self.curr_hand_list = self.hand_list2
			self.enemy_hand_list = self.hand_list1

			self.curr_deck_list = self.deck_list2
			self.enemy_deck_list = self.deck_list1

			self.curr_deck_zone = self.deck_zone2
			self.enemy_deck_zone = self.deck_zone1

			self.curr_discard_list = self.discard_list2
			self.enemy_discard_list = self.discard_list1

		self.player_status = "add_mana"
		self.draw_from_deck(self.player_turn, 1)
		for mana_pool in self.curr_mana_list:
			mana_pool.set_amount(mana_pool.max_amount)
			if mana_pool.max_amount < self.mana_cap:
				mana_pool.selected = True
				self.highlights.append(mana_pool)
		for card in self.curr_board_list:
			card.can_attack = True
		# self.display_hand()

	def populate_buttons(self):
		card_posX = self.pixel_x*25
		card_posY = self.pixel_x*725
		self.end_turn_button = Card(self.canvas, self, 1, "End_Turn", "Button", card_posX, card_posY)
		self.end_turt_text = self.canvas.create_text(self.end_turn_button.x1+(self.card_width/2), self.end_turn_button.y1+(self.card_height/2), font=("Consolas", self.font_size*2), text="End Turn")

	def populate_zones(self):
		card_posX = (self.pixel_x*300)
		card_posY1 = (self.pixel_y*625)-self.card_height
		card_posY2 = (self.pixel_y*275)
		for x in range(0, 7):
			new_card = Card(self.canvas, self, 1, "Zone"+"1"+str(x), "Open", card_posX, card_posY1)
			self.zone_list1.append(new_card)
			new_card = Card(self.canvas, self, 2, "Zone"+"2"+str(x), "Open", card_posX, card_posY2)
			self.zone_list2.append(new_card)
			card_posX += self.card_width + (self.pixel_x*50)
		self.discard_zone1 = Card(self.canvas, self, 1, "Disc1", "Empty", self.pixel_x*1475, self.pixel_y*475)
		self.discard_number1 = self.canvas.create_text(self.discard_zone1.x1+(self.card_width/2), self.discard_zone1.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.discard_list1))
		self.discard_zone2 = Card(self.canvas, self, 2, "Disc2", "Empty", self.pixel_x*1475, self.pixel_y*275)
		self.discard_number2 = self.canvas.create_text(self.discard_zone2.x1+(self.card_width/2), self.discard_zone2.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.discard_list2))

		self.deck_zone1 = Card(self.canvas, self, 1, "Deck1", "Empty", self.pixel_x*1475, self.pixel_y*725)
		self.deck_number1 = self.canvas.create_text(self.deck_zone1.x1+(self.card_width/2), self.deck_zone1.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.deck_list1))
		self.deck_zone2 = Card(self.canvas, self, 2, "Deck2", "Empty", self.pixel_x*1475, self.pixel_y*25)
		self.deck_number2 = self.canvas.create_text(self.deck_zone2.x1+(self.card_width/2), self.deck_zone2.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.deck_list2))

		self.hero_zone1 = Card(self.canvas, self, 1, "Hero1", "Alive", self.pixel_x*175, self.pixel_y*725)
		self.health_number1 = self.canvas.create_text(self.hero_zone1.x1+(self.card_width/2), self.hero_zone1.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=self.health1)
		self.hero_zone2 = Card(self.canvas, self, 2, "Hero2", "Alive", self.pixel_x*175, self.pixel_y*25)
		self.health_number2 = self.canvas.create_text(self.hero_zone2.x1+(self.card_width/2), self.hero_zone2.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=self.health2)


	def populate_mana(self):
		color_list = ['red', 'blue', 'green', 'yellow']

		mana_posX = self.pixel_x*1375
		mana_posY1 = (self.pixel_y*485) - self.mana_height
		mana_posY2 = (self.pixel_y*535)
		for color in color_list:
			new_mana = Mana(self.canvas, self, color, 1, 0, 0, self.board_width, self.board_height, self.mana_width, self.mana_height, mana_posX, mana_posY1, self.mana_cap)
			self.mana_list1.append(new_mana)
			new_mana = Mana(self.canvas, self, color, 2, 0, 0, self.board_width, self.board_height, self.mana_width, self.mana_height, mana_posX, mana_posY2, self.mana_cap)
			self.mana_list2.append(new_mana)
			mana_posY1 -= self.mana_height + self.mana_buffer
			mana_posY2 += self.mana_height + self.mana_buffer

	def select_previous(self):
		if self.prev_selected_card is not None:
			self.select_card(self.prev_selected_card, "Red")

	def select_card(self, card, color):
		self.deselect_card()
		card.select_color = color
		self.selected_card = card
		self.highlights.append(card)
		self.display_card(card)

	def add_secondary_highlight(self, card, color):
		card.select_color = color
		self.highlights.append(card)
		self.secondary_targets.append(card)


	def deselect_card(self):
		if self.selected_card is not None:
			self.prev_selected_card = self.selected_card
			self.highlights.remove(self.selected_card)
			if self.selected_card in self.secondary_targets:
				self.secondary_targets.remove(self.selected_card)
			self.deselect_secondaries()
			# for card in self.secondary_targets:
			# 	card.deselect()
			# 	self.highlights.remove(card)
			# self.secondary_targets = []
			self.displayed_card.delete()
			self.displayed_card = None
			self.selected_card.deselect()
			self.selected_card = None

	def deselect_secondaries(self):
		for card in self.secondary_targets:
			if card != self.selected_card:
				card.deselect()
				self.highlights.remove(card)
		self.secondary_targets = []

	def display_card(self, card):
		card_posX = self.pixel_x*25
		if card.card_effect is None:
			card_posY = self.pixel_y*262.5
		else:
			card_posY = self.pixel_y*262.5-((self.pixel_y*4)+len(card.readable_effect)*(self.pixel_y*12))*2.5/2
		#min = 200, max = 325
		self.displayed_card = Card(self.canvas, self, 1, card.name, "Display", card_posX, card_posY)
		self.displayed_card.attack = card.attack
		self.displayed_card.defense = card.defense
		self.displayed_card.card_cost = card.card_cost
		self.displayed_card.redraw_card()

	def display_stack(self, stack, location):
		self.simple_display = True
		self.displayed_stack = stack.copy()
		def get_name(elem):
			return elem.name
		self.displayed_stack.sort(key=get_name)
		self.displayed_stack_from = location
		if len(stack) > 7:
			stack_width = 7
			stack_height = math.ceil(len(stack)/7)
		else:
			stack_width = len(stack)
			stack_height = 1
		card_buffer = self.pixel_x*25
		card_posX = (self.board_width-((self.card_width+card_buffer)*stack_width-card_buffer))/2
		start_card_posX = card_posX
		card_posY = self.board_height-((self.board_height-((self.card_height+card_buffer)*stack_height-card_buffer))/2)
		index = 0
		self.display_stack_bg = Card(self.canvas, self, 1, "End_Turn", "Button", card_posX-card_buffer, self.board_height-card_posY-card_buffer)
		self.display_stack_bg.update_dimensions((self.card_width+card_buffer)*stack_width+card_buffer, (self.card_height+card_buffer)*stack_height+card_buffer)

		for card in self.displayed_stack:
			x1 = card_posX
			y1 = self.board_height-card_posY
			x2 = card_posX+self.card_width
			y2 = (self.board_height-card_posY)+self.card_height
			card.specific_move(location, True, x1, y1, x2, y2)
			if index == 6:
				card_posX = start_card_posX
				card_posY -= self.card_height + card_buffer
				index = 0
			else:
				card_posX += self.card_width + card_buffer
				index += 1


	def put_down_stack(self):
		self.canvas.delete(self.display_stack_bg)
		self.display_stack_bg.delete()
		for card in self.displayed_stack:
			card.face_up = False
			if "Disc" in self.displayed_stack_from:
				card.move_to_discard(self.displayed_stack_from)
			elif "Deck" in self.displayed_stack_from:
				card.move_to_deck(self.displayed_stack_from)
		# if "Disc" in self.displayed_stack_from:
		# 	self.update_discards()
		# elif self.displayed_stack_from == "Deck1":
		# 	self.update_decks()
		self.displayed_stack = []
		self.displayed_stack_from = None
		self.simple_display = False

	def get_zone_by_name(self, zone_name):
		for zone in self.zone_list1 + self.zone_list2:
			if zone.name == zone_name:
				return zone


	def enough_mana(self, mana_list, card_cost):
		total_cost = 0
		for mana_pool in mana_list:
			if mana_pool.amount < card_cost[mana_pool.num]:
				# print("Not enough mana!")
				return False
		for mana_cost in card_cost:
			total_cost += mana_cost
		if self.total_mana(mana_list) >= total_cost:
			return True
		# print("Not enough mana!")
		return False


	def total_mana(self, mana_list):
		total = 0
		for mana_pool in mana_list:
			total += mana_pool.amount
		return total


	def reset_hand(self, hand):
		for card in hand:
			card.delete()


	def populate_decks(self):
		player = 0
		for x in range(0, 2):
			num_cards = 0
			for line in self.decks:
				if line[:-1] == self.deck_name1:
					player = 1
				elif line[:-1] == self.deck_name2:
					player = 2
				elif player != 0:
					new_card = Card(self.canvas, self, player, line[:-1], "Deck"+str(player), 0, 0)
					self.get_list("Card", player).append(new_card)
					new_card.move("Deck"+str(player))
					num_cards += 1
				if num_cards == self.deck_size:
					player = 0
					break
		self.total_card_list = self.card_list1 + self.card_list2
		self.shuffle_deck(self.deck_list1)
		self.shuffle_deck(self.deck_list2)
		self.decks.close()

	def display_hand(self): #HEY REMEMBER TO DOUBLE CHECK IF THIS AND THE OTHER UPDATE FUNCTIONS GET DOUBLE CALLED LATER
		if self.player_turn == 1:
			face_up = True
		else:
			face_up = False
		# 	hand_list = self.hand_list1
		# 	card_posY = self.pixel_y*200
		# else:
		# 	hand_list = self.hand_list2
		# 	card_posY = self.pixel_y*875
		card_buffer = ((13 - len(self.hand_list1))*5)*self.pixel_x
		# card_posX = (self.pixel_x*755) - (math.floor(len(self.hand_list1)/2)*card_buffer + self.card_width*len(self.hand_list1)/2)
		card_posX = (self.board_width-((self.card_width+card_buffer)*len(self.hand_list1)-card_buffer))/2

		self.reset_hand(self.hand_list1)
		card_posY = self.pixel_y*200
		for card in self.hand_list1:
			x1 = card_posX
			x2 = card_posX+self.card_width
			y1 = self.board_height-card_posY
			y2 = (self.board_height-card_posY)+self.card_height
			card.specific_move("Hand1", face_up, x1, y1, x2, y2)
			# else:
			# 	y1 = self.board_height-card_posY2
			# 	y2 = (self.board_height-card_posY2)+self.card_height
			# 	card.specific_move("Hand2", False, x1, y1, x2, y2)

			card_posX += self.card_width + card_buffer

		self.reset_hand(self.hand_list2)
		card_buffer = ((13 - len(self.hand_list2))*5)*self.pixel_x
		# card_posX = (self.pixel_x*755) - (math.floor(len(self.hand_list2)/2)*card_buffer + self.card_width*len(self.hand_list2)/2)
		card_posX = (self.board_width-((self.card_width+card_buffer)*len(self.hand_list2)-card_buffer))/2
		card_posY = self.pixel_y*875
		for card in self.hand_list2:
			x1 = card_posX
			x2 = card_posX+self.card_width
			# if player == 1:
			# 	y1 = self.board_height-card_posY1
			# 	y2 = (self.board_height-card_posY1)+self.card_height
			# 	card.specific_move("Hand1", True, x1, y1, x2, y2)
			y1 = self.board_height-card_posY
			y2 = (self.board_height-card_posY)+self.card_height
			card.specific_move("Hand2", (not face_up), x1, y1, x2, y2)

			card_posX += self.card_width + card_buffer

		if len(self.curr_hand_list) > 7 and self.player_status != "add_mana":
			self.forced_discard(self.curr_hand_list)

	def shuffle_deck(self, deck_list):
		random.shuffle(deck_list)

	def forced_discard(self, hand_list):
		for card in hand_list:
			self.add_secondary_highlight(card, "Blue")
			# card.select_color = "Blue"
			# self.highlights.append(card)
			# self.secondary_targets.append(card)
		self.player_status = "forced_discard"

	def move_to_top(self, deck_list, target):
		deck_list.remove(target)
		deck_list.append(target)

	def move_to_bottom(self, deck_list, target):
		deck_list.remove(target)
		deck_list.insert(0, target)

	def draw_from_deck(self, player, num_cards):
		for x in range(0, num_cards):
			self.draw_card(self.get_list("Hand", player), self.get_list("Deck", player).pop())

	def draw_specific_card(self, card):
		self.get_list("Deck", card.controller).remove(card)
		self.draw_card(self.get_list("Hand", card.controller), card)

	def draw_card(self, hand, card):
		card.prev_status = card.status
		card.status = "Hand"+str(card.controller)
		hand.append(card)
		self.display_hand()
		self.update_decks()

	def get_card_from_list(self, card_list, card_name):
		for card in card_list:
			if card.name == card_name:
				return card
		return False

	def update_discards(self):
		self.canvas.delete(self.discard_number1)
		self.discard_number1 = self.canvas.create_text(self.discard_zone1.x1+(self.card_width/2), self.discard_zone1.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.discard_list1))
		self.canvas.delete(self.discard_number2)
		self.discard_number2 = self.canvas.create_text(self.discard_zone2.x1+(self.card_width/2), self.discard_zone2.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.discard_list2))

	def update_decks(self):
		self.canvas.delete(self.deck_number1)
		self.deck_number1 = self.canvas.create_text(self.deck_zone1.x1+(self.card_width/2), self.deck_zone1.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.deck_list1))
		self.canvas.delete(self.deck_number2)
		self.deck_number2 = self.canvas.create_text(self.deck_zone2.x1+(self.card_width/2), self.deck_zone2.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=len(self.deck_list2))

	def update_healths(self):
		self.canvas.delete(self.health_number1)
		if self.health1 <= 0:
			self.health1 = 0
			self.player_status = "Player2_Win"
		elif self.health1 >= 50:
			self.player_status = "Player1_Win"
		self.health_number1 = self.canvas.create_text(self.hero_zone1.x1+(self.card_width/2), self.hero_zone1.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=self.health1)
		self.canvas.delete(self.health_number2)
		if self.health2 <= 0:
			self.health2 = 0
			self.player_status = "Player1_Win"
		elif self.health2 >= 50:
			self.player_status = "Player2_Win"
		self.health_number2 = self.canvas.create_text(self.hero_zone2.x1+(self.card_width/2), self.hero_zone2.y1+(self.card_height/2), font=("Consolas", self.large_font_size), text=self.health2)

	def adjust_health(self, player, value):
		if player == 1:
			self.health1 += value
		else:
			self.health2 += value
		self.update_healths()

	def play_card_from_hand(self, card, zone):
		self.possible_played_card = self.selected_card
		self.possible_played_zone = zone
		self.selected_card.deselect()

		self.highlights.remove(zone)
		zone.deselect()
		self.secondary_targets = []

		# self.resume_master = "self.play_card_counter_check()"
		if self.trigger_dict["cast_card"+str(self.selected_card.controller)] is not []:
			self.effect_trigger([self.selected_card], "cast_card"+str(self.selected_card.controller))

		while(self.resolving_effect):
			continue

		self.play_card_counter_check()


		

	def play_card_counter_check(self):
		self.select_card(self.possible_played_card, "Red")
		zone = self.possible_played_zone
		self.resume_master = "self.main_phase()"
		
		if not self.possible_played_card.countered:
			self.selected_card.move(zone.name)
			while(self.resolving_effect):
				continue
			
			# for line in self.selected_card.highlights:
			# 	self.canvas.delete(line)
			# self.selected_card.deselect()
			if self.selected_card.alacrity:
				self.get_attack_targets()
			# if self.selected_card.aura and self.prev_status not in self.aura_status and self.status in self.aura_status:
			# 	self.add_aura_card(self.selected_card)

			# if self.selected_card.arrival:
				# self.selected_card.activate_arrival(None)
				# self.resume_master = "self.main_phase()"
				# self.trigger_card_effect(self.selected_card, "arrival", [])
			
		else:
			zone.status = "Empty"
			self.main_phase()

	def create_trigger_dict(self):
		self.trigger_dict = {
			"cast_card":[],
			"cast_card1":[],
			"cast_card2":[],
			"unit_into_play":[],
			"unit_into_play1":[],
			"unit_into_play2":[],
			"unit_play_from_hand":[],
			"unit_play_from_hand1":[],
			"unit_play_from_hand2":[],
			"attack_any":[],
			"attack_any1":[],
			"attack_any2":[],
			"attack_unit":[],
			"attack_unit1":[],
			"attack_unit2":[],
			"attack_hero":[],
			"attack_hero1":[],
			"attack_hero2":[],
			"unit_death":[],
			"unit_death1":[],
			"unit_death2":[],
			"card_discard":[],
			"card_discard1":[],
			"card_discard2":[],
			"card_mill":[],
			"card_mill1":[],
			"card_mill2":[],
			"end_of_turn":[],
			"end_of_turn1":[],
			"end_of_turn2":[]
		}

	def add_aura_card(self, card):
		self.aura_cards.append(card)
		self.trigger_dict[card.aura_type].append(card)

	def remove_aura_card(self, card):
		self.aura_cards.remove(card)
		self.trigger_dict[card.aura_type].remove(card)

	def add_prep_card(self, card):
		self.prepped_cards.append(card)
		self.trigger_dict[card.prep_type].append(card)

	def remove_prep_card(self, card):
		print(self.prepped_cards)
		self.prepped_cards.remove(card)
		self.trigger_dict[card.prep_type].remove(card)

	def get_attack_targets(self):
		self.selected_card.display_ez_stat(self.selected_card.attack)
		hero_attack = True
		for card in self.selected_card.attack_targets:
			if not card.construct:
				card.display_ez_stat(card.defense)
				self.add_secondary_highlight(card, "Red")
				if self.selected_card.undermine:
					if card.defense <= self.selected_card.attack:
						hero_attack = False
				else:
					hero_attack = False

		if hero_attack:
			self.add_secondary_highlight(self.enemy_hero_zone, "Red")


	def trigger_card_effect(self, card, effect_type, secondary_targets):
		print(card.name)
		card.effect_type = effect_type
		if effect_type == "activated":
			if eval(card.activated_condition):
				for target in self.secondary_targets:
					if target != self.selected_card:
						target.deselect()
						self.highlights.remove(target)
				self.secondary_targets = []
				if card.type == "Spell":
					card.move('Disc'+str(card.controller))
					card.face_up = True
					card.deselect()
					card.redraw_card()
					# self.display_hand()
				card.commands = card.activated_commands.copy()
				card.repeats = card.activated_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "arrival":
			if eval(card.arrival_condition):
				self.select_card(card, "Blue")
				card.commands = card.arrival_commands.copy()
				card.repeats = card.arrival_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "into_play":
			if eval(card.into_play_condition):
				card.commands = card.into_play_commands.copy()
				card.repeats = card.into_play_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "aura":
			print(card.name)
			print(card.aura_condition)
			print("aura")
			print(eval(card.aura_condition))
			print("check")
			if eval(card.aura_condition):
				print("evaled")
				card.commands = card.aura_commands.copy()
				card.repeats = card.aura_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "afterdeath":
			if eval(card.afterdeath_condition):
				card.commands = card.afterdeath_commands.copy()
				card.repeats = card.afterdeath_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "discard":
			if eval(card.discard_condition):
				card.commands = card.discard_commands.copy()
				card.repeats = card.discard_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "mill":
			if eval(card.mill_condition):
				card.commands = card.mill_commands.copy()
				card.repeats = card.mill_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "prep":
			if eval(card.prep_condition):
				card.commands = card.prep_commands.copy()
				card.repeats = card.prep_repeats
				self.iterate_card_effect(card, secondary_targets)
		elif effect_type == "prep_activated":
			print("activating")
			if eval(card.prep_activated_condition):
				if card.type == "Spell":
					card.move('Disc'+str(card.controller))
					# self.display_hand()
				if card in self.prepped_cards:
					self.remove_prep_card(card)
				# self.prepped_cards.remove(card)
				self.subtract_mana(self.enemy_mana_list, card.effect_cost)
				# self.mana_prep_check()
				card.commands = card.prep_activated_commands.copy()
				card.repeats = card.prep_activated_repeats
				self.iterate_card_effect(card, secondary_targets)

	def iterate_card_effect(self, card, secondary_targets):
		print('iterating')
		if len(card.commands) > card.iterations:
			print(card.commands[card.iterations])
			exec(card.commands[card.iterations])
			if not self.user_input:
				card.iterations += 1
				self.iterate_card_effect(card, secondary_targets)
		elif card.repeats > 1:
			card.repeats -= 1
			card.iterations = 0
			self.iterate_card_effect(card, secondary_targets)
		elif card.follow_up_commands:
			if eval(card.follow_up_condition):
				card.commands = card.follow_up_commands.copy()
				card.repeats = card.follow_up_repeats
				card.follow_up_commands = []
				card.iterations = 0
				self.iterate_card_effect(card, secondary_targets)
			else:
				self.resolve_card_effect(card)
		else:
			self.resolve_card_effect(card)

	def resolve_card_effect(self, card):
		card.iterations = 0
		if card.effect_type == "activated":
			if "Unit" in card.type:
				card.select_color = "Red"
			elif "Spell" in card.type:
				self.deselect_card()
				card.face_up = False
				card.redraw_card()
				self.update_discards()
		if card.effect_type == "prep" and not self.possible_prep:
			self.user_input = False
			self.end_turn()
		if card.effect_type != "prep":
			print("maining")
			print(card.effect_type)
			# self.main_phase()
		self.resolving_effect = False
		if not self.stack and self.start_from_interupt is not None:
			eval(self.start_from_interupt)
			self.start_from_interupt = None
		# if self.stack == []:
		# 	eval(self.resume_master)
		# if card.effect_type == "aura":
		# 	self.check_aura_triggers()
		# elif card.effect_type == "prep_activated" and card.prep:
		# 	self.check_prep_triggers()
		# else:
		# 	eval(self.resume_master)


	# def resolve_card_effect(self, card):
	# 	if card.effect_type == "activated":
	# 		for command in card.resolve_activated_commands:
	# 			eval(command)
	# 	elif card.effect_type == "arrival":
	# 		for command in card.resolve_arrival_commands:
	# 			eval(command)

	# 	eval(self.resume_master)

	def main_phase(self):
		self.player_status = "main_phase"

	def open_zones(self, zone_list):
		total_open = []
		for zone in zone_list:
			if zone.status != "Full":
				total_open.append(zone)
		return total_open

	def summon_tokens(self, card_name, zones):
		for zone in zones:
			self.summon_token(card_name, zone)

	def remove_tokens(self, tokens):
		for token in tokens:
			token.move("Disc"+str(token.controller))

	def summon_token(self, card_name, zone):
		zone.status = "Full"
		token = Card(self.canvas, self, int(zone.name[4]), card_name, zone.name, zone.x1, zone.y1)
		token.face_up = True
		token.redraw_card()
		self.get_list("Board", int(zone.name[4])).append(token)
		self.get_list("Card", int(zone.name[4])).append(token)
		if self.selected_card.repeats < 2:
			for chained_token in self.chained_tokens:
				if self.trigger_dict["unit_into_play"+str(chained_token.controller)] is not []:
					self.effect_trigger([chained_token], "unit_into_play"+str(chained_token.controller))
			self.chained_tokens = []
			if self.trigger_dict["unit_into_play"+str(token.controller)] is not []:
				self.effect_trigger([token], "unit_into_play"+str(token.controller))
		else:
			self.chained_tokens.append(token)
		# self.curr_board_list.append(new_card)
		# self.curr_card_list.append(new_card)

	def card_group(self, card_pool, card_types, card_names, card_colors, mana_totals, primary_colors):
		group = []
		print("pool")
		print(card_pool)
		print("of cards")
		for card in card_pool:
			if card.type in card_types or not card_types:
				print("1")
				if self.name_compare(card_names, card.name) or not card_names:
				# if card.name in card_names or not card_names:
					print("2")
					if self.color_compare(card.card_cost, card_colors) or not card_colors:
						print("3")
						if card.primary_color in primary_colors or not primary_colors:
							print("4")
							if card.total_mana_cost() in mana_totals or not mana_totals:
								print("5")
								group.append(card)

			# if card.type in card_types and card.name in card_names and self.color_compare(card.card_colors(), card_color) and card.total_mana_cost() in mana_total:
			# 	group.append(card)
		print(group)
		return group

	def get_zone_from_status(self, zone_name):
		for zone in self.get_list("Zone", 1) + self.get_list("Zone", 2):
			if zone.name == zone_name:
				return zone

	def color_compare(self, color_list, color_codes):
		for color in color_codes:
			if color_list[color] > 0:
				return True
		return False

	def name_compare(self, card_names, card_name):
		for name in card_names:
			if name in card_name:
				return True
		return False

	def mass_adjust_stats(self, cards, stat, value):
		for card in cards:
			card.adjust_stats(stat, value)

	def spend_mana(self, mana_list, mana_cost):
		total_mana_pool = 0
		one_color = True
		colors_left = None
		for mana_pool in mana_list:
			total_mana_pool += mana_pool.amount
			print("Mana_pool color: {} num: {}".format(mana_pool.color, mana_pool.num))
			if mana_pool.amount >= mana_cost[mana_pool.num]:
				print("Mana_pool amount {}".format(mana_pool.amount))
				print("Mana_cost {}".format(mana_cost[mana_pool.num]))
				mana_pool.adjust_amount(-1*mana_cost[mana_pool.num])
				total_mana_pool -= mana_cost[mana_pool.num]
				if mana_pool.amount > 0:
					if colors_left is None:
						colors_left = mana_pool
					else:
						one_color = False

		if mana_cost[4] == 0:
			self.player_status = "main_phase"
			eval(self.queued_move)
			self.queued_move = None
		elif mana_cost[4] == total_mana_pool:
			for mana_pool in mana_list:
				mana_pool.set_amount(0)
			self.player_status = "main_phase"
			eval(self.queued_move)
			self.queued_move = None
		else:
			if one_color and colors_left.amount > mana_cost[4]:
				colors_left.adjust_amount(-1*mana_cost[4])
				self.player_status = "main_phase"
				eval(self.queued_move)
				self.queued_move = None
			else:
				self.pick_mana = mana_cost[4]
				for mana_pool in mana_list:
					if mana_pool.amount > 0:
						mana_pool.selected = True
						self.highlights.append(mana_pool)

	def subtract_mana(self, mana_list, mana_cost):
		for mana in mana_list:
			mana.adjust_amount(-1*mana_cost[mana.num])

	def effect_trigger(self, trigger_cards, trigger_type):
		self.trigger_type = trigger_type
		self.trigger_cards = trigger_cards
		secondary_targets = trigger_cards.copy()

		# self.resume_master = "self.check_prep_triggers()"
		for card in self.prepped_cards:
			if card.prep_type in trigger_type:
				print(card.prep_type)
				print(trigger_type)
				if eval(card.prep_activated_condition) and self.enough_mana(self.enemy_mana_list, card.effect_cost):
					self.add_to_stack(card, "prep_activated", trigger_cards)

		for card in self.aura_cards:
			if card.aura_type in trigger_type:
				if eval(card.aura_condition):
					print("add to stack")
					self.add_to_stack(card, "aura", secondary_targets)

		if self.stack:
			return True
		return False


		# self.prep_testers = self.prepped_cards.copy()
		# self.check_prep_triggers()

	def check_prep_triggers(self):
		if self.prep_testers:
			card = self.prep_testers.pop()
			if card.prep_type in trigger_type:
				if self.enough_mana(self.enemy_mana_list, card.effect_cost) and eval(card.prep_activated_condition):
					self.add_to_stack(card, "prep_activated", trigger_cards)
					# self.trigger_card_effect(card, "prep_activated", self.trigger_cards)
				else:
					self.check_aura_triggers()
			else:
				self.check_prep_triggers()
		else:
			self.aura_trigger()

	def aura_trigger(self):
		# self.resume_master = "self.check_aura_triggers()"
		self.aura_testers = self.aura_cards.copy()
		self.check_aura_triggers()


		# untriggered_effects = []
		# for card in self.prepped_cards:
		# 	if card.prep_type == trigger_type:
		# 		for effect in card.effect_commands:
		# 			exec(effect)
		# 		for mana_pool in self.enemy_mana_list:
		# 			mana_pool.set_amount(mana_pool.amount - card.effect_cost[mana_pool.num])
		# 		for other_prep_card in self.prepped_cards:
		# 			if not self.enough_mana(self.enemy_mana_list, other_prep_card.effect_cost):
		# 				self.prepped_cards.remove(other_prep_card)
		# 	else:
		# 		untriggered_effects.append(card)

		# self.prepped_cards = untriggered_effects

	def mana_prep_check(self):
		removed_cards = []
		for card in self.prep_testers:
			if not self.enough_mana(self.enemy_mana_list, card.effect_cost):
				removed_cards.append(card)
		for card in removed_cards:
			self.prep_testers.remove(card)

	def check_aura_triggers(self):
		if self.aura_testers:
			card = self.aura_testers.pop()
			if card.aura_type in self.trigger_type:
				if eval(card.aura_condition):
					self.add_to_stack(card, "aura", self.trigger_cards)
					# self.trigger_card_effect(card, "aura", self.trigger_cards)
				else:
					self.check_aura_triggers()
			else:
				self.check_aura_triggers()
		else:
			# self.trigger_cards = []
			print("resume1")
			eval(self.resume_master)

	def add_to_stack(self, card, trigger_type, secondary_targets):
		self.stack.append([card, trigger_type, secondary_targets])

	def get_list(self, type_list, player):
		if player == 1:
			if type_list == "Card":
				return self.card_list1
			elif type_list == "Deck":
				return self.deck_list1
			elif type_list == "Hand":
				return self.hand_list1
			elif type_list == "Board":
				return self.board_list1
			elif type_list == "Disc":
				return self.discard_list1
			elif type_list == "Zone":
				return self.zone_list1
			elif type_list == "Mana":
				return self.mana_list1
			elif type_list == "Hero_Zone":
				return self.hero_zone1
			elif type_list == "Health":
				return self.health1
			elif type_list == "Deck_Zone":
				return self.deck_zone1
			elif type_list == "Discard_Zone":
				return self.discard_zone1
		else:
			if type_list == "Card":
				return self.card_list2
			elif type_list == "Deck":
				return self.deck_list2
			elif type_list == "Hand":
				return self.hand_list2
			elif type_list == "Board":
				return self.board_list2
			elif type_list == "Disc":
				return self.discard_list2
			elif type_list == "Zone":
				return self.zone_list2	
			elif type_list == "Mana":
				return self.mana_list2
			elif type_list == "Hero_Zone":
				return self.hero_zone2
			elif type_list == "Health":
				return self.health2
			elif type_list == "Deck_Zone":
				return self.deck_zone2
			elif type_list == "Discard_Zone":
				return self.discard_zone2


root = Tk()
my_gui = Board(root, 1600, 900)
# root.mainloop()