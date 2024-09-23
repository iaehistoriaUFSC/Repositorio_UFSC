# Importação dos módeulos/pacotes/bibliotecas que serão utilizadas nas execuções dos processos
import zipfile
import os, shutil
import platform
import time
from gensim.models import KeyedVectors
import gdown
import msgpack

# Verificação se o ambiente que está executando é o Google Colab ou não (execução local)
try:
    from google.colab import output
except Exception:
    GOOGLE_COLAB = False
    pass
else:
    GOOGLE_COLAB = True

# Definição do caminho geral que será armazenado os modelos
CAMINHO_GERAL = r'modelos_treinados'
# Definição do caminho atual como o caminho que está atualmente executando os códigos
OS_ATUAL = platform.system()

# Dicionário que armazena as informações referentes aos nossos modelos treinados
# Quantidade de intervalos = quantidade de séries temporais nos modelos daquele corpus
# O código ao lado do "Modelo X" é o id encontrado no link de compartilhamento de arquivos no Google Drive.
# Exemplo: 
# Link de compartilhamento: https://drive.google.com/file/d/1-p6Fik36eDbx1ezQs3dkrQop1_Hj-4qP/view?usp=drive_link
# Busca-se o código entre o "/d/" e o "/view?", no meio do URL, ou seja, "1-p6Fik36eDbx1ezQs3dkrQop1_Hj-4qP".
DIC_INFO = {'Com séries temporais':{'UFSC 2003-2006':{'Quantidade de intervalos':10,
                                                                'Incremental':{'Modelo 1':'1-p6Fik36eDbx1ezQs3dkrQop1_Hj-4qP',
                                                                               'Modelo 2':'1wWkdQunoiOKl86UzIpdhpoFF4J9gbsxd',
                                                                               'Modelo 3':'1MOxnajuVYYRPOgK90bTX6ZwcKbe7f6gi',
                                                                               'Modelo 4':'1NBl-sCj5CQuG90zAGGYjcaJfRT8gJceq'},
                                                                'Temporal':{'Modelo 1':'1domJgAtj-dNbIfUfi81Fimj8T9Zpc-RD',
                                                                            'Modelo 2':'1xqGq9qUduFEkLn5lw_16Q4NpGcGdz22D',
                                                                            'Modelo 3':'1O-umkGjVr5Bh5y-llNviPec73ZOuNHJM',
                                                                            'Modelo 4':'1lQhwky-z3n2zcx6Neew8vvQXJ6ObM0Co'}},
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

# Lista contendo todas as ações para gerar visualizações que temos atualmente
lista_de_acoes_com_series_temporais = ['Gráfico das similaridades ao decorrer do tempo',
                                       'Vizinhos mais próximos ao decorrer do tempo (.png e .txt)',
                                       'Rede dinâmica dos campos semânticos ao decorrer do tempo',
                                       'Mapa de calor das similaridades ao decorrer do tempo',
                                       'Estratos do Tempo',
                                       'Vetores de Palavras',
                                       'Comparação entre Palavras',
                                       'Elemento que não combina dentre os demais',
                                       'Frequência de Palavras ao decorrer do tempo',
                                       'Mudança de Palavras ao decorrer do tempo']

# Dicionário que armazena as informações referentes ao arquivo de frequências contabilizadas diretamente pelo corpus
DIC_INFO_CORPUS = {'frequencias':'1ledVOj02RB9KsV7hDQmkpmkheC3m7dt9'}

def limparConsole():
    """
    Função responsável por limpar a tela de output/console.
    """
    if GOOGLE_COLAB: # Se estivermos executando no Colab, melhor utilizar a função própria para limpar o output neste ambiente
        output.clear()        
    elif OS_ATUAL.lower() == 'windows': # Se for Windows
        os.system('cls')
    else:   # Se for MAC/Linux
        os.system('clear')

def formatarEntrada(entrada : str) -> str:
  """
  Função responsável por formatar a entrada digitada pelo usuário,
  removendo espaços em branco nos extremos e deixando tudo em minúscula.

  ### Parâmetros:
  - entrada: String contendo o conteúdo capturado pela função "input()",
  que coleta uma entrada digitada pelo usuário.
  
  ### Retornos:
  - String digitada pelo usuário formatada.
  """
  return entrada.strip().lower()

def descompactarPasta(caminho_pasta : str, excluir_zip : bool = True):
    """
    Função responsável por executar a descompactação de uma pasta "zipada" (.zip).

    ### Parâmetros:
    - caminho_pasta: String contendo o caminho até a pasta que será descompactada.
    - excluir_zip: Bool que escolherá se a pasta zipada deve ser excluída (True) ou 
    não (False) após o processo de descompactação.

    ### Retornos:
    - None: Esta função não tem retornos.
    """
    lista_arquivos_zipados = [os.path.join(caminho_pasta,arq) for arq in os.listdir(caminho_pasta) if arq.endswith('.zip')]
    qtd_zips = len(lista_arquivos_zipados)
    if qtd_zips > 0:
        print('Descompactando arquivos! Por favor, aguarde alguns instântes!')
        for i,arquivo in enumerate(lista_arquivos_zipados):
            print(f'Descompactando {i+1} de {qtd_zips}')
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(caminho_pasta)
            if excluir_zip:                
                os.remove(arquivo)

def obterResposta(resposta : str,
                  qtd_respostas : int,
                  contagem_normal : bool = False) -> int | list[int]:
    """
    Função responsável por obter a resposta esperada pelo usuário com base no cenário
    que o programa se encontra.

    ### Parâmetros:
    - resposta: String contendo a resposta digitada pelo usuário numa determinada etapa do programa.
    - qtd_respostas: Inteiro referente ao valor total de respostas plausíveis (número máximo).
    - contagem_normal: Bool que escolherá se o retorno dessa função será com as respostas com 
    seus números reais ou na "contagem da programação" onde a primeira posição, ao invés de ser o 
    número 1, é o número 0 e assim por diante.

    ### Retornos:
    - Inteiro ou lista de inteiros referente à resposta digitada pelo usuário.
    """
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

def escolherTipoTreinamento() -> str:
    """
    Função responsável por atuar na etapa de escolha do tipo de treinamento.
    Atualmente tem-se somente o tipo de treinamento "Com séries temporais", mas,
    futuramente pode-se desenvolver um tipo de treinamento voltado apenas para 
    modelos "sincrônicos", como por exemplo, UFSC 2003-2024, HST 2003-2024, etc.

    ### Retornos:
    - String contendo o caminho até a pasta de tipo de treino selecionada ou 
    contendo o número -1 ou 0 caso o usuário queira voltar ou encerrar o programa.
    """
    # Obtenção das pastas de tipos de treinamentos disponíveis
    lista_pastas_tipos_treinamentos = [t for t in os.listdir(CAMINHO_GERAL) if '.' not in t]
    qtd_pastas = len(lista_pastas_tipos_treinamentos)

    # Interação com usuário:
    print('Escolha o tipo de treinamento:\n')
    for i,pasta in enumerate(lista_pastas_tipos_treinamentos):
        print(f'{i+1} - {pasta}')
    print('\n0 - Encerrar programa')
    
    # Formatação básica da resposta
    resposta = formatarEntrada(input('\nDigite o número correspondente: '))

    if resposta not in ['-1','0']:
        # Tratamento da resposta
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)
        
        pasta_tipo_treinamento_escolhida = lista_pastas_tipos_treinamentos[resposta]
        
        caminho_pasta_tipo_treinamento_escolhida = os.path.join(CAMINHO_GERAL,pasta_tipo_treinamento_escolhida)
        return caminho_pasta_tipo_treinamento_escolhida
    else:
        return resposta

def escolherTreinamento(pasta_tipo_treinamento : str) -> str:
    """
    Função responsável por atuar na etapa de escolha do treinamento que será 
    utilizado. Esta etapa é voltada para escolher, basicamente, o corpus 
    de textos utilizado para treinar os modelos. Atualmente, temos CFH, HST, 
    SAUDE-CORPO, UFSC (todas as coleções).

    ### Parâmetros:
    - pasta_tipo_treinamento: String contendo o caminho até a pasta do tipo 
    de treino selecionado.

    ### Retornos:
    - String contendo o caminho até a pasta de treino selecionada ou contendo 
    o número -1 ou 0 caso o usuário queira voltar ou encerrar o programa.
    """
    # Obtenção das pastas de (corpus) treinamentos disponíveis
    lista_pastas_treinamentos = [p for p in os.listdir(pasta_tipo_treinamento) if '.' not in p]
    qtd_pastas = len(lista_pastas_treinamentos)

    # Interação com usuário:
    print('Escolha a pasta de treinamento:\n')
    for i,pasta in enumerate(lista_pastas_treinamentos):
        print(f'{i+1} - {pasta}')
    print('\n-1 - Voltar')
    
    # Formatação básica da resposta
    resposta = formatarEntrada(input('\nDigite o número correspondente: '))

    while not resposta.isdigit():
        resposta = formatarEntrada(input('\nPor favor, digite o NÚMERO correspondente: '))
    if resposta not in ['-1']:
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)

        pasta_treinamento_escolhida = lista_pastas_treinamentos[resposta]
        
        caminho_pasta_treinamento_escolhida = os.path.join(pasta_tipo_treinamento,pasta_treinamento_escolhida)
        return caminho_pasta_treinamento_escolhida
    else:
        return resposta

def escolherModoTreinado(caminho_pasta_treino : str) -> str:
    """
    Função responsável por atuar na etapa de escolha do modo de treinamento 
    utilizado para geração das séries temporais (Incremental ou Temporal).

    ### Parâmetros
    - caminho_pasta_treino: String contendo o caminho até a pasta de treino selecionada.

    ### Retornos:
    - String contendo o caminho até a pasta do modo de construção das séries
    temporais para o treino selecionado ou contendo o número -1 caso o usuário queira
    voltar uma etapa.
    """
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
                  pasta_destino : str) -> None:
    """
    Função responsável por baixar os modelos das séries temporais para o corpus 
    escolhido. Essa função usará o dicionário DIC_INFO para buscar o id do 
    arquivo zip que contém os modelos zipados no Google Drive e realizar o donwload
    deste arquivo para este ambiente de execução.

    ### Parâmetros:
    - tipo_treino: String contendo o tipo de treinamento escolhido.
    - escopo_treino: String contendo o corpus que foi selecionado.
    - modo_treinado: String contendo o modo escolhido para construção das séries
    temporais do treinamento selecionado.
    - nome_modelo: String contendo o nome central dos modelos da série temporal 
    (relacionado ao corpus utilizado).
    - pasta_destino: String contendo o caminho até a pasta que os modelos serão 
    "depositados".

    ### Retornos:
    - None: Esta função não possui retornos.    
    """
    try:
        # Extração do ID do arquivo no Drive
        file_id = DIC_INFO[tipo_treino][escopo_treino][modo_treinado][nome_modelo]
    except Exception:
        return False
    else:
        # Criação da pasta de destino, caso esta não exista ainda
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        # URL no formato que o gdown utiliza para baixar arquivos do Google Drive por meio do ID
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        # Caminho onde deverá ser baixado o arquivo neste ambiente de execução
        output = os.path.join(pasta_destino, f'{nome_modelo}.zip')
        # Execução do processo de baixar o arquivo do Drive e trazê-lo para este ambiente de execução
        gdown.download(url, output, quiet=False)

def escolherModelos(caminho_pasta_modo_treino : str) -> str:
    """
    Função responsável por escolher qual dos modelos que melhor performaram nas analogias (por meio do modelo 
    base) relacionados ao corpus e modo selecionados. Geralmente foi escolhido os TOP3 ou TOP4 modelos que 
    tiveram pontuações mais altas nas analogias gerais.

    ### Parâmetros:
    - caminho_pasta_modo_treino: String contendo o caminho até os modelos que se saíram melhor para o corpus
    selecionado.

    ### Retorno:
    - String contendo o caminho até o modelo selecionado, com base no corpus e modos selecionados anteriormente 
    ou o número -1 caso o usuário queira voltar uma etapa.
    """
    lista_pastas_modelos = sorted([m for m in os.listdir(caminho_pasta_modo_treino) if '.' not in m])
    qtd_pastas = len(lista_pastas_modelos)

    print('Escolha a pasta do modelo:\n')
    for i,pasta in enumerate(lista_pastas_modelos):
        print(f'{i+1} - {pasta}')
    print('\n-1 - Voltar')

    resposta = input('\nDigite o número correspondente: ').strip()

    if resposta not in ['-1']:
        resposta = obterResposta(resposta=resposta,qtd_respostas=qtd_pastas)

        pasta_modelo_escolhido = lista_pastas_modelos[resposta]

        caminho_pasta_modelo_escolhido = os.path.join(caminho_pasta_modo_treino,pasta_modelo_escolhido)

        limparConsole()

        # Extração das informações do tipo de treino, escopo, modo e nome por meio do caminho completo selecionado
        tipo_treino = os.path.basename(os.path.dirname(os.path.dirname(caminho_pasta_modo_treino)))
        escopo_treino = os.path.basename(os.path.dirname(caminho_pasta_modo_treino))
        modo_treinado = os.path.basename(caminho_pasta_modo_treino)
        nome_modelo = os.path.basename(caminho_pasta_modelo_escolhido)
        
        # Se os arquivos dos modelos das séries temporais do modelo/treino escolhido não estiverem todas na pasta requerida
        if len([modelo for modelo in os.listdir(caminho_pasta_modelo_escolhido) if modelo.endswith('.wordvectors')]) != DIC_INFO[tipo_treino][escopo_treino]['Quantidade de intervalos']:
            print('Parece que a pasta do modelo escolhido está vazia ou incompleta, vamos fazer o download adequadamente de todos os nossos arquivos para este modelo!')

            # Limpamos a pasta (caso tenha algum outro arquivo)
            for arquivo in [os.path.join(caminho_pasta_modelo_escolhido,arq) for arq in os.listdir(caminho_pasta_modelo_escolhido)]:
                os.remove(arquivo)

            print('\n\n\t Estamos baixando os arquivos referentes ao modelo escolhido!\n\n\t--> Por favor, aguarde...\n\n')
            # Baixamos todos os arquivos das séries temporais referentes ao modelo escolhido
            baixarModelos(tipo_treino=tipo_treino,
                          escopo_treino=escopo_treino,
                          modo_treinado=modo_treinado,
                          nome_modelo=nome_modelo,
                          pasta_destino=caminho_pasta_modelo_escolhido)

        return caminho_pasta_modelo_escolhido
    else:
        return resposta

def escolherModelosTemporais(caminho_pasta_modelo : str) -> list[str] | str:
    """
    Função responsável por escolher quais modelos das séries temporais baixadas serão, de fato, utilizados
    na geração das visualizações.

    ### Parâmetros:
    - caminho_pasta_modelo: String contendo o caminho até a pasta que armazena os modelos referentes às
    séries temporais da seleção feita pelo usuário.

    ### Retornos:
    - Lista de strings dos caminhos até as séries temporais escolhidas ou uma string contendo o número -1,
    caso o usuário queira voltar uma etapa.
    """
    lista_modelos_temporais = sorted([m for m in os.listdir(caminho_pasta_modelo) if m.endswith('.wordvectors')])
    qtd_modelos = len(lista_modelos_temporais)

    print('Escolha os modelos temporais que serão utilizados:\n')
    for i,pasta in enumerate(lista_modelos_temporais):
        print(f'{i+1} - {pasta.replace(".wordvectors","")}')
    print(f'{qtd_modelos+1} - Todos')
    print('\n-1 - Voltar')    

    resposta = input('\nDigite os números correspondentes separados por "," (vírgula)\nou o número correspondente a todos:\n').strip()
    if resposta not in ['-1']:
        if resposta == str(qtd_modelos+1):
            respostas = [i for i in range(qtd_modelos)]
        else:
            if ',' not in resposta:
                if resposta != str(qtd_modelos+1):
                    print('Parece que você tentou digitar o número equivalente a "Todos"...')
                    time.sleep(2)
                    respostas = [i for i in range(qtd_modelos)]
            else:
                while len([r for r in resposta.split(',') if not r.isdigit()])>0:
                    resposta = input('Por favor, digite uma resposta válida (só números): ')
                while len([r for r in resposta.split(',') if int(r) not in range(1,qtd_modelos+1)])>0 or (len(resposta) == 1 and resposta != str(qtd_modelos+1)):
                    resposta = input(f'Por favor, digite uma resposta válida (os números devem estar entre 1 e {qtd_modelos}): ')
            
                respostas = [int(r)-1 for r in resposta.split(',')]

        caminho_modelos_escolhidos = []
        if isinstance(respostas,int):
            respostas = [respostas]
        
        for index in sorted(respostas):
            caminho_modelos_escolhidos.append(os.path.join(caminho_pasta_modelo,lista_modelos_temporais[index]))

        return caminho_modelos_escolhidos
    else:
        return resposta

def carregarModelos(lista_caminhos_modelos_temporais : list[tuple[str,KeyedVectors]]):
    """
    Função responsável por carregar e armazenar os modelos das séries temporais.

    ### Parâmetros:
    - lista_caminhos_modelos_temporais: Lista de strings contendo os caminhos dos modelos das séries temporais.
    
    ### Retornos:
    - Lista de tuplas onde cada tupla tem dois elementos sendo o primeiro o nome do arquivo do modelo e o segundo
    sendo o objeto KeyedVectors do modelo propriamente dito.
    """
    modelos_carregados = []
    for caminho_modelo in lista_caminhos_modelos_temporais:
        # Adicionamos uma tupla na lista com o nome do modelo (removendo a extensão ".wordvectors") e o seu objeto que carrega, de fato, o modelo (no seu formato KeyedVectors/WorVectors)
        modelos_carregados.append((os.path.basename(caminho_modelo).replace('.wordvectors',''),KeyedVectors.load(caminho_modelo,mmap='r')))
    return modelos_carregados

def escolherAcao(tipo_treinamento : str):
    """
    Função responsável por escolher qual visualização será gerada.

    ### Parâmetros:
    - tipo_treinamento: String contendo o tipo de treino selecionado no início do programa, o qual vai dizer
    quais visualizações estão disponíveis.

    ### Retornos:
    - String contendo a ação selecionada ou número -1 ou 0 caso o usuário queira volta ou encerrar o programa,
    respectivamente.
    """
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

def baixarInfoCorpus(caminho : str = r'info_corpus'):
    """
    Função responsável por realização o download dos arquivos referentes à contabilização de frequências 
    feita diretamente no corpus de textos pré-processados usado para alimentar os treinamentos. Esses arquivos
    estão estruturados da forma que melhor se pensou para realização de armazenamento e busca eficaz das informações
    importantes para este processo de frequências de tokens no corpus.

    ### Parâmetros:
    - caminho: String contendo o caminho da pasta que armazenará os arquivos referentes às informações de
    frequências de tokens no corpus (que estarão separados por pastas de coleções).

    ### Retornos:
    - None: Esta função não tem retornos.
    """
    global DIC_INFO_CORPUS
    try:
        # Extração do ID do arquivo no Drive
        file_id = DIC_INFO_CORPUS['frequencias']
    except Exception:
        return False
    else:
        # Criação da pasta de destino, caso esta não exista ainda
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        # URL no formato que o gdown utiliza para baixar arquivos do Google Drive por meio do ID
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        # Caminho onde deverá ser baixado o arquivo neste ambiente de execução
        output = os.path.join(caminho, f'info_freq_corpus_woke.zip')
        # Execução do processo de baixar o arquivo do Drive e trazê-lo para este ambiente de execução
        gdown.download(url, output, quiet=False)

def abrirArquivoMsgPack(full_filepath : str,
                        encoding_type : str = None):
    """
    Função responsável por abrir os arquivos no formato msgpack.

    ### Parâmetros:
    - full_filepath: String contendo o caminho completo até o arquivo que deseja-se
    abrir e extrair o conteúdo (variável salva).
    - encoding_type: String contendo o tipo de encoding, caso desejar.

    ### Retornos:
    - Variável salva (e agora aberta e lida) no arquivo msgpack.
    """
    if not full_filepath.endswith('.msgpack'):
        full_filepath += '.msgpack'
    if encoding_type:
        with open(full_filepath,'rb',encoding=encoding_type) as f:
            variable_bytes = f.read()
            variable_loaded = msgpack.unpackb(variable_bytes, raw=False)
            f.close()
            return variable_loaded
    else:
        with open(full_filepath,'rb') as f:
            variable_bytes = f.read()
            variable_loaded = msgpack.unpackb(variable_bytes, raw=False)
            f.close()
            return variable_loaded
    

def organizaInfoCorpus(caminho : str = r'info_corpus'):
    """
    Função responsável por organizar o ambiente de pastas/arquivos referentes às informações de frequências
    de tokens realizada diretamente no corpus de textos pré-processados utilizado nos treinamentos.

    ### Parâmetros:
    - caminho: String contendo o caminho da pasta que armazenará os arquivos referentes às informações de
    frequências de tokens no corpus (que estarão separados por pastas de coleções).
    
    ### Retornos:
    - None: Esta função não tem retornos.
    """
    # Obtenção da lista de pastas que estão dentro do diretório fornecido
    pastas = [p for p in os.listdir(caminho) if '.' not in p]
    # Variável que vai armazenar a informação se a configuração das pastas foi feita adequadamente ou não
    config_feita = True
    for colecao in DIC_COLECOES_CORPUS.keys(): # Obtendo os nomes das coleções que estão presentes no diretório e vendo se estão nas chaves do dicionário que armazena as informações sobre o corpus
        if colecao not in pastas:
            config_feita = False    # Caso alguma pasta não seja de uma coleção que temos pré-setada no dicionário
            break
    if config_feita: # Se a configuração das pastas das coleções está correta, agora verifica-se se os arquivos dentro de cada coleção também estão corretos, comparando de acordo com as info presentes dentro do dicionário do corpus
        for colecao in DIC_COLECOES_CORPUS.keys():
            # Obtendo lista de arquivos dentro da coleção via dicionário
            lista_arquivos_dic = DIC_COLECOES_CORPUS[colecao]
            # Obtendo lista de arquivos dentro da coleção via diretório analisado
            lista_arquivos_caminho = [arq for arq in os.listdir(os.path.join(caminho,colecao)) if arq.startswith('dic_frequencias')]
            for arquivo in lista_arquivos_dic:
                if arquivo not in lista_arquivos_caminho:
                    config_feita = False        # Caso algum arquivo no diretório não esteja no dicionário
                    break
            if not config_feita:
                break
    
    # Se a configuração não tiver sido feita adequadamente, vamos limpar a pasta e baixar todos os arquivos/pastas novamente da forma correta.
    if not config_feita:
        print('\n\n\t\tBaixando arquivos para contabilização de frequências diretamente no corpus...\n\n')
        for arquivo in [os.path.join(caminho,arq) for arq in os.listdir(caminho) if os.path.isfile(os.path.join(caminho,arq))]:
            os.remove(arquivo)
        for pasta in [os.path.join(caminho,p) for p in os.listdir(caminho) if os.path.isdir(os.path.join(caminho,p))]:
            shutil.rmtree(pasta)
        baixarInfoCorpus(caminho)
        print('\n\n')
        descompactarPasta(caminho)


def organizarAmbiente():
    """
    Função responsável por organizar o ambiente de execução para comportar as pastas e arquivos esperados 
    para uma execução adequada.
    """
    global DIC_INFO

    if not os.path.exists(r'resultados_gerados'):
        os.makedirs(r'resultados_gerados')

    if not os.path.exists(r'modelos_treinados'):
        os.makedirs(r'modelos_treinados')


    for pasta_tipo_treinamento in [p for p in DIC_INFO.keys() if isinstance(p,str)]:
        if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento)):
            os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento))
        
        for pasta_treinamento in [p for p in DIC_INFO[pasta_tipo_treinamento].keys() if isinstance(p,str)]:
            if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento)):
                os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento))
        
            for pasta_modo_treinamento in [p for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento].keys() if not isinstance(DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][p],int)]:
                if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento)):
                    os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento))
        
                for pasta_modelo in [p for p in DIC_INFO[pasta_tipo_treinamento][pasta_treinamento][pasta_modo_treinamento].keys() if isinstance(p,str)]:                    
                    if not os.path.exists(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento,pasta_modelo)):
                        os.makedirs(os.path.join('modelos_treinados',pasta_tipo_treinamento,pasta_treinamento,pasta_modo_treinamento,pasta_modelo))

    if not os.path.exists(r'info_corpus'):
        os.makedirs(r'info_corpus')
    
    organizaInfoCorpus()

def printarErroInesperado() -> None:
    msg1 = 'Ops! Aconteceu um erto '
    msg_ = ':P'
    msg1_ = 'ro inesperado'
    msg1__ = '...  :/'
    msg2 = 'Por gentileza, informe este cenário para algum programador do Grupo de Estudos e Pesquisa em IA e História da UFSC.'
    msg3 = 'Pedimos perdão pelo ocorrido, vamos trabalhar para futuras correções!'
    msg = ''
    for c in msg1:        
        msg += c
        limparConsole()
        print(msg)
        time.sleep(0.1)
    
    for i in range(1,3):
        msg = msg[:-i]
        limparConsole()        
        print(msg)
        time.sleep(0.2)
    
    msg += '   ' + msg_
    limparConsole()
    print(msg)
    time.sleep(0.2)
    msg = msg[:-len('   ' + msg_)]

    for c in msg1_:        
        msg += c
        limparConsole()
        print(msg)
        time.sleep(0.1)
        
    msg += msg1__
    limparConsole()
    print(msg)
    
    msg_final = msg+ '\n\n'+msg2

    limparConsole()
    print(msg_final)
    time.sleep(2.7)

    msg_final_ = msg_final + '\n\n--> '+msg3 + ' <--\n\n'

    for i in range(4):
        limparConsole()
        print(msg_final)
        time.sleep(0.5)
        limparConsole()
        print(msg_final_)
        time.sleep(0.5)        
    time.sleep(1)

    limparConsole()
    msg_final_ += '-'*100 + '\n\n'
    print(msg_final_)


# Dicionário que armazena as informações a respeito da estrutura esperada nos arquivos relativos à contagem de tokens diretamente no corpus
# É utilizado para fazer a verificação se todos os arquivos estão presentes na pasta requerida
DIC_COLECOES_CORPUS = {'Administracao': ['dic_frequencias_Administracao_2003.msgpack',
  'dic_frequencias_Administracao_2004.msgpack',
  'dic_frequencias_Administracao_2005.msgpack',
  'dic_frequencias_Administracao_2006.msgpack',
  'dic_frequencias_Administracao_2007.msgpack',
  'dic_frequencias_Administracao_2008.msgpack',
  'dic_frequencias_Administracao_2009.msgpack',
  'dic_frequencias_Administracao_2010.msgpack',
  'dic_frequencias_Administracao_2011.msgpack',
  'dic_frequencias_Administracao_2012.msgpack',
  'dic_frequencias_Administracao_2013.msgpack',
  'dic_frequencias_Administracao_2014.msgpack',
  'dic_frequencias_Administracao_2015.msgpack',
  'dic_frequencias_Administracao_2016.msgpack',
  'dic_frequencias_Administracao_2017.msgpack',
  'dic_frequencias_Administracao_2018.msgpack',
  'dic_frequencias_Administracao_2019.msgpack',
  'dic_frequencias_Administracao_2020.msgpack',
  'dic_frequencias_Administracao_2021.msgpack',
  'dic_frequencias_Administracao_2022.msgpack',
  'dic_frequencias_Administracao_2023.msgpack'],
 'Administracao_Universitaria_Mestrado_Profissional': ['dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2012.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Administracao_Universitaria_Mestrado_Profissional_2023.msgpack'],
 'Agroecossistemas': ['dic_frequencias_Agroecossistemas_2003.msgpack',
  'dic_frequencias_Agroecossistemas_2004.msgpack',
  'dic_frequencias_Agroecossistemas_2005.msgpack',
  'dic_frequencias_Agroecossistemas_2006.msgpack',
  'dic_frequencias_Agroecossistemas_2007.msgpack',
  'dic_frequencias_Agroecossistemas_2008.msgpack',
  'dic_frequencias_Agroecossistemas_2009.msgpack',
  'dic_frequencias_Agroecossistemas_2010.msgpack',
  'dic_frequencias_Agroecossistemas_2011.msgpack',
  'dic_frequencias_Agroecossistemas_2012.msgpack',
  'dic_frequencias_Agroecossistemas_2013.msgpack',
  'dic_frequencias_Agroecossistemas_2014.msgpack',
  'dic_frequencias_Agroecossistemas_2015.msgpack',
  'dic_frequencias_Agroecossistemas_2016.msgpack',
  'dic_frequencias_Agroecossistemas_2017.msgpack',
  'dic_frequencias_Agroecossistemas_2018.msgpack',
  'dic_frequencias_Agroecossistemas_2019.msgpack',
  'dic_frequencias_Agroecossistemas_2020.msgpack',
  'dic_frequencias_Agroecossistemas_2021.msgpack',
  'dic_frequencias_Agroecossistemas_2022.msgpack',
  'dic_frequencias_Agroecossistemas_2023.msgpack'],
 'Agroecossistemas_Mestrado_Profissional': ['dic_frequencias_Agroecossistemas_Mestrado_Profissional_2012.msgpack',
  'dic_frequencias_Agroecossistemas_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Agroecossistemas_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Agroecossistemas_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Agroecossistemas_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Agroecossistemas_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Agroecossistemas_Mestrado_Profissional_2018.msgpack'],
 'Antropologia_Social': ['dic_frequencias_Antropologia_Social_2003.msgpack',
  'dic_frequencias_Antropologia_Social_2004.msgpack',
  'dic_frequencias_Antropologia_Social_2005.msgpack',
  'dic_frequencias_Antropologia_Social_2006.msgpack',
  'dic_frequencias_Antropologia_Social_2007.msgpack',
  'dic_frequencias_Antropologia_Social_2008.msgpack',
  'dic_frequencias_Antropologia_Social_2009.msgpack',
  'dic_frequencias_Antropologia_Social_2010.msgpack',
  'dic_frequencias_Antropologia_Social_2011.msgpack',
  'dic_frequencias_Antropologia_Social_2012.msgpack',
  'dic_frequencias_Antropologia_Social_2013.msgpack',
  'dic_frequencias_Antropologia_Social_2014.msgpack',
  'dic_frequencias_Antropologia_Social_2015.msgpack',
  'dic_frequencias_Antropologia_Social_2016.msgpack',
  'dic_frequencias_Antropologia_Social_2017.msgpack',
  'dic_frequencias_Antropologia_Social_2018.msgpack',
  'dic_frequencias_Antropologia_Social_2019.msgpack',
  'dic_frequencias_Antropologia_Social_2020.msgpack',
  'dic_frequencias_Antropologia_Social_2021.msgpack',
  'dic_frequencias_Antropologia_Social_2022.msgpack',
  'dic_frequencias_Antropologia_Social_2023.msgpack'],
 'Aquicultura': ['dic_frequencias_Aquicultura_2003.msgpack',
  'dic_frequencias_Aquicultura_2004.msgpack',
  'dic_frequencias_Aquicultura_2005.msgpack',
  'dic_frequencias_Aquicultura_2006.msgpack',
  'dic_frequencias_Aquicultura_2007.msgpack',
  'dic_frequencias_Aquicultura_2008.msgpack',
  'dic_frequencias_Aquicultura_2009.msgpack',
  'dic_frequencias_Aquicultura_2010.msgpack',
  'dic_frequencias_Aquicultura_2011.msgpack',
  'dic_frequencias_Aquicultura_2012.msgpack',
  'dic_frequencias_Aquicultura_2013.msgpack',
  'dic_frequencias_Aquicultura_2014.msgpack',
  'dic_frequencias_Aquicultura_2015.msgpack',
  'dic_frequencias_Aquicultura_2016.msgpack',
  'dic_frequencias_Aquicultura_2017.msgpack',
  'dic_frequencias_Aquicultura_2018.msgpack',
  'dic_frequencias_Aquicultura_2019.msgpack',
  'dic_frequencias_Aquicultura_2020.msgpack',
  'dic_frequencias_Aquicultura_2021.msgpack',
  'dic_frequencias_Aquicultura_2022.msgpack',
  'dic_frequencias_Aquicultura_2023.msgpack'],
 'Arquitetura_e_Urbanismo': ['dic_frequencias_Arquitetura_e_Urbanismo_2003.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2004.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2005.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2006.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2007.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2008.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2009.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2010.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2011.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2012.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2013.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2014.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2015.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2016.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2017.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2018.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2019.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2020.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2021.msgpack',
  'dic_frequencias_Arquitetura_e_Urbanismo_2022.msgpack'],
 'Assistencia_Farmaceutica': ['dic_frequencias_Assistencia_Farmaceutica_2014.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2015.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2016.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2017.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2018.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2019.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2020.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2021.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2022.msgpack',
  'dic_frequencias_Assistencia_Farmaceutica_2023.msgpack'],
 'Biologia_Celular_e_do_Desenvolvimento': ['dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2011.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2012.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2013.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2014.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2015.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2016.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2017.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2018.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2019.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2020.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2021.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2022.msgpack',
  'dic_frequencias_Biologia_Celular_e_do_Desenvolvimento_2023.msgpack'],
 'Biologia_Vegetal': ['dic_frequencias_Biologia_Vegetal_2003.msgpack',
  'dic_frequencias_Biologia_Vegetal_2004.msgpack',
  'dic_frequencias_Biologia_Vegetal_2005.msgpack',
  'dic_frequencias_Biologia_Vegetal_2006.msgpack',
  'dic_frequencias_Biologia_Vegetal_2007.msgpack',
  'dic_frequencias_Biologia_Vegetal_2008.msgpack',
  'dic_frequencias_Biologia_Vegetal_2009.msgpack',
  'dic_frequencias_Biologia_Vegetal_2010.msgpack',
  'dic_frequencias_Biologia_Vegetal_2011.msgpack',
  'dic_frequencias_Biologia_Vegetal_2012.msgpack',
  'dic_frequencias_Biologia_Vegetal_2013.msgpack',
  'dic_frequencias_Biologia_Vegetal_2014.msgpack'],
 'Biologia_de_Fungos_Algas_e_Plantas': ['dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2012.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2013.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2014.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2015.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2016.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2017.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2018.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2019.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2020.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2021.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2022.msgpack',
  'dic_frequencias_Biologia_de_Fungos_Algas_e_Plantas_2023.msgpack'],
 'Bioquimica': ['dic_frequencias_Bioquimica_2009.msgpack',
  'dic_frequencias_Bioquimica_2010.msgpack',
  'dic_frequencias_Bioquimica_2011.msgpack',
  'dic_frequencias_Bioquimica_2012.msgpack',
  'dic_frequencias_Bioquimica_2013.msgpack',
  'dic_frequencias_Bioquimica_2014.msgpack',
  'dic_frequencias_Bioquimica_2015.msgpack',
  'dic_frequencias_Bioquimica_2016.msgpack',
  'dic_frequencias_Bioquimica_2017.msgpack',
  'dic_frequencias_Bioquimica_2018.msgpack',
  'dic_frequencias_Bioquimica_2019.msgpack',
  'dic_frequencias_Bioquimica_2020.msgpack',
  'dic_frequencias_Bioquimica_2021.msgpack',
  'dic_frequencias_Bioquimica_2022.msgpack',
  'dic_frequencias_Bioquimica_2023.msgpack'],
 'Biotecnologia': ['dic_frequencias_Biotecnologia_2003.msgpack',
  'dic_frequencias_Biotecnologia_2004.msgpack',
  'dic_frequencias_Biotecnologia_2005.msgpack',
  'dic_frequencias_Biotecnologia_2006.msgpack',
  'dic_frequencias_Biotecnologia_2007.msgpack',
  'dic_frequencias_Biotecnologia_2008.msgpack',
  'dic_frequencias_Biotecnologia_2009.msgpack',
  'dic_frequencias_Biotecnologia_2010.msgpack',
  'dic_frequencias_Biotecnologia_2011.msgpack',
  'dic_frequencias_Biotecnologia_2012.msgpack',
  'dic_frequencias_Biotecnologia_2013.msgpack',
  'dic_frequencias_Biotecnologia_2014.msgpack',
  'dic_frequencias_Biotecnologia_2015.msgpack',
  'dic_frequencias_Biotecnologia_2016.msgpack'],
 'Biotecnologia_e_Biociencias': ['dic_frequencias_Biotecnologia_e_Biociencias_2011.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2012.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2013.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2014.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2015.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2016.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2017.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2018.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2019.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2020.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2021.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2022.msgpack',
  'dic_frequencias_Biotecnologia_e_Biociencias_2023.msgpack'],
 'Ciencia_da_Computacao': ['dic_frequencias_Ciencia_da_Computacao_2003.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2004.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2005.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2006.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2007.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2008.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2009.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2010.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2011.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2012.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2013.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2014.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2015.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2016.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2017.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2018.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2019.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2020.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2021.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2022.msgpack',
  'dic_frequencias_Ciencia_da_Computacao_2023.msgpack'],
 'Ciencia_da_Informacao': ['dic_frequencias_Ciencia_da_Informacao_2005.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2006.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2007.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2008.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2009.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2010.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2011.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2012.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2013.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2014.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2015.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2016.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2017.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2018.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2019.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2020.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2021.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2022.msgpack',
  'dic_frequencias_Ciencia_da_Informacao_2023.msgpack'],
 'Ciencia_dos_Alimentos': ['dic_frequencias_Ciencia_dos_Alimentos_2003.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2004.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2005.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2006.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2007.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2008.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2009.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2010.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2011.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2012.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2013.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2014.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2015.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2016.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2017.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2018.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2019.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2020.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2021.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2022.msgpack',
  'dic_frequencias_Ciencia_dos_Alimentos_2023.msgpack'],
 'Ciencia_e_Engenharia_de_Materiais': ['dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2003.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2004.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2005.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2006.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2007.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2008.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2009.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2010.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2011.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2012.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2013.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2014.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2015.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2016.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2017.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2018.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2019.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2020.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2021.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2022.msgpack',
  'dic_frequencias_Ciencia_e_Engenharia_de_Materiais_2023.msgpack'],
 'Ciencias_Medicas': ['dic_frequencias_Ciencias_Medicas_2003.msgpack',
  'dic_frequencias_Ciencias_Medicas_2004.msgpack',
  'dic_frequencias_Ciencias_Medicas_2005.msgpack',
  'dic_frequencias_Ciencias_Medicas_2006.msgpack',
  'dic_frequencias_Ciencias_Medicas_2007.msgpack',
  'dic_frequencias_Ciencias_Medicas_2010.msgpack',
  'dic_frequencias_Ciencias_Medicas_2011.msgpack',
  'dic_frequencias_Ciencias_Medicas_2012.msgpack',
  'dic_frequencias_Ciencias_Medicas_2013.msgpack',
  'dic_frequencias_Ciencias_Medicas_2014.msgpack',
  'dic_frequencias_Ciencias_Medicas_2015.msgpack',
  'dic_frequencias_Ciencias_Medicas_2016.msgpack',
  'dic_frequencias_Ciencias_Medicas_2017.msgpack',
  'dic_frequencias_Ciencias_Medicas_2018.msgpack',
  'dic_frequencias_Ciencias_Medicas_2019.msgpack',
  'dic_frequencias_Ciencias_Medicas_2020.msgpack',
  'dic_frequencias_Ciencias_Medicas_2021.msgpack',
  'dic_frequencias_Ciencias_Medicas_2022.msgpack',
  'dic_frequencias_Ciencias_Medicas_2023.msgpack'],
 'Ciencias_da_Reabilitacao': ['dic_frequencias_Ciencias_da_Reabilitacao_2009.msgpack',
  'dic_frequencias_Ciencias_da_Reabilitacao_2018.msgpack',
  'dic_frequencias_Ciencias_da_Reabilitacao_2019.msgpack',
  'dic_frequencias_Ciencias_da_Reabilitacao_2020.msgpack',
  'dic_frequencias_Ciencias_da_Reabilitacao_2021.msgpack',
  'dic_frequencias_Ciencias_da_Reabilitacao_2022.msgpack',
  'dic_frequencias_Ciencias_da_Reabilitacao_2023.msgpack'],
 'Contabilidade': ['dic_frequencias_Contabilidade_2006.msgpack',
  'dic_frequencias_Contabilidade_2007.msgpack',
  'dic_frequencias_Contabilidade_2008.msgpack',
  'dic_frequencias_Contabilidade_2009.msgpack',
  'dic_frequencias_Contabilidade_2010.msgpack',
  'dic_frequencias_Contabilidade_2011.msgpack',
  'dic_frequencias_Contabilidade_2012.msgpack',
  'dic_frequencias_Contabilidade_2013.msgpack',
  'dic_frequencias_Contabilidade_2014.msgpack',
  'dic_frequencias_Contabilidade_2015.msgpack',
  'dic_frequencias_Contabilidade_2016.msgpack',
  'dic_frequencias_Contabilidade_2017.msgpack',
  'dic_frequencias_Contabilidade_2018.msgpack',
  'dic_frequencias_Contabilidade_2019.msgpack',
  'dic_frequencias_Contabilidade_2020.msgpack',
  'dic_frequencias_Contabilidade_2021.msgpack',
  'dic_frequencias_Contabilidade_2022.msgpack',
  'dic_frequencias_Contabilidade_2023.msgpack'],
 'Controle_de_Gestao_Mestrado_Profissional': ['dic_frequencias_Controle_de_Gestao_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Controle_de_Gestao_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Controle_de_Gestao_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Controle_de_Gestao_Mestrado_Profissional_2023.msgpack'],
 'Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional': ['dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2012.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional_2020.msgpack'],
 'Desastres_Naturais_Mestrado_Profissional': ['dic_frequencias_Desastres_Naturais_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Desastres_Naturais_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Desastres_Naturais_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Desastres_Naturais_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Desastres_Naturais_Mestrado_Profissional_2023.msgpack'],
 'Design': ['dic_frequencias_Design_2016.msgpack',
  'dic_frequencias_Design_2017.msgpack',
  'dic_frequencias_Design_2018.msgpack',
  'dic_frequencias_Design_2019.msgpack',
  'dic_frequencias_Design_2020.msgpack',
  'dic_frequencias_Design_2021.msgpack',
  'dic_frequencias_Design_2022.msgpack',
  'dic_frequencias_Design_2023.msgpack'],
 'Design_e_Expressao_Grafica': ['dic_frequencias_Design_e_Expressao_Grafica_2008.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2009.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2010.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2011.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2012.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2013.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2014.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2015.msgpack',
  'dic_frequencias_Design_e_Expressao_Grafica_2016.msgpack'],
 'Direito': ['dic_frequencias_Direito_2003.msgpack',
  'dic_frequencias_Direito_2004.msgpack',
  'dic_frequencias_Direito_2005.msgpack',
  'dic_frequencias_Direito_2006.msgpack',
  'dic_frequencias_Direito_2007.msgpack',
  'dic_frequencias_Direito_2008.msgpack',
  'dic_frequencias_Direito_2009.msgpack',
  'dic_frequencias_Direito_2010.msgpack',
  'dic_frequencias_Direito_2011.msgpack',
  'dic_frequencias_Direito_2012.msgpack',
  'dic_frequencias_Direito_2013.msgpack',
  'dic_frequencias_Direito_2014.msgpack',
  'dic_frequencias_Direito_2015.msgpack',
  'dic_frequencias_Direito_2016.msgpack',
  'dic_frequencias_Direito_2017.msgpack',
  'dic_frequencias_Direito_2018.msgpack',
  'dic_frequencias_Direito_2019.msgpack',
  'dic_frequencias_Direito_2020.msgpack',
  'dic_frequencias_Direito_2021.msgpack',
  'dic_frequencias_Direito_2022.msgpack',
  'dic_frequencias_Direito_2023.msgpack'],
 'Direito_Mestrado_Profissional': ['dic_frequencias_Direito_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Direito_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Direito_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Direito_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Direito_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Direito_Mestrado_Profissional_2023.msgpack'],
 'Ecologia': ['dic_frequencias_Ecologia_2009.msgpack',
  'dic_frequencias_Ecologia_2010.msgpack',
  'dic_frequencias_Ecologia_2011.msgpack',
  'dic_frequencias_Ecologia_2012.msgpack',
  'dic_frequencias_Ecologia_2013.msgpack',
  'dic_frequencias_Ecologia_2014.msgpack',
  'dic_frequencias_Ecologia_2015.msgpack',
  'dic_frequencias_Ecologia_2016.msgpack',
  'dic_frequencias_Ecologia_2017.msgpack',
  'dic_frequencias_Ecologia_2018.msgpack',
  'dic_frequencias_Ecologia_2019.msgpack',
  'dic_frequencias_Ecologia_2020.msgpack',
  'dic_frequencias_Ecologia_2021.msgpack',
  'dic_frequencias_Ecologia_2022.msgpack',
  'dic_frequencias_Ecologia_2023.msgpack'],
 'Economia': ['dic_frequencias_Economia_2003.msgpack',
  'dic_frequencias_Economia_2004.msgpack',
  'dic_frequencias_Economia_2005.msgpack',
  'dic_frequencias_Economia_2006.msgpack',
  'dic_frequencias_Economia_2007.msgpack',
  'dic_frequencias_Economia_2008.msgpack',
  'dic_frequencias_Economia_2009.msgpack',
  'dic_frequencias_Economia_2010.msgpack',
  'dic_frequencias_Economia_2011.msgpack',
  'dic_frequencias_Economia_2012.msgpack',
  'dic_frequencias_Economia_2013.msgpack',
  'dic_frequencias_Economia_2014.msgpack',
  'dic_frequencias_Economia_2015.msgpack',
  'dic_frequencias_Economia_2016.msgpack',
  'dic_frequencias_Economia_2017.msgpack',
  'dic_frequencias_Economia_2018.msgpack',
  'dic_frequencias_Economia_2019.msgpack',
  'dic_frequencias_Economia_2020.msgpack',
  'dic_frequencias_Economia_2021.msgpack',
  'dic_frequencias_Economia_2022.msgpack',
  'dic_frequencias_Economia_2023.msgpack'],
 'Ecossistemas_Agricolas_e_Naturais': ['dic_frequencias_Ecossistemas_Agricolas_e_Naturais_2018.msgpack',
  'dic_frequencias_Ecossistemas_Agricolas_e_Naturais_2019.msgpack',
  'dic_frequencias_Ecossistemas_Agricolas_e_Naturais_2020.msgpack',
  'dic_frequencias_Ecossistemas_Agricolas_e_Naturais_2021.msgpack',
  'dic_frequencias_Ecossistemas_Agricolas_e_Naturais_2022.msgpack',
  'dic_frequencias_Ecossistemas_Agricolas_e_Naturais_2023.msgpack'],
 'Educacao': ['dic_frequencias_Educacao_2003.msgpack',
  'dic_frequencias_Educacao_2004.msgpack',
  'dic_frequencias_Educacao_2005.msgpack',
  'dic_frequencias_Educacao_2006.msgpack',
  'dic_frequencias_Educacao_2007.msgpack',
  'dic_frequencias_Educacao_2008.msgpack',
  'dic_frequencias_Educacao_2009.msgpack',
  'dic_frequencias_Educacao_2010.msgpack',
  'dic_frequencias_Educacao_2011.msgpack',
  'dic_frequencias_Educacao_2012.msgpack',
  'dic_frequencias_Educacao_2013.msgpack',
  'dic_frequencias_Educacao_2014.msgpack',
  'dic_frequencias_Educacao_2015.msgpack',
  'dic_frequencias_Educacao_2016.msgpack',
  'dic_frequencias_Educacao_2017.msgpack',
  'dic_frequencias_Educacao_2018.msgpack',
  'dic_frequencias_Educacao_2019.msgpack',
  'dic_frequencias_Educacao_2020.msgpack',
  'dic_frequencias_Educacao_2021.msgpack',
  'dic_frequencias_Educacao_2022.msgpack',
  'dic_frequencias_Educacao_2023.msgpack'],
 'Educacao_Cientifica_e_Tecnologica': ['dic_frequencias_Educacao_Cientifica_e_Tecnologica_2004.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2005.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2006.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2007.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2008.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2009.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2010.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2011.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2012.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2013.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2014.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2015.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2016.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2017.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2018.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2019.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2020.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2021.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2022.msgpack',
  'dic_frequencias_Educacao_Cientifica_e_Tecnologica_2023.msgpack'],
 'Educacao_Fisica': ['dic_frequencias_Educacao_Fisica_2003.msgpack',
  'dic_frequencias_Educacao_Fisica_2004.msgpack',
  'dic_frequencias_Educacao_Fisica_2005.msgpack',
  'dic_frequencias_Educacao_Fisica_2006.msgpack',
  'dic_frequencias_Educacao_Fisica_2007.msgpack',
  'dic_frequencias_Educacao_Fisica_2008.msgpack',
  'dic_frequencias_Educacao_Fisica_2009.msgpack',
  'dic_frequencias_Educacao_Fisica_2010.msgpack',
  'dic_frequencias_Educacao_Fisica_2011.msgpack',
  'dic_frequencias_Educacao_Fisica_2012.msgpack',
  'dic_frequencias_Educacao_Fisica_2013.msgpack',
  'dic_frequencias_Educacao_Fisica_2014.msgpack',
  'dic_frequencias_Educacao_Fisica_2015.msgpack',
  'dic_frequencias_Educacao_Fisica_2016.msgpack',
  'dic_frequencias_Educacao_Fisica_2017.msgpack',
  'dic_frequencias_Educacao_Fisica_2018.msgpack',
  'dic_frequencias_Educacao_Fisica_2019.msgpack',
  'dic_frequencias_Educacao_Fisica_2020.msgpack',
  'dic_frequencias_Educacao_Fisica_2021.msgpack',
  'dic_frequencias_Educacao_Fisica_2022.msgpack',
  'dic_frequencias_Educacao_Fisica_2023.msgpack'],
 'Energia_e_Sustentabilidade': ['dic_frequencias_Energia_e_Sustentabilidade_2018.msgpack',
  'dic_frequencias_Energia_e_Sustentabilidade_2019.msgpack',
  'dic_frequencias_Energia_e_Sustentabilidade_2020.msgpack',
  'dic_frequencias_Energia_e_Sustentabilidade_2021.msgpack',
  'dic_frequencias_Energia_e_Sustentabilidade_2022.msgpack',
  'dic_frequencias_Energia_e_Sustentabilidade_2023.msgpack'],
 'Enfermagem': ['dic_frequencias_Enfermagem_2003.msgpack',
  'dic_frequencias_Enfermagem_2004.msgpack',
  'dic_frequencias_Enfermagem_2005.msgpack',
  'dic_frequencias_Enfermagem_2006.msgpack',
  'dic_frequencias_Enfermagem_2007.msgpack',
  'dic_frequencias_Enfermagem_2008.msgpack',
  'dic_frequencias_Enfermagem_2009.msgpack',
  'dic_frequencias_Enfermagem_2010.msgpack',
  'dic_frequencias_Enfermagem_2011.msgpack',
  'dic_frequencias_Enfermagem_2012.msgpack',
  'dic_frequencias_Enfermagem_2013.msgpack',
  'dic_frequencias_Enfermagem_2014.msgpack',
  'dic_frequencias_Enfermagem_2015.msgpack',
  'dic_frequencias_Enfermagem_2016.msgpack',
  'dic_frequencias_Enfermagem_2017.msgpack',
  'dic_frequencias_Enfermagem_2018.msgpack',
  'dic_frequencias_Enfermagem_2019.msgpack',
  'dic_frequencias_Enfermagem_2020.msgpack',
  'dic_frequencias_Enfermagem_2021.msgpack',
  'dic_frequencias_Enfermagem_2022.msgpack',
  'dic_frequencias_Enfermagem_2023.msgpack'],
 'Engenharia_Ambiental': ['dic_frequencias_Engenharia_Ambiental_2003.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2004.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2005.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2006.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2007.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2008.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2009.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2010.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2011.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2012.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2013.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2014.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2015.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2016.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2017.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2018.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2019.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2020.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2021.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2022.msgpack',
  'dic_frequencias_Engenharia_Ambiental_2023.msgpack'],
 'Engenharia_Ambiental_Mestrado_Profissional': ['dic_frequencias_Engenharia_Ambiental_Mestrado_Profissional_2012.msgpack',
  'dic_frequencias_Engenharia_Ambiental_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Engenharia_Ambiental_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Engenharia_Ambiental_Mestrado_Profissional_2016.msgpack'],
 'Engenharia_Civil': ['dic_frequencias_Engenharia_Civil_2003.msgpack',
  'dic_frequencias_Engenharia_Civil_2004.msgpack',
  'dic_frequencias_Engenharia_Civil_2005.msgpack',
  'dic_frequencias_Engenharia_Civil_2006.msgpack',
  'dic_frequencias_Engenharia_Civil_2007.msgpack',
  'dic_frequencias_Engenharia_Civil_2008.msgpack',
  'dic_frequencias_Engenharia_Civil_2009.msgpack',
  'dic_frequencias_Engenharia_Civil_2010.msgpack',
  'dic_frequencias_Engenharia_Civil_2011.msgpack',
  'dic_frequencias_Engenharia_Civil_2012.msgpack',
  'dic_frequencias_Engenharia_Civil_2013.msgpack',
  'dic_frequencias_Engenharia_Civil_2014.msgpack',
  'dic_frequencias_Engenharia_Civil_2015.msgpack',
  'dic_frequencias_Engenharia_Civil_2016.msgpack',
  'dic_frequencias_Engenharia_Civil_2017.msgpack',
  'dic_frequencias_Engenharia_Civil_2018.msgpack',
  'dic_frequencias_Engenharia_Civil_2019.msgpack',
  'dic_frequencias_Engenharia_Civil_2020.msgpack',
  'dic_frequencias_Engenharia_Civil_2021.msgpack',
  'dic_frequencias_Engenharia_Civil_2022.msgpack',
  'dic_frequencias_Engenharia_Civil_2023.msgpack'],
 'Engenharia_Eletrica': ['dic_frequencias_Engenharia_Eletrica_2003.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2004.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2005.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2006.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2007.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2008.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2009.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2010.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2011.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2012.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2013.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2014.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2015.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2016.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2017.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2018.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2019.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2020.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2021.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2022.msgpack',
  'dic_frequencias_Engenharia_Eletrica_2023.msgpack'],
 'Engenharia_Mecanica': ['dic_frequencias_Engenharia_Mecanica_2003.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2004.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2005.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2006.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2007.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2008.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2009.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2010.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2011.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2012.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2013.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2014.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2015.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2016.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2017.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2018.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2019.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2020.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2021.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2022.msgpack',
  'dic_frequencias_Engenharia_Mecanica_2023.msgpack'],
 'Engenharia_Mecanica_Mestrado_Profissional': ['dic_frequencias_Engenharia_Mecanica_Mestrado_Profissional_2006.msgpack'],
 'Engenharia_Quimica': ['dic_frequencias_Engenharia_Quimica_2003.msgpack',
  'dic_frequencias_Engenharia_Quimica_2004.msgpack',
  'dic_frequencias_Engenharia_Quimica_2005.msgpack',
  'dic_frequencias_Engenharia_Quimica_2006.msgpack',
  'dic_frequencias_Engenharia_Quimica_2007.msgpack',
  'dic_frequencias_Engenharia_Quimica_2008.msgpack',
  'dic_frequencias_Engenharia_Quimica_2009.msgpack',
  'dic_frequencias_Engenharia_Quimica_2010.msgpack',
  'dic_frequencias_Engenharia_Quimica_2011.msgpack',
  'dic_frequencias_Engenharia_Quimica_2012.msgpack',
  'dic_frequencias_Engenharia_Quimica_2013.msgpack',
  'dic_frequencias_Engenharia_Quimica_2014.msgpack',
  'dic_frequencias_Engenharia_Quimica_2015.msgpack',
  'dic_frequencias_Engenharia_Quimica_2016.msgpack',
  'dic_frequencias_Engenharia_Quimica_2017.msgpack',
  'dic_frequencias_Engenharia_Quimica_2018.msgpack',
  'dic_frequencias_Engenharia_Quimica_2019.msgpack',
  'dic_frequencias_Engenharia_Quimica_2020.msgpack',
  'dic_frequencias_Engenharia_Quimica_2021.msgpack',
  'dic_frequencias_Engenharia_Quimica_2022.msgpack',
  'dic_frequencias_Engenharia_Quimica_2023.msgpack'],
 'Engenharia_Textil': ['dic_frequencias_Engenharia_Textil_2021.msgpack',
  'dic_frequencias_Engenharia_Textil_2022.msgpack',
  'dic_frequencias_Engenharia_Textil_2023.msgpack'],
 'Engenharia_de_Alimentos': ['dic_frequencias_Engenharia_de_Alimentos_2003.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2004.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2005.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2006.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2007.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2008.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2009.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2010.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2011.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2012.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2013.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2014.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2015.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2016.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2017.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2018.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2019.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2020.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2021.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2022.msgpack',
  'dic_frequencias_Engenharia_de_Alimentos_2023.msgpack'],
 'Engenharia_de_Automacao_e_Sistemas': ['dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2008.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2009.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2010.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2011.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2012.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2013.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2014.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2015.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2016.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2017.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2018.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2019.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2020.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2021.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2022.msgpack',
  'dic_frequencias_Engenharia_de_Automacao_e_Sistemas_2023.msgpack'],
 'Engenharia_de_Producao': ['dic_frequencias_Engenharia_de_Producao_2003.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2004.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2005.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2006.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2007.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2008.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2009.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2010.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2011.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2012.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2013.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2014.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2015.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2016.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2017.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2018.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2019.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2020.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2021.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2022.msgpack',
  'dic_frequencias_Engenharia_de_Producao_2023.msgpack'],
 'Engenharia_de_Sistemas_Eletronicos': ['dic_frequencias_Engenharia_de_Sistemas_Eletronicos_2019.msgpack',
  'dic_frequencias_Engenharia_de_Sistemas_Eletronicos_2020.msgpack',
  'dic_frequencias_Engenharia_de_Sistemas_Eletronicos_2021.msgpack',
  'dic_frequencias_Engenharia_de_Sistemas_Eletronicos_2022.msgpack',
  'dic_frequencias_Engenharia_de_Sistemas_Eletronicos_2023.msgpack'],
 'Engenharia_de_Transportes_e_Gestao_Territorial': ['dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2016.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2017.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2018.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2019.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2020.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2021.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2022.msgpack',
  'dic_frequencias_Engenharia_de_Transportes_e_Gestao_Territorial_2023.msgpack'],
 'Engenharia_e_Ciencias_Mecanicas': ['dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2017.msgpack',
  'dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2018.msgpack',
  'dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2019.msgpack',
  'dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2020.msgpack',
  'dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2021.msgpack',
  'dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2022.msgpack',
  'dic_frequencias_Engenharia_e_Ciencias_Mecanicas_2023.msgpack'],
 'Engenharia_e_Gestao_do_Conhecimento': ['dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2006.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2007.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2008.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2009.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2010.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2011.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2012.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2013.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2014.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2015.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2016.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2017.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2018.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2019.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2020.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2021.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2022.msgpack',
  'dic_frequencias_Engenharia_e_Gestao_do_Conhecimento_2023.msgpack'],
 'Ensino_de_Biologia': ['dic_frequencias_Ensino_de_Biologia_2022.msgpack',
  'dic_frequencias_Ensino_de_Biologia_2023.msgpack'],
 'Ensino_de_Biologia_Mestrado_Profissional': ['dic_frequencias_Ensino_de_Biologia_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Ensino_de_Biologia_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Ensino_de_Biologia_Mestrado_Profissional_2022.msgpack'],
 'Ensino_de_Fisica_Mestrado_Profissional': ['dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Ensino_de_Fisica_Mestrado_Profissional_2023.msgpack'],
 'Ensino_de_Historia_Mestrado_Profissional': ['dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Ensino_de_Historia_Mestrado_Profissional_2023.msgpack'],
 'Estudos_da_Traducao': ['dic_frequencias_Estudos_da_Traducao_2005.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2006.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2007.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2008.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2009.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2010.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2011.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2012.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2013.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2014.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2015.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2016.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2017.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2018.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2019.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2020.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2021.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2022.msgpack',
  'dic_frequencias_Estudos_da_Traducao_2023.msgpack'],
 'Farmacia': ['dic_frequencias_Farmacia_2003.msgpack',
  'dic_frequencias_Farmacia_2004.msgpack',
  'dic_frequencias_Farmacia_2005.msgpack',
  'dic_frequencias_Farmacia_2006.msgpack',
  'dic_frequencias_Farmacia_2007.msgpack',
  'dic_frequencias_Farmacia_2008.msgpack',
  'dic_frequencias_Farmacia_2009.msgpack',
  'dic_frequencias_Farmacia_2010.msgpack',
  'dic_frequencias_Farmacia_2011.msgpack',
  'dic_frequencias_Farmacia_2012.msgpack',
  'dic_frequencias_Farmacia_2013.msgpack',
  'dic_frequencias_Farmacia_2014.msgpack',
  'dic_frequencias_Farmacia_2015.msgpack',
  'dic_frequencias_Farmacia_2016.msgpack',
  'dic_frequencias_Farmacia_2017.msgpack',
  'dic_frequencias_Farmacia_2018.msgpack',
  'dic_frequencias_Farmacia_2019.msgpack',
  'dic_frequencias_Farmacia_2020.msgpack',
  'dic_frequencias_Farmacia_2021.msgpack',
  'dic_frequencias_Farmacia_2022.msgpack',
  'dic_frequencias_Farmacia_2023.msgpack'],
 'Farmacologia': ['dic_frequencias_Farmacologia_2003.msgpack',
  'dic_frequencias_Farmacologia_2004.msgpack',
  'dic_frequencias_Farmacologia_2005.msgpack',
  'dic_frequencias_Farmacologia_2006.msgpack',
  'dic_frequencias_Farmacologia_2007.msgpack',
  'dic_frequencias_Farmacologia_2008.msgpack',
  'dic_frequencias_Farmacologia_2009.msgpack',
  'dic_frequencias_Farmacologia_2010.msgpack',
  'dic_frequencias_Farmacologia_2011.msgpack',
  'dic_frequencias_Farmacologia_2012.msgpack',
  'dic_frequencias_Farmacologia_2013.msgpack',
  'dic_frequencias_Farmacologia_2014.msgpack',
  'dic_frequencias_Farmacologia_2015.msgpack',
  'dic_frequencias_Farmacologia_2016.msgpack',
  'dic_frequencias_Farmacologia_2017.msgpack',
  'dic_frequencias_Farmacologia_2018.msgpack',
  'dic_frequencias_Farmacologia_2019.msgpack',
  'dic_frequencias_Farmacologia_2020.msgpack',
  'dic_frequencias_Farmacologia_2021.msgpack',
  'dic_frequencias_Farmacologia_2022.msgpack',
  'dic_frequencias_Farmacologia_2023.msgpack'],
 'Farmacologia_Mestrado_Profissional': ['dic_frequencias_Farmacologia_Mestrado_Profissional_2011.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2012.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Farmacologia_Mestrado_Profissional_2023.msgpack'],
 'Filosofia': ['dic_frequencias_Filosofia_2003.msgpack',
  'dic_frequencias_Filosofia_2004.msgpack',
  'dic_frequencias_Filosofia_2005.msgpack',
  'dic_frequencias_Filosofia_2006.msgpack',
  'dic_frequencias_Filosofia_2007.msgpack',
  'dic_frequencias_Filosofia_2008.msgpack',
  'dic_frequencias_Filosofia_2009.msgpack',
  'dic_frequencias_Filosofia_2010.msgpack',
  'dic_frequencias_Filosofia_2011.msgpack',
  'dic_frequencias_Filosofia_2012.msgpack',
  'dic_frequencias_Filosofia_2013.msgpack',
  'dic_frequencias_Filosofia_2014.msgpack',
  'dic_frequencias_Filosofia_2015.msgpack',
  'dic_frequencias_Filosofia_2016.msgpack',
  'dic_frequencias_Filosofia_2017.msgpack',
  'dic_frequencias_Filosofia_2018.msgpack',
  'dic_frequencias_Filosofia_2019.msgpack',
  'dic_frequencias_Filosofia_2020.msgpack',
  'dic_frequencias_Filosofia_2021.msgpack',
  'dic_frequencias_Filosofia_2022.msgpack',
  'dic_frequencias_Filosofia_2023.msgpack'],
 'Fisica': ['dic_frequencias_Fisica_2003.msgpack',
  'dic_frequencias_Fisica_2004.msgpack',
  'dic_frequencias_Fisica_2005.msgpack',
  'dic_frequencias_Fisica_2006.msgpack',
  'dic_frequencias_Fisica_2007.msgpack',
  'dic_frequencias_Fisica_2008.msgpack',
  'dic_frequencias_Fisica_2009.msgpack',
  'dic_frequencias_Fisica_2010.msgpack',
  'dic_frequencias_Fisica_2011.msgpack',
  'dic_frequencias_Fisica_2012.msgpack',
  'dic_frequencias_Fisica_2013.msgpack',
  'dic_frequencias_Fisica_2014.msgpack',
  'dic_frequencias_Fisica_2015.msgpack',
  'dic_frequencias_Fisica_2016.msgpack',
  'dic_frequencias_Fisica_2017.msgpack',
  'dic_frequencias_Fisica_2018.msgpack',
  'dic_frequencias_Fisica_2019.msgpack',
  'dic_frequencias_Fisica_2020.msgpack',
  'dic_frequencias_Fisica_2021.msgpack',
  'dic_frequencias_Fisica_2022.msgpack',
  'dic_frequencias_Fisica_2023.msgpack'],
 'Fonoaudiologia': ['dic_frequencias_Fonoaudiologia_2022.msgpack',
  'dic_frequencias_Fonoaudiologia_2023.msgpack'],
 'Geografia': ['dic_frequencias_Geografia_2003.msgpack',
  'dic_frequencias_Geografia_2004.msgpack',
  'dic_frequencias_Geografia_2005.msgpack',
  'dic_frequencias_Geografia_2006.msgpack',
  'dic_frequencias_Geografia_2007.msgpack',
  'dic_frequencias_Geografia_2008.msgpack',
  'dic_frequencias_Geografia_2009.msgpack',
  'dic_frequencias_Geografia_2010.msgpack',
  'dic_frequencias_Geografia_2011.msgpack',
  'dic_frequencias_Geografia_2012.msgpack',
  'dic_frequencias_Geografia_2013.msgpack',
  'dic_frequencias_Geografia_2014.msgpack',
  'dic_frequencias_Geografia_2015.msgpack',
  'dic_frequencias_Geografia_2016.msgpack',
  'dic_frequencias_Geografia_2017.msgpack',
  'dic_frequencias_Geografia_2018.msgpack',
  'dic_frequencias_Geografia_2019.msgpack',
  'dic_frequencias_Geografia_2020.msgpack',
  'dic_frequencias_Geografia_2021.msgpack',
  'dic_frequencias_Geografia_2022.msgpack',
  'dic_frequencias_Geografia_2023.msgpack'],
 'Geologia': ['dic_frequencias_Geologia_2022.msgpack',
  'dic_frequencias_Geologia_2023.msgpack'],
 'Gestao_do_Cuidado_em_Enfermagem': ['dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_2022.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_2023.msgpack'],
 'Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional': ['dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2012.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional_2022.msgpack'],
 'Historia': ['dic_frequencias_Historia_2003.msgpack',
  'dic_frequencias_Historia_2004.msgpack',
  'dic_frequencias_Historia_2005.msgpack',
  'dic_frequencias_Historia_2006.msgpack',
  'dic_frequencias_Historia_2007.msgpack',
  'dic_frequencias_Historia_2008.msgpack',
  'dic_frequencias_Historia_2009.msgpack',
  'dic_frequencias_Historia_2010.msgpack',
  'dic_frequencias_Historia_2011.msgpack',
  'dic_frequencias_Historia_2012.msgpack',
  'dic_frequencias_Historia_2013.msgpack',
  'dic_frequencias_Historia_2014.msgpack',
  'dic_frequencias_Historia_2015.msgpack',
  'dic_frequencias_Historia_2016.msgpack',
  'dic_frequencias_Historia_2017.msgpack',
  'dic_frequencias_Historia_2018.msgpack',
  'dic_frequencias_Historia_2019.msgpack',
  'dic_frequencias_Historia_2020.msgpack',
  'dic_frequencias_Historia_2021.msgpack',
  'dic_frequencias_Historia_2022.msgpack',
  'dic_frequencias_Historia_2023.msgpack'],
 'Informatica_em_Saude_Mestrado_Profissional': ['dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Informatica_em_Saude_Mestrado_Profissional_2023.msgpack'],
 'Ingles_Estudos_Linguisticos_e_Literarios': ['dic_frequencias_Ingles_Estudos_Linguisticos_e_Literarios_2013.msgpack',
  'dic_frequencias_Ingles_Estudos_Linguisticos_e_Literarios_2022.msgpack'],
 'Jornalismo': ['dic_frequencias_Jornalismo_2009.msgpack',
  'dic_frequencias_Jornalismo_2010.msgpack',
  'dic_frequencias_Jornalismo_2011.msgpack',
  'dic_frequencias_Jornalismo_2012.msgpack',
  'dic_frequencias_Jornalismo_2013.msgpack',
  'dic_frequencias_Jornalismo_2014.msgpack',
  'dic_frequencias_Jornalismo_2015.msgpack',
  'dic_frequencias_Jornalismo_2016.msgpack',
  'dic_frequencias_Jornalismo_2017.msgpack',
  'dic_frequencias_Jornalismo_2018.msgpack',
  'dic_frequencias_Jornalismo_2019.msgpack',
  'dic_frequencias_Jornalismo_2020.msgpack',
  'dic_frequencias_Jornalismo_2021.msgpack',
  'dic_frequencias_Jornalismo_2022.msgpack',
  'dic_frequencias_Jornalismo_2023.msgpack'],
 'Letras_Ingles_e_Literatura_Correspondente': ['dic_frequencias_Letras_Ingles_e_Literatura_Correspondente_2003.msgpack',
  'dic_frequencias_Letras_Ingles_e_Literatura_Correspondente_2004.msgpack',
  'dic_frequencias_Letras_Ingles_e_Literatura_Correspondente_2005.msgpack',
  'dic_frequencias_Letras_Ingles_e_Literatura_Correspondente_2007.msgpack',
  'dic_frequencias_Letras_Ingles_e_Literatura_Correspondente_2008.msgpack'],
 'Letras_Literatura_Brasileira': ['dic_frequencias_Letras_Literatura_Brasileira_2003.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2004.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2005.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2006.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2007.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2008.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2011.msgpack',
  'dic_frequencias_Letras_Literatura_Brasileira_2012.msgpack'],
 'Letras_Mestrado_Profissional': ['dic_frequencias_Letras_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Letras_Mestrado_Profissional_2023.msgpack'],
 'Linguistica': ['dic_frequencias_Linguistica_2003.msgpack',
  'dic_frequencias_Linguistica_2004.msgpack',
  'dic_frequencias_Linguistica_2005.msgpack',
  'dic_frequencias_Linguistica_2006.msgpack',
  'dic_frequencias_Linguistica_2007.msgpack',
  'dic_frequencias_Linguistica_2008.msgpack',
  'dic_frequencias_Linguistica_2009.msgpack',
  'dic_frequencias_Linguistica_2010.msgpack',
  'dic_frequencias_Linguistica_2011.msgpack',
  'dic_frequencias_Linguistica_2012.msgpack',
  'dic_frequencias_Linguistica_2013.msgpack',
  'dic_frequencias_Linguistica_2014.msgpack',
  'dic_frequencias_Linguistica_2015.msgpack',
  'dic_frequencias_Linguistica_2016.msgpack',
  'dic_frequencias_Linguistica_2017.msgpack',
  'dic_frequencias_Linguistica_2018.msgpack',
  'dic_frequencias_Linguistica_2019.msgpack',
  'dic_frequencias_Linguistica_2020.msgpack',
  'dic_frequencias_Linguistica_2021.msgpack',
  'dic_frequencias_Linguistica_2022.msgpack',
  'dic_frequencias_Linguistica_2023.msgpack'],
 'Literatura': ['dic_frequencias_Literatura_2003.msgpack',
  'dic_frequencias_Literatura_2004.msgpack',
  'dic_frequencias_Literatura_2005.msgpack',
  'dic_frequencias_Literatura_2006.msgpack',
  'dic_frequencias_Literatura_2007.msgpack',
  'dic_frequencias_Literatura_2008.msgpack',
  'dic_frequencias_Literatura_2009.msgpack',
  'dic_frequencias_Literatura_2010.msgpack',
  'dic_frequencias_Literatura_2011.msgpack',
  'dic_frequencias_Literatura_2012.msgpack',
  'dic_frequencias_Literatura_2013.msgpack',
  'dic_frequencias_Literatura_2014.msgpack',
  'dic_frequencias_Literatura_2015.msgpack',
  'dic_frequencias_Literatura_2016.msgpack',
  'dic_frequencias_Literatura_2017.msgpack',
  'dic_frequencias_Literatura_2018.msgpack',
  'dic_frequencias_Literatura_2019.msgpack',
  'dic_frequencias_Literatura_2020.msgpack',
  'dic_frequencias_Literatura_2021.msgpack',
  'dic_frequencias_Literatura_2022.msgpack',
  'dic_frequencias_Literatura_2023.msgpack'],
 'Matematica_Mestrado_Profissional': ['dic_frequencias_Matematica_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Matematica_Mestrado_Profissional_2023.msgpack'],
 'Matematica_Pura_e_Aplicada': ['dic_frequencias_Matematica_Pura_e_Aplicada_2013.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2014.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2015.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2016.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2017.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2018.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2019.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2020.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2021.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2022.msgpack',
  'dic_frequencias_Matematica_Pura_e_Aplicada_2023.msgpack'],
 'Matematica_e_Computacao_Cientifica': ['dic_frequencias_Matematica_e_Computacao_Cientifica_2003.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2004.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2005.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2006.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2007.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2008.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2009.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2010.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2011.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2012.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2013.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2014.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2015.msgpack',
  'dic_frequencias_Matematica_e_Computacao_Cientifica_2016.msgpack'],
 'Medicina_Veterinaria_Convencional_e_Integrativa': ['dic_frequencias_Medicina_Veterinaria_Convencional_e_Integrativa_2023.msgpack'],
 'Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional': ['dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Metodos_e_Gestao_em_Avaliacao_Mestrado_Profissional_2023.msgpack'],
 'Metrologia_Cientifica_e_Industrial': ['dic_frequencias_Metrologia_Cientifica_e_Industrial_2003.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2004.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2005.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2006.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2007.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2008.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2009.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2010.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2011.msgpack',
  'dic_frequencias_Metrologia_Cientifica_e_Industrial_2013.msgpack'],
 'Nanociencia_Processos_e_Materiais_Avancados': ['dic_frequencias_Nanociencia_Processos_e_Materiais_Avancados_2021.msgpack',
  'dic_frequencias_Nanociencia_Processos_e_Materiais_Avancados_2022.msgpack',
  'dic_frequencias_Nanociencia_Processos_e_Materiais_Avancados_2023.msgpack'],
 'Nanotecnologia_Farmaceutica': ['dic_frequencias_Nanotecnologia_Farmaceutica_2014.msgpack',
  'dic_frequencias_Nanotecnologia_Farmaceutica_2016.msgpack',
  'dic_frequencias_Nanotecnologia_Farmaceutica_2021.msgpack'],
 'Neurociencias': ['dic_frequencias_Neurociencias_2003.msgpack',
  'dic_frequencias_Neurociencias_2004.msgpack',
  'dic_frequencias_Neurociencias_2005.msgpack',
  'dic_frequencias_Neurociencias_2006.msgpack',
  'dic_frequencias_Neurociencias_2007.msgpack',
  'dic_frequencias_Neurociencias_2008.msgpack',
  'dic_frequencias_Neurociencias_2009.msgpack',
  'dic_frequencias_Neurociencias_2010.msgpack',
  'dic_frequencias_Neurociencias_2011.msgpack',
  'dic_frequencias_Neurociencias_2012.msgpack',
  'dic_frequencias_Neurociencias_2013.msgpack',
  'dic_frequencias_Neurociencias_2014.msgpack',
  'dic_frequencias_Neurociencias_2015.msgpack',
  'dic_frequencias_Neurociencias_2016.msgpack',
  'dic_frequencias_Neurociencias_2017.msgpack',
  'dic_frequencias_Neurociencias_2018.msgpack',
  'dic_frequencias_Neurociencias_2019.msgpack',
  'dic_frequencias_Neurociencias_2020.msgpack',
  'dic_frequencias_Neurociencias_2021.msgpack',
  'dic_frequencias_Neurociencias_2022.msgpack',
  'dic_frequencias_Neurociencias_2023.msgpack'],
 'Nutricao': ['dic_frequencias_Nutricao_2003.msgpack',
  'dic_frequencias_Nutricao_2004.msgpack',
  'dic_frequencias_Nutricao_2005.msgpack',
  'dic_frequencias_Nutricao_2006.msgpack',
  'dic_frequencias_Nutricao_2007.msgpack',
  'dic_frequencias_Nutricao_2008.msgpack',
  'dic_frequencias_Nutricao_2009.msgpack',
  'dic_frequencias_Nutricao_2010.msgpack',
  'dic_frequencias_Nutricao_2011.msgpack',
  'dic_frequencias_Nutricao_2012.msgpack',
  'dic_frequencias_Nutricao_2013.msgpack',
  'dic_frequencias_Nutricao_2014.msgpack',
  'dic_frequencias_Nutricao_2015.msgpack',
  'dic_frequencias_Nutricao_2016.msgpack',
  'dic_frequencias_Nutricao_2017.msgpack',
  'dic_frequencias_Nutricao_2018.msgpack',
  'dic_frequencias_Nutricao_2019.msgpack',
  'dic_frequencias_Nutricao_2020.msgpack',
  'dic_frequencias_Nutricao_2021.msgpack',
  'dic_frequencias_Nutricao_2022.msgpack',
  'dic_frequencias_Nutricao_2023.msgpack'],
 'Oceanografia': ['dic_frequencias_Oceanografia_2017.msgpack',
  'dic_frequencias_Oceanografia_2018.msgpack',
  'dic_frequencias_Oceanografia_2019.msgpack',
  'dic_frequencias_Oceanografia_2020.msgpack',
  'dic_frequencias_Oceanografia_2021.msgpack',
  'dic_frequencias_Oceanografia_2022.msgpack',
  'dic_frequencias_Oceanografia_2023.msgpack'],
 'Odontologia': ['dic_frequencias_Odontologia_2003.msgpack',
  'dic_frequencias_Odontologia_2004.msgpack',
  'dic_frequencias_Odontologia_2005.msgpack',
  'dic_frequencias_Odontologia_2006.msgpack',
  'dic_frequencias_Odontologia_2007.msgpack',
  'dic_frequencias_Odontologia_2008.msgpack',
  'dic_frequencias_Odontologia_2009.msgpack',
  'dic_frequencias_Odontologia_2010.msgpack',
  'dic_frequencias_Odontologia_2011.msgpack',
  'dic_frequencias_Odontologia_2012.msgpack',
  'dic_frequencias_Odontologia_2013.msgpack',
  'dic_frequencias_Odontologia_2014.msgpack',
  'dic_frequencias_Odontologia_2015.msgpack',
  'dic_frequencias_Odontologia_2016.msgpack',
  'dic_frequencias_Odontologia_2017.msgpack',
  'dic_frequencias_Odontologia_2018.msgpack',
  'dic_frequencias_Odontologia_2019.msgpack',
  'dic_frequencias_Odontologia_2020.msgpack',
  'dic_frequencias_Odontologia_2021.msgpack',
  'dic_frequencias_Odontologia_2022.msgpack',
  'dic_frequencias_Odontologia_2023.msgpack'],
 'Pericias_Criminais_Ambientais_Mestrado_Profissional': ['dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Pericias_Criminais_Ambientais_Mestrado_Profissional_2023.msgpack'],
 'Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas': ['dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2003.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2004.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2005.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2006.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2007.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2008.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2009.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2010.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2011.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2012.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2013.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2014.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2015.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2016.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2017.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2018.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2019.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2020.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2021.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2022.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas_2023.msgpack'],
 'Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas': ['dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2011.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2012.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2013.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2014.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2015.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2016.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2017.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2018.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2019.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2020.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2021.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2022.msgpack',
  'dic_frequencias_Programa_de_Pos_Graduacao_Multicentrico_em_Ciencias_Fisiologicas_2023.msgpack'],
 'Programa_de_Pos_Graduacao_Multidisciplinar_em_Saude_Mestrado_Profissional': ['dic_frequencias_Programa_de_P_G_Multdisc_em_Saude_M_P_2012.msgpack',
  'dic_frequencias_Programa_de_P_G_Multdisc_em_Saude_M_P_2013.msgpack',
  'dic_frequencias_Programa_de_P_G_Multdisc_em_Saude_M_P_2014.msgpack',
  'dic_frequencias_Programa_de_P_G_Multdisc_em_Saude_M_P_2015.msgpack',
  'dic_frequencias_Programa_de_P_G_Multdisc_em_Saude_M_P_2016.msgpack'],
 'Propriedade_Intelectual_e_Transferencia_de_Tecnologia_para_Inovacao_Mestrado_Profissional': ['dic_frequencias_Prop_Intelec_e_Transf_de_Tec_para_Inov_M_P_2018.msgpack',
  'dic_frequencias_Prop_Intelec_e_Transf_de_Tec_para_Inov_M_P_2019.msgpack',
  'dic_frequencias_Prop_Intelec_e_Transf_de_Tec_para_Inov_M_P_2020.msgpack',
  'dic_frequencias_Prop_Intelec_e_Transf_de_Tec_para_Inov_M_P_2021.msgpack',
  'dic_frequencias_Prop_Intelec_e_Transf_de_Tec_para_Inov_M_P_2022.msgpack',
  'dic_frequencias_Prop_Intelec_e_Transf_de_Tec_para_Inov_M_P_2023.msgpack'],
 'Psicologia': ['dic_frequencias_Psicologia_2003.msgpack',
  'dic_frequencias_Psicologia_2004.msgpack',
  'dic_frequencias_Psicologia_2005.msgpack',
  'dic_frequencias_Psicologia_2006.msgpack',
  'dic_frequencias_Psicologia_2007.msgpack',
  'dic_frequencias_Psicologia_2008.msgpack',
  'dic_frequencias_Psicologia_2009.msgpack',
  'dic_frequencias_Psicologia_2010.msgpack',
  'dic_frequencias_Psicologia_2011.msgpack',
  'dic_frequencias_Psicologia_2012.msgpack',
  'dic_frequencias_Psicologia_2013.msgpack',
  'dic_frequencias_Psicologia_2014.msgpack',
  'dic_frequencias_Psicologia_2015.msgpack',
  'dic_frequencias_Psicologia_2016.msgpack',
  'dic_frequencias_Psicologia_2017.msgpack',
  'dic_frequencias_Psicologia_2018.msgpack',
  'dic_frequencias_Psicologia_2019.msgpack',
  'dic_frequencias_Psicologia_2020.msgpack',
  'dic_frequencias_Psicologia_2021.msgpack',
  'dic_frequencias_Psicologia_2022.msgpack',
  'dic_frequencias_Psicologia_2023.msgpack'],
 'Quimica': ['dic_frequencias_Quimica_2003.msgpack',
  'dic_frequencias_Quimica_2004.msgpack',
  'dic_frequencias_Quimica_2005.msgpack',
  'dic_frequencias_Quimica_2006.msgpack',
  'dic_frequencias_Quimica_2007.msgpack',
  'dic_frequencias_Quimica_2008.msgpack',
  'dic_frequencias_Quimica_2009.msgpack',
  'dic_frequencias_Quimica_2010.msgpack',
  'dic_frequencias_Quimica_2011.msgpack',
  'dic_frequencias_Quimica_2012.msgpack',
  'dic_frequencias_Quimica_2013.msgpack',
  'dic_frequencias_Quimica_2014.msgpack',
  'dic_frequencias_Quimica_2015.msgpack',
  'dic_frequencias_Quimica_2016.msgpack',
  'dic_frequencias_Quimica_2017.msgpack',
  'dic_frequencias_Quimica_2018.msgpack',
  'dic_frequencias_Quimica_2019.msgpack',
  'dic_frequencias_Quimica_2020.msgpack',
  'dic_frequencias_Quimica_2021.msgpack',
  'dic_frequencias_Quimica_2022.msgpack',
  'dic_frequencias_Quimica_2023.msgpack'],
 'Recursos_Geneticos_Vegetais': ['dic_frequencias_Recursos_Geneticos_Vegetais_2003.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2004.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2005.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2006.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2007.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2008.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2009.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2010.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2011.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2012.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2013.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2014.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2015.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2016.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2017.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2018.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2019.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2020.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2021.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2022.msgpack',
  'dic_frequencias_Recursos_Geneticos_Vegetais_2023.msgpack'],
 'Relacoes_Internacionais': ['dic_frequencias_Relacoes_Internacionais_2013.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2014.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2015.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2016.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2017.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2018.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2019.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2020.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2021.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2022.msgpack',
  'dic_frequencias_Relacoes_Internacionais_2023.msgpack'],
 'Saude_Coletiva': ['dic_frequencias_Saude_Coletiva_2010.msgpack',
  'dic_frequencias_Saude_Coletiva_2011.msgpack',
  'dic_frequencias_Saude_Coletiva_2012.msgpack',
  'dic_frequencias_Saude_Coletiva_2013.msgpack',
  'dic_frequencias_Saude_Coletiva_2014.msgpack',
  'dic_frequencias_Saude_Coletiva_2015.msgpack',
  'dic_frequencias_Saude_Coletiva_2016.msgpack',
  'dic_frequencias_Saude_Coletiva_2017.msgpack',
  'dic_frequencias_Saude_Coletiva_2018.msgpack',
  'dic_frequencias_Saude_Coletiva_2019.msgpack',
  'dic_frequencias_Saude_Coletiva_2020.msgpack',
  'dic_frequencias_Saude_Coletiva_2021.msgpack',
  'dic_frequencias_Saude_Coletiva_2022.msgpack',
  'dic_frequencias_Saude_Coletiva_2023.msgpack'],
 'Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional': ['dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2013.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2014.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2015.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2016.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2017.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2018.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2019.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2020.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2021.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2022.msgpack',
  'dic_frequencias_Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional_2023.msgpack'],
 'Saude_Publica': ['dic_frequencias_Saude_Publica_2003.msgpack',
  'dic_frequencias_Saude_Publica_2004.msgpack',
  'dic_frequencias_Saude_Publica_2005.msgpack',
  'dic_frequencias_Saude_Publica_2006.msgpack',
  'dic_frequencias_Saude_Publica_2007.msgpack',
  'dic_frequencias_Saude_Publica_2008.msgpack',
  'dic_frequencias_Saude_Publica_2009.msgpack',
  'dic_frequencias_Saude_Publica_2010.msgpack',
  'dic_frequencias_Saude_Publica_2011.msgpack',
  'dic_frequencias_Saude_Publica_2012.msgpack'],
 'Servico_Social': ['dic_frequencias_Servico_Social_2003.msgpack',
  'dic_frequencias_Servico_Social_2004.msgpack',
  'dic_frequencias_Servico_Social_2005.msgpack',
  'dic_frequencias_Servico_Social_2006.msgpack',
  'dic_frequencias_Servico_Social_2007.msgpack',
  'dic_frequencias_Servico_Social_2008.msgpack',
  'dic_frequencias_Servico_Social_2009.msgpack',
  'dic_frequencias_Servico_Social_2010.msgpack',
  'dic_frequencias_Servico_Social_2011.msgpack',
  'dic_frequencias_Servico_Social_2012.msgpack',
  'dic_frequencias_Servico_Social_2013.msgpack',
  'dic_frequencias_Servico_Social_2014.msgpack',
  'dic_frequencias_Servico_Social_2015.msgpack',
  'dic_frequencias_Servico_Social_2016.msgpack',
  'dic_frequencias_Servico_Social_2017.msgpack',
  'dic_frequencias_Servico_Social_2018.msgpack',
  'dic_frequencias_Servico_Social_2019.msgpack',
  'dic_frequencias_Servico_Social_2020.msgpack',
  'dic_frequencias_Servico_Social_2021.msgpack',
  'dic_frequencias_Servico_Social_2022.msgpack',
  'dic_frequencias_Servico_Social_2023.msgpack'],
 'Sociologia_Politica': ['dic_frequencias_Sociologia_Politica_2003.msgpack',
  'dic_frequencias_Sociologia_Politica_2004.msgpack',
  'dic_frequencias_Sociologia_Politica_2005.msgpack',
  'dic_frequencias_Sociologia_Politica_2006.msgpack',
  'dic_frequencias_Sociologia_Politica_2007.msgpack',
  'dic_frequencias_Sociologia_Politica_2008.msgpack',
  'dic_frequencias_Sociologia_Politica_2009.msgpack',
  'dic_frequencias_Sociologia_Politica_2010.msgpack',
  'dic_frequencias_Sociologia_Politica_2011.msgpack',
  'dic_frequencias_Sociologia_Politica_2012.msgpack',
  'dic_frequencias_Sociologia_Politica_2013.msgpack',
  'dic_frequencias_Sociologia_Politica_2014.msgpack',
  'dic_frequencias_Sociologia_Politica_2015.msgpack',
  'dic_frequencias_Sociologia_Politica_2016.msgpack',
  'dic_frequencias_Sociologia_Politica_2017.msgpack',
  'dic_frequencias_Sociologia_Politica_2018.msgpack',
  'dic_frequencias_Sociologia_Politica_2019.msgpack',
  'dic_frequencias_Sociologia_Politica_2020.msgpack'],
 'Sociologia_e_Ciencia_Politica': ['dic_frequencias_Sociologia_e_Ciencia_Politica_2020.msgpack',
  'dic_frequencias_Sociologia_e_Ciencia_Politica_2021.msgpack',
  'dic_frequencias_Sociologia_e_Ciencia_Politica_2022.msgpack',
  'dic_frequencias_Sociologia_e_Ciencia_Politica_2023.msgpack'],
 'Tecnologias_da_Informacao_e_Comunicacao': ['dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2016.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2017.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2018.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2019.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2020.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2021.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2022.msgpack',
  'dic_frequencias_Tecnologias_da_Informacao_e_Comunicacao_2023.msgpack'],
 'Teses_e_dissertacoes_do_Centro_Tecnologico': ['dic_frequencias_Teses_e_dissertacoes_do_Centro_Tecnologico_2004.msgpack'],
 'Teses_e_dissertacoes_nao_defendidas_na_UFSC': ['dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2003.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2004.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2005.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2006.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2008.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2010.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2012.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2013.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2014.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2015.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2016.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2017.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2018.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2019.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2021.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2022.msgpack',
  'dic_frequencias_Teses_e_dissertacoes_nao_defendidas_na_UFSC_2023.msgpack'],
 'Urbanismo_Historia_e_Arquitetura_da_Cidade': ['dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2007.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2008.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2009.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2010.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2011.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2012.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2013.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2014.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2015.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2016.msgpack',
  'dic_frequencias_Urbanismo_Historia_e_Arquitetura_da_Cidade_2017.msgpack']}

