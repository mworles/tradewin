import logging
import random

from constants import MY_TEAM


class RosterHolder:
    def __init__(self, rosters, my_team = MY_TEAM):
        self.rosters = rosters
        self.my_team = my_team
