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

DIC_INFO = {'Com séries temporais':{'RI todo início 2003 2006':{'Quantidade de intervalos':10,
                                                                'Incremental':{'Modelo 1':'1-p6Fik36eDbx1ezQs3dkrQop1_Hj-4qP',
                                                                               'Modelo 2':'1wWkdQunoiOKl86UzIpdhpoFF4J9gbsxd',
                                                                               'Modelo 3':'1MOxnajuVYYRPOgK90bTX6ZwcKbe7f6gi',
                                                                               'Modelo 4':'1NBl-sCj5CQuG90zAGGYjcaJfRT8gJceq'},
                                                                'Temporal':{'Modelo 1':'1domJgAtj-dNbIfUfi81Fimj8T9Zpc-RD'}},
                                    'HST-03-10':{'Quantidade de intervalos':5,
                                                 'Incremental':{'Modelo 1':'1yRnVZJ-n6yl2gxSGGVpa5MmAj7SKMu_Q',
                                                                'Modelo 2':'1Q_JiD7vga-wziqQ4hIbqJeqUKB54h2aL',
                                                                'Modelo 3':'1mNRbPDGUVEZRFRDxQhZYJyHWxYlYCEW2',
                                                                'Modelo 4':'1nMoqj4o3caJBW76e6Ldh-IDjULsqvWrR'},
                                                 'Temporal':{'Modelo 1':'1q3hKduwksarMpgPMp6KXzQ9R34Cc6-DU',
                                                             'Modelo 2':'1ZtzFwMFAfDw7sBkorU4LooxTS2GsHEkY',
                                                             'Modelo 3':'1h9qQd4n3Ky9G-i_P6-CYNUWUTDFCX94Y',
                                                             'Modelo 4':'1tRTMTF4INu3sD1mUoAOt7hHFvC869wlD'}},
                                    'CFH-03-10':{'Quantidade de intervalos':5,
                                                 'Incremental':{'Modelo 1':'1E_Nif-V1msn_AocFPUC4HJGgwd0PUuI3',
                                                                'Modelo 2':'1RjXLPyq5jVnkQu33-CHa6qz3oTSA8-pu',
                                                                'Modelo 3':'1jCMGOK4tTHawZA6cWo0EJw1rsjWfy1mZ'},
                                                 'Temporal':{'Modelo 1':'10ndoZXudtCpgkc8-HKAF8O2xLNcIX09R',
                                                             'Modelo 2':'1ltkkII36Jwadgp2BR_cLyMXhqe7XLDGv',
                                                             'Modelo 3':'1jhLe-J01zPy5S8-hKx_oGyhoOrkQH6wz'}},
                                    'Saude-Corpo-03-10':{'Quantidade de intervalos':5,
                                                         'Incremental':{'Modelo 1':'1tEXGtfdABndYxbgXQ-x5wwZczTCfgpMx',
                                                                        'Modelo 2':'1aopWw81GVsEUe6_jXTmxvpe83ZqYA1yq',
                                                                        'Modelo 3':'1E1220ZYfc7MiVbmNUnE7U4hNDESUFgiP'},
                                                         'Temporal':{'Modelo 1':'12VY5FqkMrPkTxEfMjuLEPfRQ_PioTv-p',
                                                                     'Modelo 2':'1ZjolluRy-nw33sYqzrPQrK2ZRCWE-op0',
                                                                     'Modelo 3':'1GTXirosiGq7A0cYMXAZtU6u7pZD-JsAj'}}}}


lista_de_acoes_com_series_temporais = ['Gráfico das similaridades ao decorrer do tempo',
                                       'Vizinhos mais próximos ao decorrer do tempo (.png e .txt)',
                                       'Rede dinâmica dos campos semânticos ao decorrer do tempo',
                                       'Mapa de calor das similaridades ao decorrer do tempo',
                                       'Estratos do Tempo',
                                       'Vetores de Palavras',
                                       'Comparação entre Palavras',
                                       'Elemento que não combina dentre os demais (só .txt)',
                                       'Frequência de Palavras ao decorrer do tempo',
                                       'Mudança de Palavras ao decorrer do tempo']


def limparConsole():
    if GOOGLE_COLAB:
        output.clear()        
    elif OS_ATUAL.lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def formatarEntrada(entrada : str) -> str:
  return entrada.strip().lower()

def descompactarPastaModelos(caminho_pasta_modelo : str, excluir_zip : bool = True):
    lista_arquivos_zipados = [os.path.join(caminho_pasta_modelo,arq) for arq in os.listdir(caminho_pasta_modelo) if arq.endswith('.zip')]
    qtd_zips = len(lista_arquivos_zipados)
    if qtd_zips > 0:
        print('Descompactando arquivos! Por favor, aguarde alguns instântes!')
        for i,arquivo in enumerate(lista_arquivos_zipados):
            print(f'Descompactando {i+1} de {qtd_zips}')
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(caminho_pasta_modelo)
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
                    while not r.isdigit() or r not in range(qtd_respostas):
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
    print('\n0 - Encerrar programa')
    
    resposta = input('\nDigite o número correspondente: ').strip()

    if resposta not in ['-1','0']:
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
        
        pasta_tipo_treinamento_escolhida = lista_pastas_tipos_treinamentos[resposta]
        
        caminho_pasta_tipo_treinamento_escolhida = os.path.join(CAMINHO_GERAL,pasta_tipo_treinamento_escolhida)
        return caminho_pasta_tipo_treinamento_escolhida
    else:
        return resposta

def escolherTreinamento(pasta_tipo_treinamento : str):

    lista_pastas_treinamentos = [p for p in os.listdir(pasta_tipo_treinamento) if '.' not in p]
    qtd_pastas = len(lista_pastas_treinamentos)

    print('Escolha a pasta de treinamento:\n')
    for i,pasta in enumerate(lista_pastas_treinamentos):
        print(f'{i+1} - {pasta}')
    print('\n-1 - Voltar')

    resposta = formatarEntrada(input('\nDigite o número correspondente: '))

    while not resposta.isdigit():
        resposta = formatarEntrada(input('\nPor favor, digite o NÚMERO correspondente: '))
    # while resposta not in [str(n) for n in range(1,qtd_pastas+1)]:
    #    resposta = input('\nDigite o número correspondente (entre as opções a cima): ')
    if resposta not in ['-1']:
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)

        pasta_treinamento_escolhida = lista_pastas_treinamentos[resposta]
        
        caminho_pasta_treinamento_escolhida = os.path.join(pasta_tipo_treinamento,pasta_treinamento_escolhida)
        return caminho_pasta_treinamento_escolhida
    else:
        return resposta

def escolherModoTreinado(caminho_pasta_treino : str):
    lista_pastas_modos_treinados = [t for t in os.listdir(caminho_pasta_treino) if '.' not in t]
    qtd_pastas = len(lista_pastas_modos_treinados)

    print('Escolha o modo treinado:\n')
    for i,pasta in enumerate(lista_pastas_modos_treinados):
        print(f'{i+1} - {pasta}')
    print('\n-1 - Voltar')

    resposta = input('\nDigite o número correspondente: ').strip()

    if resposta not in ['-1']:
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
        
        pasta_tipo_treinamento_escolhida = lista_pastas_modos_treinados[resposta]
        
        caminho_pasta_tipo_treinamento_escolhida = os.path.join(caminho_pasta_treino,pasta_tipo_treinamento_escolhida)
        return caminho_pasta_tipo_treinamento_escolhida
    else:
        return resposta

def baixarModelos(tipo_treino : str,
                  escopo_treino : str,
                  modo_treinado : str,
                  nome_modelo: str,
                  pasta_destino : str):

    try:
        file_id = DIC_INFO[tipo_treino][escopo_treino][modo_treinado][nome_modelo]
    except Exception:
        return False
    else:
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        output = os.path.join(pasta_destino, f'{nome_modelo}.zip')
        gdown.download(url, output, quiet=False)

def escolherModelos(caminho_pasta_modo_treino : str):
    lista_pastas_modelos = sorted([m for m in os.listdir(caminho_pasta_modo_treino) if '.' not in m])
    qtd_pastas = len(lista_pastas_modelos)

    print('Escolha a pasta do modelo:\n')
    for i,pasta in enumerate(lista_pastas_modelos):
        print(f'{i+1} - {pasta}')
    print('\n-1 - Voltar')

    resposta = input('\nDigite o número correspondente: ').strip()

    if resposta not in ['-1']:
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
        # while resposta not in [str(n) for n in range(1,qtd_pastas+1)]:
        #    resposta = input('\nDigite o número correspondente (entre as opções a cima): ')

        pasta_modelo_escolhido = lista_pastas_modelos[resposta]

        caminho_pasta_modelo_escolhido = os.path.join(caminho_pasta_modo_treino,pasta_modelo_escolhido)

        limparConsole()

        tipo_treino = os.path.basename(os.path.dirname(os.path.dirname(caminho_pasta_modo_treino)))
        escopo_treino = os.path.basename(os.path.dirname(caminho_pasta_modo_treino))
        modo_treinado = os.path.basename(caminho_pasta_modo_treino)
        nome_modelo = os.path.basename(caminho_pasta_modelo_escolhido)
        
        if len([modelo for modelo in os.listdir(caminho_pasta_modelo_escolhido) if modelo.endswith('.wordvectors')]) != DIC_INFO[tipo_treino][escopo_treino]['Quantidade de intervalos']:
            print('Parece que a pasta do modelo escolhido está vazia ou incompleta, vamos fazer o download adequadamente de todos os nossos arquivos para este modelo!')

            for arquivo in [os.path.join(caminho_pasta_modelo_escolhido,arq) for arq in os.listdir(caminho_pasta_modelo_escolhido)]:
                os.remove(arquivo)

            print('\n\n\t Estamos baixando os arquivos referentes ao modelo escolhido!\n\n\t--> Por favor, aguarde...\n\n')

            baixarModelos(tipo_treino=tipo_treino,
                          escopo_treino=escopo_treino,
                          modo_treinado=modo_treinado,
                          nome_modelo=nome_modelo,
                          pasta_destino=caminho_pasta_modelo_escolhido)

        return caminho_pasta_modelo_escolhido
    else:
        return resposta

def escolherModelosTemporais(caminho_pasta_modelo : str):
    lista_modelos_temporais = sorted([m for m in os.listdir(caminho_pasta_modelo) if m.endswith('.wordvectors')])
    qtd_modelos = len(lista_modelos_temporais)

    print('Escolha os modelos temporais que serão utilizados:\n')
    for i,pasta in enumerate(lista_modelos_temporais):
        print(f'{i+1} - {pasta}')
    print(f'{qtd_modelos+1} - Todos')
    print('\n-1 - Voltar')    

    resposta = input('\nDigite os números correspondentes separados por "," (vírgula)\nou o número correspondente a todos:\n').strip()
    if resposta not in ['-1']:
        if ',' in resposta:
            while len([r for r in resposta.split(',') if not r.isdigit()])>0:
                resposta = input('Por favor, digite uma resposta válida: ')
        if resposta == str(qtd_modelos+1):
            respostas = [i for i in range(qtd_modelos)]
        else:
            respostas = obterResposta(resposta=resposta,qtd_respostas=qtd_modelos)
        

        # while resposta not in [str(n) for n in range(1,qtd_pastas+1)]:
        #    resposta = input('\nDigite o número correspondente (entre as opções a cima): ')
        
        caminho_modelos_escolhidos = []
        if isinstance(respostas,int):
            respostas = [respostas]
        
        for index in sorted(respostas):
            caminho_modelos_escolhidos.append(os.path.join(caminho_pasta_modelo,lista_modelos_temporais[index]))

        return caminho_modelos_escolhidos
    else:
        return resposta

def carregarModelos(lista_caminhos_modelos_temporais : list[str]):
    modelos_carregados = []
    for caminho_modelo in lista_caminhos_modelos_temporais:
        modelos_carregados.append((os.path.basename(caminho_modelo).replace('.wordvectors',''),KeyedVectors.load(caminho_modelo,mmap='r')))
    return modelos_carregados

def escolherAcao(tipo_treinamento):
    print('Escolha uma das visualizações abaixo:\n\n')
    if tipo_treinamento == 'Com séries temporais':
        for i,acao in enumerate(lista_de_acoes_com_series_temporais):
            print(f'{i+1} - {acao}')
        print('\n-1 - Voltar')
        print('0 - Finalizar programa')

    resposta = input('\nDigite o número referente à sua escolha: ').strip()
    if resposta not in ['-1','0']:    
        index_acao = obterResposta(resposta=resposta,qtd_respostas=len(lista_de_acoes_com_series_temporais))
        return lista_de_acoes_com_series_temporais[index_acao]
    else:
        return resposta
            
def organizarAmbiente():
    global DIC_INFO

    if not os.path.exists(r'resultados_gerados'):
        os.makedirs(r'resultados_gerados')

    if not os.path.exists(r'modelos_treinados'):
        os.makedirs(r'modelos_treinados')

    # print('Pastas de tipo de treinamento',[p for p in DIC_INFO.keys() if isinstance(p,str)])
    for pasta_tipo_treinamento in [p for p in DIC_INFO.keys() if isinstance(p,str)]:        
        if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento)):
            os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento))
        # print('Pastas de treinamento',[p for p in DIC_INFO[pasta_tipo_treinamento].keys() if isinstance(p,str)])
        for pasta_treinamento in [p for p in DIC_INFO[pasta_tipo_treinamento].keys() if isinstance(p,str)]:            
            if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento)):
                os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento))
            # print('Pastas modo de treinamento',[p for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento].keys() if not isinstance(DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][p],int)])
            # print(DIC_INFO[pasta_tipo_treinamento][pasta_treinamento].keys())
            # for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento].keys():
                # print(DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][p],type(DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][p]))            
            for pasta_modo_treinamento in [p for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento].keys() if not isinstance(DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][p],int)]:
                if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento)):
                    os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento))
                # print('Pastas modelo',[p for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][pasta_modo_treinamento].keys() if isinstance(p,str)])
                for pasta_modelo in [p for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][pasta_modo_treinamento].keys() if isinstance(p,str)]:                    
                    if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento,pasta_modelo)):
                        os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento,pasta_modelo))

