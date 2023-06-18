"""
Este codigo se trata de uma classe que recebe uma url de um campeonato do site: https://www.gp1.com.br/
Apos a url ser informada, podera ser criado um objeto com o link informado, podendo pegar os jogos que irao acontecer
no campeonato informado, e assim fazendo uma analise com o metodo 'analisa_pontos_de_jogos_que_acontecerao' que se
o metodo nao receber os parametros, ele ira fazer um calculo onde ele soma os pontos de cada time e pega a porcentagem
fazendo assim um 'ponto minimo' para ser um jogo onde um dos times tenha mais probabilidade de ganhar com a comparacao
do pontos do time com o ponto minimo. Caso os parametros sejam informados, a funcao so ira pegar os times que tiverem
os pontos iguais aos parametros informados, podendo assim fazer uma analise especifica de jogos que irao acontecer.
"""

import requests  # Modulo utilizado para pegar dados de paginas da web
import unicodedata  # Modulo usado para trabalhar com caracteres Unicode
import re  # RegEx para filtrar os dados da pagina web e pegar apenas os dados necessarios
from bs4 import BeautifulSoup  # Modulo que extrai os dados HTML da pagina
from datetime import date  # Funcao usada para

links_campeonatos_gp1 = [
    'https://www.gp1.com.br/tabelas/campeonato-brasileiro-a/',
    'https://www.gp1.com.br/tabelas/campeonato-brasileiro-b/',
    'https://www.gp1.com.br/tabelas/campeonato-brasileiro-c/',
    'https://www.gp1.com.br/tabelas/campeonato-brasileiro-d/',
    'https://www.gp1.com.br/tabelas/campeonato-alagoano/',
    'https://www.gp1.com.br/tabelas/campeonato-baiano/',
    'https://www.gp1.com.br/tabelas/campeonato-capixaba/',
    'https://www.gp1.com.br/tabelas/campeonato-carioca/',
    'https://www.gp1.com.br/tabelas/campeonato-catarinense/',
    'https://www.gp1.com.br/tabelas/campeonato-cearense/',
    'https://www.gp1.com.br/tabelas/campeonato-gaucho/',
    'https://www.gp1.com.br/tabelas/campeonato-goiano/',
    'https://www.gp1.com.br/tabelas/campeonato-maranhense/',
    'https://www.gp1.com.br/tabelas/campeonato-matogrossense/',
    'https://www.gp1.com.br/tabelas/campeonato-mineiro/',
    'https://www.gp1.com.br/tabelas/campeonato-paraense/',
    'https://www.gp1.com.br/tabelas/campeonato-paraibano/',
    'https://www.gp1.com.br/tabelas/campeonato-paranaense/',
    'https://www.gp1.com.br/tabelas/campeonato-paulista/',
    'https://www.gp1.com.br/tabelas/campeonato-pernambucano/',
    'https://www.gp1.com.br/tabelas/campeonato-piauiense/',
    'https://www.gp1.com.br/tabelas/campeonato-potiguar/',
    'https://www.gp1.com.br/tabelas/campeonato-sergipano/',
    'https://www.gp1.com.br/tabelas/campeonato-sul-matogrossense/',
    'https://www.gp1.com.br/tabelas/campeonato-sul-matogrossense/',
    'https://www.gp1.com.br/tabelas/copa-do-mundo-fifa/',
    'https://www.gp1.com.br/tabelas/copa-sul-americana/',
    'https://www.gp1.com.br/tabelas/eliminatorias-da-copa-do-mundo/',
    'https://www.gp1.com.br/tabelas/copa-libertadores-da-america/',
    'https://www.gp1.com.br/tabelas/liga-dos-campeoes-da-uefa/'
]


class AnaliseEsportivaSiteGp1:
    def __init__(self, url_campeonato):
        self.url_campeonato = url_campeonato
        self.nome_campeonato = ''
        self.times_pontuacoes = dict()
        self.analises_feitas = dict()
        self.jogos_pendentes = []

    def pega_dados_campeonato(self):
        """
        Funcao que pega os dados do campeonato, estes sendo...
        Nome do campeonato, nomes dos times e suas pontuacoes.
        A funcao faz a raspagem de dados da url do campeonato e extrai o nome,
        apos isso, faz a raspagem de dados para pegar o nome de cada time e seus
        pontos no campeonato, colocando em um dicionario o nome do time como chave,
        e uma lista com suas pontuacoes sendo o valor. Exemplo;
            nome_campeonato = 'campeonato X'
            {'sport': [1, 2, 3, 4, 5, 6, 7, 8], ....}
        :return: None
        """

        dados = requests.get(self.url_campeonato)
        html = BeautifulSoup(dados.text, 'html.parser')

        for item in html.select('.editoria.editoria-top'):  # Pegando o nome do campeonato
            self.nome_campeonato = item.text.strip()

        nomes_times = []
        dados_times = []  # Lista onde ficara os dados de todos os times
        dados_time = []  # Lista onde ficara os dados de um time especifico

        # Formatando e pegando o nome de cada time do campeonato
        for item in html.select('.d-block.p-2.club-name'):
            # Pegando nomes dos times, retirando caracteres acentuados, diacriticos e trocando espacos por '-'
            nomes_times.append(''.join(c for c in unicodedata.normalize('NFD', item.text.strip().lower()) if unicodedata.category(c) != 'Mn'). replace(' ', '-'))

        # Pegando os dados de classificacao de cada time
        for index, item in enumerate(html.select('.d-block.p-2.text-center')):
            try:
                dados_time.append(int(item.text.strip()))
            except ValueError:  # Ignorando strings e pegando apenas valores numericos
                ...
            else:
                if len(dados_time) == 8:  # Se pegou todos os dados de um time
                    dados_times.append(dados_time)  # Adicionando dados do time
                    dados_time = []  # Limpando lista para adicionar os dados de outro time

        # Adicionando no dicionario a chave sendo o nome do time, e o valor sendo os pontos deste time
        for index, nome_time in enumerate(nomes_times):
            self.times_pontuacoes[nome_time] = dados_times[index]  # Usando o index para pegar os dados do time certo

    def pega_jogos_que_acontecerao(self):
        """
        Funcao responsavel por fazer as raspagem de dados dos jogos que aconteceram
        e os que ainda irao acontecer, fazendo uma filtragem para apenas os jogos
        que ainda irao acontecer e colocando o nome de cada time e sua data em uma lista.
        Apos tudo isso, o algoritmo adiciona o jogo que ira acontecer em uma lista com
        todos os jogos que irao acontecer... Exemplo;
            jogos_pendentes = [['sport', 'santa-cruz', ('06', '06', '2023')], ....]
        :return: None
        """

        if len(self.times_pontuacoes) == 0:  # Se ainda nao foi coletado os dados do campeonato
            self.pega_dados_campeonato()

        dados = requests.get(self.url_campeonato)
        html = BeautifulSoup(dados.text, 'html.parser')

        data_atual = date.today().strftime('%d/%m/%Y').split('/')

        # Para cada data de jogo
        for item in html.select('.rodada.d-block.py-3.mb-4'):
            data_do_jogo = re.findall(r'(\d?\d)/(\d?\d)/(\d\d\d\d)', str(item.text.strip().splitlines()[0].split()))[0]

            # Se a data do jogo for igual ou maior que a data atual
            if int(data_do_jogo[0]) == int(data_atual[0]) and int(data_do_jogo[1]) == int(data_atual[1]) and int(
                    data_do_jogo[2]) == int(data_atual[2]):

                nomes = unicodedata.normalize('NFD', item.text)  # Tirando acentos
                nomes = ''.join(c for c in nomes if not unicodedata.combining(c))  # Tirando caracteres diacriticos

                cont = 0  # Contador para adicionar apenas os times que jogarao
                nome_time1 = ''
                nome_time2 = ''

                # Deixando os caracteres simples e trocando os espacos por '-'
                for time in nomes.lower().strip().replace(' ', '-').split():
                    if time in self.times_pontuacoes.keys():  # Se a string for o nome de um time
                        if cont == 0:  # Adicionando primeiro time que ira jogar
                            nome_time1 = time
                            cont += 1

                        elif cont == 1:  # Adicionando segundo time que ira jogar
                            nome_time2 = time
                            cont = 0
                            self.jogos_pendentes.append([nome_time1, nome_time2, data_do_jogo])

    def analisa_pontos_de_jogos_que_acontecerao(self, pontos_time1_deve_ter=None, pontos_time2_deve_ter=None):
        """
        Funcao que soma +1 ponto para cada vantagem que um time tiver nos seus dados da classificacao. A
        funcao é responsavel por analisar os jogos que irao acontecer e somar +1 ponto para cada vantagem de
        cada time. Apos feita analise, se o usuario NAO informou os valores numericos dos parametros, a funcao
        ira salvar no dicionario 'analises_feitas', os jogos onde um dos times tiverem o minimo de pontos necessario
        e o time adversario tiver pontos menor. Caso o usuario preencha os parametros com numeros inteiros,
        a funcao so ira salvar no dicionario 'analises_feitas', os jogos onde os pontos dos times forem iguais
        aos pontos que o usuario esperava.
        :param pontos_time1_deve_ter: Parametro opcional, caso o usuario queira que os times tenham pontos especificos
        :param pontos_time2_deve_ter: Parametro opcional, caso o usuario queira que os times tenham pontos especificos
        :return: None
        """

        if len(self.times_pontuacoes) == 0:  # Se ainda nao foi coletado os dados do campeonato
            self.pega_dados_campeonato()

        if len(self.jogos_pendentes) == 0:  # Se ainda nao foi coletado os jogos que irao acontecer
            self.pega_jogos_que_acontecerao()

        pontos_time1 = 0
        pontos_time2 = 0

        # Para cada jogo que ira acontecer, fazer analise deste jogo
        for jogo in self.jogos_pendentes:
            try:
                # Somando pontos do time1
                if self.times_pontuacoes[jogo[0]][0] > self.times_pontuacoes[jogo[1]][0]:  # Se time1 tiver mais pontos
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][1] < self.times_pontuacoes[jogo[1]][1]:  # Se tiver menos jogos
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][2] > self.times_pontuacoes[jogo[1]][2]:  # Se time1 tiver mais vitorias
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][3] < self.times_pontuacoes[jogo[1]][3]:  # Se time1 tiver menos empates
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][4] < self.times_pontuacoes[jogo[1]][4]:  # Se time1 tiver menos derrotas
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][5] > self.times_pontuacoes[jogo[1]][5]:  # Se time1 tiver mais gols-pro
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][6] < self.times_pontuacoes[jogo[1]][6]:  # Se time1 sofreu menos gols
                    pontos_time1 += 1
                if self.times_pontuacoes[jogo[0]][7] > self.times_pontuacoes[jogo[1]][7]:  # Se time1 tiver mais gols
                    pontos_time1 += 1

                # Somando pontos do time2
                if self.times_pontuacoes[jogo[1]][0] > self.times_pontuacoes[jogo[0]][0]:  # Se time2 tiver mais pontos
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][1] < self.times_pontuacoes[jogo[0]][1]:  # Se tiver menos jogos
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][2] > self.times_pontuacoes[jogo[0]][2]:  # Se time2 tiver mais vitorias
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][3] < self.times_pontuacoes[jogo[0]][3]:  # Se time2 tiver menos empates
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][4] < self.times_pontuacoes[jogo[0]][4]:  # Se time2 tiver menos derrotas
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][5] > self.times_pontuacoes[jogo[0]][5]:  # Se time2 tiver mais gols-pro
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][6] < self.times_pontuacoes[jogo[0]][6]:  # Se time2 sofreu menos gols
                    pontos_time2 += 1
                if self.times_pontuacoes[jogo[1]][7] > self.times_pontuacoes[jogo[0]][7]:  # Se time2 tiver mais gols
                    pontos_time2 += 1

            except KeyError:
                ...

            else:
                # Se o usuario nao informou a quantidade de pontos especificos que os times devem ter
                if pontos_time1_deve_ter is None or pontos_time2_deve_ter is None:

                    # Se o time1 tiver o maximo de pontos
                    if pontos_time1 - pontos_time2 >= 3:
                        self.analises_feitas[f'{jogo[0]} x {jogo[1]}'] = [jogo[0], '/'.join(jogo[2])]

                    if pontos_time2 - pontos_time1 >= 3:
                        self.analises_feitas[f'{jogo[0]} x {jogo[1]}'] = [jogo[1], '/'.join(jogo[2])]

                else:
                    # Se os pontos dos times forem iguais aos pontos que o usuario quer
                    if pontos_time1 == pontos_time1_deve_ter and pontos_time2 == pontos_time2_deve_ter:
                        self.analises_feitas[f'{jogo[0]} x {jogo[1]}'] = {'pontos_time1': pontos_time1,
                                                                          'pontos_time2': pontos_time2,
                                                                          'data_do_jogo': '/'.join(jogo[2])}
                pontos_time1 = 0
                pontos_time2 = 0


if __name__ == '__main__':
    print('\n\n\t\tJogos para apostas de mais de 0.5 gols\n\n')
    for link in links_campeonatos_gp1:  # Para cada link de campeonato
        campeonato = AnaliseEsportivaSiteGp1(link)
        campeonato.analisa_pontos_de_jogos_que_acontecerao()  # Analisando campeonato

        if len(campeonato.analises_feitas) > 0:  # Se a analise foi feita com exito
            print(f'\033[;31m{campeonato.nome_campeonato}\033[m')

            for partida, valores in campeonato.analises_feitas.items():
                print(valores[1])  # Imprimindo data do jogo
                print(f'{partida} == {valores[0]}')  # Mostrando times que jogarao e o time mais provavel de ganhar
                print()
