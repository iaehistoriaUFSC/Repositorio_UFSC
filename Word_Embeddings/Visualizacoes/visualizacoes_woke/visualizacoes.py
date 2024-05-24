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

def SimilaridadesAoDecorrerDoTempo(modelos_treinados : list[tuple],pasta_para_salvar=PASTA_SAVE_IMAGENS):
  
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


  ax.set_title(f'Similaridade entre "{palavra_central}" e outras palavras selecionadas\nWOKE', fontsize=20, pad= 25)
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

  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Similaridades para modelos de {ano_inicial} até {ano_final}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  plt.clf()
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
    
    caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Vizinhos mais próximos - {nome_modelo_escolhido} - {palavra_central}.png')

    while os.path.exists(caminho_save_fig):  
      caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

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


def MapaDeCalorSimilaridadesAoDecorrerDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  
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
    data[re.search(r'(\d{4})\_\d{4}',nome_modelo_escolhido).group(1) + '\n-\n' + re.search(r'\d{4}\_(\d{4})',nome_modelo_escolhido).group(1)] = dic_comparativo




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

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
  
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Mapas de Calor','-->',palavra_central,'\n\n')
  
  plt.clf()
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
  
  plt.xticks(rotation=45, ha='right')

  ano_inicial = re.search(r'(\d{4})\_\d{4}',nome_modelo_escolhido).group(1)

  ano_final = re.search(r'\d{4}\_(\d{4})',nome_modelo_escolhido).group(1)

  plt.title(f"Frequência de palavras treinamento {ano_inicial} - {ano_final}",fontsize=20)

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Frequência de Palavras')

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
    
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Frequência de palavras para {nome_modelo_escolhido}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Frequência de Palavras','\n\n')
  plt.clf()

  # plt.show()


def EstratosDoTempo(modelos_treinados,pasta_para_salvar=PASTA_SAVE_IMAGENS):
  def pega_cor(bg_color):
      gray = np.dot(bg_color, [0.2989, 0.5870, 0.1140])
      return 'black' if gray > 0.5 else 'white'

  def agrupar_em_trios(lista):
      lista_nova = [(lista[i], lista[i + 1], lista[i + 2]) for i in range(0, len(lista), 3)]
      return lista_nova
  
  print('\n\n\tVocê está montando uma visualização para Estratos do Tempo.\n\n')
  palavra_central = input('Digite a palavra central: ').lower().strip()

  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra_central):
    palavra_central = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra palavra: ').lower().strip()

  data = {}

  for nome_modelo, modelo in modelos_treinados:

    ano_inicial = re.search(r'(\d{4})\_\d{4}',nome_modelo).group(1)
    ano_final = re.search(r'\d{4}\_(\d{4})',nome_modelo).group(1)

    chave = ano_inicial + ' - ' + ano_final

    lista_valores = [{r[0]:r[1]} for r in modelo.most_similar(palavra_central)]

    data[chave] = lista_valores


  lista_de_tuplas = list(data.items())
  lista_de_tuplas_invertida = lista_de_tuplas[::-1]
  data = dict(lista_de_tuplas_invertida)


  index = list(data.keys())
  values = [[list(d.values())[0] for d in data[key]] for key in data]

  heatmap_values = [[list(data[key][0].values())[0]] for key in data]
  df = pd.DataFrame(heatmap_values, index=index)

  plt.figure(figsize=(8, 8))
  heatmap = sns.heatmap(df, annot=False, fmt="", cmap='coolwarm', cbar=True, cbar_kws={'shrink': 0.8})
  # heatmap = sns.heatmap(df, annot=False, fmt="", cmap='coolwarm', cbar=True, cbar_kws={'shrink': 0.8}, linewidths=1, linecolor='black')


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

  plt.title(f'Estratos do Tempo\npara "{palavra_central}"', fontsize=20, pad=30)
  plt.tight_layout()

  limparConsole()

  pasta_para_salvar_palavra_central = os.path.join(pasta_para_salvar,'Estratos do Tempo',palavra_central)

  if not os.path.exists(pasta_para_salvar_palavra_central):
    os.makedirs(pasta_para_salvar_palavra_central)
  
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Estratos do Tempo para {palavra_central}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png','_copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')
  
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Estratos do Tempo','-->',palavra_central,'\n\n')
  
  plt.clf()

def VetoresDePalavrasAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Vetores de Palavras ao decorrer do tempo.\n\n')

  lista_de_palavras = []
  palavra = input('Digite a primeira palavra: ').lower().strip()
  while palavra != '0':
    while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=palavra) and palavra != '1':
      print(f'A palavra "{palavra}" não está presente em todos os modelos, em algumas imagens ela não aparecerá.')
      print('Caso queira substituí-la por outra, digite abaixo qual palavra a substituirá.')
      print('Caso queira removê-la do conjunto de palavras, digite 1')
      print('Digite 0 caso queira parar de escolher palavras.')
      palavra = input().lower().strip()    
    
    if palavra != '1':
      if palavra not in lista_de_palavras:
        lista_de_palavras.append(palavra)
    palavra = input('\nDigite mais uma palavra (0 para parar): ').lower().strip()

  for modelo in modelos_treinados:
    vetoresDePalavras(tupla_modelo_escolhido=modelo,
                      lista_de_palavras=lista_de_palavras,
                      pasta_para_salvar=pasta_para_salvar)

def vetoresDePalavras(tupla_modelo_escolhido,
                      lista_de_palavras : list[str],
                      pasta_para_salvar : str):

  nome_modelo_escolhido,modelo_escolhido = tupla_modelo_escolhido
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
    
  caminho_save_fig = os.path.join(pasta_para_salvar_palavra_central,f'Vetores de palavras para {nome_modelo_escolhido} - {", ".join(lista_de_palavras[:3])+" etc"}.png')

  while os.path.exists(caminho_save_fig):  
    caminho_save_fig = caminho_save_fig.replace('.png',' copia.png')

  plt.savefig(caminho_save_fig, dpi=300, bbox_inches='tight')

  limparConsole()
  print('\n\n\tImagem salva em',PASTA_SAVE_IMAGENS,'-->','Vetores de palavras','\n\n')
  plt.clf()


def ComparacaoEntrePalavrasAoDecorrerDoTempo(modelos_treinados, pasta_para_salvar=PASTA_SAVE_IMAGENS):
  print('\n\n\tVocê está montando uma visualização para Comparacao Entre Palavras ao decorrer do tempo.\n\n')

  print('\n\nHomem --> Rei\n\nMulher --> X\n\n')

  homem = input('O que deseja substituir por "homem"? ').lower().strip()
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=homem):
    homem = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra: ').lower().strip()

  rei = input('O que deseja substituir por "rei"? ')
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=rei):
    rei = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra: ').lower().strip()
  
  mulher = input('O que deseja substituir por "mulher"? ')
  while not verificaExistenciaNosModelos(modelos_treinados=modelos_treinados,palavra_central=mulher):
    mulher = input('Esta palavra não está presente em todos os modelos.\nPor favor, digite outra: ').lower().strip()      

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

  lista_de_vetores_base = [[1,5],[5,7],[2,2],[6,4]]
  lista_de_vetores_adc = []

  for i,r in enumerate(resultado[1:]):
    if i ==0:
      raiox = 1-r[1] + 0.25
      raioy = 1-r[1] + 0.25
    elif i ==1:
      raiox = 1-r[1] -0.75
      raioy = 1-r[1] -0.5
    elif i ==2:
      raiox = 0
      raioy = 0.87
    elif i ==3:
      raiox = 1-r[1] + 0.5
      raioy = 1-r[1] -0.87
    elif i ==4:
      raiox = 1-r[1] +0.6
      raioy = 1-r[1] +0.5
    elif i ==5:
      raiox = 1-r[1] -0.9
      raioy = 1-r[1] +0.7
    elif i ==6:
      raiox = 1-r[1] + - 1
      raioy = 1-r[1] - 0
    elif i ==7:
      raiox = 1-r[1] +1.1
      raioy = 1-r[1] -0
    elif i ==8:
      raiox = 1-r[1] +1.2
      raioy = 1-r[1] -0.25
    lista_de_vetores_adc.append([6+raiox,4+raioy])


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
