from sim import Sim

class TransportManager(object):
	def __init__(self, planets=[]):
		self.planets = planets
		self.sim = Sim()
		self.dest_planet = None
		self.building = None
		self.resources_needed = {
			'metal': 0,
			'crystal': 0,
			'deuterium': 0
		}
		self.resources_sent = self.resources_needed
		self.building_queue = set()

	def find_solar_to_upgrade(self):
		planets = filter(lambda x: not x.in_construction_mode and not (x in self.building_queue), self.planets)
		for p in iter(planets):
			if p.resources['energy'] < 0:
				return p, 'solarPlant'
		return None, None

	def find_planet_to_upgrade(self):
		# check mine levels and pick one to upgrade
		mm, cm, dm, sp = [], [], [], []
		planets = filter(lambda x: not x.in_construction_mode and not (x in self.building_queue), self.planets)
		if not planets:
			return None, None
		for p in iter(planets):
			mm.append(p.buildings['metalMine']['level'])
			cm.append(p.buildings['crystalMine']['level'])
			dm.append(p.buildings['deuteriumMine']['level'])
			sp.append(p.buildings['solarPlant']['level'])

		# search biggest difference
		worst_mm = min(mm)
		mm_diff = max(mm) - worst_mm
		worst_cm = min(cm)
		cm_diff = max(cm) - worst_cm
		worst_dm = min(dm)
		dm_diff = max(dm) - worst_dm
		worst_sp = min(sp)
		sp_diff = max(sp) - worst_sp
		worst_planets = {
			'metalMine' : planets[mm.index(worst_mm)],
			'crystalMine': planets[cm.index(worst_cm)],
			'deuteriumMine': planets[dm.index(worst_dm)],
			'solarPlant' : planets[sp.index(worst_sp)]
		}

		diff = {
			'metalMine': mm_diff,
			'crystalMine': cm_diff,
			'deuteriumMine': dm_diff,
			'solarPlant': sp_diff
		}

		sorted_diff = sorted(diff, key=diff.get, reverse=True)
		#we now what to build, but where?
		what = sorted_diff[0]

		#print 'planet to upgrade', worst_planets[what], what
		return worst_planets[what], what

	def calc_resources_needed(self):
		level = self.dest_planet.buildings[self.building]['level']
		cost = self.sim.get_cost(self.building, level+1)
		available = self.dest_planet.resources
		#print 'level: ', level
		#print 'cost: ', cost
		#print 'available: ', available
		res = {}
		for resType in ('metal', 'crystal', 'deuterium'):
			res[resType] = cost[resType] - available[resType]
			if res[resType] < 0:
				res[resType] = 0
		return res

	def get_resources_available_to_send(self, planet, need_to_send):
		total = self.sim.get_total_transport_capacity(planet.ships)
		will_be_sent = {'metal': 0, 'crystal': 0, 'deuterium': 0}
		for resourceType in ('metal', 'crystal', 'deuterium'):
			if need_to_send[resourceType] <= 0:
				continue
			if need_to_send[resourceType] <= total:
				if need_to_send[resourceType] <= planet.resources[resourceType]:
					total -= need_to_send[resourceType]
					will_be_sent[resourceType] = need_to_send[resourceType]
				else:
					will_be_sent[resourceType] = planet.resources[resourceType]
					total-= planet.resources[resourceType]
			else:
				return will_be_sent
		return will_be_sent

	def process_dest_planet(self):
		self.resources_needed = self.calc_resources_needed()
		planets = filter(lambda x: x != self.dest_planet, self.planets)
		if self.enough_resources_to_build():
			self.building_queue.add(self.dest_planet)
			#sort planets by resources
			planets.sort(key=lambda p: sum([p.resources['metal'], p.resources['crystal']]), reverse=True)
			res = []
			need_to_send = {}
			send = False
			for resourceType in ('metal', 'crystal', 'deuterium'):
				need_to_send[resourceType] = self.resources_needed[resourceType] - self.resources_sent[resourceType]
				if need_to_send[resourceType] > 0:
					send = True
			if not send:
				return
			for p in iter(planets):
				task = {'from': p, 'where': self.dest_planet, 'resources': {}}
				task['resources'] = self.get_resources_available_to_send(p, need_to_send)
				if task['resources']['metal'] + task['resources']['crystal'] < 50000:
					continue
				res.append(task)
				for resourceType in ('metal', 'crystal', 'deuterium'):
					need_to_send[resourceType] -= task['resources'][resourceType]
					return res
			return res
		else:
			return None


	def enough_resources_to_build(self):
		res = {
			'metal': 0,
			'crystal': 0,
			'deuterium': 0
		}

		for p in iter(self.planets):
			r = p.resources
			res['metal'] += r['metal']
			res['crystal'] += r['crystal']
			res['deuterium'] += r['deuterium']
		#print 'available: ', res
		#print 'needed: ', self.resources_needed
		#print 'sent: ', self.resources_sent
		for resType in ('metal', 'crystal', 'deuterium'):
			if res[resType] < (self.resources_needed[resType] - self.resources_sent[resType]):
				return False

		return True

	def reset(self):
		self.dest_planet = None
		self.building = None
		self.resources_needed = {
			'metal': 0,
			'crystal': 0,
			'deuterium': 0
		}
		self.resources_sent = self.resources_needed


	def update_sent_resources(self, resources):
		all_sent = True
		for resType in ('metal', 'crystal', 'deuterium'):
			self.resources_sent[resType] += resources[resType]
			if self.resources_sent[resType] < self.resources_needed[resType]:
				all_sent = False

		if all_sent:
			self.building_queue.add(self.dest_planet)
			self.reset()

	def get_resources_needed(self):
		return self.resources_needed

	def get_summary(self):
		summ = '\nDest planet: %s\n'
		summ += 'Building: %s\n'
		summ += 'Resources needed: %s\n'
		summ += 'Resources sent: %s\n'
		summ = summ % (self.dest_planet, self.building, 
			self.resources_needed, self.resources_sent)
		return summ


	def update_building(self, planet):
		if planet in self.building_queue:
			self.building_queue.remove(planet)
			self.reset()

	def find_dest_planet(self, planets):
		self.planets = planets
		if len(self.planets) < 2:
			return None

		if self.dest_planet is not None:
			return self.process_dest_planet()

		# check if solar plant needs upgrade somewhere
		p, building = self.find_solar_to_upgrade()
		if not p:
			p, building = self.find_planet_to_upgrade()
		if p:
			self.dest_planet = p
			self.building = building
			return self.process_dest_planet()

		# nothing to do
		return None


		
		
		