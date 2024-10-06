"""
This project is an algorithm capable of carrying out sports analysis for games that will take place on the current date
and show which games you have the most chances of winning by betting on the 'over 0.5 goals' bet type.

It is important to highlight that it gives predictions for betting, so you can lose or win in any way, as it is a
bets. The objective of the project is to make an analysis quickly so that the user can make a decision
end. Have a good time! I would be grateful if you have any suggestions for improvements to this project! <3

ASS: Wesley Oliveira ;)
"""

from constants import URLS_CHAMPIONSHIPS
from src.scrapper import Scraper

if __name__ == '__main__':
    scrapper = Scraper()
    matches_analyzed = []
    
    for url in URLS_CHAMPIONSHIPS:
        teams_scores = scrapper.get_championship_data(url)
        outstanding_games = scrapper.get_todays_matches(url)
        analyzes = scrapper.define_possible_games()

        for match, _ in analyzes.items():
            if match not in matches_analyzed:
                print(f'\033[;32m◖\033[m{match}\033[;32m◗\033[m')  # Showing teams that will play
                matches_analyzed.append(match)

    print(f'\n{len(matches_analyzed)} Games found!')
