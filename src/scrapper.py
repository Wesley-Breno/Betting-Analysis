import unicodedata
import requests
import re

from bs4 import BeautifulSoup
from datetime import date


class Scraper:
    def __init__(self):
        self.teams_scores = dict()
        self.pending_games = []

    def get_championship_data(self, url_championship: str) -> dict:
        """
        Function responsible for accessing the URL of a championship on the www.gp1.com.br website and returning a dictionary containing
        the names of the teams and their specific points in the classification.
        :param url_championship: Championship URL from the gp1 website
        :return: Returns a dictionary containing the teams and their championship scores
        """

        data = requests.get(url_championship)
        html = BeautifulSoup(data.text, 'html.parser')

        team_names = []
        teams_data = []  # List where the data of all teams will be located
        team_data = []  # List where the data for a specific team will be located

        # Formatting and getting the name of each team in the championship
        for team in html.select('.d-block.p-2.club-name'):
            team_names.append(''.join(c for c in unicodedata.normalize('NFD', team.text.strip().lower()) if
                                      unicodedata.category(c) != 'Mn').replace(' ', '-'))

        # Getting the classification data for each team
        for index, team in enumerate(html.select('.d-block.p-2.text-center')):
            try:
                team_data.append(int(team.text.strip()))
            except ValueError:  # Ignoring strings and taking only numeric values
                ...
            else:
                if len(team_data) == 8:  # If you took all the data from a team
                    teams_data.append(team_data)  # Adding team data
                    team_data = []  # Clearing list to add data from another team

        # Adding to the dictionary the key being the name of the team, and the value being the points of this team
        for index, team_name in enumerate(team_names):
            self.teams_scores[team_name] = teams_data[index]

        return self.teams_scores

    def get_todays_matches(self, url_championship: str):
        """
        Function responsible for checking the games that will happen on the current date and returning them
        :param url_championship: URL of the championship that will be checked for games that will take place on the current date
        :return: Returns a list containing the games that will take place, with the name of the teams and the date
        """
        data = requests.get(url_championship)
        html = BeautifulSoup(data.text, 'html.parser')

        current_date = date.today().strftime('%d/%m/%Y').split('/')

        for match in html.select('.rodada.d-block.py-3.mb-4'):
            game_date = re.findall(r'(\d?\d)/(\d?\d)/(\d\d\d\d)', str(match.text.strip().splitlines()[0].split()))[0]

            # If the game date is the same as the current date
            if int(game_date[0]) == int(current_date[0]) and int(game_date[1]) == int(current_date[1]) and int(game_date[2]) == int(current_date[2]):
                names = unicodedata.normalize('NFD', match.text)  # Removing accents
                names = ''.join(c for c in names if not unicodedata.combining(c))  # # Removing diacritical characters

                cont = 0  # Contador para adicionar apenas os times que jogarao
                first_team_name = ''
                second_team_name = ''

                # Leaving the characters simple and replacing the spaces with '-'
                for team in names.lower().strip().replace(' ', '-').split():
                    if team in self.teams_scores.keys():  # If the string is the name of a team
                        if cont == 0:  # Adding first team that will play
                            first_team_name = team
                            cont += 1

                        elif cont == 1:  # Adding second team that will play
                            second_team_name = team
                            cont = 0
                            self.pending_games.append([first_team_name, second_team_name, game_date])
        return self.pending_games

    def define_possible_games(self, minimum_points: int = 3) -> dict:
        """
        Function responsible for receiving the games that will take place on the current date and analyzing each game that will take place and
        put in a dictionary the games in which at least one of the teams has more than 3 points difference when adding all the
        points. It is also possible to inform the number of points needed by entering a new value for the minimum_points parameter
        :param minimum_points: Parameter that will be responsible for adding games based on whether one of the teams has the
        number of points reported
        :return: Returns the games in which one of the teams has 3 more points than the opposing team or the reported points.
        """
        first_team_points = 0
        second_team_points = 0
        analysis = dict()

        for game in self.pending_games:
            try:
                # Adding points for first team
                if self.teams_scores[game[0]][0] > self.teams_scores[game[1]][0]:  # If the first team has more points
                    first_team_points += 1
                if self.teams_scores[game[0]][1] < self.teams_scores[game[1]][1]:  # If the first team have fewer games
                    first_team_points += 1
                if self.teams_scores[game[0]][2] > self.teams_scores[game[1]][2]:  # If the first team has more wins
                    first_team_points += 1
                if self.teams_scores[game[0]][3] < self.teams_scores[game[1]][3]:  # If the first team has fewer draws
                    first_team_points += 1
                if self.teams_scores[game[0]][4] < self.teams_scores[game[1]][4]:  # If the first team has fewer losses
                    first_team_points += 1
                if self.teams_scores[game[0]][5] > self.teams_scores[game[1]][5]:  # If the first team has more pro-goals
                    first_team_points += 1
                if self.teams_scores[game[0]][6] < self.teams_scores[game[1]][6]:  # If the first team conceded fewer goals
                    first_team_points += 1
                if self.teams_scores[game[0]][7] > self.teams_scores[game[1]][7]:  # If the first team has more goals
                    first_team_points += 1

                # Adding second team points
                if self.teams_scores[game[1]][0] > self.teams_scores[game[0]][0]:  # If the second team has more points
                    second_team_points += 1
                if self.teams_scores[game[1]][1] < self.teams_scores[game[0]][1]:  # If the second team have fewer games
                    second_team_points += 1
                if self.teams_scores[game[1]][2] > self.teams_scores[game[0]][2]:  # If the second team has more wins
                    second_team_points += 1
                if self.teams_scores[game[1]][3] < self.teams_scores[game[0]][3]:  # If the second team has fewer draws
                    second_team_points += 1
                if self.teams_scores[game[1]][4] < self.teams_scores[game[0]][4]:  # If the second team has fewer losses
                    second_team_points += 1
                if self.teams_scores[game[1]][5] > self.teams_scores[game[0]][5]:  # If the second team has more pro-goals
                    second_team_points += 1
                if self.teams_scores[game[1]][6] < self.teams_scores[game[0]][6]:  # If the second team conceded fewer goals
                    second_team_points += 1
                if self.teams_scores[game[1]][7] > self.teams_scores[game[0]][7]:  # If the second team has more goals
                    second_team_points += 1

            except KeyError:
                continue

            else:
                if first_team_points - second_team_points >= minimum_points:
                    analysis[f'{game[0]} x {game[1]}'] = [game[0], '/'.join(game[2])]

                if second_team_points - first_team_points >= minimum_points:
                    analysis[f'{game[0]} x {game[1]}'] = [game[1], '/'.join(game[2])]

                first_team_points = 0
                second_team_points = 0

        return analysis
