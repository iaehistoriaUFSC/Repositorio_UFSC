import matplotlib.pyplot as plt
import numpy as np
from .funcoes import limparConsole
from gensim.models import KeyedVectors
import time
import os
from sklearn.decomposition import PCA
import seaborn as sns
import pandas as pd
import re

PASTA_SAVE_IMAGENS = r'imagens_geradas'

def verificaExistenciaNosModelos(modelos_treinados : list[tuple],palavra_central : str):
  try:
    for modelo in [modelo[1] for modelo in modelos_treinados]:
      modelo[palavra_central]
    return True
  except Exception:
    return False

def SimilaridadesAoDecorrerDoTempo(modelos_treinados : list[tuple,tuple],pasta_para_salvar=PASTA_SAVE_IMAGENS):
  
  print('\n\n\tVocê está montando uma visualização para Similaridade Semântica ao decorrer do tempo.\n\n')
  palavra_central = input('Digite a palavra central: ').lower().strip()
  
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: ').lower().strip()
    
  cores = ['green','red','c','blue','violet','yellow','orange','black','purple']


  lista_palavras_comparacao = []
  while True:

    if len(lista_palavras_comparacao) < len(cores):
      palavra_digitada = input(f'\nDigite uma palavra para ser comparada (no máximo {len(cores)} e 0 para parar):  ').lower().strip()

      if (palavra_digitada != '0') and verificaExistenciaNosModelos(modelos_treinados,palavra_digitada):
        lista_palavras_comparacao.append(palavra_digitada)
      elif (verificaExistenciaNosModelos(modelos_treinados,palavra_digitada) == False) and (palavra_digitada != '0'):
        while (verificaExistenciaNosModelos(modelos_treinados,palavra_digitada) == False) and (palavra_digitada != '0'):
          palavra_digitada = input(f'Ocorreu um erro com "{palavra_digitada}".\nPor favor, digite outra:  ').lower().strip()
        lista_palavras_comparacao.append(palavra_digitada)
      else:
        break
    else:
      break



  nomes = [modelo[0].replace('_','\n-\n') for modelo in modelos_treinados]

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


  ax.set_title(f'Similaridade semântica entre "{palavra_central}" e outras palavras selecionadas\nWOKE', fontsize=20, pad= 25)
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

  ano_inicial = re.search(r'\d{4}\_',modelos_treinados[0][0]).group()
  ano_final = re.search(r'\_\d{4}',modelos_treinados[-1][0]).group()

  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Similaridades para modelos de {ano_inicial} até {ano_final}.png')

  if os.path.exists(caminho_save_fig):
    caminho_save_fig = caminho_save_fig.replace('.png',caminho_save_fig[-5]+'_.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  # plt.show()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Gráfico Similaridades','-->',palavra_central,'\n\n')
  

def VizinhosMaisProximosAoDecorrerDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Vizinhos mais Próximos ao decorrer do tempo.\n\n')
  palavra_central = input('Digite uma palavra: ').lower().strip()
  
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: ').lower().strip()

  if not os.path.exists(pasta_para_salvar):
    os.makedirs(pasta_para_salvar)

  for modelo in modelos_treinados:
    VizinhosMaisProximos(tupla_modelo_escolhido=modelo,
                        palavra_central=palavra_central,
                        pasta_para_salvar=pasta_para_salvar)
        
def VizinhosMaisProximos(tupla_modelo_escolhido : tuple[str,KeyedVectors],
                        palavra_central : str,
                        pasta_para_salvar : str):
  
  try:
    nome_modelo_escolhido = tupla_modelo_escolhido[0]
    modelo_escolhido = tupla_modelo_escolhido[1]
    
    palavras_vizinhas = modelo_escolhido.most_similar(palavra_central)

    palavras_vizinhas = []
    palavras_vizinhas_com_similaridade= []

    for palavra in modelo_escolhido.most_similar(palavra_central):
      palavras_vizinhas.append(palavra[0])
      palavras_vizinhas_com_similaridade.append((palavra[0],palavra[1]))


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
    
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Vizinhos mais próximos - {nome_modelo_escolhido}.png')

    if os.path.exists(caminho_save_fig):
      caminho_save_fig = caminho_save_fig.replace('.png',caminho_save_fig[-5]+'_.png')

    plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  except:
    limparConsole()
    print(f'Ocorreu um erro com a palavra {palavra}...')
    # erro = f'Na função: campoSemantico, usando {nome_modelo_escolhido}.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    # with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    #   f.write(erro+'\n\n')
  else:
    limparConsole()
    print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Vizinhos mais próximos','-->',palavra_central,'\n\n')
    plt.clf()


def MapaDeCalorAoDecorrerDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  
  print('\n\n\tVocê está montando uma visualização para Mapa de Calor ao decorrer do tempo.\n\n')
  palavra_central = input('Digite a palavra central: ').lower().strip()

  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: ').lower().strip()

  palavras_selecionadas = []

  while True:
    palavra_digitada = input('Digite a palavra para ser comparada com a palavra central (0 para parar): ').lower().strip()
    if palavra_digitada != '0':
      palavras_selecionadas.append(palavra_digitada)
    else:
      break


  data = {}

  for nome_modelo_escolhido,modelo in modelos_treinados:
    dic_comparativo = {}
    for palavra_selecionada in palavras_selecionadas:
      try:
        dic_comparativo[palavra_selecionada] = modelo.similarity(palavra_central,palavra_selecionada)
      except:
        dic_comparativo[palavra_selecionada] = 0
    data[nome_modelo_escolhido.replace('_','\n-\n')] = dic_comparativo


  df = pd.DataFrame(data)

  plt.figure(figsize=(16, 8))
  heatmap = sns.heatmap(df, annot=True, cmap='coolwarm')

  heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=0)
  heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0,fontsize=11)


  plt.title(f'Mapa de calor da similaridade para palavra "{palavra_central}"',fontsize=20)
  
  limparConsole()

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Mapas de Calor',palavra_central)

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
  
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Mapa de Calor para {palavra_central}.png')

  if os.path.exists(caminho_save_fig):
    caminho_save_fig = caminho_save_fig.replace('.png',caminho_save_fig[-5]+'_.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
  
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Mapas de Calor','-->',palavra_central,'\n\n')
  
  # plt.show()


def FrequenciaDePalavrasAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS):

  for modelo in modelos_treinados:
    FrequenciaDePalavras(tupla_modelo_escolhido=modelo,
                        pasta_para_salvar=pasta_para_salvar)
    
def FrequenciaDePalavras(tupla_modelo_escolhido,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  nome_modelo_escolhido,modelo = tupla_modelo_escolhido
  plt.figure(figsize=(20, 10))
  # plt.bar([word for word in [palavra for palavra in modelo.wv.index_to_key[:500] if (palavra not in ['como','uma','um','ao','mais','mesmo','forma','pois','essa','apenas','parte','além','nesse']) and (nlp_spacy(palavra)[0].pos_ not in ['VERB','AUX']) and (len(palavra)>3)][:20]],[modelo.wv.get_vecattr(word,'count') for word in [palavra for palavra in modelo.wv.index_to_key[:500] if (palavra not in ['como','uma','um','ao','mais','mesmo','forma','pois','essa','apenas','parte','além','nesse']) and (nlp_spacy(palavra)[0].pos_ not in ['VERB','AUX']) and (len(palavra)>3)][:20]])
  
  plt.bar([word for word in [palavra for palavra in modelo.index_to_key[:500] if (palavra not in ['como','uma','um','ao','mais','mesmo','forma','pois','essa','apenas','parte','além','nesse']) and (len(palavra)>3)][:20]],[modelo.get_vecattr(word,'count') for word in [palavra for palavra in modelo.index_to_key[:500] if (palavra not in ['como','uma','um','ao','mais','mesmo','forma','pois','essa','apenas','parte','além','nesse']) and (len(palavra)>3)][:20]])
  
  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Frequência de Palavras',nome_modelo_escolhido)

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
    
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Frequência de palavras para {nome_modelo_escolhido}.png')

  if os.path.exists(caminho_save_fig):
    caminho_save_fig = caminho_save_fig.replace('.png',caminho_save_fig[-5]+'_.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Frequência de Palavras','\n\n')
  plt.clf()

  # plt.show()
