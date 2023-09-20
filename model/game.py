import logging
import random

from model.player import Player
from service.recognition import RecognitionService

possible_player_names = ['Simone', 'Stefan', 'Dennis', 'Roy', 'Pieter', 'Marcel', 'Julian', 'Martin', 'Piter', 'Thijs', 'Nicolette']


class Yahtzee:
    def __init__(self, number_of_players: int):
        logging.info(f'starting game with {number_of_players} players')
        self.recognition_service: RecognitionService = RecognitionService()

        self.players: [Player] = []

        for i in range(number_of_players):
            randint = random.Random().randint(0, len(possible_player_names) - 1)
            self.players.append(Player(possible_player_names[randint]))

        logging.info(f'started with: \n {[player.name for player in self.players]}')

    def play_round(self):
        logging.info(f'start of round, current scores: \n {[player.get_total() for player in self.players]}')
        for player in self.players:
            player.play_round(self.recognition_service.dice_rols(None))

    def play_game(self):
        for player in self.players:
            player.start_game()

        for i in range(13):
            self.play_round()

        logging.info(f'winner is {self.get_winner().name}')

    def get_winner(self) -> Player:
        winner = self.players[0]
        for player in self.players:
            if player.get_total() > winner.get_total():
                winner = player

        return winner
