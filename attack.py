# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint

from config import options

attack_options = options['attack']


class Attack(object):

    def __init__(self, planet, attack_id, arrivalTime, coordsOrigin, destCoords, 
        detailsFleet, player, message_url):

        self.planet = planet
        self.id = attack_id
        self.arrivalTime = arrivalTime
        self.coordsOrigin = coordsOrigin
        self.destCoords = destCoords
        self.detailsFleet = detailsFleet
        self.player = player
        self.message_url = message_url
        self.noticed_time = datetime.now()
        self.message_sent = False
        self.sms_sent = False

    def _parse_time(self, time_str):
        d = datetime.now()
        dd = datetime.strptime(time_str, '%H:%M:%S')

        gd = datetime(d.year, d.month, d.day, dd.hour, dd.minute, dd.second)
        return gd

    def is_dangerous(self):
        return self.detailsFleet > int(attack_options['max_ships'])

    def get_random_message(self):
        messages = attack_options['messages'].split(',')
        return messages[randint(0, len(messages) - 1)]

    def get_sms_text(self):
        return u'%s %s %s %s' % (self.planet, self.arrivalTime, self.player, 
            self.detailsFleet)

    def __str__(self):
        return 'Attack id: %s to: %s. Agressor: %s, ships: %s. Time:%s' % \
            (self.id, self.destCoords, self.player, self.detailsFleet, 
            self.arrivalTime)
