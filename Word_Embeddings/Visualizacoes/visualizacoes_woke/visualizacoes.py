import matplotlib.pyplot as plt
import numpy as np
from .funcoes import limparConsole, obterResposta, formatarEntrada, abrirArquivoMsgPack
from gensim.models import KeyedVectors
import time
import os
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import pandas as pd
import networkx as nx
import re
import string
try:
  # try: # Se tiver rodando no Colab já será instalado o spaCy e o modelo treinado em português para reconhecer os verbos no filtro, se não (execução local) terá que ser instalado "manualmente" com estes comandos no terminal sem o "!" na frente.
  #   !pip install -U spacy
  #   !pip install -U spacy-lookups-data
  #   !python -m spacy download pt_core_news_lg
  # except Exception:
  #   pass
  import spacy
  nlp = spacy.load('pt_core_news_lg',enable=["tok2vec","morphologizer"])
except Exception:
  print('\n\n\t! spaCy não foi importado com sucesso, o filtro de verbos não poderá ser utilizado.\n\n')
  time.sleep(3)


PONTUACOES = string.punctuation

PASTA_SAVE_IMAGENS = r'resultados_gerados'




def verificaExistenciaNosModelos(modelos_treinados : list[tuple], palavra_central : str | list[str], checagem_unica : bool = False):
  if not checagem_unica:
    try:
      if isinstance(palavra_central,str):
        for modelo in [modelo[1] for modelo in modelos_treinados]:
          modelo[palavra_central]
        return True
      else:        
        for modelo in [modelo[1] for modelo in modelos_treinados]:
          for palavra in palavra_central:
            modelo[palavra]
        return True
    except Exception:
      return False
  else:
    existencia_em_pelo_menos_um = False

    if isinstance(palavra_central,str):      
      for modelo in [modelo[1] for modelo in modelos_treinados]:
        if palavra_central in modelo.index_to_key:
          existencia_em_pelo_menos_um = True
          break
    else:      
      qtd = len(palavra_central)
      for modelo in [modelo[1] for modelo in modelos_treinados]:
        qtd_modelo = 0
        for palavra in palavra_central:
          if palavra in modelo.index_to_key:
            qtd_modelo += 1
        if qtd_modelo == qtd:
          existencia_em_pelo_menos_um = True
          break
    if existencia_em_pelo_menos_um:
      return True
    else:
      return False


def SimilaridadesAoDecorrerDoTempo(modelos_treinados : list[tuple],pasta_para_salvar=PASTA_SAVE_IMAGENS):
  
  print('\n\n\tVocê está montando uma visualização para Similaridades ao decorrer do tempo.\n\n')
  palavra_central = formatarEntrada(input('Digite a palavra central: '))
  
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = formatarEntrada(input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: '))
    
  cores = ['green','red','cyan','violet','blue','gold','orange','c','black','purple','lime','tomato','magenta','lightslategrey','lightgreen','paleturquoise','aquamarine','moccasin','lightcoral','chocolate','sandybrown','rosybrown']


  lista_palavras_comparacao = []
  while True:

    if len(lista_palavras_comparacao) < len(cores):
      palavra_digitada = formatarEntrada(input(f'\nDigite uma palavra para ser comparada (no máximo {len(cores)} e 0 para parar):  '))

      if (palavra_digitada != '0') and verificaExistenciaNosModelos(modelos_treinados,palavra_digitada):
        lista_palavras_comparacao.append(palavra_digitada)
      elif (verificaExistenciaNosModelos(modelos_treinados,palavra_digitada) == False) and (palavra_digitada != '0'):
        while (verificaExistenciaNosModelos(modelos_treinados,palavra_digitada) == False) and (palavra_digitada != '0'):
          palavra_digitada = formatarEntrada(input(f'O token "{palavra_digitada}" não está presente em todos os modelos.\nPor favor, digite outro token:  '))
        if palavra_digitada != '0':
          lista_palavras_comparacao.append(palavra_digitada)
      else:
        break
    else:
      break



  nomes = [re.search(r'(\d{4})\_\d{4}',modelo[0]).group(1) + '\n-\n' + re.search(r'\d{4}\_(\d{4})',modelo[0]).group(1) for modelo in modelos_treinados]

  fig, ax = plt.subplots(figsize=(16, 8))

  x = [i+1 for i in range(len(modelos_treinados))]

  cores_usadas = []
  for palavra in lista_palavras_comparacao:
    i = 0
    cor = cores[i]
    while cor in cores_usadas:
      cor = cores[i+1]
      i += 1
    cores_usadas.append(cor)
    y = []
    for modelo in [modelo[1] for modelo in modelos_treinados]:
      y.append(modelo.similarity(palavra_central,palavra))

    ax.scatter(x, y, color='black', s=10)
    line_x = [x[0]] + x[1:-1] + [x[-1]]
    line_y = [y[0]] + y[1:-1] + [y[-1]]
    ax.plot(line_x, line_y, label=palavra, color=cor)
    for i in range(len((y))):
      ax.text(x[i], y[i]+0.01, str(round(y[i],2)), fontsize=6, ha='center', va='bottom')

  nome_modelo = re.sub(r'\_\d{4}\_\d{4}', '', modelos_treinados[0][0])

  ax.set_title(f'Similaridade entre "{palavra_central}" e outras palavras selecionadas\n{nome_modelo}', fontsize=20, pad= 25)
  ax.set_xlabel('Intervalos de tempo', fontsize=15, labelpad=20)
  ax.set_ylabel('Similaridade', fontsize=15, labelpad=20)

  ax.set_xticks(x)
  ax.set_xticklabels(nomes,fontsize=11)

  ax.grid('on')
  ax.legend(fontsize = 11,loc='center left', bbox_to_anchor=(1, 0.5))
  plt.tight_layout(rect=[0, 0, 0.85, 1])

  limparConsole()

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Gráfico Similaridades',palavra_central)

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)

  ano_inicial = re.search(r'(\d{4})\_\d{4}',modelos_treinados[0][0]).group(1)
  ano_final = re.search(r'\d{4}\_(\d{4})',modelos_treinados[-1][0]).group(1)

  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Sim_{ano_inicial}_{ano_final}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  plt.clf()
  # plt.show()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Gráfico Similaridades','-->',palavra_central,'\n\n')


def VizinhosMaisProximosAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS, modo : int = 1):
  
  limparConsole()
  print('\n\n\tVocê está montando uma visualização para Vizinhos mais Próximos ao decorrer do tempo.\n\n')

  print('Como você gostaria de visualizar os resultados?\n\n')
  print('1 - Apenas com visualização')
  print('2 - Apenas arquivo de texto detalhado (possível analisar mais de uma palavra)')

  modo = input('\nDigite o número correspondente: ')
  modo = obterResposta(resposta=modo,qtd_respostas=2,contagem_normal=True)
  
  limparConsole()
  print('\n\n\tVocê está montando uma visualização para Vizinhos mais Próximos ao decorrer do tempo.\n\n')

  if modo == 1:
    palavra_central = formatarEntrada(input('Digite uma palavra: '))
    while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central,checagem_unica=True):
      palavra_central = formatarEntrada(input('Esta palavra não está presente em nenhum dos modelos.\nPor favor, digite outra palavra: '))


  if modo == 2:
    while True:
      lista_palavras = []
      palavra = formatarEntrada(input('\nDigite uma palavra: '))
      while palavra != '0':
        lista_palavras.append(palavra)
        palavra = formatarEntrada(input('\nDigite mais uma palavra (0 para parar): '))

      if verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=lista_palavras,checagem_unica=True):
        break
      else:
        print('Esse conjunto de palavras não está presente em nenhum dos modelos.\nPor favor digite outro...')
    limparConsole()
    topn = formatarEntrada(input('\nQuantos vizinhos mais próximos você gostaria de coletar?\n'))
    while not topn.isdigit():
      topn = formatarEntrada(input('\nDigite um NÚMERO, por favor: '))
    topn = int(topn)
      
  
  os.makedirs(pasta_para_salvar,exist_ok=True)

  if modo == 1:
    for modelo in modelos_treinados:
      VizinhosMaisProximos(tupla_modelo_escolhido=modelo,
                          palavra_central=palavra_central,
                          pasta_para_salvar=pasta_para_salvar)
  elif modo == 2:
    for modelo in modelos_treinados:
      VizinhosMaisProximosTxt(tupla_modelo_escolhido=modelo,
                              palavra_central=lista_palavras,
                              pasta_para_salvar=pasta_para_salvar,
                              topn=topn)
        
def VizinhosMaisProximos(tupla_modelo_escolhido : tuple[str,KeyedVectors],
                        palavra_central : str,
                        pasta_para_salvar : str):
  
  try:
    nome_modelo_escolhido, modelo_escolhido = tupla_modelo_escolhido
    
    if palavra_central in modelo_escolhido.index_to_key:
      palavras_vizinhas = modelo_escolhido.most_similar(palavra_central)

      palavras_vizinhas = []
      palavras_vizinhas_com_similaridade= []

      for palavra,similaridade in modelo_escolhido.most_similar(palavra_central):
        palavras_vizinhas.append(palavra)
        palavras_vizinhas_com_similaridade.append((palavra,similaridade))


      fig, ax = plt.subplots(1, 2,figsize=(12, 5),gridspec_kw={'width_ratios': [4, 1]})

      ax[0].axis('off')
      ax[1].axis('off')

      ax[0].text(0.5, 0.5, palavra_central, ha='center', va='center', fontsize=14, fontweight='bold')

      num_vizinhas = len(palavras_vizinhas)

      theta = np.linspace(0, 2 * np.pi, num_vizinhas, endpoint=False)
      raio = 0.1

      x_vizinhas = 0.5 + raio * np.cos(theta)
      y_vizinhas = 0.5 + raio * np.sin(theta)

      distancia_raio = 0.7

      for i, palavra in enumerate(palavras_vizinhas):
          ax[0].text(x_vizinhas[i], y_vizinhas[i], palavra, ha='center', va='center', fontsize=12, fontweight='bold')

          x_inicio = x_vizinhas[i] + (0.5 - x_vizinhas[i]) * distancia_raio
          y_inicio = y_vizinhas[i] + (0.5 - y_vizinhas[i]) * distancia_raio
          x_fim = x_vizinhas[i]
          y_fim = y_vizinhas[i]

          ax[0].plot([x_inicio, x_fim], [y_inicio, y_fim], color='gray')

      ax[0].set_title(f'TOP 10 Vizinhos mais próximos de {palavra_central}\n{nome_modelo_escolhido}')

      texto = "Resultado:\n('palavra', similaridade)"
      for i in range(len(palavras_vizinhas_com_similaridade)):
        texto += '\n\n'+str(palavras_vizinhas_com_similaridade[i])

      ax[1].text(1, 0.5,texto, fontsize=11, ha='center', va='center')

      
      pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Vizinhos mais próximos',palavra_central)

      if not os.path.exists(pasta_para_salvar_palavra_central):
        os.makedirs(pasta_para_salvar_palavra_central)
      
      caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'VP_{nome_modelo_escolhido}_{palavra_central}.png')

      while os.path.exists(caminho_save_fig):  
        caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

      plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  except:
    pass
    # limparConsole()
    # print(f'Ocorreu um erro com a palavra {palavra}...')
    # erro = f'Na função: campoSemantico, usando {nome_modelo_escolhido}.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    # with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    #   f.write(erro+'\n\n')
  else:
    limparConsole()
    print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Vizinhos mais próximos','-->',palavra_central,'\n\n')
    plt.clf()

def VizinhosMaisProximosTxt(tupla_modelo_escolhido : tuple[str,KeyedVectors],
                            palavra_central : str,
                            pasta_para_salvar : str,
                            topn : int):
  nome_modelo_escolhido, modelo_escolhido = tupla_modelo_escolhido
  conjunto_dentro = True
  for palavra in palavra_central:
    if palavra not in modelo_escolhido.index_to_key:
      conjunto_dentro = False
      break
  if conjunto_dentro:
    palavras_vizinhas_com_similaridade = [(r[0],r[1]) for r in modelo_escolhido.most_similar(positive=palavra_central,topn=topn)]

    txt = f'Lista dos TOP {str(topn)} vizinhos mais próximos de {", ".join(palavra_central)}:\n\n'

    for i, resultado in enumerate(palavras_vizinhas_com_similaridade):
      txt += f'{str(i+1)}. {resultado[0]}: {str(resultado[1])}\n'

    nome_pasta = '_'.join(palavra_central[:5])
    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Vizinhos mais próximos',nome_pasta)

    os.makedirs(pasta_para_salvar_palavra_central,exist_ok=True)
    
    caminho_save_txt = os.path.join(pasta_para_salvar_palavra_central,f'VP_{nome_modelo_escolhido}.txt')

    while os.path.exists(caminho_save_txt):
      caminho_save_txt = caminho_save_txt.replace('.txt','_copia.txt')
    
    with open(caminho_save_txt,'w',encoding='utf-8') as f:
      f.write(txt)
    
    limparConsole()
    print(f'Arquivo de texto gerado e salvo em "Vizinhos mais próximos" --> "{nome_pasta}"')


def MapaDeCalorSimilaridadesAoDecorrerDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  
  print('\n\n\tVocê está montando uma visualização para Mapa de Calor ao decorrer do tempo.\n\n')
  palavra_central = formatarEntrada(input('Digite a palavra central: '))

  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = formatarEntrada(input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: '))

  palavras_selecionadas = []

  while True:
    palavra_digitada = formatarEntrada(input('Digite uma palavra para ser comparada com a palavra central (0 para parar): '))
    while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_digitada,checagem_unica=True) and palavra_digitada != '0':
      palavra_digitada = formatarEntrada(input('Esta palavra não está presente em nenhum dos modelos.\nPor favor, digite outra palavra: '))    
    if palavra_digitada == '0':
      break
    else:    
      palavras_selecionadas.append(palavra_digitada)
    
  if palavras_selecionadas:
    data = {}

    for nome_modelo_escolhido,modelo in modelos_treinados:
      dic_comparativo = {}
      for palavra_selecionada in palavras_selecionadas:
        try:
          dic_comparativo[palavra_selecionada] = modelo.similarity(palavra_central,palavra_selecionada)
        except:
          dic_comparativo[palavra_selecionada] = 0
      data[re.search(r'(\d{4})\_\d{4}',nome_modelo_escolhido).group(1) + '\n-\n' + re.search(r'\d{4}\_(\d{4})',nome_modelo_escolhido).group(1)] = dic_comparativo




    df = pd.DataFrame(data)

    plt.figure(figsize=(16, 8))
    heatmap = sns.heatmap(df, annot=True, cmap='coolwarm')

    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=0)
    heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0,fontsize=11)

    nome_modelo_atual = re.sub(r'\_\d{4}\_\d{4}','',modelos_treinados[0][0])

    plt.title(f'Mapa de calor da similaridade para palavra "{palavra_central}"\n{nome_modelo_atual}',fontsize=20)
    
    limparConsole()

    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Mapas de Calor',palavra_central)

    if not os.path.exists(pasta_para_salvar_palavra_central):
      os.makedirs(pasta_para_salvar_palavra_central)
    
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'MC_{palavra_central}.png')

    while os.path.exists(caminho_save_fig):  
      caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

    plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
    
    print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Mapas de Calor','-->',palavra_central,'\n\n')
    
    plt.clf()
    # plt.show()
  else:
    limparConsole()


def Filtro(palavras : list,
           condicoes : list[str] = ['maior que 3 letras','remover stopwords','remover verbos','somente verbos']):
  
  str_remocao = ''
  remover_palavras = []
  for palavra in palavras:
    if (palavra[0] in PONTUACOES or palavra[-1] in PONTUACOES) and palavra not in remover_palavras:
      remover_palavras.append(palavra)
  if remover_palavras:
    for palavra in remover_palavras:
      palavras.remove(palavra)
      str_remocao += palavra+', '
    remover_palavras = []
  
  if 'maior que 3 letras' in condicoes:
    for palavra in palavras:
      if len(palavra)<=3 and palavra not in remover_palavras:
        remover_palavras.append(palavra)
    if remover_palavras:
      for palavra in remover_palavras:
        palavras.remove(palavra)
        str_remocao += palavra+', '
      remover_palavras = []

  if 'remover stopwords' in condicoes:
    # remover_palavras += [palavra for palavra in palavras if palavra in LISTA_STOP_WORDS and palavra not in remover_palavras]
    for palavra in palavras:
      if palavra in LISTA_STOP_WORDS and palavra not in remover_palavras:
        remover_palavras.append(palavra)
    if remover_palavras:
      for palavra in remover_palavras:
        palavras.remove(palavra)
        str_remocao += palavra+', '
      remover_palavras = []

  if 'remover verbos' in condicoes and 'somente verbos' not in condicoes:
    try:
      for palavra in palavras:
        if nlp(palavra)[0].pos_ in ['VERB','AUX'] and palavra not in remover_palavras:
          remover_palavras.append(palavra)
      if remover_palavras:
        for palavra in remover_palavras:
          palavras.remove(palavra)
          str_remocao += palavra+', '
        remover_palavras = []
    except Exception as e:
      erro = f'{e.__class__.__name__}: {str(e)}'
      print(f'\n\n\t! Problema ao filtrar verbos...\n\t! Por favor, certifique-se de ter instalado apropriadamente a biblioteca spaCy e as dependências necessárias.\n\t! Qualquer dúvida entre em contato com o Grupo de Estudos e Pesquisa em IA e História da UFSC.\n\t! Info do erro:{erro}\n\n')
      print('Aguardando 5s...\n')
      time.sleep(5)

  if 'somente verbos' in condicoes and 'remover verbos' not in condicoes:
    try:
      for palavra in palavras:
        if nlp(palavra)[0].pos_ not in ['VERB','AUX'] and palavra not in remover_palavras:
          remover_palavras.append(palavra)
      if remover_palavras:
        for palavra in remover_palavras:
          palavras.remove(palavra)
          str_remocao += palavra+', '
        remover_palavras = []
    except Exception as e:
      erro = f'{e.__class__.__name__}: {str(e)}'
      print(f'\n\n\t! Problema ao filtrar verbos...\n\t! Por favor, certifique-se de ter instalado apropriadamente a biblioteca spaCy e as dependências necessárias.\n\t! Qualquer dúvida entre em contato com o Grupo de Estudos e Pesquisa em IA e História da UFSC.\n\t! Info do erro:{erro}\n\n')
      print('Aguardando 5s...\n')
      time.sleep(5)

  return palavras,str_remocao[:-2]


def FrequenciaDePalavrasAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS):

  limparConsole()
  print('Escolha que tipo de frequência que você quer usar:\n')
  print('1 - Top 20 palavras mais frequentes')
  print('2 - Frequência de palavras específicas')

  resposta = formatarEntrada(input('\nDigite o número referente à sua escolha: '))
  resposta = obterResposta(resposta=resposta,qtd_respostas=2,contagem_normal=True)
  

  if resposta == 1:
    limparConsole()
  
    print('Escolha, se quiser, quais filtros você gostaria de aplicar à resposta:\n')
    print('1 - Mostrar somente palavras com mais de 3 letras')
    print('2 - Remover stopwords')
    print('3 - Remover verbos')
    print('4 - Mostrar somente os verbos')
    print('5 - Não quero aplicar nenhum filtro, quero a resposta nua e crua!')
    
    resposta_filtro = formatarEntrada(input('\nDigite os números correspondentes separados por "," (vírgula) em caso de mais de uma resposta:\n'))
    if ',' in resposta_filtro:
      while len([r for r in resposta_filtro.split(',') if not r.isdigit()])>0:
          resposta_filtro = formatarEntrada(input('Por favor, reescreva uma resposta válida (só números): '))
      resposta_filtro = obterResposta(resposta=resposta_filtro,qtd_respostas=5,contagem_normal=True)
    else:
      if resposta_filtro != '5':
        resposta_filtro = obterResposta(resposta=resposta_filtro,qtd_respostas=5,contagem_normal=True)
      else:
        resposta_filtro = int(resposta_filtro)

    
    condicoes_filtro = []
    if resposta_filtro != 5:
      resposta_filtro = str(resposta_filtro)
      if '1' in resposta_filtro:
        condicoes_filtro.append('maior que 3 letras')
      if '2' in resposta_filtro:
        condicoes_filtro.append('remover stopwords')
      if '3' in resposta_filtro:
        condicoes_filtro.append('remover verbos')
      if '4' in resposta_filtro:
        condicoes_filtro.append('somente verbos')


    for modelo in modelos_treinados:
      FrequenciaDePalavrasTop20(tupla_modelo_escolhido=modelo,
                                pasta_para_salvar=pasta_para_salvar,
                                condicoes_filtro = condicoes_filtro)
  elif resposta == 2:
    FrequenciaDePalavrasSelecionadasAoDecorrerDoTempo(modelos_treinados=modelos_treinados)


def coletarFrequenciasNoCorpus(nome_modelo : str,
                               tokens : list[str],
                               anos : list[str] = ['2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023'],
                               caminho_pasta_corpus_freq : str = r'info_corpus'):

  if 'UFSC' in nome_modelo:
    lista_colecoes = 'todas'
  elif 'CFH' in nome_modelo:
    lista_colecoes = ['Filosofia','Geografia','Geologia','Historia','Psicologia','Teses_e_dissertacoes_do_Centro_de_Filosofia_e_Ciencias_Humanas','Programa_de_Pos_Graduacao_Interdisciplinar_em_Ciencias_Humanas','Servico_Social','Sociologia_e_Ciencia_Politica','Sociologia_Politica','Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional','Ensino_de_Historia_Mestrado_Profissional']
  elif 'HST' in nome_modelo:
    lista_colecoes = ['Historia']
  elif 'SAUDE-CORPO' in nome_modelo:
    lista_colecoes = ['Biologia_Celular_e_do_Desenvolvimento','Biotecnologia_e_Biociencias','Ciencias_da_Reabilitacao','Ciencias_Medicas','Cuidados_Intensivos_e_Paliativos_Mestrado_Profissional',
                     'Educacao_Fisica','Enfermagem','Gestao_do_Cuidado_em_Enfermagem','Gestao_do_Cuidado_em_Enfermagem_Mestrado_Profissional','Medicina_Veterinaria_Convencional_e_Integrativa',
                     'Neurociencias','Saude_Coletiva','Saude_Mental_e_Atencao_Psicossocial_Mestrado_Profissional','Saude_Publica','Programa_de_Pos_Graduacao_Multidisciplinar_em_Saude_Mestrado_Profissional']
  else:
    lista_colecoes = []

  if lista_colecoes == 'todas':
    colecoes = sorted([colecao for colecao in os.listdir(caminho_pasta_corpus_freq) if '.' not in colecao])
  else:
    colecoes = sorted([colecao for colecao in os.listdir(caminho_pasta_corpus_freq) if colecao in lista_colecoes])

  dic_contagens = {ano:{'total_de_palavras':0,'contagens':{token:{'frequencia_normal':0,'frequencia_relativa':0} for token in sorted(tokens)}} for ano in sorted(anos)}

  for ano in dic_contagens.keys():
    for colecao in colecoes:
      caminho_colecao = os.path.join(caminho_pasta_corpus_freq,colecao)
      for caminho_dic in [os.path.join(caminho_colecao,d) for d in os.listdir(caminho_colecao) if d.startswith('dic_') and d.endswith(f'{ano}.msgpack')]:
        dic_atual = abrirArquivoMsgPack(caminho_dic)
        for trabalho in dic_atual.keys():
          l_tokens = dic_atual[trabalho]['contagens'].keys()
          dic_contagens[ano]['total_de_palavras'] += dic_atual[trabalho]['total_de_palavras']
          for token in dic_contagens[ano]['contagens'].keys():
            if token in l_tokens:
              dic_contagens[ano]['contagens'][token]['frequencia_normal'] += dic_atual[trabalho]['contagens'][token]
    for token in dic_contagens[ano]['contagens'].keys():
      if dic_contagens[ano]['total_de_palavras'] != 0:
        dic_contagens[ano]['contagens'][token]['frequencia_relativa'] = round(dic_contagens[ano]['contagens'][token]['frequencia_normal']/dic_contagens[ano]['total_de_palavras'],8)

  return dic_contagens



def FrequenciaDePalavrasSelecionadasAoDecorrerDoTempo(modelos_treinados : list[tuple],pasta_para_salvar=PASTA_SAVE_IMAGENS):

  limparConsole()
  print('\n\n\tVocê está montando uma visualização para Frequência de Palavras Selecionadas ao decorrer do tempo.\n\n')

  print('Qual tipo de frequência você quer visualizar?\n\n')
  print('1 - Frequência completa durante os treinamentos')
  print('2 - Frequência entre os diferentes períodos de treinamento')
  print('3 - Frequência de palavras no corpus todo')

  resposta_tipo_freq = formatarEntrada(input('\n\nDigite o número correspondente à sua escolha: '))
  resposta_tipo_freq = obterResposta(resposta=resposta_tipo_freq,qtd_respostas=3,contagem_normal=True)

  limparConsole()
  print('\n\n\tVocê está montando uma visualização para Frequência de Palavras Selecionadas ao decorrer do tempo.\n\n')
  lista_palavras = []

  cores = ['green','red','cyan','violet','blue','gold','orange','c','black','purple','lime','tomato','magenta','lightslategrey','lightgreen','paleturquoise','aquamarine','moccasin','lightcoral','chocolate','sandybrown','rosybrown']


  palavra_freq = formatarEntrada(input('Digite a primeira palavra: '))
  while True:
    while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_freq,checagem_unica=True) and palavra_freq != '0':
      palavra_freq = formatarEntrada(input('\n! Esta palavra não está presente em nenhum dos modelos.\n! Por favor, digite outra palavra: '))
    if palavra_freq != '0':
      if palavra_freq not in lista_palavras:
        lista_palavras.append(palavra_freq)
    else:
      break
    if len(lista_palavras) == len(cores):
      break
    else:
      palavra_freq = formatarEntrada(input('\nDigite mais uma palavra (0 para parar): '))

  if resposta_tipo_freq == 1:
    nomes = [re.search(r'(\d{4})\_\d{4}',modelo[0]).group(1) + '\n-\n' + re.search(r'\d{4}\_(\d{4})',modelo[0]).group(1) for modelo in modelos_treinados]
  elif resposta_tipo_freq == 2:
    # nomes = [re.search(r'\d{4}\_(\d{4})',modelo[0]).group(1) for modelo in modelos_treinados]
    nomes = []
    for i in range(len(modelos_treinados)):
      modelo_atual = modelos_treinados[i][0]
      if i == 0:
        nomes.append(re.search(r'(\d{4})\_\d{4}',modelo_atual).group(1) + '\n-\n' + re.search(r'\d{4}\_(\d{4})',modelo_atual).group(1))
      else:
        nomes.append(str(int(re.search(r'\d{4}\_(\d{4})',modelos_treinados[i-1][0]).group(1))+1) + '\n-\n' + re.search(r'\d{4}\_(\d{4})',modelo_atual).group(1))

  elif resposta_tipo_freq == 3:
    limparConsole()
    print('\n\n\tVocê está montando uma visualização para Frequência de Palavras Selecionadas ao decorrer do tempo.\n\n')
    print('Qual tipo de contabilização de frequência você gostaria de utilizar?\n\n')
    print('1 - Frequência Normal (contabilizar as aparições nos textos naquele determinado período de tempo)')
    print('2 - Frequência Relativa (contabilizar a proporção de aparições pela quantidade de palavras naquele determinado período de tempo)')

    resposta_tipo_freq_corpus = formatarEntrada(input('\n\nDigite o número correspondente à sua escolha: '))
    resposta_tipo_freq_corpus = obterResposta(resposta=resposta_tipo_freq_corpus,qtd_respostas=2,contagem_normal=True)

    nomes = [str(ano) for ano in range(2003,2024)]
  
  limparConsole()
  print('\n\n\tPor favor, aguarde! A visualização está em construção!\n\n')

  fig, ax = plt.subplots(figsize=(16, 8))

  if resposta_tipo_freq in [1,2]:
    x = [i+1 for i in range(len(modelos_treinados))]
  else:
    x = [ano for ano in range(2003,2024)]

  cores_usadas = []
  for palavra in lista_palavras:
    i = 0
    cor = cores[i]
    while cor in cores_usadas:
      cor = cores[i+1]
      i += 1
    cores_usadas.append(cor)
    y = []
    if resposta_tipo_freq == 1:
      for modelo in [modelo[1] for modelo in modelos_treinados]:
        if palavra in modelo.index_to_key:
          y.append(modelo.get_vecattr(palavra,'count'))
        else:
          y.append(0)
    elif resposta_tipo_freq == 2:
      for i in range(len(modelos_treinados)):
        modelo_atual = modelos_treinados[i][1]
        if palavra in modelo_atual.index_to_key:
          if i == 0: # primeiro
            y.append(modelo_atual.get_vecattr(palavra,'count'))
          elif palavra in modelos_treinados[i-1][1].index_to_key:
            y.append(abs(modelo_atual.get_vecattr(palavra,'count')-modelos_treinados[i-1][1].get_vecattr(palavra,'count')))
          else:
            y.append(modelo_atual.get_vecattr(palavra,'count'))
        else:
          y.append(0)
    elif resposta_tipo_freq == 3:
      dic_contagens = coletarFrequenciasNoCorpus(nome_modelo=modelos_treinados[0][0],
                                                 tokens=lista_palavras)
      for ano in dic_contagens.keys():
        if resposta_tipo_freq_corpus == 1: # freq. normal
          y.append(dic_contagens[ano]['contagens'][palavra]['frequencia_normal'])
        else: # freq. relativa
          y.append(dic_contagens[ano]['contagens'][palavra]['frequencia_relativa']*10000)


    ax.scatter(x, y, color='black', s=10)
    line_x = [x[0]] + x[1:-1] + [x[-1]]
    line_y = [y[0]] + y[1:-1] + [y[-1]]
    ax.plot(line_x, line_y, label=palavra, color=cor)
    for i in range(len((y))):
      ax.text(x[i], y[i]+y[i]*0.02, str(round(y[i],2)), fontsize=6, ha='center', va='bottom')


  nome_modelo = re.sub(r'\_\d{4}\_\d{4}', '', modelos_treinados[0][0])

  if y:
    if resposta_tipo_freq == 1:
      ax.set_title(f'Frequência completa nos treinamentos das palavras selecionadas\n{nome_modelo}', fontsize=20, pad= 25)
      ax.set_xlabel('Intervalos de tempo', fontsize=15, labelpad=20)
    elif resposta_tipo_freq == 2:
      ax.set_title(f'Frequência separada nos treinamentos das palavras selecionadas\n{nome_modelo}', fontsize=20, pad= 25)
      ax.set_xlabel('Intervalos de tempo', fontsize=15, labelpad=20)
    elif resposta_tipo_freq == 3:
      if resposta_tipo_freq_corpus == 1:
        ax.set_title(f'Frequência normal no corpus das palavras selecionadas\n{nome_modelo}', fontsize=20, pad= 25)
      else:
        ax.set_title(f'Frequência relativa no corpus das palavras selecionadas\n{nome_modelo}', fontsize=20, pad= 25)
      ax.set_xlabel('Anos', fontsize=15, labelpad=20)
    
    ax.set_ylabel('Frequências', fontsize=15, labelpad=20)

    ax.set_xticks(x)
    ax.set_xticklabels(nomes,fontsize=11)

    ax.grid('off')
    ax.legend(fontsize = 11,loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    limparConsole()

    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Frequências de Palavras Selecionadas')

    if not os.path.exists(pasta_para_salvar_palavra_central):
      os.makedirs(pasta_para_salvar_palavra_central)

    if resposta_tipo_freq == 1:
      caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'FTC_{nome_modelo}_{"_".join(lista_palavras[:3])}_etc.png') # Freq treinos completa
    elif resposta_tipo_freq == 2:
      caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'FTS_{nome_modelo}_{"_".join(lista_palavras[:3])}_etc.png') # Freq treinos separada
    elif resposta_tipo_freq == 3:
      if resposta_tipo_freq_corpus == 1:
        caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'FNC_{nome_modelo}_{"_".join(lista_palavras[:3])}_etc.png') # Freq normal corpus
      else:
        caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'FRC_{nome_modelo}_{"_".join(lista_palavras[:3])}_etc.png') # Freq relativa corpus

    while os.path.exists(caminho_save_fig):
      caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

    plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

    # plt.show()

    plt.clf()

    print('\n\n\tImagem salva em',pasta_para_salvar,'-->','Frequências de Palavras Selecionadas','\n\n')
 
    
def FrequenciaDePalavrasTop20(tupla_modelo_escolhido,
                              condicoes_filtro : list[str] = [],
                              pasta_para_salvar : str = PASTA_SAVE_IMAGENS):
  nome_modelo_escolhido,modelo = tupla_modelo_escolhido
  plt.figure(figsize=(20, 10))

  # plt.bar([word for word in [palavra for palavra in modelo.wv.index_to_key[:500] if (palavra not in ['como','uma','um','ao','mais','mesmo','forma','pois','essa','apenas','parte','além','nesse']) and (nlp_spacy(palavra)[0].pos_ not in ['VERB','AUX']) and (len(palavra)>3)][:20]],[modelo.wv.get_vecattr(word,'count') for word in [palavra for palavra in modelo.wv.index_to_key[:500] if (palavra not in ['como','uma','um','ao','mais','mesmo','forma','pois','essa','apenas','parte','além','nesse']) and (nlp_spacy(palavra)[0].pos_ not in ['VERB','AUX']) and (len(palavra)>3)][:20]])  

  # dic_vocab_freq = {palavra:modelo.get_vecattr(palavra,'count') for palavra in modelo.index_to_key[:500]}
  tokens_filtrados,str_palavras_removidas = Filtro(palavras=modelo.index_to_key[:500],condicoes=condicoes_filtro)
  dic_vocab_freq = {palavra:modelo.get_vecattr(palavra,'count') for palavra in tokens_filtrados}

  dic_vocab_freq_ordenado = dict(sorted(dic_vocab_freq.items(), key=lambda item: item[1], reverse=True))
  
  # palavras_filtradas,str_palavras_removidas = Filtro(palavras=list(dic_vocab_freq_ordenado.keys()),condicoes=condicoes_filtro)
  palavras_filtradas = list(dic_vocab_freq_ordenado.keys())

  lista_palavras = palavras_filtradas[:20]

  

  plt.bar([palavra for palavra in lista_palavras],[modelo.get_vecattr(palavra,'count') for palavra in lista_palavras])
  
  plt.xticks(rotation=45, ha='right')

  plt.title(f"Frequência de palavras treinamento {nome_modelo_escolhido}",fontsize=20)



  if condicoes_filtro:      
    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Frequência de Palavras','Filtrado')
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Freq_{nome_modelo_escolhido}.png')    
    cond_filtro = ', '.join(condicoes_filtro)
    txt = f'Frequência das TOP 300 palavras com filtro(s) de {cond_filtro}:\n\n'
    caminho_save_txt = os.path.join(pasta_para_salvar_palavra_central,f'Freq_{nome_modelo_escolhido}.txt')
  else:    
    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Frequência de Palavras','Sem filtro')
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Freq_{nome_modelo_escolhido}.png')
    txt = f'Frequência das TOP 300 palavras sem filtro:\n\n'
    caminho_save_txt = os.path.join(pasta_para_salvar_palavra_central,f'Freq_{nome_modelo_escolhido}.txt')

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  for i,palavra in enumerate(palavras_filtradas[:300]):
    txt += f'{str(i+1)}. {palavra}: {"{0:,}".format(modelo.get_vecattr(palavra,"count")).replace(",",".")}\n'


  while os.path.exists(caminho_save_txt):  
    caminho_save_txt = caminho_save_txt.replace('.txt','_copia.txt')

  with open(caminho_save_txt,'w',encoding='utf-8') as f:
    f.write(txt)

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Frequência de Palavras','\n\n')
  # if str_palavras_removidas != '':
  #   print('Os seguintes tokens foram removidos das visualizações:',str_palavras_removidas)

  plt.clf()



def EstratosDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  def pega_cor(bg_color):
      gray = np.dot(bg_color, [0.2989, 0.5870, 0.1140])
      return 'black' if gray > 0.5 else 'white'

  def agrupar_em_trios(lista):
      lista_nova = [(lista[i], lista[i + 1], lista[i + 2]) for i in range(0, len(lista), 3)]
      return lista_nova
  
  limparConsole()

  print('\n\n\tVocê está montando uma visualização para Estratos do Tempo.\n\n')
  palavra_central = formatarEntrada(input('Digite uma palavra: '))

  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central,checagem_unica=True):
    palavra_central = formatarEntrada(input('Esta palavra não está presente em nenhum dos modelos.\nPor favor, digite outra palavra: '))

  palavras_selecionadas = [palavra_central]

  while True:
    palavra_digitada = formatarEntrada(input('Se quiser, digite mais uma palavra (0 para parar): '))
    while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_digitada,checagem_unica=True) and palavra_digitada != '0':
      palavra_digitada = formatarEntrada(input('Esta palavra não está presente em nenhum dos modelos.\nPor favor, digite outra palavra: '))    
    if palavra_digitada == '0':
      break
    else:    
      palavras_selecionadas.append(palavra_digitada)

  if palavras_selecionadas:
    data = {}
    
    for nome_modelo, modelo in modelos_treinados:

      if len([p for p in palavras_selecionadas if p in modelo.index_to_key]) == len(palavras_selecionadas):
        ano_inicial = re.search(r'(\d{4})\_\d{4}',nome_modelo).group(1)
        ano_final = re.search(r'\d{4}\_(\d{4})',nome_modelo).group(1)

        chave = ano_inicial + ' - ' + ano_final

        lista_valores = [{r[0]:r[1]} for r in modelo.most_similar(positive=palavras_selecionadas)]
        data[chave] = lista_valores
      


    lista_de_tuplas = list(data.items())
    lista_de_tuplas_invertida = lista_de_tuplas[::-1]
    data = dict(lista_de_tuplas_invertida)


    index = list(data.keys())
    values = [[list(d.values())[0] for d in data[key]] for key in data]

    heatmap_values = [[list(data[key][0].values())[0]] for key in data]
    df = pd.DataFrame(heatmap_values, index=index)

    plt.figure(figsize=(8, 8))
    heatmap = sns.heatmap(df, annot=False, fmt="", cmap='coolwarm', cbar=True, cbar_kws={'shrink': 0.8}) #,vmin=0, vmax=1, center=0.5
    # heatmap = sns.heatmap(df, annot=False, fmt="", cmap='coolwarm', cbar=True, cbar_kws={'shrink': 0.8}, linewidths=1, linecolor='black')

    nome_modelo_atual = re.sub(r'\_\d{4}\_\d{4}','',modelos_treinados[0][0])

    for i in range(len(df.index)):
        key = df.index[i]
        principal_key = list(data[key][0].keys())[0]
        principal_value = round(list(data[key][0].values())[0],4)
        
        lista_nova = agrupar_em_trios(data[key][1:])
        other_keys_values = [f"{list(c.keys())[0]}: {round(list(c.values())[0],4)} / {list(d.keys())[0]}: {round(list(d.values())[0],4)} / {list(b.keys())[0]}: {round(list(b.values())[0],4)}" for c,d,b in lista_nova]
        bg_color = heatmap.get_children()[0].get_facecolor()[i][:3]
        text_color = pega_cor(bg_color)

        plt.text(0.5, i + 0.2, f"{principal_key}: {principal_value}", ha='center', va='center', fontsize=12, weight='bold',
                color=text_color)
        for j, line in enumerate(other_keys_values):
            plt.text(0.5, i + 0.45 + j * 0.15, line, ha='center', va='center', fontsize=8, color=text_color)

    plt.xticks([])
    heatmap.set_yticklabels(sorted(list(df.index[::-1]),reverse=True), fontsize=12, rotation=0, weight='bold')

    palavra_alvo = ', '.join(palavras_selecionadas)
    plt.title(f'Estratos do Tempo para\n"{palavra_alvo}"\nusando {nome_modelo_atual}', fontsize=20, pad=30)
    plt.tight_layout()

    limparConsole()

    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Estratos do Tempo',palavra_central)

    if not os.path.exists(pasta_para_salvar_palavra_central):
      os.makedirs(pasta_para_salvar_palavra_central)
    
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Estratos do Tempo para {palavra_central}.png')

    while os.path.exists(caminho_save_fig):  
      caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

    plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
    
    print('\n\n\tImagem salva em',pasta_para_salvar,'-->','Estratos do Tempo','-->',palavra_central,'\n\n')
    # plt.show()
    plt.clf()
  else:
    limparConsole()



def VetoresDePalavrasAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Vetores de Palavras ao decorrer do tempo.\n\n')

  lista_de_palavras = []
  palavra = formatarEntrada(input('Digite a primeira palavra: '))
  while palavra != '0':
        
    if palavra not in lista_de_palavras:
      lista_de_palavras.append(palavra)

    palavra = formatarEntrada(input('\nDigite mais uma palavra (0 para parar): '))

  for modelo in modelos_treinados:
    vetoresDePalavras(tupla_modelo_escolhido=modelo,
                      lista_de_palavras=lista_de_palavras,
                      pasta_para_salvar=pasta_para_salvar)


def vetoresDePalavras(tupla_modelo_escolhido,
                      lista_de_palavras : list[str],
                      pasta_para_salvar : str):

  nome_modelo_escolhido,modelo_escolhido = tupla_modelo_escolhido
  lista_de_palavras = [palavra for palavra in lista_de_palavras if palavra in modelo_escolhido.index_to_key]
  lista_de_vetores = [modelo_escolhido[palavra] for palavra in lista_de_palavras]

  pca = PCA(n_components=2)
  lista_de_vetores_2D = pca.fit_transform(lista_de_vetores)

  limite_pos_x = 0
  limite_neg_x = 0
  limite_pos_y = 0
  limite_neg_y = 0
  x = []
  y = []

  for coords in lista_de_vetores_2D:
    x.append(coords[0])
    if coords[0] > limite_pos_x:
      limite_pos_x = coords[0]
    elif coords[0] < limite_neg_x:
      limite_neg_x = coords[0]

    y.append(coords[1])
    if coords[1] > limite_pos_y:
      limite_pos_y = coords[1]
    elif coords[1] < limite_neg_y:
      limite_neg_y = coords[1]

  fig, ax = plt.subplots(1, 2,figsize=(12, 5),gridspec_kw={'width_ratios': [4, 1]})

  ax[0].grid('on')
  ax[1].axis('off')
  # ax[0].grid('off')

  for i, palavra in enumerate(lista_de_palavras):
      ax[0].arrow(0, 0, lista_de_vetores_2D[i, 0], lista_de_vetores_2D[i, 1], head_width=0.1, head_length=0.1, fc='blue', ec='blue')
      ax[0].text(lista_de_vetores_2D[i, 0], lista_de_vetores_2D[i, 1]+0.25, palavra, fontsize=12, ha='center', va='center', color='black')

  ax[0].set_xlim(limite_neg_x-1, limite_pos_x+1)
  ax[0].set_ylim(limite_neg_y-1, limite_pos_y+1)

  cosseno_formula = r'$\cos(\theta) = \frac{\mathbf{v} \cdot \mathbf{u}}{\|\mathbf{v}\| \cdot \|\mathbf{u}\|}$'

  ax[1].text(0.25, 0.5,cosseno_formula, fontsize=20, ha='center', va='center')

  ax[0].set_title(f'Vetores de palavras representados em 2D com {nome_modelo_escolhido}')
  ax[0].set_xlabel('Dimensão 1')
  ax[0].set_ylabel('Dimensão 2')

  
  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Vetores de palavras',', '.join(lista_de_palavras[:3])+' etc')

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
    
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'VP_{nome_modelo_escolhido}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png',' copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Vetores de palavras','\n\n')
  plt.clf()



def ComparacaoEntrePalavrasAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Comparacao Entre Palavras ao decorrer do tempo.\n\n')

  print('\n\nHomem --> Rei\n\nMulher --> X\n\n')

  homem = formatarEntrada(input('O que deseja substituir por "homem"? '))
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=homem):
    homem = formatarEntrada(input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra: '))

  rei = formatarEntrada(input('O que deseja substituir por "rei"? '))
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=rei):
    rei = formatarEntrada(input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra: '))
  
  mulher = formatarEntrada(input('O que deseja substituir por "mulher"? '))
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=mulher):
    mulher = formatarEntrada(input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra: '))

  tupla_comparacao = (homem,rei,mulher)

  for modelo in modelos_treinados:
    ComparacaoEntrePalavras(tupla_modelo_escolhido=modelo,
                            tupla_comparacao=tupla_comparacao,
                            pasta_para_salvar=pasta_para_salvar)


def ComparacaoEntrePalavras(tupla_modelo_escolhido,
                            tupla_comparacao : tuple[str],
                            pasta_para_salvar : str):
  nome_modelo_escolhido, modelo_escolhido = tupla_modelo_escolhido
  homem,rei,mulher = tupla_comparacao
     
  lista_de_palavras = []
  lista_de_palavras.append(homem)
  lista_de_palavras.append(rei)
  lista_de_palavras.append(mulher)

  resultado = modelo_escolhido.most_similar_cosmul(positive=[rei,mulher], negative=[homem])
  
  lista_de_palavras.extend(r[0] for r in resultado)

  lista_de_palavras_e_suas_similaridades = [(r[0],r[1]) for r in resultado]

  pto_resultado = [6,4]
  lista_de_vetores_base = [[0,6],[5,9],[1,1],pto_resultado]
  lista_de_vetores_adc = []

  for i,r in enumerate(resultado[1:]):
    if i ==0: # 4
      h_x = -0.35
      h_y = 0.6
    elif i ==1: # 5
      h_x = 0.3
      h_y = -0.85
    elif i ==2: # 6
      h_x = 0.55
      h_y = 1.25
    elif i ==3: # 7
      h_x = 0.8
      h_y = -1.9
    elif i ==4: # 8
      h_x = 0.2
      h_y = 2
    elif i ==5: # 9
      h_x = -1.5
      h_y = 1.65
    elif i ==6: # 10
      h_x = -1.6
      h_y = -1.75
    elif i ==7: # 11
      h_x = 2
      h_y = 0.2
    elif i ==8: # 12
      h_x = 2.2
      h_y = -1.3
    lista_de_vetores_adc.append([pto_resultado[0]+h_x,pto_resultado[1]+h_y])


  lista_de_vetores_2D = lista_de_vetores_base
  lista_de_vetores_2D.extend(lista_de_vetores_adc)


  limite_pos_x = 0
  limite_neg_x = 0
  limite_pos_y = 0
  limite_neg_y = 0
  x = []
  y = []

  for coords in lista_de_vetores_2D:
    x.append(coords[0])
    if coords[0] > limite_pos_x:
      limite_pos_x = coords[0]
    elif coords[0] < limite_neg_x:
      limite_neg_x = coords[0]

    y.append(coords[1])
    if coords[1] > limite_pos_y:
      limite_pos_y = coords[1]
    elif coords[1] < limite_neg_y:
      limite_neg_y = coords[1]


  fig, ax = plt.subplots(1, 2,figsize=(12, 5),gridspec_kw={'width_ratios': [4, 1]})

  ax[0].grid('on')
  ax[0].axis('on')
  ax[1].axis('off')

  for i, palavra in zip(range(0,3),lista_de_palavras[0:3]):
    ax[0].scatter(x[i], y[i],color='b')
    ax[0].text(x[i], y[i]+0.25, palavra, fontsize=11, ha='center', va='center', color='black')
  for i, palavra in zip(range(3,len(lista_de_palavras)),lista_de_palavras[3:]):
    if i == 3:
      ax[0].scatter(x[i], y[i]-0.15,color='b')
      ax[0].text(x[i], y[i]-0.15+0.25, palavra, fontsize=10, ha='center', va='center', color='black')
    else:
      ax[0].scatter(x[i], y[i],color='g')
      ax[0].text(x[i], y[i]+0.25, palavra, fontsize=10, ha='center', va='center', color='black')

  ax[0].arrow(x[0],y[0],x[1]-x[0],y[1]-y[0],head_width=0.1, head_length=0.1, fc='red', ec='red')
  ax[0].arrow(x[2],y[2],x[3]-x[2],y[3]-y[2],head_width=0.1, head_length=0.1, fc='red', ec='red')


  ax[0].set_xlim(limite_neg_x-1, limite_pos_x+1)
  ax[0].set_ylim(limite_neg_y-1, limite_pos_y+1)


  ax[0].set_title(f'Vetores representados em 2D com {nome_modelo_escolhido}')
  ax[0].set_xlabel('Dimensão 1')
  ax[0].set_ylabel('Dimensão 2')

  texto = "Resultado:\n('palavra', similaridade)"
  for elemento_vet in lista_de_palavras_e_suas_similaridades:
    texto += '\n\n'+str(elemento_vet)

  ax[1].text(1, 0.5,texto, fontsize=11, ha='center', va='center')

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Comparação Entre Palavras',', '.join(tupla_comparacao)+', X')

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
    
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Comparação Entre Palavras para {nome_modelo_escolhido}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png',' copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Comparação Entre Palavras','\n\n')
  plt.clf()


def ElementoQueNaoCombina(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  try:
    limparConsole()
    print('\n\n\tVocê está gerando resultado para Análise de elemento que menos combina\n\n')

    while True:
      lista_palavras = []
      palavra = formatarEntrada(input('\nDigite uma palavra: '))
      while palavra != '0':
        lista_palavras.append(palavra)
        palavra = formatarEntrada(input('\nDigite mais uma palavra (0 para parar): '))

      if verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=lista_palavras,checagem_unica=True):
        break
      else:
        print('Esse conjunto de palavras não está presente em nenhum dos modelos.\nPor favor digite outro...')
    limparConsole()

    def ajustar_tamanho_fonte(palavra, max_tam_fonte, ax, tam_max=18, min_tam_fonte=8):
      if len(palavra) <= tam_max:
          return max_tam_fonte
      
      max_width = 0.9  # largura máxima permitida dentro do retângulo
      font_size = max_tam_fonte
      while font_size >= min_tam_fonte:
          test_text = ax.text(0.5, 0.5, palavra, ha='center', va='center', fontsize=font_size)
          renderer = ax.figure.canvas.get_renderer()
          bbox = test_text.get_window_extent(renderer=renderer)
          text_width = bbox.width / ax.figure.dpi  # conversão de pixels para polegadas
          test_text.remove()
          if text_width <= max_width:
              return font_size
          font_size -= 1
      return min_tam_fonte

    # txt = f'Analisando qual elemento combina menos com os demais\n\n\n'

    num_series = len(modelos_treinados)
    num_cols = 4
    num_rows = (num_series + num_cols - 1) // num_cols  # Calcula o número de linhas necessárias

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(num_cols * 3, num_rows * 3))

    axes = axes.flatten()
    
    for ax in axes[num_series:]:
        ax.axis('off')

    for (ax, tupla_modelo) in zip(axes, modelos_treinados):
        nome_modelo, modelo = tupla_modelo
        lista_palavras_modelo = [palavra for palavra in lista_palavras if palavra in modelo.index_to_key]
        resultado = modelo.doesnt_match(lista_palavras_modelo)        
        # txt += f'{nome_modelo}: {", ".join(lista_palavras_modelo)}\nElemento que menos combina: {resultado}\n\n'

        for j, palavra in enumerate(lista_palavras_modelo):
            color = 'red' if palavra == resultado else 'green'
            ax.add_patch(plt.Rectangle((0, len(lista_palavras_modelo) - j - 1), 1, 1, color=color))
            
            # Ajusta dinamicamente o tamanho da fonte se a palavra for muito longa
            font_size = ajustar_tamanho_fonte(palavra, 14, ax)
            ax.text(0.5, len(lista_palavras_modelo) - j - 0.5, palavra, ha='center', va='center', color='white', fontsize=font_size)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, len(lista_palavras_modelo))
        ax.axis('off')
        nome_modelo = re.search(r'(\d{4}\_\d{4})',nome_modelo).group(1)
        ax.set_title(f'{nome_modelo}', fontsize=14)

    
    limparConsole()

    palavras_usadas = ', '.join(lista_palavras[:3])+' etc'

    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Elemento que menos combina',palavras_usadas)

    os.makedirs(pasta_para_salvar_palavra_central,exist_ok=True)

    nome_modelo_escolhido = re.sub(r'\_\d{4}\_\d{4}','',modelos_treinados[0][0])

    fig.suptitle(f'Elemento que menos combina dentre os demais\nusando {nome_modelo_escolhido}', fontsize=16)
 
    # ax.set_title(f'Elemento que menos combina dentre os demais\nusando {nome_modelo_escolhido}', fontsize=16,pad=20)

    plt.tight_layout(rect=[0, 0, 1, 0.9])  # Ajusta o layout para não sobrepor o título e deixar espaço em branco
    if num_series > 4:
      plt.subplots_adjust(top=0.85)
    else:
      plt.subplots_adjust(top=0.5)  # Adiciona espaço extra entre o título e os subplots


    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'EQMC_{nome_modelo_escolhido}.png')

    while os.path.exists(caminho_save_fig):
      caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

    plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

    plt.clf()
    # plt.show()
  except Exception as e:
    limparConsole()
    print('\n\n\tOcorreu um problema na geração desta imagem. Por favor, contate um programador do grupo de estudos sobre este cenário.\n\n')
  else:
    limparConsole()
    print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Elemento que menos combina','-->',palavras_usadas,'\n\n')

    # caminho_save_txt = os.path.join(pasta_para_salvar_palavra_central,f'EQMC_{nome_modelo_escolhido}.txt')

    # while os.path.exists(caminho_save_txt):
    #   caminho_save_txt = caminho_save_txt.replace('.txt','_copia.txt')
    
    # with open(caminho_save_txt,'w',encoding='utf-8') as f:
    #   f.write(txt)


def DistanciaEntreVetores(a,b):
  A = np.array([a])
  B = np.array([b])
  return np.linalg.norm(A - B)

def SimilaridadePorCosseno(a,b):
  A = np.array([a])
  B = np.array([b])
  return cosine_similarity(A,B)[0][0]

def MudancaDePalavrasAoDecorrerDoTempo(modelos_treinados : list[tuple], pasta_para_salvar : str = PASTA_SAVE_IMAGENS):
  limparConsole()
  print('Escolha que tipo de mudança você quer visualizar:\n')
  print('1 - Quero visualizar um apanhado geral de todas as palavras')
  print('2 - Quero visualizar para palavras específicas')

  resposta_1 = formatarEntrada(input('\nDigite o número referente à sua escolha: '))
  resposta_1 = obterResposta(resposta=resposta_1,qtd_respostas=2,contagem_normal=True)

  condicoes_filtro = []
  lista_palavras = []

  if resposta_1 == 1:
    limparConsole()
  
    print('Escolha, se quiser, quais filtros você gostaria de aplicar à resposta:\n')
    print('1 - Mostrar somente palavras com mais de 3 letras')
    print('2 - Remover stopwords')
    print('3 - Remover verbos')
    print('4 - Mostrar somente os verbos')
    print('5 - Não quero aplicar nenhum filtro, quero a resposta nua e crua!')
    
    resposta_filtro = formatarEntrada(input('\nDigite os números correspondentes separados por "," (vírgula) em caso de mais de uma resposta:\n'))
    if ',' in resposta_filtro:
      while len([r for r in resposta_filtro.split(',') if not r.isdigit()])>0:
          resposta_filtro = formatarEntrada(input('Por favor, reescreva uma resposta válida (só números): '))
      resposta_filtro = obterResposta(resposta=resposta_filtro,qtd_respostas=5,contagem_normal=True)
    else:
      if resposta_filtro != '5':
        resposta_filtro = obterResposta(resposta=resposta_filtro,qtd_respostas=5,contagem_normal=True)
      else:
        resposta_filtro = int(resposta_filtro)
    
    if resposta_filtro != 5:
      resposta_filtro = str(resposta_filtro)
      if '1' in resposta_filtro:
        condicoes_filtro.append('maior que 3 letras')
      if '2' in resposta_filtro:
        condicoes_filtro.append('remover stopwords')
      if '3' in resposta_filtro:
        condicoes_filtro.append('remover verbos')
      if '4' in resposta_filtro:
        condicoes_filtro.append('somente verbos')

  elif resposta_1 == 2:
    limparConsole()
    palavra = formatarEntrada(input('Digite a primeira palavra: '))
    while True:
      while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra) and palavra != '0':
        palavra = formatarEntrada(input('\n! Esta palavra não está presente em todos os modelos.\n! Por favor, digite outra palavra: '))
      if palavra != '0':
        if palavra not in lista_palavras:
          lista_palavras.append(palavra)
      else:
        break      
      palavra = formatarEntrada(input('\nDigite mais uma palavra (0 para parar): '))

  limparConsole()
  print('Escolha que tipo de taxa de mudança que você quer usar:\n')
  print('1 - Taxa percentual usando apenas a Similaridade de cosseno entre dois períodos')
  print('2 - Taxa percentual usando índice de Jaccard (.png e .txt)')

  resposta_2 = formatarEntrada(input('\nDigite o número referente à sua escolha: '))
  
  while not resposta_2.isdigit():
    resposta_2 = formatarEntrada(input('Por favor, digite o NÚMERO correspondente: '))

  resposta_2 = obterResposta(resposta=resposta_2,qtd_respostas=4,contagem_normal=True)
  
  limparConsole()
  print('Escolha qual início (primeiro modelo) e fim (último modelo) a ser considerado:\n')
  for i, modelo in enumerate([m[0] for m in modelos_treinados]):
    print(f'{i+1} - {modelo}')

  resposta_3 = formatarEntrada(input('\nDigite os números referentes à sua escolha, separados por vírgula e seguindo a ordem "primeiro, último":\n'))
  while len(resposta_3.split(',')) != 2:
    resposta_3 = formatarEntrada(input('\nEsperamos DOIS valores separados por vírgula.\nPor favor, digite os números referentes à sua escolha, separados por vírgula e seguindo a ordem "primeiro, último":\n'))
  while ',' not in resposta_3:
    resposta_3 = formatarEntrada(input('\nPor favor, digite os números referente os números referentes à sua escolha, SEPARADOS POR VÍRGULA e seguindo a ordem "PRIMEIRO MODELO, ÚLTIMO MODELO":\n'))
  while len([r for r in resposta_3.split(',') if not r.isdigit()])>0:
    resposta_3 = formatarEntrada(input('\nPor favor, digite OS NÚMEROS referente os números referentes à sua escolha, SEPARADOS POR VÍRGULA e seguindo a ordem "PRIMEIRO MODELO, ÚLTIMO MODELO":\n'))
    while ',' not in resposta_3:
      resposta_3 = formatarEntrada(input('\nPor favor, digite os números referente os números referentes à sua escolha, SEPARADOS POR VÍRGULA e seguindo a ordem "PRIMEIRO MODELO, ÚLTIMO MODELO":\n'))

  resposta_3 = obterResposta(resposta=resposta_3,qtd_respostas=len(modelos_treinados),contagem_normal=False)

  primeiro_modelo = modelos_treinados[resposta_3[0]]
  ultimo_modelo = modelos_treinados[resposta_3[-1]]


  if resposta_2 == 1:
    TaxaSimilaridadeCosseno(modelo_inicial=primeiro_modelo,
                            modelo_final=ultimo_modelo,
                            lista_de_palavras=lista_palavras,
                            condicoes_filtro=condicoes_filtro)
  elif resposta_2 == 2:
    limparConsole()
    print('\n\n\tVocê está criando uma visualização de Taxa de Mudança Semântica usando Índice de Jaccard.\n\n')
    qtd_vizinhos = formatarEntrada(input('\nDigite a quantidade de vizinhos mais próximos a ser considerada: '))
    while not qtd_vizinhos.isdigit():
      qtd_vizinhos = formatarEntrada(input('\nPor favor, digite um número para representar a quantidade: '))

    qtd_vizinhos = int(qtd_vizinhos)

    TaxaIndiceJaccard(modelo_inicial=primeiro_modelo,
                      modelo_final=ultimo_modelo,
                      lista_de_palavras=lista_palavras,
                      quantidade_de_vizinhos_mais_proximos=qtd_vizinhos)
    

def CalcularTaxaMudancaPelaSimilaridade(similaridade):
    # if similaridade < -1 or similaridade > 1:
    #     raise ValueError("O valor deve estar no intervalo de -1 a 1.")
    taxa = -50 * similaridade + 50
    return round(taxa,4)

def TaxaSimilaridadeCosseno(modelo_inicial,
                            modelo_final,
                            lista_de_palavras : list[str],
                            condicoes_filtro : list[str] = [],
                            pasta_para_salvar=PASTA_SAVE_IMAGENS):
  limparConsole()
  nome_primeiro_modelo, primeiro_modelo = modelo_inicial
  nome_ultimo_modelo, ultimo_modelo = modelo_final

  str_palavras_removidas = ''
  if not lista_de_palavras:
    taxa_global = True
    print('Contabilizando todos os tokens...\nPor favor, aguarde!')
    tokens_filtrados,str_palavras_removidas = Filtro(palavras=primeiro_modelo.index_to_key,condicoes=condicoes_filtro)
    lista_de_palavras = [palavra for palavra in tokens_filtrados]
  else:
    taxa_global = False

  dic_mudanca = {}
  for palavra in lista_de_palavras:
    dic_mudanca[palavra] = CalcularTaxaMudancaPelaSimilaridade(similaridade=SimilaridadePorCosseno(primeiro_modelo[palavra], ultimo_modelo[palavra]))

  dicionario_ordenado = dict(sorted(dic_mudanca.items(), key=lambda item: item[1],reverse=True))

  if taxa_global:
    palavras = list(dicionario_ordenado.keys())[:20]
    numeros = list(dicionario_ordenado.values())[:20]
  else:
    palavras = list(dicionario_ordenado.keys())
    numeros = list(dicionario_ordenado.values())
  

  plt.figure(figsize=(20, 10))

  plt.gca().set_facecolor('ivory')

  bars = plt.bar(palavras, numeros, color='darkorchid') #['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']

  plt.title(f'Maiores mudança dos vetores ao decorrer dos treinamentos\n{nome_primeiro_modelo} até {nome_ultimo_modelo}', fontsize=20, fontweight='bold', pad = 30)
  plt.xlabel('Vetores de palavras', fontsize=16)
  plt.ylabel('Porcentagem de mudança [%]', fontsize=16)

  plt.xticks(rotation=45, ha='right', fontsize=12)

  plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

  for bar in bars:
      bar.set_edgecolor('black')
      bar.set_linewidth(1)

  primeiro_ano_inicial = re.search(r'(\d{4})\_\d{4}',nome_primeiro_modelo).group(1)
  ultimo_ano_final = re.search(r'\d{4}\_(\d{4})',nome_ultimo_modelo).group(1)

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Mudança pela Similaridade por Cosseno')

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
      
  if condicoes_filtro:
    # caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Mudança todas as palavras para {primeiro_ano_inicial} e {ultimo_ano_final} filtro de {" e ".join(condicoes_filtro)}.png')  
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Mdnc_todas_{primeiro_ano_inicial}_{ultimo_ano_final}_filtrado.png')  
  else:
    if taxa_global:
      caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Mdnc_todas_{primeiro_ano_inicial}_{ultimo_ano_final}_sem_filtro.png')
    else:
      caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Mdn_selecionadas_{primeiro_ano_inicial}_{ultimo_ano_final}.png')

  while os.path.exists(caminho_save_fig):
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Mudança pela Similaridade por Cosseno','\n\n')
  if str_palavras_removidas != '':
    print('Os seguintes tokens foram removidos das visualizações:',str_palavras_removidas)

  plt.clf()


# def TaxaSimilaridadeCossenoAcumulada():


def TaxaIndiceJaccard(modelo_inicial,modelo_final,lista_de_palavras,quantidade_de_vizinhos_mais_proximos,pasta_para_salvar=PASTA_SAVE_IMAGENS):

  def indiceJaccard(conjunto_A : list[str],conjunto_B : list[str], detalhes : bool = False):
    uniao = len(set(conjunto_A+conjunto_B))
    interseccao = len([elemento for elemento in conjunto_A if elemento in conjunto_B])
    if not detalhes:
      return interseccao/uniao
    else:
      return {'União':(uniao,set(conjunto_A+conjunto_B)),'Interseção':(interseccao,[elemento for elemento in conjunto_A if elemento in conjunto_B])},interseccao/uniao

  def TaxaDeMudancaUsandoIndiceJaccard(token : str, modelo_t1, modelo_t2, qtd_vizinhos : int = 10, detalhes : bool = False):
    campo_semantico_antes = [resultado[0] for resultado in modelo_t1.most_similar(token,topn=qtd_vizinhos)]
    campo_semantico_depois = [resultado[0] for resultado in modelo_t2.most_similar(token,topn=qtd_vizinhos)]
    if not detalhes:
      taxa_mudanca = 1 - indiceJaccard(conjunto_A=campo_semantico_antes,conjunto_B=campo_semantico_depois,detalhes=detalhes)
      return round(taxa_mudanca*100,2)
    else:
      dic_mudancas, indice = indiceJaccard(conjunto_A=campo_semantico_antes,conjunto_B=campo_semantico_depois,detalhes=detalhes)
      taxa_mudanca = 1 - indice
      return dic_mudancas,round(taxa_mudanca*100,2)

  mudanca_do_campo_semantico = {}

  nome_modelo_inical,modelo_inicial = modelo_inicial
  nome_modelo_final,modelo_final = modelo_final

  txt = 'Detalhes sobre mudança semântica\n\n'
  for palavra in lista_de_palavras:
    txt += f'\nPalavra: "{palavra}"'+'\n'+'='*100+'\n'
    dic_mudancas, taxa_mudanca = TaxaDeMudancaUsandoIndiceJaccard(token=palavra,
                                                                  modelo_t1=modelo_inicial,
                                                                  modelo_t2=modelo_final,
                                                                  qtd_vizinhos=quantidade_de_vizinhos_mais_proximos,
                                                                  detalhes=True)

    mudanca_do_campo_semantico[palavra] = str(taxa_mudanca).replace('.',',')+'%'

    txt+= f'Vizinhos mais próximos com o modelo inicial ({nome_modelo_inical}):\n'
    for i,r in enumerate(modelo_inicial.most_similar(palavra,topn=quantidade_de_vizinhos_mais_proximos)):
      txt+=str(i+1)+' '+str(r)+'\n'
    txt+='-'*100+'\n'
    txt+= f'Vizinhos mais próximos com o modelo final ({nome_modelo_final}):\n'
    for i,r in enumerate(modelo_final.most_similar(palavra,topn=quantidade_de_vizinhos_mais_proximos)):
      txt+=str(i+1)+' '+str(r)+'\n'

    for chave in dic_mudancas:
      txt+= f'\nQuantidade {chave} = {dic_mudancas[chave][0]}: '
      txt += ', '.join(dic_mudancas[chave][1])+'\n'
    taxa_mudanca = str(taxa_mudanca).replace('.',',')+'%'
    txt += f'\nTaxa da Mudança Semântica de {palavra}: {taxa_mudanca}\n\n\n'

  dicionario_ordenado = dict(sorted(mudanca_do_campo_semantico.items(), key=lambda item: item[1],reverse=True))

  print(f'Taxa percentual de mudança semântica com base no\níndice de Jaccard nos top {quantidade_de_vizinhos_mais_proximos} vizinhos mais próximos:\n')
  for chave in dicionario_ordenado:
    print(chave+':',dicionario_ordenado[chave])
  
  palavras = list(dicionario_ordenado.keys())
  numeros = [float(valor.replace('%','').replace(',','.')) for valor in dicionario_ordenado.values()]

  # Criando o gráfico de barras
  plt.figure(figsize=(10, 6))

  # Definindo a cor de fundo do gráfico
  plt.gca().set_facecolor('ivory')

  # Criando as barras com uma paleta de cores diferente
  bars = plt.bar(palavras, numeros, color='darkorchid') #['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']

  plt.ylim(0, 100)

  nome_modelo_escolhido = re.sub(r'\_\d{4}\_\d{4}','',nome_modelo_inical)
  ano_inicial = re.search(r'\_(\d{4})\_\d{4}',nome_modelo_inical).group(1)
  ano_final = re.search(r'\_\d{4}\_(\d{4})',nome_modelo_final).group(1)


  # Adicionando títulos e rótulos
  plt.title(f'Mudança dos vetores de palavras com índice de Jaccard\nusando modelo {nome_modelo_escolhido} de {ano_inicial} até {ano_final}', fontsize=18, fontweight='bold',pad =30)
  plt.xlabel('Vetores de palavras', fontsize=14)
  plt.ylabel('Mudança [%]', fontsize=14)

  # Inclinar as palavras no eixo x
  plt.xticks(rotation=45, fontsize=12)

  # Adicionar uma grade
  plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

  # Adicionando bordas às barras
  for bar in bars:
      bar.set_edgecolor('black')
      bar.set_linewidth(1)

  for bar, valor in zip(bars, numeros):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, f'{valor}%', ha='center', va='bottom', fontsize=10)


  palavras_usadas = ', '.join(lista_de_palavras[:3])+' etc'
  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Mudança pelo índice de Jaccard',palavras_usadas)

  os.makedirs(pasta_para_salvar_palavra_central,exist_ok=True)
    
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'MdcIndJcd.png')
  caminho_save_txt = os.path.join(pasta_para_salvar_palavra_central,f'MdcIndJcd.txt')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png',' copia.png')

  while os.path.exists(caminho_save_txt):  
    caminho_save_txt = caminho_save_txt.replace('.png',' copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Mudança pelo índice de Jaccard','-->',palavras_usadas,'\n\n')
  plt.clf()

  with open(caminho_save_txt,'w',encoding='utf-8') as f:
    f.write(txt)

  

def RedeDinamicaCampoSemantico(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):

  limparConsole()

  print('\n\n\tVocê está montando uma visualização para Rede Dinâmica do Campo Semântico.\n\n')
  palavra_central = formatarEntrada(input('Digite a palavra central: '))

  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = formatarEntrada(input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: '))

  G = nx.Graph()

  def add_nodes_edges(data, year,palavra_central):
      G.add_node(f"{palavra_central}_{year}")
      if palavra_central in data.index_to_key:
          for word, score in data.most_similar(palavra_central, topn=10):
              G.add_node(f"{word}_{year}")
              G.add_edge(f"{palavra_central}_{year}", f"{word}_{year}", weight=score)

  for modelo in modelos_treinados:
    add_nodes_edges(modelo[1], re.search(r'(\d{4})\_\d{4}',modelo[0]).group(1) + ' - ' + re.search(r'\d{4}\_(\d{4})',modelo[0]).group(1),palavra_central=palavra_central)

  pos = nx.spring_layout(G, seed=42, scale=1, k=0.21, weight=1000)#

  plt.figure(figsize=(12, 12))

  nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=300)

  weights = [G[u][v]['weight'] for u, v in G.edges()]
  nx.draw_networkx_edges(G, pos, width=weights, edge_color="grey")

  labels = {}
  for node in G.nodes():
      labels[node] = node.split("_")[0]
  nx.draw_networkx_labels(G, pos, labels, font_size=10)

  for year in [re.search(r'(\d{4})\_\d{4}',modelo[0]).group(1) + ' - ' + re.search(r'\d{4}\_(\d{4})',modelo[0]).group(1) for modelo in modelos_treinados]:
      plt.text(pos[f"{palavra_central}_{year}"][0], pos[f"{palavra_central}_{year}"][1] + 0.25, year, fontsize=14, ha='center',fontweight='bold')

  nome_modelo = re.sub(r'\_\d{4}\_\d{4}','',modelos_treinados[0][0])

  plt.title(f'Rede dinâmica de campos semânticos ao decorrer do tempo\npara "{palavra_central}"\n{nome_modelo}',fontsize=16)
  
  limparConsole()

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Rede Dinâmica',palavra_central)

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
  
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'RD_CS_{palavra_central}_{nome_modelo}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
  
  print('\n\n\tImagem salva em',pasta_para_salvar,'-->','Rede Dinâmica','-->',palavra_central,'\n\n')
  # plt.show()
  plt.clf()



def obterListaStopWords():  
  return ['esses','essa','essas','esta','estas','estes',
          'nesse','nesses','nessa','nessas',
          'apenas','tipo','sim','não','aí',
          'meio','maior','menor','igual','forma',
          'primeiro','segundo','terceiro','quarto','quinto','figura','através',
          'em-que','o-que']

LISTA_STOP_WORDS = obterListaStopWords()

