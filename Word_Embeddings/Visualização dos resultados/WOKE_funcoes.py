from WOKE_carregando_modelos import *

def limpa_tela():
  output.clear()
  print(('* '*50)+'*')
  print('*'+(' '*99)+'*')
  print('*'+'\t\tPROGRAMA DE EXIBIÇÃO DE MODELO DE WORD EMBEDDING PRÉ-TREINADO'+(' '*8)+(' '*15)+'*')
  print('*'+(' '*99)+'*')
  print(('* '*50)+'*')
  print('\n')
  
def verificaExistenciaNoModelo(modelo_escolhido,palavra_central):
  existe = False
  while not existe:
    try:
      modelo_escolhido.most_similar(palavra_central)
    except:
      existe = False
      palavra_central = input(f'Ocorreu um erro com "{palavra_central}".\nPor favor, digite outra palavra: ')
    else:
      existe = True
  return palavra_central

def InfoModelo(modelo):
  return info[modelo]['base_dataset'], info[modelo]['Dimensão'], info[modelo]['Descrição']

def mostraInformacaoDoModelo(nome_modelo_escolhido,modelo_escolhido):
  limpa_tela()
  dataset, dimensao, descricao = InfoModelo(nome_modelo_escolhido)
  print('\tInformações sobre modelo utilizado')
  print(f'\nModelo:\n{nome_modelo_escolhido}.')
  print(f'\nDataset usado no treinamento:\n{dataset}.')
  print(f'\nDimensão:\n{dimensao}.')
  print(f'\nDescrição do modelo:\n{descricao}')
  time.sleep(2)
  input('\n\n\t--> Pressione "Enter" para voltar para o Menu inicial.')

  escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido)


def campoSemantico(nome_modelo_escolhido,modelo_escolhido, palavra):
  try:
    output.clear()
    if palavra == '':
      palavra_central = input(f'Você está usando {nome_modelo_escolhido}.\nDigite uma palavra para construir o campo semântico: ')
      palavra_central = verificaExistenciaNoModelo(modelo_escolhido,palavra_central)
    else:
      palavra_central = palavra
      palavra_central = verificaExistenciaNoModelo(modelo_escolhido,palavra_central)
    output.clear()

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

    ax[0].set_title(f'Campo semântico com 10 palavras mais próximas usando {nome_modelo_escolhido}')

    texto = "Resultado:\n('palavra', similaridade)"
    for i in range(len(palavras_vizinhas_com_similaridade)):
      texto += '\n\n'+str(palavras_vizinhas_com_similaridade[i])

    ax[1].text(1, 0.5,texto, fontsize=11, ha='center', va='center')

    # plt.show()
    plt.savefig(f'/content/Campo semântico de {palavra_central} usando {nome_modelo_escolhido}.png', dpi=300, bbox_inches='tight')
    print('\n\n\tImagem salva com sucesso!\n\n')
  except:
    output.clear()
    print('Ocorreu um erro inesperado...')
    erro = 'Na função: campoSemantico.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
      f.write(erro+'\n\n')
      f.close()
  time.sleep(5)
  plt.clf()
  output.clear()
  print('\nO que deseja fazer?\n')
  print(f'1 - Construir campo semântico da mesma palavra ({palavra_central}) com outro modelo')
  print(f'2 - Construir campo semântico para outra palavra com o modelo {nome_modelo_escolhido}')
  print(f'3 - Testar outra funcionalidade do modelo {nome_modelo_escolhido}')
  print('4 - Voltar para o menu principal')
  ans_cs = input('\nDigite o número referente a sua escolha: ')
  while ans_cs not in ['1','2','3','4']:
    ans_cs = input('\nDigite o número referente a sua escolha entre (1 e 4): ')
  if ans_cs == '1':
    nome_modelo_escolhido,modelo_escolhido = escolhaDeModelo()
    campoSemantico(nome_modelo_escolhido,modelo_escolhido,palavra_central)
  elif ans_cs == '2':
    campoSemantico(nome_modelo_escolhido,modelo_escolhido,'')
  elif ans_cs == '3':
    escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido)
  elif ans_cs == '4':
    menu()


def vetoresDePalavras(nome_modelo_escolhido,modelo_escolhido):
  try:
    lista_de_palavras = []
    output.clear()
    palavra = input('Digite a primeira palavra: ')
    while palavra != '0':
      try:
        vetor_palavra = modelo_escolhido.get_vector(palavra)
      except:
        palavra = input(f'\nA palavra {palavra} não foi carregada com sucesso, provavelmente não foi encontrada no vocabulário.\nDigite outra palavra (0 para parar): ')
      else:
        lista_de_palavras.append(palavra)
        palavra = input('\nDigite mais uma palavra (0 para parar): ')


    lista_de_vetores = [modelo_escolhido.get_vector(palavra) for palavra in lista_de_palavras]

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
    ax[0].grid('off')

    for i, palavra in enumerate(lista_de_palavras):
        ax[0].arrow(0, 0, lista_de_vetores_2D[i, 0], lista_de_vetores_2D[i, 1], head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        # plt.quiver(0, 0, vetores_pca[i, 0], vetores_pca[i, 1], angles='xy', scale_units='xy', scale=1, color='b', label='Vetores')
        ax[0].text(lista_de_vetores_2D[i, 0], lista_de_vetores_2D[i, 1]+0.25, palavra, fontsize=12, ha='center', va='center', color='black')

    ax[0].set_xlim(limite_neg_x-1, limite_pos_x+1)
    ax[0].set_ylim(limite_neg_y-1, limite_pos_y+1)

    cosseno_formula = r'$\cos(\theta) = \frac{\mathbf{v} \cdot \mathbf{u}}{\|\mathbf{v}\| \cdot \|\mathbf{u}\|}$'

    ax[1].text(0.25, 0.5,cosseno_formula, fontsize=20, ha='center', va='center')

    ax[0].set_title(f'Vetores de palavras representados em 2D com {nome_modelo_escolhido}')
    ax[0].set_xlabel('Dimensão 1')
    ax[0].set_ylabel('Dimensão 2')
    output.clear()
    # plt.show()
    plt.savefig(f'/content/Gráfico de vetores de palavras com resultados de {nome_modelo_escolhido} para {str(lista_de_palavras)}.png', dpi=300, bbox_inches='tight')
    print('\n\n\tImagem salva com sucesso!\n\n')
  except:
    output.clear()
    print('Ocorreu um erro inesperado...')
    erro = 'Na função: vetoresDePalavras.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
      f.write(erro+'\n\n')
      f.close()
  time.sleep(5)
  plt.clf()
  output.clear()
  print('\nO que deseja fazer?\n')
  print(f'1 - Visualizar vetores de palavras com outro modelo')
  print(f'2 - Visualizar outros vetores de palavras com o modelo {nome_modelo_escolhido}')
  print(f'3 - Testar outra funcionalidade do modelo {nome_modelo_escolhido}')
  print('4 - Voltar para o menu principal')
  ans_vet = input('\nDigite o número referente a sua escolha: ')
  while ans_vet not in ['1','2','3','4']:
    ans_vet = input('\nDigite o número referente a sua escolha entre (1 e 4): ')
  if ans_vet == '1':
    nome_modelo_escolhido,modelo_escolhido = escolhaDeModelo()
    vetoresDePalavras(nome_modelo_escolhido,modelo_escolhido)(nome_modelo_escolhido,modelo_escolhido,palavra_central)
  elif ans_vet == '2':
    vetoresDePalavras(nome_modelo_escolhido,modelo_escolhido)(nome_modelo_escolhido,modelo_escolhido,'')
  elif ans_vet == '3':
    escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido)
  elif ans_vet == '4':
    menu()

def distanciaEntrePalavras(nome_modelo_escolhido,modelo_escolhido):
  try:
    output.clear()
    print('\nO que você gostaria de fazer?')
    print('\n1 - Analisar a distância entre duas palavras')
    print('2 - Analisar a proximidade de uma palavra entre outras duas')
    ans_dist = input('\nDigite o número referente a sua escolha: ')
    while ans_dist not in ['1','2']:
      ans_dist = input('\nDigite o número referente a sua escolha entre (1 e 2): ')
    if ans_dist == '1':
      output.clear()
      print(f'Comparando distância entre duas palavras com {nome_modelo_escolhido}')
      palavra1 = input('\nEscolha a primeira palavra: ')
      palavra1 = verificaExistenciaNoModelo(modelo_escolhido,palavra1)
      palavra2 = input('\nEscolha a segunda palavra: ')
      palavra2 = verificaExistenciaNoModelo(modelo_escolhido,palavra2)
      distancia = modelo_escolhido.distance(palavra1,palavra2)
      output.clear()
      print(f'Comparando distância entre duas palavras com {nome_modelo_escolhido}')
      print(f'\n\nA distância entre {palavra1} e {palavra2} é de: {distancia}')
      lista_de_vetores_exemplo_dist = [[1,1],[5,2]]
      lista_de_palavras = [palavra1,palavra2]

      limite_pos_x = 0
      limite_neg_x = 0
      limite_pos_y = 0
      limite_neg_y = 0
      x = []
      y = []

      for coords in lista_de_vetores_exemplo_dist:
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

      for i, palavra in enumerate(lista_de_palavras):
        plt.scatter(x[i], y[i],color='b')
        plt.text(x[i], y[i]+0.25, palavra, fontsize=12
                , ha='center', va='center', color='black')

      plt.arrow(x[0],y[0],x[1]-x[0],y[1]-y[0],head_width=0.1, head_length=0.1, fc='red', ec='red')
      plt.text((x[1]-x[0]-x[0]),(y[0]+(y[1]-y[0])/2)+0.25,round(distancia,5), fontsize=11, ha='center', va='center', color='black')

      plt.grid(True)
      plt.xlim(limite_neg_x-1, limite_pos_x+2)
      plt.ylim(limite_neg_y-1, limite_pos_y+2)

      plt.title(f'Distância entre vetores representada em 2D com {nome_modelo_escolhido}')
      plt.xlabel('Dimensão 1')
      plt.ylabel('Dimensão 2')
      # plt.show()
      plt.savefig(f'/content/Gráfico de distância entre duas palavras resultados de {nome_modelo_escolhido} para {str(lista_de_palavras)}.png', dpi=300, bbox_inches='tight')
      print('\n\n\tImagem salva!\n\n')      

    elif ans_dist == '2':
      output.clear()
      print(f'Comparando distância entre três palavras com {nome_modelo_escolhido}')
      palavra1 = input('\nEscolha a primeira palavra: ')
      palavra1 = verificaExistenciaNoModelo(modelo_escolhido,palavra1)
      palavra2 = input('\nEscolha a segunda palavra: ')
      palavra2 = verificaExistenciaNoModelo(modelo_escolhido,palavra2)
      palavra3 = input('\nEscolha a terceira palavra: ')
      palavra3 = verificaExistenciaNoModelo(modelo_escolhido,palavra3)

      distancia1_2 = modelo_escolhido.distance(palavra1,palavra2)
      distancia1_3 = modelo_escolhido.distance(palavra1,palavra3)
      output.clear()
      print(f'Comparando distância entre três palavras com {nome_modelo_escolhido}')
      if distancia1_2 < distancia1_3:
        palavra_mais_perto = palavra2
        palavra_mais_longe = palavra3
        distancia_perto = distancia1_2
        distancia_longe = distancia1_3
        print(f'\n\n{palavra1} está mais perto de {palavra2} do que de {palavra3}!')
      else:
        palavra_mais_perto = palavra3
        palavra_mais_longe = palavra2
        distancia_perto = distancia1_3
        distancia_longe = distancia1_2
        print(f'\n\n{palavra1} está mais perto de {palavra3} do que de {palavra2}!')

      print(f'\n\n{palavra1} --> {palavra2}\n{distancia1_2}')
      print(f'\n\n{palavra1} --> {palavra3}\n{distancia1_3}\n')


      lista_de_vetores_exemplo_dist = [[1,1],[5,2.5],[8,2]]
      lista_de_palavras = [palavra1,palavra_mais_perto,palavra_mais_longe]

      limite_pos_x = 0
      limite_neg_x = 0
      limite_pos_y = 0
      limite_neg_y = 0
      x = []
      y = []

      for coords in lista_de_vetores_exemplo_dist:
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

      for i, palavra in enumerate(lista_de_palavras):
        plt.scatter(x[i], y[i],color='b')
        plt.text(x[i], y[i]+0.25, palavra, fontsize=12
                , ha='center', va='center', color='black')

      plt.arrow(x[0],y[0],x[1]-x[0],y[1]-y[0],head_width=0.1, head_length=0.1, fc='red', ec='red')
      plt.text((x[1]-x[0]-x[0]),(y[0]+(y[1]-y[0])/2)+0.25,round(distancia_perto,5), fontsize=11, ha='center', va='center', color='black')

      plt.arrow(x[0],y[0],x[2]-x[0],y[2]-y[0],head_width=0.1, head_length=0.1, fc='red', ec='red')
      plt.text((x[2]-x[0]-x[0]),(y[0]+(y[2]-y[0])/2)-0.15,round(distancia_longe,5), fontsize=11, ha='center', va='center', color='black')

      plt.grid(True)
      plt.xlim(limite_neg_x-1, limite_pos_x+2)
      plt.ylim(limite_neg_y-1, limite_pos_y+2)

      plt.title(f'Distância entre vetores representada em 2D com {nome_modelo_escolhido}')
      plt.xlabel('Dimensão 1')
      plt.ylabel('Dimensão 2')
      # plt.show()
      plt.savefig(f'/content/Gráfico de distância entre três palavras resultados de {nome_modelo_escolhido} para {str(lista_de_palavras)}.png', dpi=300, bbox_inches='tight')
      print('\n\n\tImagem salva!\n\n')
  except:
    output.clear()
    print('Ocorreu um erro inesperado...')
    erro = 'Na função: distanciaEntrePalavras.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
      f.write(erro+'\n\n')
      f.close()
  time.sleep(5)
  output.clear()
  plt.clf()
  print('\nO que deseja fazer?')
  print(f'\n1 - Continuar analisando distância entre palavras')
  print(f'2 - Testar outra funcionalidade do modelo {nome_modelo_escolhido}')
  print('3 - Voltar para o menu principal')
  ans_vet = input('\nDigite o número referente a sua escolha: ')
  while ans_vet not in ['1','2','3']:
    ans_vet = input('\nDigite o número referente a sua escolha entre (1 e 4): ')
  if ans_vet == '1':
    distanciaEntrePalavras(nome_modelo_escolhido,modelo_escolhido)
  elif ans_vet == '2':
    escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido)
  elif ans_vet == '3':
    menu()


def comparacaoEntrePalavras(nome_modelo_escolhido,modelo_escolhido):
  try:
    output.clear()
    print(f'Comparação de palavras usando {nome_modelo_escolhido}')
    print('\n\n\nHomem --> Rei\n\nMulher --> X\n\n\n')
    man = input('O que deseja substituir por "homem"? ')
    man = verificaExistenciaNoModelo(modelo_escolhido,man)
    king = input('O que deseja substituir por "rei"? ')
    king = verificaExistenciaNoModelo(modelo_escolhido,king)
    woman = input('O que deseja substituir por "mulher"? ')
    woman = verificaExistenciaNoModelo(modelo_escolhido,woman)
    output.clear()
    print(f'Resposta usando {nome_modelo_escolhido}\n')
    print(f'\n\t{king} - {man} + {woman} = ?')
    resultado = modelo_escolhido.most_similar_cosmul(positive=[king,woman], negative=[man])
    time.sleep(1)
    output.clear()
    print(f'Resposta usando {nome_modelo_escolhido}\n')
    print(f'\n\t{king} - {man} + {woman} = {resultado[0][0].upper()}')
    print('\n\n')


    lista_de_palavras = []
    lista_de_palavras.append(man)
    lista_de_palavras.append(king)
    lista_de_palavras.append(woman)
    resultado = modelo_escolhido.most_similar_cosmul(positive=[king,woman], negative=[man])
    lista_de_palavras.extend(r[0] for r in resultado)

    lista_de_palavras_e_suas_similaridades = [(r[0],r[1]) for r in resultado]

    lista_de_vetores_exemplo = [[1,5],[5,7],[2,2],[6,4]]
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


    lista_de_vetores_2D = lista_de_vetores_exemplo
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

    # fig, ax = plt.subplots(figsize=(12, 5))
    fig, ax = plt.subplots(1, 2,figsize=(12, 5),gridspec_kw={'width_ratios': [4, 1]})

    ax[0].grid('on')
    # ax[1].grid('off')
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
    # plt.xlim(limite_neg_x-1, limite_pos_x+1)
    # plt.ylim(limite_neg_y-1, limite_pos_y+1)

    ax[0].set_title(f'Vetores representados em 2D com {nome_modelo_escolhido}')
    ax[0].set_xlabel('Dimensão 1')
    ax[0].set_ylabel('Dimensão 2')
    # # Remove os valores dos eixos
    # plt.xticks([])
    # plt.yticks([])

    texto = "Resultado:\n('palavra', similaridade)"
    for elemento_vet in lista_de_palavras_e_suas_similaridades:
      texto += '\n\n'+str(elemento_vet)

    ax[1].text(1, 0.5,texto, fontsize=11, ha='center', va='center')

    # plt.show()
    plt.savefig(f'/content/Gráfico de comparação entre palavras resultados de {nome_modelo_escolhido} para {str(lista_de_palavras[0:4])}.png', dpi=300, bbox_inches='tight')
    print('\n\n\tImagem salva com sucesso!\n\n')
  except:
    output.clear()
    print('Ocorreu um erro inesperado...')
    erro = 'Na função: comparacaoEntrePalavras.\nDescrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'
    with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
      f.write(erro+'\n\n')
      f.close()
  time.sleep(5)
  plt.clf()
  output.clear()
  print('\nO que deseja fazer?')
  print(f'\n1 - Continuar comparando palavras com o modelo {nome_modelo_escolhido}')
  print('2 - Continuar comparando palavras, mas com outro modelo')
  print(f'3 - Testar outra funcionalidade do modelo {nome_modelo_escolhido}')
  print('4 - Voltar para o menu principal')
  ans_comp = input('\nDigite o número referente a sua escolha: ')
  while ans_comp not in ['1','2','3','4']:
    ans_comp = input('\nDigite o número referente a sua escolha entre (1 e 4): ')
  if ans_comp == '1':
    comparacaoEntrePalavras(nome_modelo_escolhido,modelo_escolhido)
  elif ans_comp == '2':
    nome_modelo_escolhido,modelo_escolhido = escolhaDeModelo()
    comparacaoEntrePalavras(nome_modelo_escolhido,modelo_escolhido)(nome_modelo_escolhido,modelo_escolhido,palavra_central)
  elif ans_comp == '3':
    escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido)
  elif ans_comp == '4':
    menu()



def escolhaDeModelo():
  output.clear()
  print('\n\tEscolha qual modelo deseja usar:')
  print('\n1 - WOKE Skip-Gram 400D')
  print('2 - WOKE Skip-Gram 700D')
  print('3 - WOKE Skip-Gram 1000D')
  print('4 - WOKE CBOW 400D')
  print('5 - WOKE CBOW 700D')
  print('6 - WOKE CBOW 1000D')
  print('7 - N2V WOKE Skip-Gram 400D')
  print('8 - N2V WOKE CBOW 400D')

  ans = input('\nDigite o número referente a sua escolha: ')
  while ans not in ['1','2','3','4','5','6','7','8']:
    ans = input('\nDigite o número referente a sua escolha (entre 1 e 6): ')

  if ans == '1':
    nome_modelo_escolhido = 'WOKE HST Skip-Gram 400D'
    modelo_escolhido = word2vec_woke_hst_sg_400
  elif ans == '2':
    nome_modelo_escolhido = 'WOKE HST Skip-Gram 700D'
    modelo_escolhido = word2vec_woke_hst_sg_700
  elif ans == '3':
    nome_modelo_escolhido = 'WOKE HST Skip-Gram 1000D'
    modelo_escolhido = word2vec_woke_hst_sg_1000
  elif ans == '4':
    nome_modelo_escolhido = 'WOKE HST CBOW 400D'
    modelo_escolhido = word2vec_woke_hst_cbow_400
  elif ans == '5':
    nome_modelo_escolhido = 'WOKE HST CBOW 700D'
    modelo_escolhido = word2vec_woke_hst_cbow_700
  elif ans == '6':
    nome_modelo_escolhido = 'WOKE HST CBOW 1000D'
    modelo_escolhido = word2vec_woke_hst_cbow_1000
  elif ans == '7':
    nome_modelo_escolhido = 'N2V WOKE HST Skip-Gram 400D'
    modelo_escolhido = nonce2vec_woke_hst_sg_400
  elif ans == '8':
    nome_modelo_escolhido = 'N2V WOKE HST CBOW 400D'
    modelo_escolhido = nonce2vec_woke_hst_cbow_400


  return nome_modelo_escolhido,modelo_escolhido

def escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido):
  output.clear()
  print(f'\n\tEscolha o que deseja fazer usando {nome_modelo_escolhido}:\n')
  print('1 - Campo semântico de uma palavra')
  print('2 - Visualização de vetores de palavras no espaço vetorial')
  print('3 - Comparação entre palavras')
  print('4 - Distância entre palavras')
  print('5 - Mostrar informações do modelo')


  ans2 = input('\nDigite o número referente a sua escolha: ')
  while ans2 not in ['1','2','3','4','5']:
    ans2 = input('\nDigite o número referente a sua escolha entre (1 e 4): ')

  if ans2 == '1':
    campoSemantico(nome_modelo_escolhido,modelo_escolhido,'')
  elif ans2 == '2':
    vetoresDePalavras(nome_modelo_escolhido,modelo_escolhido)
  elif ans2 == '3':
    comparacaoEntrePalavras(nome_modelo_escolhido,modelo_escolhido)
  elif ans2 == '4':
    distanciaEntrePalavras(nome_modelo_escolhido,modelo_escolhido)
  elif ans2 == '5':
    mostraInformacaoDoModelo(nome_modelo_escolhido,modelo_escolhido)

def menu():
  nome_modelo_escolhido,modelo_escolhido = escolhaDeModelo()
  output.clear()
  escolhaDeAcoes(nome_modelo_escolhido,modelo_escolhido)