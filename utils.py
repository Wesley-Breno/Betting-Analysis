import requests
from bs4 import BeautifulSoup
import unicodedata
from datetime import date
import re
from constants import ANALISES_FEITAS, TIMES_PONTUACOES, JOGOS_PENDENTES, NOMES_CAMPEONATOS


def pega_dados_campeonato(url_campeonato: str):
    """
    Funcao responsavel por acessar a url de um campeonato do site da www.gp1.com.br e retornar um dicionario contendo
    os nomes dos times e seus pontos especificos da classificacao.
    :param url_campeonato: URL do campeonato do site da gp1
    :return: Retorna um dicionario contendo os times e suas pontuacoes do campeonato
    """

    dados = requests.get(url_campeonato)
    html = BeautifulSoup(dados.text, 'html.parser')

    for item in html.select('.editoria.editoria-top'):  # Pegando o nome do campeonato
        NOMES_CAMPEONATOS.append(item.text.strip())

    nomes_times = []
    dados_times = []  # Lista onde ficara os dados de todos os times
    dados_time = []  # Lista onde ficara os dados de um time especifico

    # Formatando e pegando o nome de cada time do campeonato
    for item in html.select('.d-block.p-2.club-name'):
        # Pegando nomes dos times, retirando caracteres acentuados, diacriticos e trocando espacos por '-'
        nomes_times.append(''.join(c for c in unicodedata.normalize('NFD', item.text.strip().lower()) if
                                   unicodedata.category(c) != 'Mn').replace(' ', '-'))

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
        TIMES_PONTUACOES[nome_time] = dados_times[index]  # Usando o index para pegar os dados do time certo

    return TIMES_PONTUACOES


def pega_jogos_que_acontecerao(url_campeonato: str):
    """
    Funcao responsavel por verificar os jogos que irao acontecer na data atual e retorna-los
    :param url_campeonato: URL do campeonato que sera verificado os jogos que acontecerao na data atual
    :return: Retorna uma lista contendo os jogos que irao acontecer, com o nome dos times e a data
    """
    dados = requests.get(url_campeonato)
    html = BeautifulSoup(dados.text, 'html.parser')

    data_atual = date.today().strftime('%d/%m/%Y').split('/')

    # Para cada data de jogo
    for item in html.select('.rodada.d-block.py-3.mb-4'):
        data_do_jogo = re.findall(r'(\d?\d)/(\d?\d)/(\d\d\d\d)', str(item.text.strip().splitlines()[0].split()))[0]

        # Se a data do jogo for igual a data atual
        if int(data_do_jogo[0]) == int(data_atual[0]) and int(data_do_jogo[1]) == int(data_atual[1]) and int(
                data_do_jogo[2]) == int(data_atual[2]):

            nomes = unicodedata.normalize('NFD', item.text)  # Tirando acentos
            nomes = ''.join(c for c in nomes if not unicodedata.combining(c))  # Tirando caracteres diacriticos

            cont = 0  # Contador para adicionar apenas os times que jogarao
            nome_time1 = ''
            nome_time2 = ''

            # Deixando os caracteres simples e trocando os espacos por '-'
            for time in nomes.lower().strip().replace(' ', '-').split():
                if time in TIMES_PONTUACOES.keys():  # Se a string for o nome de um time
                    if cont == 0:  # Adicionando primeiro time que ira jogar
                        nome_time1 = time
                        cont += 1

                    elif cont == 1:  # Adicionando segundo time que ira jogar
                        nome_time2 = time
                        cont = 0
                        JOGOS_PENDENTES.append([nome_time1, nome_time2, data_do_jogo])

    return JOGOS_PENDENTES


def analisa_pontos_de_jogos_que_acontecerao(pontos_minimos: int = 3):
    """
    Funcao responsavel por receber os jogos que acontecerao na data atual e analisar cada jogo que ira acontecer e
    colocar em um dicionario os jogos que pelo menos um dos times tiverem mais de 3 pontos diferenca ao somar todos os
    pontos. Tambem é possivel informar a quantidade de pontos necessarias ao informar um novo valor ao parametro pontos_minimos
    :param pontos_minimos: Parametro que sera responsavel por adicionar os jogos com base se um dos times tiverem a
    quantidade de pontos informada
    :return: Retorna os jogos que um dos times tiverem 3 pontos a mais que o time adversario ou os pontos informados.
    """
    pontos_time1 = 0
    pontos_time2 = 0

    # Para cada jogo que ira acontecer, fazer analise deste jogo
    for jogo in JOGOS_PENDENTES:
        try:
            # Somando pontos do time1
            if TIMES_PONTUACOES[jogo[0]][0] > TIMES_PONTUACOES[jogo[1]][0]:  # Se time1 tiver mais pontos
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][1] < TIMES_PONTUACOES[jogo[1]][1]:  # Se tiver menos jogos
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][2] > TIMES_PONTUACOES[jogo[1]][2]:  # Se time1 tiver mais vitorias
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][3] < TIMES_PONTUACOES[jogo[1]][3]:  # Se time1 tiver menos empates
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][4] < TIMES_PONTUACOES[jogo[1]][4]:  # Se time1 tiver menos derrotas
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][5] > TIMES_PONTUACOES[jogo[1]][5]:  # Se time1 tiver mais gols-pro
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][6] < TIMES_PONTUACOES[jogo[1]][6]:  # Se time1 sofreu menos gols
                pontos_time1 += 1
            if TIMES_PONTUACOES[jogo[0]][7] > TIMES_PONTUACOES[jogo[1]][7]:  # Se time1 tiver mais gols
                pontos_time1 += 1

            # Somando pontos do time2
            if TIMES_PONTUACOES[jogo[1]][0] > TIMES_PONTUACOES[jogo[0]][0]:  # Se time2 tiver mais pontos
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][1] < TIMES_PONTUACOES[jogo[0]][1]:  # Se tiver menos jogos
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][2] > TIMES_PONTUACOES[jogo[0]][2]:  # Se time2 tiver mais vitorias
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][3] < TIMES_PONTUACOES[jogo[0]][3]:  # Se time2 tiver menos empates
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][4] < TIMES_PONTUACOES[jogo[0]][4]:  # Se time2 tiver menos derrotas
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][5] > TIMES_PONTUACOES[jogo[0]][5]:  # Se time2 tiver mais gols-pro
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][6] < TIMES_PONTUACOES[jogo[0]][6]:  # Se time2 sofreu menos gols
                pontos_time2 += 1
            if TIMES_PONTUACOES[jogo[1]][7] > TIMES_PONTUACOES[jogo[0]][7]:  # Se time2 tiver mais gols
                pontos_time2 += 1

        except KeyError:
            continue

        else:
            if pontos_time1 - pontos_time2 >= pontos_minimos:
                ANALISES_FEITAS[f'{jogo[0]} x {jogo[1]}'] = [jogo[0], '/'.join(jogo[2])]

            if pontos_time2 - pontos_time1 >= pontos_minimos:
                ANALISES_FEITAS[f'{jogo[0]} x {jogo[1]}'] = [jogo[1], '/'.join(jogo[2])]

            pontos_time1 = 0
            pontos_time2 = 0

    return ANALISES_FEITAS
