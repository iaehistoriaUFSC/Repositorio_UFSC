import os
import re
import joblib
from unidecode import unidecode
from .funcoes_relatorio_pdf import dic_erros_amostrados, caminho_pasta_dicts_falhas

def criarDiretorio(caminho : str) -> None:
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        return caminho
    else:
        return caminho
    
def obterDiretorioAtual() -> str:
    """
    Essa função retornará o diretório atual da pasta de trabalho que está executando o 
    script.

    Retorno:
    -------
    - :return: String contendo o caminho total até a pasta de trabalho que está executando 
    este script.
    """
    return os.getcwd()

diretorio_atual = obterDiretorioAtual()

if 'Etapa_3' not in diretorio_atual:
    diretorio_atual = criarDiretorio(os.path.join(diretorio_atual,'Etapa_3'))


caminho_pasta_planilhas = os.path.join(os.path.dirname(diretorio_atual),'Resultados','Planilhas de metadados')
caminho_pasta_dicts = os.path.join(os.path.dirname(diretorio_atual),'Etapa 2','Dicts atualizados')
caminho_pasta_dicts_falhas = os.path.join(os.path.dirname(diretorio_atual),'Etapa 2','Dicionário de Falhas')
caminho_pasta_arquivos_geracao_relatorio_pdf = os.path.join(diretorio_atual,'Arquivos para geração do PDF')
caminho_pasta_relatorio_pdf = os.path.join(os.path.dirname(diretorio_atual),'Resultados','Relatórios')

caminho_lista_colecoes_site = os.path.join(os.path.dirname(diretorio_atual),'Etapa_1','Lista_de_colecoes','lista_de_colecoes.joblib')

style_css_src = os.path.join(caminho_pasta_arquivos_geracao_relatorio_pdf,'style.css')
imagem_src = os.path.join(caminho_pasta_arquivos_geracao_relatorio_pdf,'logo_grupo_de_estudos_sem_fundo.png')
caminho_arquivo_relatorio_pdf = os.path.join(caminho_pasta_relatorio_pdf,'Relatório - Extração de Dados WOKE_teste.pdf')
caminho_arquivo_html = os.path.join(caminho_pasta_arquivos_geracao_relatorio_pdf,'HTML_relatorio_teste.html')

caminho_para_salvar = os.path.join(diretorio_atual,'Avisos detalhados por coleção')

def formatarNomeArquivoColecao(nome_colecao : str):
    nome_colecao_formatado = re.sub(r'[^\w]', '_', unidecode(nome_colecao))
    nome_colecao_formatado = nome_colecao_formatado.replace('__','_')
    if nome_colecao_formatado.endswith('_'):
        nome_colecao_formatado = nome_colecao_formatado[:len(nome_colecao_formatado)-1]
    nome_colecao_formatado = nome_colecao_formatado.replace('Programa_de_Pos_Graduacao_em_','')
    return nome_colecao_formatado

def gerarDicionarioDeFalhas() -> dict:
    """
    Organiza todos os dicionários de falhas gerados pelos diferentes programas,
    nos diferentes dias em um só dicionário de falhas contendo todas as
    informações.

    Parâmetros:
    -----------
    - param caminho_pasta_dicts_falhas: String referente ao caminho até a pasta
    onde está armazenados os arquivos de dicionários de falhas das execuções
    dos programas.
    
    Retornos:
    ---------
    - return: Dicionário de falhas com todas as coleções e suas respectivas
    informações agrupadas.
    """
    lista_dics_falhas = [os.path.join(caminho_pasta_dicts_falhas,arquivo_dic_falhas) for arquivo_dic_falhas in os.listdir(caminho_pasta_dicts_falhas) if arquivo_dic_falhas.endswith('.joblib')]
    dic_falhas = {'Coleções':{}}
    for arquivo_dic_falhas in lista_dics_falhas:
        try:
          dic_falhas_atual = joblib.load(arquivo_dic_falhas)
          for colecao in dic_falhas_atual['Coleções'].keys():
              if colecao not in dic_falhas['Coleções'].keys():
                  dic_falhas['Coleções'][colecao] = dic_falhas_atual['Coleções'][colecao]
        except Exception as e:
          erro = f'{e.__class__.__name__}: {str(e)}'
          print(f'Problema ao carregar dic de falhas "{os.path.basename(arquivo_dic_falhas)}"\n-->{erro}\n')
    return dic_falhas

def exibirErrosAmostrados(erro : str) -> str:
    """
    Exibe os erros identificados no decorrer das etapas do programa de extração
    de uma forma mais compreensível, para ser melhor entendido por pessoas que
    lerão o relatório e não terão conhecimento sobre os nomes de erros
    provenientes da área de programação.
    Observação: utiliza um dicionário com chave (nome mais amigável para o erro)
    e valor (lista de erros identificados referentes aquela descrição mais
    amigável) para adaptar o nome dos erros no relatório.

    :param erro: String do erro a ser "tratado".
    :return: String do erro de uma forma mais amigável, caso este esteja na
    listagem de erros identificados a serem transformados.
    """
    erro_amostrado = erro

    for chave in dic_erros_amostrados:
      for erro_identificado in dic_erros_amostrados[chave]:
          if erro_identificado in erro:
              return chave

    return erro_amostrado

def gerarTxtAvisosDetalhadosCadaColecao() -> None:
    """
    Gerar arquivos de textos, para cada coleção presente no dicionário de falhas,
    mostrando com mais detalhes e especificamente os erros que ocorreram durante
    as execuções da extração para aquela determinada coleção e os trabalhos que
    obtiveram o erro em questão.

    :param caminho_dic_falhas: String referente ao caminho para a pasta que
    armazena os dicionários de falhas referentes as execuções dos programas e
    seus dias (usada para criação do dicionário de falhas completo).
    :param caminho_para_salvar: String referente ao caminho para a pasta que
    armazenará o arquivo de texto gerado por esta função.
    :return: None, não há retornos nessa função.
    """
    print('\nIniciando detalhamento dos avisos das coleções em txts...\n\n')
    dic_falhas = gerarDicionarioDeFalhas()

    for colecao in list(dic_falhas['Coleções'].keys()):
        print('Coleção:',colecao)
        if len(dic_falhas['Coleções'][colecao]['Avisos']['Possivelmente dentro do recorte']['Erro']) > 0 or len(dic_falhas['Coleções'][colecao]['Avisos']['Fora do recorte']['Erro']) > 0:
            txt = '*'*100 + '\n\n' + f'Coleção: {colecao}' + '\n\n' + '*'*100+'\n\n'
            if len(dic_falhas['Coleções'][colecao]['Avisos']['Possivelmente dentro do recorte']['Erro']) > 0:

              dic_colecao_dentro_recorte = dic_falhas["Coleções"][colecao]['Avisos']['Possivelmente dentro do recorte']

              lista_de_erros = sorted(list(set(dic_colecao_dentro_recorte["Erro"])))

              dic_erros_amostrados_contagem = {}

              txt += ('='*100)+'\n\n'+'Aviso(s) encontrado(s) dentro do recorte:\n\n'
              txt += ('='*100)+'\n\n'

              for erro in lista_de_erros:
                  txt += '- ' + erro + '\n'
                  contagem_erro = dic_colecao_dentro_recorte["Erro"].count(erro)
                  if erro not in dic_erros_amostrados_contagem.keys():
                      dic_erros_amostrados_contagem[erro] = contagem_erro

              for erro_amostrado in list(dic_erros_amostrados_contagem.keys()):
                  erro_visivel = erro_amostrado
                  for chave in list(dic_erros_amostrados.keys()):
                      for erro_identificado in dic_erros_amostrados[chave]:
                          if erro_identificado in erro_amostrado:
                              erro_visivel += ' ' + chave[chave.find('('):]
                  txt += '\n\n' + f'--> {erro_visivel}: {dic_erros_amostrados_contagem[erro_amostrado]}'
                  txt += '\n\nLink(s) do(s) trabalho(s) com este aviso:\n'

                  if erro_amostrado in dic_erros_amostrados.keys():
                      erros_referentes_ao_erro_amostrado = dic_erros_amostrados[erro_amostrado]
                  else:
                      erros_referentes_ao_erro_amostrado = [erro_amostrado]

                  for i in range(len(dic_colecao_dentro_recorte['Link para o trabalho'])):
                      if dic_colecao_dentro_recorte["Erro"][i] == erro_amostrado:
                          if dic_colecao_dentro_recorte['Link para o trabalho'][i] != 'N.I.':
                              txt += f'''Trabalho {dic_colecao_dentro_recorte["Trabalho"][i]}: {dic_colecao_dentro_recorte['Link para o trabalho'][i]}\n'''
                          else:
                              txt += f'''Trabalho {dic_colecao_dentro_recorte["Trabalho"][i]}: {dic_colecao_dentro_recorte['Link para o trabalho'][i]} (verificá-lo na Planilha de Metadados).\n'''

            if len(dic_falhas['Coleções'][colecao]['Avisos']['Fora do recorte']['Erro']) > 0:
              dic_colecao_fora_recorte = dic_falhas["Coleções"][colecao]['Avisos']['Fora do recorte']

              lista_de_erros = sorted(list(set(dic_colecao_fora_recorte["Erro"])))

              dic_erros_amostrados_contagem = {}

              txt += '\n'+('='*100)+'\n\n'+'Aviso(s) encontrado(s) fora do recorte:\n\n'
              txt += ('='*100)+'\n\n'

              for erro in lista_de_erros:
                  txt += '- ' + erro + '\n'
                  contagem_erro = dic_colecao_fora_recorte["Erro"].count(erro)
                  if erro not in dic_erros_amostrados_contagem.keys():
                      dic_erros_amostrados_contagem[erro] = contagem_erro

              for erro_amostrado in list(dic_erros_amostrados_contagem.keys()):
                  erro_visivel = erro_amostrado
                  for chave in list(dic_erros_amostrados.keys()):
                      for erro_identificado in dic_erros_amostrados[chave]:
                          if erro_identificado in erro_amostrado:
                              erro_visivel += ' ' + chave[chave.find('('):]
                  txt += '\n\n' + f'--> {erro_visivel}: {dic_erros_amostrados_contagem[erro_amostrado]}'
                  txt += '\n\nLink(s) do(s) trabalho(s) com este aviso:\n'

                  if erro_amostrado in dic_erros_amostrados.keys():
                      erros_referentes_ao_erro_amostrado = dic_erros_amostrados[erro_amostrado]
                  else:
                      erros_referentes_ao_erro_amostrado = [erro_amostrado]

                  for i in range(len(dic_colecao_fora_recorte['Link para o trabalho'])):
                      if dic_colecao_fora_recorte["Erro"][i] == erro_amostrado:
                          if dic_colecao_fora_recorte['Link para o trabalho'][i] != 'N.I.':
                              txt += f'''Trabalho {dic_colecao_fora_recorte["Trabalho"][i]}: {dic_colecao_fora_recorte['Link para o trabalho'][i]}\n'''
                          else:
                              txt += f'''Trabalho {dic_colecao_fora_recorte["Trabalho"][i]}: {dic_colecao_fora_recorte['Link para o trabalho'][i]} (verificá-lo na Planilha de Metadados).\n'''


            nome_arquivo_colecao = formatarNomeArquivoColecao(nome_colecao = colecao)
            caminho_completo_arquivo_txt = os.path.join(caminho_para_salvar,f'{nome_arquivo_colecao}.txt')

            with open(caminho_completo_arquivo_txt,'w',encoding='utf-8') as f:
                f.write(txt)
                f.close()
            print('Arquivo txt criado com sucesso!\n')
        else:
            print('Não foram encontrados erros no processo de extração de texto.\n')
