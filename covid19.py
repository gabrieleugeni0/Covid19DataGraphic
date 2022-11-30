# importacao de bibliotecas
import requests
import csv
# import datetime (NAO SERA UTILIZADO E NAO FUNCIONOU NO PYCHARM)
from PIL import Image
from urllib.parse import quote
from time import sleep

# recebendo os dados da API
url = 'https://api.covid19api.com/dayone/country/brazil'
requisicao = requests.get(url)
dados_api = requisicao.json()

# criando uma lista de listas (final_data) com os dados recebidos da API, para ser usada em um arquivo CSV
dados_finais = []
for dicionario in dados_api:
    dados_finais.append([dicionario['Confirmed'], dicionario['Deaths'], dicionario['Recovered'],
                         dicionario['Active'], dicionario['Date'][:10]])
dados_finais.insert(0, ['Confirmados', 'Obitos', 'Recuperados', 'Ativos', 'Data'])

# nomeando as posicoes de cada lista
confirmados = 0
mortos = 1
recuperados = 2
ativos = 3
data = 4

# criando o arquivo CSV (final_data ja e uma lista de listas, facilitando esse processo) NAO SERA USADO PARA O GRAFICO
with open('brasil-covid.csv', 'w', newline='') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerows(dados_finais)

# transformando a string da data em um formato de data real (NAO FUNCIONOU NO PYCHARM, MAS NAO IREI USAR)
'''for dados_diarios in range(1, len(dados_finais)):
    dados_finais[dados_diarios][data] = datetime.datetime.strptime(final_data[dados_diarios][data], '%Y-%m-%d')'''


# criando funcao para gerar datasets para a API geradora de graficos chamada quickchart
def gerar_dados(lista_dados, etiqueta):
    if len(lista_dados) > 1:
        conjunto_dados = []
        for contador in range(len(lista_dados)):
            conjunto_dados.append({
                'label': etiqueta[contador],
                'data': lista_dados[contador]
            })
        return conjunto_dados
    else:
        return [{
            'label': etiqueta,
            'data': lista_dados
        }]


# criando funcao para colocar titulo no grafico
def titulo_grafico(titulo=''):
    if titulo != '':
        mostrar = 'true'
    else:
        mostrar = 'false'
    return {
        'display': mostrar,
        'title': titulo
    }


# criando funcao para gerar o codigo(dicionario) do grafico
def gerar_grafico(etiquetasx, lista_dados, etiquetasy, tipo='bar', titulo=''):
    conjunto_dados = gerar_dados(lista_dados, etiquetasy)
    opcoes = titulo_grafico(titulo)
    dadosdografico = {
        'type': tipo,
        'data': {
            'labels': etiquetasx,
            'datasets': conjunto_dados
        },
        'options': opcoes
    }
    return dadosdografico


# criando funcao para requisitar o grafico da API
def requrer_grafico(dadosdografico):
    url_base = 'https://quickchart.io/chart?c='
    req = requests.get(f'{url_base}{str(dadosdografico)}')
    conteudo = req.content
    return conteudo


# criando funcao para salvar a imagem do grafico
def salvar_imagem_grafico(caminho, conteudo_binario):
    with open(caminho, 'wb') as imagem_grafico:
        imagem_grafico.write(conteudo_binario)


# criando funcao para exibir a imagem do grafico na tela
def mostrar_grafico(caminho):
    imagem = Image.open(caminho)
    imagem.show()


# criando funcao para gerar qr code
def requerer_qrcode(url_texto):
    url_link = quote(url_texto)
    url_final = f'https://quickchart.io/qr?text={url_link}'
    req = requests.get(url_final)
    conteudo = req.content
    return conteudo


# PROGRAMA PRINCIPAL

# 1o. - criando dados para informar para as funcoes
try:
    while True:
        intervalo_dados = int(input('Com qual intervalo deseja gerar o grafico? [20 ou mais]\n'))
        if 20 <= intervalo_dados <= 400:
            break
        else:
            print('OPCAO INVALIDA!', end=' ')
except:
    sleep(1)
    print('ERRO - OPCAO INVALIDA!')
    sleep(1)
    print('INTERVALO PADRAO DE 50 DIAS ESCOLHIDO!')
    sleep(3)
finally:
    intervalo_dados = 50
etiquetas_x = []
for dados_diarios in dados_finais[1::intervalo_dados]:
    etiquetas_x.append(dados_diarios[data])
dados_confirmados = []
dados_recuperados = []
for dados_diarios in dados_finais[1::intervalo_dados]:
    dados_confirmados.append(dados_diarios[confirmados])
    dados_recuperados.append(dados_diarios[recuperados])
lista_de_dados_final = [dados_confirmados, dados_recuperados]
etiquetas_y = ['Confirmados', 'Recuperados']


# 2o. - chamandos as funcoes e exibindo o grafico
grafico = gerar_grafico(etiquetas_x, lista_de_dados_final, etiquetas_y, titulo='Confirmados x Recuperados')
conteudo_do_grafico = requrer_grafico(grafico)
salvar_imagem_grafico('meu-primeiro-grafico.png', conteudo_do_grafico)
mostrar_grafico('meu-primeiro-grafico.png')

# 3o. - criando um qr code do grafico
conteudo_qrcode = requerer_qrcode(f'https://quickchart.io/chart?c={grafico}')
salvar_imagem_grafico('qr_code_meu_primeiro_grafico.png', conteudo_qrcode)
mostrar_grafico('qr_code_meu_primeiro_grafico.png')
