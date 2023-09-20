import logging
import random

from model.player import Player

possible_player_names = ['Simone', 'Stefan', 'Dennis', 'Roy', 'Pieter', 'Marcel', 'Julian', 'Martin', 'Piter', 'Thijs', 'Nicolette']


class Yahtzee:
    def __init__(self, number_of_players: int):
        logging.info(f'starting game with {number_of_players} players')
        self.players: [Player] = []

        for i in range(number_of_players):
            randint = random.Random().randint(0, len(possible_player_names) - 1)
            self.players.append(Player(possible_player_names[randint]))

        logging.info(f'started with: \n {[player.name for player in self.players]}')
