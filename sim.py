import math

class Sim(object):
	FIRST_COST = {
		'metalMine': {
			'metal':    60,
			'crystal':  15,
			'deuterium': 0,
		},
		'crystalMine': {
			'metal':   48,
			'crystal': 24,
			'deuterium': 0
		},
		'deuteriumMine':{
			'metal':   225,
			'crystal':  75,
			'deuterium': 0
		},
		'solarPlant': {
			'metal':   75,
			'crystal': 30,
			'deuterium': 0
		},
		'fusionPlant': {
			'metal': 900,
			'crystal': 360,
			'deuterium': 180
		}
	}
	FACTORS = {
		'metalMine': 1.5,
		'crystalMine': 1.6,
		'deuteriumMine': 1.5,
		'solarPlant': 1.5,
		'fusionPlant': 1.8
	}

	ENERGY_COST_FACTORS = {
		'metalMine': 10,
		'crystalMine': 10,
		'deuteriumMine': 20
	}

	def _calc_building_cost(self, what, level):
		assert what in ('metalMine', 'crystalMine', 'deuteriumMine', 'solarPlant', 'fusionPlant')
		return {
			'metal': int(self.FIRST_COST[what]['metal'] * (self.FACTORS[what] ** (level - 1))),
			'crystal': int(self.FIRST_COST[what]['crystal'] * (self.FACTORS[what] ** (level - 1))),
			'deuterium': int(self.FIRST_COST[what]['deuterium'] * (self.FACTORS[what] ** (level - 1))),
		}

	def _calc_energy_cost(self, what, level):
		return math.floor(self.ENERGY_COST_FACTORS[what] * level * 1.1 ** level) + 1

	def upgrade_energy_cost(self, what, to_level):
		try:
			return self._calc_energy_cost(what, to_level) - self._calc_energy_cost(what, to_level-1)
		except KeyError:
			return -10000000

	def cost_solar_plant(self, level):
		return self._calc_building_cost('solarPlant', level)

	def cost_metal_mine(self, level):
		return self._calc_building_cost('metalMine', level)

	def cost_crystal_mine(self, level):
		return self._calc_building_cost('crystalMine', level)

	def cost_deuterium_mine(self, level):
		return self._calc_building_cost('deuteriumMine', level)

	def get_cost(self, what, level):
		return self._calc_building_cost(what, level)

	def get_total_transport_capacity(self, ships):
		return (ships['lt'] * 5000) + (ships['dt'] * 25000)

#test
if __name__ == "__main__":
	s = Sim()
