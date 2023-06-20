"""
Este projeto se trata de um algoritmo capaz de fazer analise esportiva para jogos que acontecerao na data atual
e mostrar quais jogos tem mais chances de ganhar apostando no tipo de aposta 'mais de 0.5 gols'.

É importante ressaltar que ele da palpites para aposta, entao voce perder ou ganhar de qualquer forma por se tratar de
apostas. O objetivo do projeto é fazer com que seja feita uma analise rapidamente para o usuario poder tomar a decisao
final. Tenha um bom aproveito! Ficarei agradecido, caso voce tenha alguma sugestao de melhoria para este projeto! <3

ASS: Wesley Oliveira ;)
"""

from constants import LINKS_CAMPEONATOS_GP1
from utils import pega_jogos_que_acontecerao, pega_dados_campeonato, analisa_pontos_de_jogos_que_acontecerao

if __name__ == '__main__':
    print('\n\n\t\tJogos para apostas de mais de 0.5 gols\n\n')
    for link in LINKS_CAMPEONATOS_GP1:
        times_pontuacoes = pega_dados_campeonato(link)
        jogos_pendentes = pega_jogos_que_acontecerao(link)
        analises_feitas = analisa_pontos_de_jogos_que_acontecerao()

        for partida, valores in analises_feitas.items():
            print(f'{partida}')  # Mostrando times que jogarao
            print()
