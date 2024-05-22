import zipfile
import os
import platform
from gensim.models import KeyedVectors
import gdown

try:
    from google.colab import output
except Exception:
    GOOGLE_COLAB = False
    pass
else:
    GOOGLE_COLAB = True

CAMINHO_GERAL = r'modelos_treinados'
OS_ATUAL = platform.system()

DIC_INFO = {'RI_todo_2003_2006':{'quantidade_de_intervalos':10,
                                'modelos':{'Modelo_1':'1mibDVSGMQMvmhkQYs95SX1QrYtu_dGuW',
                                           'Modelo_2':'1QtiaU5rWTkLTwGUDRgHN4m1kC5d-c4UB',
                                           'Modelo_3':'1UYrnDwemzjmGKApe1ssYJkvXvyF7aW9s'}}}


def limparConsole():
    if GOOGLE_COLAB:
        output.clear()        
    elif OS_ATUAL.lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def descompactarPastaModelos(campinho_pasta_modelo : str, excluir_zip : bool = True):
    lista_arquivos_zipados = [os.path.join(campinho_pasta_modelo,arq) for arq in os.listdir(campinho_pasta_modelo) if arq.endswith('.zip')]
    qtd_zips = len(lista_arquivos_zipados)
    if qtd_zips > 0:
        print('Hmmm... Parece que temos arquivos compactados.\nEstamos descompactando, aguarde alguns instântes!')
        for i,arquivo in enumerate(lista_arquivos_zipados):
            print(f'Descompactando {i+1} de {qtd_zips}')
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(campinho_pasta_modelo)
            if excluir_zip:
                os.remove(arquivo)

def obterResposta(resposta : str,
                  qtd_respostas : int,
                  contagem_normal : bool = False) -> int | list[int]:
    if ',' in resposta:
        respostas = []
        for r in [valor.strip() for valor in resposta.split(',')]:
            if not r.isdigit():
                print(f'--> Você digitou "{r}", mas esperamos um número...')
                r = input('--> Por favor, nos forneça o número correto (0 para excluir): ')
                while not r.isdigit():
                    r = input('\nDigite um NÚMERO válido: ')
            r = int(r) - 1
            if r >= 0:
                while r not in range(qtd_respostas):
                    print('Você digitou',r+1)
                    r = input('\nPor favor, digite um número entre as opções listadas (0 para excluir): ')
                    while not r.isdigit():
                        r = input('\nPor favor, digite um NÚMERO válido: ')
                    r = int(r) - 1
                    if r < 0:
                        break
                if r >= 0:
                    respostas.append(r)
        if contagem_normal:
            respostas = [r+1 for r in respostas]
        return respostas
    else:
        while not resposta.isdigit():
            resposta = input('\nDigite um NÚMERO correspondente: ')
        resposta = int(resposta) - 1
        while resposta not in range(qtd_respostas):
            resposta = input('\nDigite um número entre as opções listadas: ')
            while not resposta.isdigit():
                resposta = input('\nDigite um NÚMERO válido: ')
            resposta = int(resposta) - 1
        if contagem_normal:
            resposta += 1
        return resposta

def escolherTipoTreinamento():
    lista_pastas_tipos_treinamentos = [t for t in os.listdir(CAMINHO_GERAL) if '.' not in t]
    qtd_pastas = len(lista_pastas_tipos_treinamentos)

    print('Escolha o tipo de treinamento:\n')
    for i,pasta in enumerate(lista_pastas_tipos_treinamentos):
        print(f'{i+1} - {pasta}')
    
    resposta = input('\nDigite o número correspondente: ').strip()

    resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
    
    pasta_tipo_treinamento_escolhida = lista_pastas_tipos_treinamentos[resposta]
    
    caminho_pasta_tipo_treinamento_escolhida = os.path.join(CAMINHO_GERAL,pasta_tipo_treinamento_escolhida)
    return caminho_pasta_tipo_treinamento_escolhida

def escolherTreinamento(pasta_tipo_treinamento : str):

    lista_pastas_treinamentos = [p for p in os.listdir(pasta_tipo_treinamento) if '.' not in p]
    qtd_pastas = len(lista_pastas_treinamentos)

    print('Escolha a pasta de treinamento:\n')
    for i,pasta in enumerate(lista_pastas_treinamentos):
        print(f'{i+1} - {pasta}')
    
    resposta = input('\nDigite o número correspondente: ').strip()

    # while resposta not in [str(n) for n in range(1,qtd_pastas+1)]:
    #    resposta = input('\nDigite o número correspondente (entre as opções a cima): ')
    resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
    
    pasta_treinamento_escolhida = lista_pastas_treinamentos[resposta]
    
    caminho_pasta_treinamento_escolhida = os.path.join(pasta_tipo_treinamento,pasta_treinamento_escolhida)
    return caminho_pasta_treinamento_escolhida


def baixarModelos(escopo_treino : str,
                  nome_modelo: str,
                  pasta_destino : str):

    try:
        file_id = DIC_INFO[escopo_treino]['modelos'][nome_modelo]
    except Exception:
        return False
    else:
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        output = os.path.join(pasta_destino, f'{nome_modelo}.zip')
        gdown.download(url, output, quiet=False)



def escolherModelos(caminho_pasta_treino : str):
    lista_pastas_modelos = [m for m in os.listdir(caminho_pasta_treino) if '.' not in m]
    qtd_pastas = len(lista_pastas_modelos)

    print('Escolha a pasta do modelo:\n')
    for i,pasta in enumerate(lista_pastas_modelos):
        print(f'{i+1} - {pasta}')
    
    resposta = input('\nDigite o número correspondente: ').strip()
    resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
    # while resposta not in [str(n) for n in range(1,qtd_pastas+1)]:
    #    resposta = input('\nDigite o número correspondente (entre as opções a cima): ')

    pasta_modelo_escolhido = lista_pastas_modelos[resposta]

    caminho_pasta_modelo_escolhido = os.path.join(caminho_pasta_treino,pasta_modelo_escolhido)

    limparConsole()

    escopo_treino = os.path.basename(caminho_pasta_treino)
    nome_modelo = os.path.basename(caminho_pasta_modelo_escolhido)

    if len([modelo for modelo in os.listdir(caminho_pasta_modelo_escolhido) if modelo.endswith('.wordvectors')]) != DIC_INFO[escopo_treino]['quantidade_de_intervalos']:
        print('Parece que a pasta do modelo escolhido está vazia ou incompleta, vamos fazer o donwload adequadamente de todos os nossos arquivos para este modelo!')

        for arquivo in [os.path.join(caminho_pasta_modelo_escolhido,arq) for arq in os.listdir(caminho_pasta_modelo_escolhido)]:
            os.remove(arquivo)

        print('\n\n\t Estamos baixando os arquivos referentes ao modelo escolhido!\n\n\t--> Por favor, aguarde...\n\n')

        baixarModelos(escopo_treino=escopo_treino,
                        nome_modelo=nome_modelo,
                        pasta_destino=caminho_pasta_modelo_escolhido)

    return caminho_pasta_modelo_escolhido

def escolherModelosTemporais(caminho_pasta_modelo : str):
    lista_modelos_temporais = [m for m in os.listdir(caminho_pasta_modelo) if m.endswith('.wordvectors')]
    qtd_modelos = len(lista_modelos_temporais)

    print('Escolha os modelos temporais que serão utilizados:\n')
    for i,pasta in enumerate(lista_modelos_temporais):
        print(f'{i+1} - {pasta}')
    print(f'{qtd_modelos+1} - Todos')
    resposta = input('\nDigite os números correspondentes separados por "," (vírgula)\nou o número correspondente a todos:\n').strip()
    if resposta == str(qtd_modelos+1):
        respostas = [i for i in range(qtd_modelos)]
    else:
        respostas = obterResposta(resposta=resposta,qtd_respostas=qtd_modelos)
    # while resposta not in [str(n) for n in range(1,qtd_pastas+1)]:
    #    resposta = input('\nDigite o número correspondente (entre as opções a cima): ')

    caminho_modelos_escolhidos = []
    for index in sorted(respostas):
        caminho_modelos_escolhidos.append(os.path.join(caminho_pasta_modelo,lista_modelos_temporais[index]))

    return caminho_modelos_escolhidos

def carregarModelos(lista_caminhos_modelos_temporais : list[str]):
    modelos_carregados = []
    for caminho_modelo in lista_caminhos_modelos_temporais:
        modelos_carregados.append((os.path.basename(caminho_modelo).replace('.wordvectors',''),KeyedVectors.load(caminho_modelo,mmap='r')))
    return modelos_carregados

lista_de_acoes_com_series_temporais = ['Gráfico das similaridades ao decorrer do tempo',
                                       'Vizinhos mais próximos ao decorrer do tempo',
                                       'Mapa de calor das similaridades ao decorrer do tempo',
                                       'Frequência de Palavras ao decorrer do tempo']

def escolherAcao(tipo_treinamento):
    print('Escolha uma das visualizações abaixo:\n\n')
    if tipo_treinamento == 'com_series_temporais':
        for i,acao in enumerate(lista_de_acoes_com_series_temporais):
            print(f'{i+1} - {acao}')

    resposta = input('\nDigite o número referente à sua escolha: ').strip()
    if resposta != '0':
        index_acao = obterResposta(resposta=resposta,qtd_respostas=len(lista_de_acoes_com_series_temporais))    
        return lista_de_acoes_com_series_temporais[index_acao]
    else:
        return 'Sair'
            

def organizarAmbiente():
    if not os.path.exists(r'imagens_geradas'):
        os.makedirs(r'imagens_geradas')
    if not os.path.exists(r'modelos_treinados'):
        os.makedirs(r'modelos_treinados')
    if not os.path.exists(os.path.join('modelos_treinados','com_series_temporais')):
        os.makedirs(os.path.join('modelos_treinados','com_series_temporais'))
    if not os.path.exists(os.path.join('modelos_treinados','sem_series_temporais')):
        os.makedirs(os.path.join('modelos_treinados','sem_series_temporais'))
    if not os.path.exists(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006')):
        os.makedirs(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006'))
    if not os.path.exists(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006','Modelo_1')):
        os.makedirs(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006','Modelo_1'))
    if not os.path.exists(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006','Modelo_2')):
        os.makedirs(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006','Modelo_2'))
    if not os.path.exists(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006','Modelo_3')):
        os.makedirs(os.path.join('modelos_treinados','com_series_temporais','RI_todo_2003_2006','Modelo_3'))
