import matplotlib.pyplot as plt
import numpy as np
from .funcoes import limparConsole
from gensim.models import Word2Vec,KeyedVectors
import time
import os
import sys
from sklearn.decomposition import PCA
import re

PASTA_SAVE_IMAGENS = r'imagens_geradas'

def verificaExistenciaNoModelo(modelos_treinados : list[tuple],palavra_central : str):
  try:
    for modelo in [modelo[1] for modelo in modelos_treinados]:
      modelo[palavra_central]
    return True
  except Exception:
    return False

def SimilaridadeSemanticaAoDecorrerDoTempo(modelos_treinados : list[tuple,tuple],pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Similaridade Semântica ao decorrer do tempo.\n\n')
  palavra_central = input('Digite a palavra central: ').lower()
  while not verificaExistenciaNoModelo(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: ').lower()
    
  cores = ['green','red','c','blue','violet','yellow','orange','black','purple']


  lista_palavras_comparacao = []
  while True:
    if len(lista_palavras_comparacao) < len(cores):
      palavra_digitada = input(f'\nDigite uma palavra para ser comparada (no máximo {len(cores)} e 0 para parar):  ')
      if (palavra_digitada != '0') and verificaExistenciaNoModelo(modelos_treinados,palavra_digitada):
        lista_palavras_comparacao.append(palavra_digitada)
      elif (verificaExistenciaNoModelo(modelos_treinados,palavra_digitada) == False) and (palavra_digitada != '0'):
        while (verificaExistenciaNoModelo(modelos_treinados,palavra_digitada) == False) and (palavra_digitada != '0'):
          palavra_digitada = input(f'Ocorreu um erro com "{palavra_digitada}".\nPor favor, digite outra:  ')
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

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Similaridades ao decorrer do tempo',palavra_central)

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)

  ano_inicial = re.search(r'\d{4}\_',modelos_treinados[0][0]).group()
  ano_final = re.search(r'\_\d{4}',modelos_treinados[-1][0]).group()

  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Similaridade Semântica para modelos de {ano_inicial} até {ano_final}.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  plt.show()




def campoSemanticoAoDecorrerDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Campo Semântico ao decorrer do tempo.\n\n')
  palavra_central = input('Digite uma palavra: ').lower()  
  
  while not verificaExistenciaNoModelo(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: ').lower()

  if not os.path.exists(pasta_para_salvar):
    os.makedirs(pasta_para_salvar)

  for modelo in modelos_treinados:
    campoSemantico(tupla_modelo_escolhido=modelo,
                   palavra_central=palavra_central,
                   pasta_para_salvar=pasta_para_salvar)
        
def campoSemantico(tupla_modelo_escolhido : tuple[str,KeyedVectors],
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

    ax[0].set_title(f'Campo semântico com 10 palavras mais próximas de {palavra_central}\nWOKE CFH {nome_modelo_escolhido}')

    texto = "Resultado:\n('palavra', similaridade)"
    for i in range(len(palavras_vizinhas_com_similaridade)):
      texto += '\n\n'+str(palavras_vizinhas_com_similaridade[i])

    ax[1].text(1, 0.5,texto, fontsize=11, ha='center', va='center')

    # plt.show()
    pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Campo Semântico',palavra_central)

    if not os.path.exists(pasta_para_salvar_palavra_central):
      os.makedirs(pasta_para_salvar_palavra_central)
    
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Campo Semântico - {nome_modelo_escolhido}.png')

    plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
    print(f'\n\n\tImagem salva com sucesso para {nome_modelo_escolhido}!\n\n')
  except:
    limparConsole()
    print(f'Ocorreu um erro com a palavra {palavra}...')
    # erro = f'Na função: campoSemantico, usando {nome_modelo_escolhido}.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    # with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    #   f.write(erro+'\n\n')
  else:
    plt.clf()