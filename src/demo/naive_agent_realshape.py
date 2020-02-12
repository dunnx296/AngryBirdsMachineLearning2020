import sys
sys.path.append('..')
import time
from threading import Thread
import random
import json
import socket
import cv2
from math import cos, sin, degrees, pi
from client.agent_client import AgentClient, GameState
from trajectory_planner.simple_trajectory_planner import SimpleTrajectoryPlanner
from computer_vision.VisionRealShape import VisionRealShape
from computer_vision.game_object import GameObjectType
from utils.point2D import Point2D

class ClientNaiveAgent(Thread):
	"""Naive agent (server/client version)"""

	def __init__(self):
		#Wrapper of the communicating messages
		with open('../client/server_client_config.json', 'r') as config:
			sc_json_config = json.load(config)
		self.ar = AgentClient(sc_json_config[0])
		try:
			self.ar.connect_to_server()
		except socket.error as e:
			print("Error in client-server communication: " + str(e))
		self.current_level = -1
		self.failed_counter = 0
		self.solved = []
		self.tp = SimpleTrajectoryPlanner()
		self.id = 28888
		self.first_shot = True
		self.prev_target = None

	def get_next_level(self):
		level = 0
		unsolved = False
		#all the level have been solved, then get the first unsolved level
		for i in range(len(self.solved)):
			if self.solved[i] == 0:
				unsolved = True
				level = i + 1
				if level <= self.current_level and self.current_level < len(self.solved):
					continue
				else:
					return level

		if unsolved:
			return level
		level = (self.current_level + 1)%len(self.solved)
		if level == 0:
			level = len(self.solved)
		return level

	def check_my_score(self):
		"""
	     * Run the Client (Naive Agent)
		*"""
		scores = self.ar.get_all_level_scores()
		print(" My score: ")
		level = 1
		for i in scores:
			print(" level ", level, "  ", i)
			if i > 0:
				self.solved[level - 1] = 1
			level += 1

	def run(self):
		info = self.ar.configure(self.id)
		self.solved = [0 for x in range(int(info[2]))]

		#load the initial level (default 1)
		#Check my score
		self.check_my_score()

		self.current_level = self.get_next_level()
		self.ar.load_level(self.current_level)
		#ar.load_level((byte)9)
		while True:
			state = self.solve()
			#If the level is solved , go to the next level
			if state == GameState.WON:
				#/System.out.println(" loading the level " + (self.current_level + 1) )
				self.check_my_score()
				self.current_level = self.get_next_level()
				self.ar.load_level(self.current_level)
				#ar.load_level((byte)9)
				#display the global best scores

				#TODO check global score method to be implemented
				#scores = self.ar.get_global_score()
				#print("Global best score: ")
				#for i in range(len(scores)):
				#	print( " level ", (i+1), ": ", scores[i])

				# make a new trajectory planner whenever a new level is entered
				self.tp = SimpleTrajectoryPlanner()

				# first shot on this level, try high shot first
				first_shot = True

			elif state == GameState.LOST:
				#If lost, then restart the level
				self.failed_counter += 1
				if self.failed_counter > 3:

					self.failed_counter = 0
					self.current_level = self.get_next_level()
					self.ar.load_level(self.current_level)

					#ar.load_level((byte)9)
				else:
					print("restart")
					self.ar.restart_level()

			elif state == GameState.LEVEL_SELECTION:
				print("unexpected level selection page, go to the last current level : " \
				, self.current_level)
				self.ar.load_level(self.current_level)

			elif state == GameState.MAIN_MENU:
				print("unexpected main menu page, reload the level : " \
				, self.current_level)
				self.ar.load_level(self.current_level)

			elif state == GameState.EPISODE_MENU:
				print("unexpected episode menu page, reload the level: "\
				, self.current_level)
				self.ar.load_level(self.current_level)


	def solve(self):
		"""
		* Solve a particular level by shooting birds directly to pigs
		* @return GameState: the game state after shots.
		"""
		# capture Image
		screenshot = self.ar.do_screenshot()
		# process image
		vision = VisionRealShape(screenshot)
		#print(vision.find_slingshot_mbr()['slingshot'])
		sling = vision.find_slingshot_mbr()[0]
		sling.width,sling.height = sling.height,sling.width
		print('sling: ',sling.get_centre_point())
		#If the level is loaded (in PLAYING　state)but no slingshot detected, then the agent will request to fully zoom out.
		while sling == None and self.ar.get_game_state() == GameState.PLAYING:
			print("no slingshot detected. Please remove pop up or zoom out")
			try:
				time.sleep(1000)

			except:
				print("failed to sleep")

			self.ar.fully_zoom_out()
			screenshot = self.ar.do_screenshot()
			cv2.imwrite('screenshot.png',screenshot[:,:,::-1])
			vision = VisionRealShape(screenshot)
			sling = vision.find_slingshot_mbr()[0]
			sling.width,sling.height = sling.height,sling.width


		# get all the pigs
		pigs = vision.find_pigs_mbr()
		for i in range(len(pigs)):
			print('pigs: ',pigs[i].get_centre_point())
		state = self.ar.get_game_state()

		# if there is a sling, then play, otherwise skip.
		if sling != None:
			#If there are pigs, we pick up a pig randomly and shoot it.
			if len(pigs)!=0:
				release_point = None
				# random pick up a pig
				pig_list = pigs
				pig = pig_list[random.randint(0,len(pig_list)-1)]
				temp_pt = pig.get_centre_point()

				#TODO change computer_vision.cv_utils.Rectangle
				#to be more intuitive
				_tpt = Point2D(temp_pt[1],temp_pt[0])

				# if the target is very close to before, randomly choose a
				# point near it
				if self.prev_target != None and self.prev_target.distance(_tpt) < 10:
					_angle = random.uniform(0, 1) * pi * 2
					_tpt.X = _tpt.X + int(cos(_angle)) * 10
					_tpt.Y = _tpt.Y + int(sin(_angle)) * 10
					print("Randomly changing to ",  _tpt)

				self.prev_target = Point2D(_tpt.X, _tpt.Y)

				# estimate the trajectory
				print('################estimate the trajectory###################')
				print('sling: ',sling.get_centre_point())
				print('target: ', _tpt)
				pts = self.tp.estimate_launch_point(sling, _tpt)

				# do a high shot when entering a level to find an accurate velocity
				if self.first_shot and len(pts) > 1:
					release_point = pts[1]

				elif len(pts) == 1:
						release_point = pts[0]
				elif len(pts) == 2:
					# System.out.println("first shot " + first_shot)
					# randomly choose between the trajectories, with a 1 in
					# 6 chance of choosing the high one
					if random.randint(0,5) == 0:
						release_point = pts[1]
					else:
						release_point = pts[0]

				ref_point = self.tp.get_reference_point(sling)

				# Get the release point from the trajectory prediction module
				tap_time = 0
				if release_point != None:
					release_angle = self.tp.get_release_angle(sling,release_point)
					print("Release Point: ", release_point)
					print("Release Angle: ", degrees(release_angle))
					tap_interval = 0

					birds = vision.find_birds()
					bird_on_sling = vision.find_bird_on_sling(birds,sling)
					bird_type = bird_on_sling.type

					if bird_type == GameObjectType.REDBIRD:
						tap_interval = 0 # start of trajectory
					elif bird_type == GameObjectType.YELLOWBIRD:
						tap_interval = 65 + random.randint(0,24) # 65-90% of the way
					elif bird_type == GameObjectType.WHITEBIRD:
						tap_interval =  50 + random.randint(0,19) # 50-70% of the way
					elif bird_type == GameObjectType.BLACKBIRD:
						tap_interval =  0 # 70-90% of the way
					elif bird_type == GameObjectType.BLUEBIRD:
						tap_interval =  65 + random.randint(0,19) # 65-85% of the way
					else:
						tap_interval =  60

					tap_time = self.tp.get_tap_time(sling, release_point, _tpt, tap_interval)

				else:
					print("No Release Point Found")
					return self.ar.get_game_state()

				# check whether the slingshot is changed. the change of the slingshot indicates a change in the scale.
				self.ar.fully_zoom_out()
				screenshot = self.ar.do_screenshot()
				cv2.imwrite('screenshot.png',screenshot[:,:,::-1])
				vision = VisionRealShape(screenshot)
				_sling = vision.find_slingshot_mbr()[0]
				_sling.width,_sling.height = _sling.height,_sling.width
				if _sling != None:
					scale_diff = (sling.width - _sling.width)^2 +  (sling.height - _sling.height)^2
					if scale_diff < 25:
						dx = int(release_point.X - ref_point.X)
						dy = int(release_point.Y - ref_point.Y)
						if dx < 0:
							print ('ref point ', ref_point.X, ',', ref_point.Y)
							self.ar.shoot(ref_point.X, ref_point.Y, dx, dy, 0, tap_time, False)
							state = self.ar.get_game_state()
							if state == GameState.PLAYING:
								screenshot = self.ar.do_screenshot()
								cv2.imwrite('screenshot.png',screenshot[:,:,::-1])
								vision = VisionRealShape(screenshot)

								#TODO vision detect trajectory
								#traj = vision.findTrajPoints()
								#self.tp.adjust_trajectory(traj, sling, release_point)
								first_shot = False



					else:
						print("Scale is changed, can not execute the shot, will re-segement the image")
				else:
					print("no sling detected, can not execute the shot, will re-segement the image")
		return state

if __name__ == "__main__":
	na = ClientNaiveAgent()
	na.run()
