#%% md
# Link para melhor visualização do Notebook em seu ambiente de execução: [Notebook Colab](https://colab.research.google.com/drive/14d_-xFgDa7DpMRwnem675xVEmmBVkFiq?usp=sharing)
# 
# 
# ---
# 
# 
# 
# Notebook para executar os múltiplos treinamentos com alternância de parâmetros pré-setados e posterior validação usando analogias selecionadas. Assim conseguimos testar diversos parâmetros de treino para um mesmo corpus a ser explorado e verificar quais parâmetros originaram os modelos "mais espertos", que serão usados posteriormente para continuação de mais treinamentos para a construção das séries temporais. Ou seja, neste notebook será treinado diversos modelos para validação dos melhores, mas as séries temporais serão construídas (com e sem atualização de treinamento) posteriormente, em um outro notebook.
# 
# *Observação: Esse notebook foi pensado em ser executado com "execuções paralelas", ou seja, com outros notebooks executando o mesmo código, mas com um identificador (n_programa) diferente, para otimizar o tempo treinando vários modelos.*
#%% md
# # Preparação/Configuração de ambiente
#%%
try:
    import joblib
    import sys
    import os
    import time
    import pandas as pd
    from gensim.models import Word2Vec
    from google.colab import drive
    drive.mount('/content/drive')
    from google.colab import output
    import msgpack
    !pip install ferramentas-basicas-pln -U
    from ferramentas_basicas_pln import formatarTexto,removerCaracteresEspeciais,removerCaracteresEstranhos,removerEspacosEmBrancoExtras,transformarTextoSubstituindoCaracteres,coletarTextoDeArquivoTxt
    from ferramentas_basicas_pln import STRING_CARACTERES_ESPECIAIS_PADRAO
except Exception as e:
    erro = f'{e._class__.__name__}: {str(e)}'
    print(f'Erro ao configurar ambiente:\n--> {erro}')
else:
    print('Ambiente configurado com sucesso!')
#%% md
# # Definição de Funções
#%% md
# Algumas funções não foram utilizadas aqui, pois os códigos deste notebook foram divididos com o notebook de geração de planilha para validação das analogias (básicas e gerais).
#%%
from typing import Generator

def obtemQuestoes(caminho_arquivo_txt_questoes : str = r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/analogias_WOKE.txt',
                  caminho_arquivo_txt_contra_conceitos : str = r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/contra-conceitos_WOKE.txt') -> dict:
  """
  Função responsável por obter e construir uma variável que contemple as
  questões/analogias para validação dos resultados relacionados à acurácia dos
  modelos treinados.

  ### Parâmetros:
  - caminho_arquivo_txt_questoes: String contendo o caminho até o txt com as questões
  relacionadas às analogias.
  - caminho_arquivo_txt_contra_conceitos: String contendo o caminho até o txt de
  questões relacionadas ao teste de captura de contra-conceitos. Esse arquivo é
  para testar uma ideia que apareceu para verificar se algum modelo treinado em
  determinados parâmetros seria capaz de capturar contra-conceitos sendo estes
  praticamente opostos ao vetor do seu conceito, ou seja, vetor do conceito estaria
  a, praticamente, 180 graus do vetor do contra-conceito. Depois de alguns testes
  foi observado que uma tática melhor era usar analogias de conceitos e contra-conceitos
  para tentar mensurar esse tipo de desempenho nos modelos treinados.

  ### Retornos:
  - Dicionário com as questões organizadas em "similaridade-positiva" (caso queiramos
  validar simplesmente os vizinhos mais próximos de detemrinados tokens), "analogias"
  para testar, de fato, as analogias, "similaridade-negativa" para fazer a verificação
  dos contra-conceitos. Cada parte dita anteriormente possuíra temas e dentro de
  cada tema terá uma lista com as "questões".
  """
  # Obtenção do texto referente às questões propostas
  txt_questoes = coletarTextoDeArquivoTxt(caminho_arquivo=caminho_arquivo_txt_questoes,tipo_de_encoding='utf-8').lower()

  # Criação da variável dicionário que armazenará as questões com seus respectivos tipos/temas
  dic_questoes = {'similaridade-positiva':{},'analogia':{}}

  # Para cada linha de questão dentro do texto de questões
  for linha in [line.strip() for line in txt_questoes.split('\n') if line.strip() != '']:
    if linha.startswith(':'): # Se o início da linha for ":" sabe-se que é uma linha que faz referência a um tema
      tema = linha[1:].strip()
      dic_questoes['analogia'][tema] = [] # Cria-se uma estrutura dentro do dicionário que irá armazenar as questões para este tema (que estarão abaixo da linha do tema no arquivo de texto)
    else:
      questao = [palavra.strip() for palavra in linha.lower().split(',') if palavra.strip() != ''] # Criação da lista referente à questão
      if len(questao) == 4: # Se a lista tiver 4 elementos, quer dizer que é uma analogia a ser inputada no dicionário de questões
        dic_questoes['analogia'][tema].append(questao)
      # Posteriormente, a validação por meio de vizinhos mais próximos onde a lista referente a questão teria 2 elementos foi desconsiderada

  # Alternativa para capturar contra-conceitos
  txt_questoes_similaridade_negativa = coletarTextoDeArquivoTxt(caminho_arquivo=caminho_arquivo_txt_contra_conceitos,tipo_de_encoding='utf-8').lower()
  dic_questoes['similaridade-negativa'] = {'contra-conceitos':[]}
  for linha in [l.strip() for l in txt_questoes_similaridade_negativa.split('\n') if l.strip() != '']:
    questao = [palavra.strip() for palavra in linha.lower().split(',') if palavra.strip() != '']
    if len(questao) > 1:
      dic_questoes['similaridade-negativa']['contra-conceitos'].append(questao)

  return dic_questoes


def validarQuestoesBasicas(modelo,
                           incluido_no_topn : int = 5,
                           caminho_arquivo_txt_questoes_basicas : str = r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/analogias_basicas_WOKE.txt',
                           silence : bool = True):
    """
    Função responsável por realizar a validação das questões básicas. Ou seja,
    retornará True caso o modelo acerte todas as questões básicas ou False caso
    erre alguma.

    ### Parâmetros:
    - modelo: Modelo Word2Vec a ser testado nas analogias básicas.
    - incluido_no_topn: Inteiro responsável por restringir a resposta das analogias.
    - caminho_arquivo_txt_questoes_basicas: String contendo o caminho até o arquivo
    de texto que consta as analogias básicas.
    - silence: Bool que printará (True) ou não (False) na tela de output se o modelo
    em questão errou ou não alguma analogia.

    ### Retornos:
    - Bool responsável por dizer se o modelo em questão acertou todas as analogias
    básicas (True) ou não (False).
    """
    txt_questoes_questoes_basicas = coletarTextoDeArquivoTxt(caminho_arquivo=caminho_arquivo_txt_questoes_basicas,tipo_de_encoding='utf-8').lower()
    for linha in [l.strip() for l in txt_questoes_questoes_basicas.split('\n') if l.strip() != '']:
      questao = [palavra.strip() for palavra in linha.lower().split(',') if palavra.strip() != '']

      if len(questao) == 4:
        try:
          resultado = [r[0] for r in modelo.wv.most_similar_cosmul(positive=[questao[1],questao[2]],negative=[questao[0]],topn=incluido_no_topn)]
          acertou = False
          for resposta_certa in questao[3].split('|'):
            if resposta_certa in resultado:
              acertou = True
              break
          if not acertou:
            if not silence:
              print(f'\nErrou: {str(questao)}, resultado: {str(resultado)}')
            return False
        except Exception as e:
          return False

      # # Testando similaridade positiva
      # if len(questao) == 2:
      #   try:
      #     resultado = [r[0] for r in modelo.wv.most_similar(questao[0],topn=incluido_no_topn)]
      #     acertou = False
      #     for resposta_certa in questao[1].split('|'):
      #       if resposta_certa in resultado:
      #         acertou = True
      #         break
      #     if not acertou:
      #       if not silence:
      #         print(f'\nErrou: {str(questao)}, resultado: {str(resultado)}')
      #       return False
      #   except Exception as e:
      #     return False


    # Caso o modelo acerte todas
    return True


def Comparacao(modelo, homem, rei, mulher):
  """
  Função responsável por realizar a comparação (analogia) e retornar o resultado.
  Os parâmetros estão pensados no seguinte tipo de analogia:

  homem   -->   rei
  mulher  -->    X

  Sendo X o resultado que deseja-se obter.

  ### Parâmetros:
  - modelo: Modelo Word2Vec o qual quer se extrair o resultado de alguma analogia.
  - homem: String que substituirá o token "homem" na analogia.
  - rei: String que substituirá o token "rei" na analogia.
  - mulher: String que substituirá o token "mulher" na analogia.

  ### Retornos:
  - Lista de strings em ordem de resultado (top 3) para a analogia dada como entrada.
  """
  try:
    resultado = [resultado[0] for resultado in modelo.wv.most_similar_cosmul(positive=[rei,mulher],negative=[homem],topn=3)]
    return resultado
  except Exception as e:
    return []

def Similaridade(modelo, palavra):
  """
  Função responsável por realizar a obtenção dos vizinhos mais próximos de um token
  num determinado modelo.

  ### Parâmetros:
  - modelo: Modelo Word2Vec o qual quer se extrair o resultado dos vizinhos mais
  próximos do token/palavra dado como entrada.
  - palavra: String contendo o token/palavra que deseja-se buscar os vizinhos mais
  próximos.

  ### Retornos:
  - Lista de strings em ordem de resultado (top 3) para os vizinhos mais próximos
  do token dado como entrada.
  """
  try:
    resultado = [resultado[0] for resultado in modelo.wv.most_similar(palavra,topn=3)]
    return resultado
  except Exception as e:
    return []

def SimilaridadeNegativaTestada(modelo, questao):
  """
  Função responsável por realizar o teste de similaridade negativa de uma questão
  num determinado modelo. A questão vem no formato ["token1","token2|token3"],
  onde "token1" é o token o qual será comparado à similaridade com os demais "token2"
  e "token3" (neste exemplo). Ou seja, será comparado a similaridade:
  similarity(token1,token2) e similarity(token1,token3) e os resultados retornados.

  ### Parâmetros:
  - modelo: Modelo Word2Vec o qual quer se extrair as similaridades entre os tokens
  dados na questão de entrada.
  - questao: Lista de dois elementos (do tipo string) sendo o primeiro elemento
  o token que deseja se obtem a similaridade entre os demais que estão no segundo
  elemento da lista (caso desejar comparar mais de um token separá-los pelo caracter
  "|". Exemplo: questao = ["historia","matemática|física"] ).

  ### Retornos:
  - Lista contendo as similaridades (na ordem dos tokens da questao) referentes
  à questão dada como entrada.
  """
  lista_similaridades = []
  for resposta_certa in questao[-1].split('|'):
    try:
      lista_similaridades.append(modelo.wv.similarity(questao[0],resposta_certa))
    except Exception as e:
      pass
  return lista_similaridades

def validaResultadoSimilaridadeNegativaTestada(lista_respostas_similaridades : list[float],
                                               valor_minimo : float = -0.8) -> int:
  """
  Função responsável por verificar (retornando True/False) se o menor valor na
  lista de similaridades é menor do que o valor mínimo pré-setado (-0,8). Caso
  isso ocorra retorna True, caso contrário False.

  ### Parâmetros:
  - lista_respostas_similaridades: Lista de elementos do tipo float referente à
  lista de similaridades entre tokens.
  - valor_minimo: float (geralmente negativo) para comparar com o menor valor obtido
  na lista de similaridades.

  ### Retornos:
  - Bool: True se existir um valor menor que o valor mínimo na lista de similaridades,
  ou False caso não existir.
  """
  if min(lista_respostas_similaridades) < valor_minimo:
    return 3
  else:
    return 0

def SimilaridadeNegativaReal(modelo, palavra):
  """
  Função responsável por obter os top 3 vizinhos menos próximos (via similaridade)
  de uma palavra/token num determinado modelo.

  ### Parâmetros:
  - modelo: Modelo Word2Vec o qual se deseja extrair as informações.
  - palavra: String contendo o token que se deseja extrair os top 3 vizinhos menos
  próximos.

  ### Retornos:
  - Lista de strings contendo os top 3 vizinhos menos próximos já na ordem do menos
  próximo pro mais próximo.
  """
  max_size = len(modelo.wv.index_to_key)
  try:
    # Pode-se tentar usar topn=None para retornar a lista inteira de vizinhos mais próximos também
    resultado = [r[0] for r in modelo.wv.most_similar(palavra,topn=max_size)][-3:] # [-3:] pegamos somente os 3 últimos da lista (os "menos" similares ou seja, menos próximos de 1, mais próximos de -1)
    resultado.reverse()
    return resultado
  except Exception as e:
      return []

def ValidaResultado(gabarito : list, resposta : list):
  """
  Função responsável por fazer a validação de um resultado obtido de acordo com
  um gabarito esperado no resultado. O resultado pode ter mais de uma resposta,
  as quais serão comparadas com a resposta esperada do gabarito.

  ### Parâmetros:
  - gabarito: Lista de strings que seria o gabarito de uma questão.
  - resposta: Lista de strings obtida como resultado de uma questão.

  ### Retornos:
  - Inteiro 3, 1 ou 0 que faz referência à acerto total (algum resultado bateu com
  o gabarito), acerto parcial (o gabarito estava presente na segunda ou terceira
  posição do resultado) ou resposta errada (resultado não bateu com o gabarito),
  respectivamente.
  """
  if '|' in gabarito[-1]:
    respostas_certas = gabarito[-1].split('|')
    for resposta_certa in respostas_certas:
      if resposta_certa == resposta[0]:
        return 3
    for resposta_certa in respostas_certas:
      if resposta_certa in resposta[1:]:
        return 1
    return 0

  else:
    resposta_certa = gabarito[-1]
    if resposta_certa == resposta[0]:
      return 3
    elif resposta_certa in resposta[1:]:
      return 1
    return 0

def montarDicResultados(modeloW2V,
                        dic_questoes : dict) -> dict:
  """
  Função responsável por construir um dicionário de resultados para as questões.

  ### Parâmetros:
  - modeloW2V: Modelo Word2Vec que está se testando no momento.
  - dic_questoes: Dicionário contendo as questões que serão testadas/validadas.

  ### Retornos:
  - Dicionário contendo as questões e suas devidas pontuações para um determinado
  modelo.
  """
  dic_resultados = {'similaridade-positiva':{},'analogia':{}}

  for tema in dic_questoes['similaridade-positiva']:

    dic_resultados['similaridade-positiva'][tema] = {}

    for questao in dic_questoes['similaridade-positiva'][tema]:

      resultado = Similaridade(modeloW2V,questao[0])
      if resultado:
        pontuacao = ValidaResultado(questao,resultado)
      else:
        pontuacao = 0

      dic_resultados['similaridade-positiva'][tema][', '.join(questao).replace("'","")] = pontuacao

  for tema in dic_questoes['analogia']:

    dic_resultados['analogia'][tema] = {}

    for questao in dic_questoes['analogia'][tema]:

      resultado = Comparacao(modeloW2V,questao[0],questao[1],questao[2])
      if resultado:
        pontuacao = ValidaResultado(questao,resultado)
      else:
        pontuacao = 0

      dic_resultados['analogia'][tema][', '.join(questao).replace("'","")] = pontuacao


  dic_resultados['similaridade-negativa op1'] = {}

  for tema in dic_questoes['similaridade-negativa']:

    dic_resultados['similaridade-negativa op1'][tema] = {}

    for questao in dic_questoes['similaridade-negativa'][tema]:
      resultado = SimilaridadeNegativaReal(modeloW2V,questao[0])
      if resultado:
        pontuacao = ValidaResultado(questao,resultado)
      else:
        pontuacao = 0

      dic_resultados['similaridade-negativa op1'][tema][', '.join(questao).replace("'","")] = pontuacao

  dic_resultados['similaridade-negativa op2'] = {}

  for tema in dic_questoes['similaridade-negativa']:

    dic_resultados['similaridade-negativa op2'][tema] = {}

    for questao in dic_questoes['similaridade-negativa'][tema]:
      resultado = SimilaridadeNegativaTestada(modelo=modeloW2V,questao=questao)
      if resultado:
        pontuacao = validaResultadoSimilaridadeNegativaTestada(lista_respostas_similaridades=resultado)
      else:
        pontuacao = 0

      dic_resultados['similaridade-negativa op2'][tema][', '.join(questao).replace("'","")] = pontuacao

  return dic_resultados

def salvarResultadosEmMsgPack(nome_variavel : str,
                              variavel_em_questao,
                              pasta_para_salvar : str) -> tuple[bool,str]:
    """
    Função responsável por salvar, no formato "msgpack", alguma variável deste
    ambiente numa pasta especificada.

    ### Parâmetros:
    - nome_variavel: String contendo o nome da variável que será dado ao arquivo.
    - variavel_em_questao: Variável propriamente dita que se deseja salvar num
    arquivo.
    - pasta_para_salvar: String contendo o caminho até a pasta onde se deseja
    salvar o arquivo da variável em questão.

    ### Retornos:
    - Tupla com dois elementos. O primeiro do tipo bool que faz referência ao
    status do processo (True bem sucedido, False falhou) e o segundo do tipo
    string contendo a mensagem referente ao status obtido.
    """
    try:
        # Se a pasta não existir, efetuamos sua criação
        if not os.path.exists(pasta_para_salvar):
            os.makedirs(pasta_para_salvar)

        # Obtendo os bytes da variável que queremos salvar
        variable_bytes = msgpack.packb(variavel_em_questao)

        # Se o nome do arquivo que salvará a variável não tiver o formato msgpack ao final, iremos adicioná-lo.
        if not nome_variavel.endswith('.msgpack'):
            nome_variavel += '.msgpack'

        # Salvando a variável desejada em bytes no formato .msgpack
        with open(os.path.join(pasta_para_salvar,nome_variavel),'wb') as f:
            f.write(variable_bytes)
            f.close()
            return True, f'Variável {nome_variavel} salva com sucesso no formato .msgpack'

    # Caso ocorra algum erro inesperado, trataremos o enviando como mensagem de falha juntamente com um status False (de falha/erro no processo)
    except Exception as e:
        error_message = f'{e.__class__.__name__}: {str(e)}'
        return False, error_message

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

def organizarAmbienteDeTreinos(nome_pasta_treino : str,
                               escopo_de_treinamento : tuple[list[str],tuple[int,int]],
                               reset_arquivo_txt_mapa_treinos : bool = False,
                               caminho_pasta_para_arquivo_txt_mapa_treinos : str = r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/Resultados Múltiplos Treinamentos') -> tuple[bool,str]:

  """
  Função responsável por efetuar a organização das pastas para deixar o ambiente
  preparado para salvar as pastas e os arquivos de treinamento.

  ### Parâmetros:
  - nome_pasta_treino: String contendo o nome da pasta de treino.
  - escopo_de_treinamento: Tupla de dois elementos sendo o primeiro uma lista das
  coleções que serão contempladas neste treinamento e o segundo uma outra tupla
  de dois inteiros do ano inicial e ano final, respectivamente, para o treinamento.
  - reset_arquivo_txt_mapa_treinos: Bool que dirá se deve-se apagar ou não o arquivo
  de informação dos treinos já efetuados.
  - caminho_pasta_para_arquivo_txt_mapa_treinos: Caminho até o corpus pré-processado
  onde será buscado as coleções, anos, trabalhos e arquivos de pré-processamento
  para alimentação do treinamento.

  ### Retornos:
  - Tupla com elemento do tipo bool (status do processo) e elemento do tipo string
  sendo uma mensagem referente ao status (True deu tudo certo e False ocorreu um
  erro).
  """
  caminho_arquivo_txt_mapa_treinos = os.path.join(caminho_pasta_para_arquivo_txt_mapa_treinos,'Mapa dos Treinos.txt')
  try:
    string_escopo_treino = '--> Coleções:\n'+'\n'.join(escopo_de_treinamento[0])+f"\n--> Datas contempladas:\nDe {escopo_de_treinamento[1][0]} até {escopo_de_treinamento[1][1]}.\n\n"
    if (not os.path.exists(caminho_arquivo_txt_mapa_treinos)) or reset_arquivo_txt_mapa_treinos:
      with open(caminho_arquivo_txt_mapa_treinos,'w',encoding='utf-8') as f:
          f.write('='*(len('MAPA DE TREINOS')+4)+'\n'+'  MAPA DE TREINOS  \n'+'='*(len('MAPA DE TREINOS')+4)+'\n\n')
    if not os.path.exists(caminho_arquivo_txt_mapa_treinos.replace(os.path.basename(caminho_arquivo_txt_mapa_treinos),nome_pasta_treino)):
      os.makedirs(caminho_arquivo_txt_mapa_treinos.replace(os.path.basename(caminho_arquivo_txt_mapa_treinos),nome_pasta_treino))
      with open(caminho_arquivo_txt_mapa_treinos,'a',encoding='utf-8') as f:
          f.write('\n'+nome_pasta_treino+'\n'+'-'*100+'\n'+string_escopo_treino+'\n\n')
    return True, ''
  except Exception as e:
    return False, e.__class__.__name__ + ': ' +str(e)

def validarResultados(modeloW2V,
                      nome_modelo : str,
                      dic_questoes : dict,
                      pasta_para_salvar_resultados : str) -> dict:

  """
  Função responsável por obter e salvar os resultados para as questões de um determinado
  modelo.

  ### Parâmetros:
  - modeloW2V: Modelo Word2Vec que deseja-se validar os resultados para as questões.
  - nome_modelo: String contendo o nome do modelo que está se testando/validando.
  - dic_questoes: Dicionário contendo as questões que serão testadas.
  - pasta_para_salvar_resultados: String contendo o caminho até a pasta que será
  salvo os resultados para as questões do determinado modelo em questão.

  ### Retornos:
  - Tupla de dois elementos sendo o primeiro o status da validação de resultados
  (True se ocorreu tudo certo e False caso tenha ocorrido algum erro) e o segundo
  uma string contendo a mensagem referente ao status do processo (em caso de falha
  retorna o erro junto).
  """

  dic_resultados = montarDicResultados(modeloW2V=modeloW2V,dic_questoes=dic_questoes)

  status_save, msg_save = salvarResultadosEmMsgPack(nome_variavel=nome_modelo,variavel_em_questao=dic_resultados,pasta_para_salvar=pasta_para_salvar_resultados)

  if status_save:
    return True,'Resultados do treino salvos com sucesso!'
  else:
    return False,'\n! Problema ao salvar resultados do treino: '+msg_save+'\n'


class GeradorCorpusTokenizado:
    """
    Classe geradora de corpus amigável à memória RAM. Utiliza-se de iterador e gerador
    para não saturar a RAM do sistema que for executá-la. Desta forma não é necessário
    carregar todos os textos de todos os trabalhos e passar como parâmetros de frases
    na hora de treinar os modelos, pois a função de treino só precisa de um objeto
    "iterável" no parâmetro de frases (sentences). Sendo geradora só será carregado
    na RAM o texto que está se passando no momento ao invés do corpus de textos
    todos juntos ao mesmo tempo.

    ### Parâmetros:
    - intervalo_anos: Tupla de dois inteiros referentes ao ano de início e final
    da escrita dos textos que serão inseridos no corpus de alimentação de treino
    (ambos os extremos incluídos no intervalo).
    - colecoes: Lista de strings referentes às coleções que serão contempladas
    na criação do corpus de alimentação de treino.
    - caminho_pasta_colecoes_tokenizadas: Caminho até o corpus pré-processado onde
    será buscado as coleções, anos, trabalhos e arquivos de pré-processamento para
    alimentação do treinamento.
    - usando_reconhecimento_de_entidades: Bool que dirá se os arquivos de pré-processamento
    procurados serão os que usaram (True) ou não (False) o reconhecimento de entidades
    nos textos (atualmente o pré-processamento que foi totalmente concluído foi
    utilizando o reconhecimento de entidades).

    ### Retornos:
    - Objeto gerador e iterável sobre o corpus de textos contemplados pelos parâmetros
    ("intervalo_anos" e "colecoes") passados como entrada.
    """

    def __init__(self, intervalo_anos : tuple[int,int], usando_reconhecimento_de_entidades : bool = True, colecoes : list[str] | str ='todas', caminho_pasta_colecoes_tokenizadas : str =r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Textos_pre_processados/Colecoes_textos_pre_processados'):
        self.intervalo_anos = range(intervalo_anos[0], intervalo_anos[1] + 1)
        self.usando_reconhecimento_de_entidades = usando_reconhecimento_de_entidades
        if usando_reconhecimento_de_entidades:
            self.arquivo_pre_processamento = 'pre_processamento_c_re.msgpack'
        else:
            self.arquivo_pre_processamento = 'pre_processamento_s_re.msgpack'
        if isinstance(colecoes, str):
            if colecoes.lower() == 'todas':
                colecoes = [c for c in os.listdir(caminho_pasta_colecoes_tokenizadas) if '.' not in c]
        self.arquivos = []
        for colecao in [os.path.join(caminho_pasta_colecoes_tokenizadas, c) for c in os.listdir(caminho_pasta_colecoes_tokenizadas) if c in colecoes]:
            lista_anos = sorted([a for a in os.listdir(colecao) if a.isdigit()])
            for ano in [os.path.join(colecao, a) for a in lista_anos if int(os.path.basename(a)) in self.intervalo_anos]:
                for trabalho in [os.path.join(ano, t) for t in os.listdir(ano) if t.startswith('Trabalho')]:
                    for arquivo in [os.path.join(trabalho, arq) for arq in os.listdir(trabalho) if arq == self.arquivo_pre_processamento]:
                        self.arquivos.append(arquivo)

    def __iter__(self):
        for cont,arquivo in enumerate(self.arquivos):
            for frase_tokenizada in abrirArquivoMsgPack(arquivo):
                yield frase_tokenizada

def listagemDeParametros(lista_de_trabalhos : list,
                        n_programa : int,
                        numero_max_programas : int = 33) -> list:
  """
  Função responsável por dividir os conjuntos de parâmetros de um determinado treino
  nos programas que irão executar estes códigos.

  ### Parâmetros:
  - lista_de_trabalhos: Lista de dicionários que conterão os parâmetros de um determinado
  treino.
  - n_programa: Inteiro referente ao número do programa que está sendo executado.
  - numero_max_programas: Inteiro referente ao número total de programas que irão
  executar estes códigos.

  ### Retornos:
  - Lista de dicionários referentes aos conjuntos de parâmetros de treino que este
  programa irá executar.
  """
  dic_programas_trabalhos = {}
  for i in range(1,numero_max_programas+1):

    dic_programas_trabalhos[f'Prog {i}'] = []

  for i in range(len(lista_de_trabalhos)):
    if (i+1) <= numero_max_programas:
      num = i + 1
      dic_programas_trabalhos[f'Prog {num}'].append(lista_de_trabalhos[i])
    else:
      if (i+1)%numero_max_programas != 0:
        num = (i+1)%numero_max_programas
        dic_programas_trabalhos[f'Prog {num}'].append(lista_de_trabalhos[i])
      else:
        num = numero_max_programas
        dic_programas_trabalhos[f'Prog {num}'].append(lista_de_trabalhos[i])
  return dic_programas_trabalhos[f'Prog {n_programa}']

#%% md
# # Teste com validação de construção de corpus com iterador - gerador
#%% md
# **Execução para testar a construção de corpus com iterador-gerador**
#%% md
# Usando lógica implementada
#%%
lista_de_colecoes = ['Biologia_Celular_e_do_Desenvolvimento','Biotecnologia_e_Biociencias','Ciencias_da_Reabilitacao','Ciencias_Medicas','Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional',
                     'Educacao_Fisica','Enfermagem','Gestao_do_Cuidado_em_Enfermagem','Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional','Medicina_Veterinaria_Convencional_e_Integrativa',
                     'Neurociencias','Saude_Coletiva','Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional','Saude_Publica','Programa_de_Pos_Graduacao_Multidisciplinar_em_Saude_Mestrado_Profissional']

intervalo_de_datas = (2003,2010)

corpus_tokenizado = GeradorCorpusTokenizado(intervalo_anos=intervalo_de_datas,
                                            colecoes = lista_de_colecoes)

modelo = Word2Vec(sentences=corpus_tokenizado,vector_size=2,window=2,negative=2,epochs=1,min_count=1,workers=94)

print(modelo.corpus_total_words)
len(modelo.wv.index_to_key)
#%% md
# Usando contagem diretamente no corpus pré-processado
#%%
caminho_colecoes = r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Textos_pre_processados/Colecoes_textos_pre_processados'

lista_de_colecoes = ['Biologia_Celular_e_do_Desenvolvimento','Biotecnologia_e_Biociencias','Ciencias_da_Reabilitacao','Ciencias_Medicas','Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional',
                     'Educacao_Fisica','Enfermagem','Gestao_do_Cuidado_em_Enfermagem','Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional','Medicina_Veterinaria_Convencional_e_Integrativa',
                     'Neurociencias','Saude_Coletiva','Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional','Saude_Publica','Programa_de_Pos_Graduacao_Multidisciplinar_em_Saude_Mestrado_Profissional']

intervalo_de_datas = (2003,2010)


if lista_de_colecoes == 'todas':
  colecoes = [os.path.join(caminho_colecoes,c) for c in os.listdir(caminho_colecoes) if '.' not in c]
else:
  colecoes = [os.path.join(caminho_colecoes,c) for c in os.listdir(caminho_colecoes) if c in lista_de_colecoes]
tokens = 0
# arquivos = 0
# frases = 0
dic_vocab = {}
for colecao in colecoes:
  anos = sorted([os.path.join(colecao,a) for a in os.listdir(colecao) if (a.isdigit()) and (a in [str(an) for an in range(intervalo_de_datas[0],intervalo_de_datas[1]+1)])])
  for ano in anos:
    trabs = [os.path.join(ano,t) for t in os.listdir(ano) if t.startswith('Trabalho')]
    for trab in trabs:
      if os.path.exists(os.path.join(trab,'pre_processamento_c_re.msgpack')):
        arquivo = os.path.join(trab,'pre_processamento_c_re.msgpack')
        # arquivos += 1
        lista_de_frases_tokenizadas = abrirArquivoMsgPack(arquivo)
        # frases += len(lista_de_frases_tokenizadas)
        # print('Arquivo',arquivos,'qtd frases',len(lista_de_frases_tokenizadas))
        # t = 0
        for frase_tokenizada in lista_de_frases_tokenizadas:
          tokens += len(frase_tokenizada)
          for token in frase_tokenizada:
            if token not in dic_vocab.keys():
              dic_vocab[token] = 1
            else:
              dic_vocab[token] += 1
          # t += len(frase_tokenizada)
        # print('tokens',t)
    output.clear()
    print(os.path.basename(colecao))
    print(os.path.basename(ano))
    print('{0:,}'.format(tokens).replace(',','.'))
    print('vocab: {0:,}'.format(len(dic_vocab.keys())).replace(',','.'))
# print('arquivos',arquivos)
print('tokens:','{0:,}'.format(tokens).replace(',','.'))
# print('frases',frases)
#%% md
# Validação da quantidade no vocab de acordo com min_count (no caso se o min_count no treino for 25 botamos como condição dentro da list comprehensive "if dic_vocab[chave] >= 25")
#%%
len([chave for chave in dic_vocab.keys() if dic_vocab[chave] >= 25])
#%% md
# # Teste de treinamento com construção de corpus (parâmetros)
#%% md
# ## Execução para testar a construção de corpus com iterador-gerador usando corpus de teste (documentos criados manualmente)
#%%
corpus_tokenizado = GeradorCorpusTokenizado(intervalo_anos=(2004,2005),caminho_pasta_colecoes_tokenizadas=r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Textos_tokenizados/Colecoes_Teste',
                                            colecoes = ['Colecao_1','Colecao_4'])

for r in corpus_tokenizado:
  print(r)
modelo = treinarModelo(corpus=corpus_tokenizado,modo=0,dimensao=2,negative=1,window=2,epochs=3,min_count=1,alpha=0.025)
#%% md
# ## Validação da lógica implementada para separação dos diversos treinamentos com parâmetros diferentes
#%%
modos = [1,0]
dimensoes = [100,300,500] # Alterar ao redor do valor da raiz quadrada do total de tokens no vocab.
negatives = [5,10]
windows = [8,12] # 8 pra cima
epochss = [5] # Diminuir as epochs
alphas = [0.025]
min_counts = [60,100]

lista_parametros = []
for modo in modos:
  for dimensao in dimensoes:
    for negative in negatives:
      for window in windows:
        for epochs in epochss:
          for alpha in alphas:
            for min_count in min_counts:
              lista_parametros.append(str([modo,dimensao,negative,window,epochs,alpha,min_count]))

print(len(lista_parametros))
print(len(set(lista_parametros)))
#%%
lista_total = []
for n in range(1,4):
  # print(n)
  lista_atual = listagemDeParametros(lista_de_trabalhos=lista_parametros,n_programa=n,numero_max_programas=3)
  lista_total += lista_atual
  print(len(lista_atual))

print(len(lista_total))
print(len(set(lista_total)))
#%% md
# # Execução
#%% md
# Nesta execução deverá ser escolhido, antes de executar, as coleções e as datas de início e fim para construção de corpus, o qual será alimentado no treinamento dos modelos.
#%%
## # Escolha das coleções que construirão o corpus para alimentar o treinamento.

# UFSC (todas as coleções)
# lista_de_colecoes = "todas"

# CFH (somente coleções do Centro de Filosofia e Ciências Humanas)
# lista_de_colecoes = ['Filosofia','Geografia','Geologia','Historia','Psicologia','Teses_e_dissertacoes_do_Centro_de_Filosofia_e_Ciencias_Humanas','Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas','Servico_Social','Sociologia_e_Ciencia_Politica','Sociologia_Politica','Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional','Ensino_de_Historia_Mestrado_Profissional'] # Corpus CFH

# HST (comente textos da coleção de História)
# lista_de_colecoes = ['Historia']

# SAUDE-CORPO (somente coleções voltadas para saúde e corpo num geral)
lista_de_colecoes = ['Biologia_Celular_e_do_Desenvolvimento','Biotecnologia_e_Biociencias','Ciencias_da_Reabilitacao','Ciencias_Medicas','Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional',
                     'Educacao_Fisica','Enfermagem','Gestao_do_Cuidado_em_Enfermagem','Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional','Medicina_Veterinaria_Convencional_e_Integrativa',
                     'Neurociencias','Saude_Coletiva','Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional','Saude_Publica','Programa_de_Pos_Graduacao_Multidisciplinar_em_Saude_Mestrado_Profissional'] # Corpus SAUDE-CORPO

# Escolha dos anos que serão contemplados na construção desse corpus de coleções escolhidas
intervalo_de_datas = (2003,2010)

# Variável que vai carregar as configurações da construção do corpus de treinamento para o escopo desse treinamento (coleções e anos desejados)
escopo_treinamento = (lista_de_colecoes,
                      intervalo_de_datas)

# Seleção do nome da pasta de treino
nome_pasta_treino = 'Saude-do-Corpo-03-10'

# Organização do ambiente de treino
status_organizacao, msg_organizacao = organizarAmbienteDeTreinos(nome_pasta_treino=nome_pasta_treino,escopo_de_treinamento=escopo_treinamento,reset_arquivo_txt_mapa_treinos=False) # Depois do primeiro treino "valendo", setar o reset_arquivo_txt_mapa_treinos=False pra não excluir o histórico dos treinos passados

# Identificador da numeração do programa que está executando este notebook (também será usado "execuções" paralelas com outras contas para este programa)
n_programa = 1

# Geração do corpus de treinamento (que será usado para alimentar os treinos)
corpus_tokenizado = GeradorCorpusTokenizado(intervalo_anos=intervalo_de_datas,
                                            colecoes = lista_de_colecoes)

# Importação e instanciação da quantidade de threads disponíveis para execuções em paralelo no processador (usado pela função de treino do Word2Vec para treinar mais rápido)
from gensim.utils import effective_n_jobs
n_workers = effective_n_jobs(-1)

if status_organizacao:
  # Ambiente no Drive que irá salvar os modelos treinados
  pasta_para_salvar_treinamentos = os.path.join(r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/Resultados Múltiplos Treinamentos',nome_pasta_treino)
  if not os.path.exists(pasta_para_salvar_treinamentos):
    os.makedirs(pasta_para_salvar_treinamentos)

  # Ambiente no Drive que irá salvar os resultados da analogias para os modelos treinados (atualmente está sendo usado outro programa que realiza a validação das analogias separadamente, com analogias básicas e analogias gerais)
  pasta_para_salvar_resultados = os.path.join(r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/Resultados Múltiplos Treinamentos',nome_pasta_treino+' - Resultados')
  if not os.path.exists(pasta_para_salvar_resultados):
    os.makedirs(pasta_para_salvar_resultados)

  # Obtenção das questões referentes às analogias que farão a validação da acurácia dos modelos treinados
  dic_questoes = obtemQuestoes()

  # Todos os diferentes parâmetros interessantes de serem testados estão abaixo
  # modos = [0,1]
  # dimensoes = [25,50,80,100,120,150,180,200,220,250,280,300,350,380,400,420,450,480,500]
  # negatives = [5,10,15,20]
  # windows = [4,6,8,10,12,14]
  # epochss = [3,5,8,10]
  # alpha = [0.01,0.025,0.05]
  # min_counts = [1,10,20,30,40,50,60,70,100]


  # Escolha de parâmetros que irão variar ao decorrer dos treinos
  modos = [1,0] # 1 = Skip-Gram e 0 = CBOW
  dimensoes = [80,100,150,200,250,300,350] # Alterar ao redor do valor da raiz quadrada do total de tokens no vocab.
  negatives = [5,10] # Quantidade de amostras negativas
  windows = [4,8,12] # 8 pra cima - Janela de contexto
  epochss = [2,3,5] # Diminuir as epochs - Quantidade de vezes que irá passar pelo corpus selecionado para estes treinos
  alphas = [0.025] # Taxa de aprendizado
  min_counts = [15,20,30,45,60] # Mínima ocorrência que um token tem que ter no corpus para entrar pro treinamento

  # Construção de uma lista de dicionários que armazenarão as informações dos parâmetros de treinos
  lista_dics_parametros = []
  for modo in modos:
    for dimensao in dimensoes:
      for negative in negatives:
        for window in windows:
          for epochs in epochss:
            for alpha in alphas:
              for min_count in min_counts:
                lista_dics_parametros.append({'modo':modo,'dimensao':dimensao,'negative':negative,'window':window,'epochs':epochs,'alpha':alpha,'min_count':min_count})

  # Separação dos treinos (com seus respectivos parâmetros) entre os programas que irão executar esta etapa
  lista_dics_parametros_atual = listagemDeParametros(lista_dics_parametros,n_programa,numero_max_programas=3)

  # Obtenção da quantidade de "diversificação" de treinos para este programa
  qtd_dics_parametros = len(lista_dics_parametros_atual)

  # Execução de treino por treino colocando seus parâmetros na função de treinamento do Word2Vec
  for contagem,dic in enumerate(lista_dics_parametros_atual): # contagem para saber em que treino estamos de todos os treinamentos que serão efetuados e dic é o dicionário que armazenará as informações dos parâmetros do treino atual
    print(contagem+1,'de',qtd_dics_parametros)
    # Nomeando o treino atual com os parâmetros que este usará para construir o modelo
    nome_modelo_atual = f"modelo_modo_{dic['modo']}_dimensao_{dic['dimensao']}_negative_{dic['negative']}_window_{dic['window']}_epochs_{dic['epochs']}_alpha_{dic['alpha']}_min_count_{dic['min_count']}"
    if not os.path.exists(os.path.join(pasta_para_salvar_treinamentos,nome_modelo_atual+'.model')): # Se o treino não tiver sido feito ainda (isso serve para continuar a execução deste notebook caso ele seja encerrado/cancelado antes de finalizar todos os treinos)
      print('TREINANDO:',nome_modelo_atual)
      ini = time.time()
      # Função de treinamento de modelos Word2Vec preenchendo os parâmetros que iremos modificar (os outros parâmetros serão usados os padrões provenientes da função Word2Vec da gensim)
      modelo = Word2Vec(sentences=corpus_tokenizado,vector_size=dic['dimensao'],
                        alpha=dic['alpha'],negative=dic['negative'],
                        window=dic['window'],epochs=dic['epochs'],
                        min_count=dic['min_count'],sg=dic['modo'],
                        workers=n_workers)

      # IMPORTANTE!
      # Foi pensado em não salvar TODOS os treinamentos efetuados, pois modelos
      # treinados no corpus inteiro da UFSC ocupariam muito espaço se ocorresse
      # uma grande quantidade de treinos. Tendo isso em vista, foi pensado em criar
      # uma espécie de validação mínima em que o modelo treinado teria que passar
      # para então ser salvo em nossas pastas de modelos treinados. Para isso foi
      # criado uma lista de analogias básicas que o modelo deveria acertar todas.
      # Infelizmente, essa ideia não foi pra frente porque (nos testes observados)
      # nenhum modelo passava com 100% de acerto em todas as analogias, por mais
      # que a considerássemos como básica. Por mais que a gente tentasse deixar
      # o mais simples, não temos como ter conhecimento total de quais assuntos
      # serão tratados minimamente bem e quais não serão, muito menos possíveis
      # misturas de significado entre as diferentes formas de se tratar a mesma
      # palavra em diferentes cenários (como "potência" na física/elétrica e potência
      # na história/geopolítica). Desta forma, como foi comprado 2TB de armazenamento
      # no Drive, optamos por salvar todos os treinamentos e depois usar apenas
      # os que melhor desempenhassem nas analogias gerais. Por isso o bloco de códigos
      # abaixo está comentado.

      # print(modelo.corpus_count)
      # if validarQuestoesBasicas(modelo,silence=False):
      #   modelo.save(os.path.join(pasta_para_salvar_treinamentos,nome_modelo_atual+'.model'))
      # else:
      #   print('Modelo não passou nas questões básicas...')

      # Armazenamento do modelo recém treinado
      modelo.save(os.path.join(pasta_para_salvar_treinamentos,nome_modelo_atual+'.model'))

      # Armazenamento da validação feita com o modelo recém treinado
      status_validacao, msg_validacao = validarResultados(nome_modelo=nome_modelo_atual,
                                                          modeloW2V=modelo,
                                                          pasta_para_salvar_resultados=pasta_para_salvar_resultados,
                                                          dic_questoes=dic_questoes)
      fim = time.time()
      print('Duração:',round(((fim-ini)/60),2),'minutos')
      if status_validacao:
        print('Validação do treino realizada com sucesso!')
      else:
        print('\n! Problema ao validar resultados do treino:',msg_validacao,'\n')

      print('\n'+'-'*100+'\n')

    else:
      print('Já foi encontrado treinamento registrado para',nome_modelo_atual)

else:
  print('\n! Problema organizar ambiente de treinos:',msg_organizacao,'\n')
