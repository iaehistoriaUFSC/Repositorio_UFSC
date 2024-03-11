import time
import os
import joblib
import re
from unidecode import unidecode
from urllib import request
try:
  from variaveis_utilizadas import string_dos_caracteres_especiais
except ImportError as e:
  from .variaveis_utilizadas import string_dos_caracteres_especiais


def criarDiretorio(caminho : str):
  try:
    os.makedirs(caminho, exist_ok=True)
    time.sleep(1)
    if os.path.isdir(caminho):
      # print(f'Pasta {caminho} criada com sucesso.')
      return True
    else:
      print(f'Tentando criar pasta {caminho} novamente.')
      time.sleep(3)
      if os.path.isdir(caminho):
        # print(f'Pasta {caminho} criada com sucesso.')
        return True, ''
      else:
        # print(f'Pasta {caminho} não foi carregada corretamente.')
        return False, f'Pasta {caminho} não foi carregada corretamente.'
  except Exception as e:
    erro = f'Erro "{e.__class__.__name__}": {str(e)}'
    return False, erro

def criarGeradorDicts(lista_de_caminhos_dicionarios : list):
  for arquivo_dic in lista_de_caminhos_dicionarios:
    nome_arquivo = os.path.basename(arquivo_dic)
    yield (nome_arquivo.replace('.joblib',''),joblib.load(arquivo_dic))


def baixarPDF(link_pdf : str,caminho_do_pdf : str):
  try:
    request.urlretrieve(url=link_pdf,filename=caminho_do_pdf)
    return True, ''
  except Exception as e:
    erro = f'Erro "{e.__class__.__name__}": {str(e)}'
    return False, erro

def excluirPDF(caminho_do_pdf : str):
  try:
    os.remove(caminho_do_pdf)
    time.sleep(1)
    if os.path.exists(caminho_do_pdf):
      os.remove(caminho_do_pdf)
      time.sleep(3)
      if os.path.exists(caminho_do_pdf):
        return False, f'Problema ao excluir "{caminho_do_pdf}" na segunda tentativa.'
      else:
        return True, ''
    else:
      return True, ''
  except Exception as e:
    erro = f'Erro "{e.__class__.__name__}": {str(e)}'
    return False, erro


def formatarNomeArquivoColecao(nome_colecao : str):
    nome_colecao_formatado = re.sub(r'[^\w]', '_', unidecode(nome_colecao))
    nome_colecao_formatado = nome_colecao_formatado.replace('__','_')
    if nome_colecao_formatado.endswith('_'):
        nome_colecao_formatado = nome_colecao_formatado[:len(nome_colecao_formatado)-1]
    nome_colecao_formatado = nome_colecao_formatado.replace('Programa_de_Pos_Graduacao_em_','')
    return nome_colecao_formatado

def removerCaracteresEspeciais(texto : str,
                               string_dos_caracteres_especiais: str = '''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~''') -> str:
  texto_sem_caracteres_especiais = texto.translate(str.maketrans('','',string_dos_caracteres_especiais))
  return texto_sem_caracteres_especiais

def removerNumeros(texto : str,
                    lista_de_numeros_especificos : list = ['1','2','3','4','5','6','7','8','9','0']) -> str:
    # return re.sub(r'\d+', '', texto)
    padrao = '|'.join(map(re.escape, map(str, lista_de_numeros_especificos)))
    texto_substituido = re.sub(padrao, '', texto)
    return texto_substituido

def padronizarTextoDoBloco(texto_bloco : str,
                           string_dos_caracteres_especiais : str = string_dos_caracteres_especiais) -> str:
    texto_bloco_analisado = texto_bloco.lower()
    # texto_bloco_analisado = texto_bloco_analisado[:3].replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('0','').replace('.','')+texto_bloco_analisado[3:]
    # texto_bloco_analisado = texto_bloco_analisado.strip()
    texto_bloco_analisado = removerNumeros(texto=texto_bloco_analisado)
    texto_bloco_analisado = removerCaracteresEspeciais(texto=texto_bloco_analisado,string_dos_caracteres_especiais=string_dos_caracteres_especiais)
    return texto_bloco_analisado.strip()



def validarDicTextoExtraido(dic_texto_extraido : dict):
    if 'blocks' in dic_texto_extraido.keys():
        if isinstance(dic_texto_extraido['blocks'],list):
            for block in dic_texto_extraido['blocks']:
                if isinstance(block,dict):
                    if 'lines' in block.keys():
                        if isinstance(block['lines'],list):
                            for item_linha in block['lines']:
                                if isinstance(item_linha,dict):
                                    if 'spans' in item_linha.keys():
                                        return True
    return False

def encontrarAnoTrabalhoNosMetadados(ano_repositorio : str,
                                     lingua : str,
                                     ano_capa : str = '') -> str:
    if lingua.lower().strip() in ['por','pt','pt_br','br','por_br','português','portugues']:
      if ano_capa != '':
        if ano_capa != 'N.I.' and ano_capa.isdigit():
          if int(ano_capa) > 2002:
            return 'Possivelmente dentro do recorte'
          else:
            return 'Fora do recorte'

      if ano_repositorio != 'N.I.' and ano_repositorio.isdigit():
        if int(ano_repositorio) > 2002:
          return 'Possivelmente dentro do recorte'
        else:
          return 'Fora do recorte'
      else:
        return 'Fora do recorte'
    else:
      return 'Fora do recorte'


def limparLixeira(drive_service) -> str:
    try:
        drive_service.files().emptyTrash().execute()
        return '\n\t!!!!!!! Lixeira esvaziada com sucesso!'
    except Exception as e:
        if drive_service != None:
            descricao_erro = f"{e.__class__}: {e.args}"
            with open('Problemas exclusão lixeira.txt') as f:
                f.write(descricao_erro+'\n\n'+'-'*100)
                f.close()
            return descricao_erro
        else: # Exec fora do Google Colab
            pass

def printarAdicionandoProblemaNumTxt(string_problema : str,
                                     n_programa : int,
                                     caminho_pasta_execs_etapa_2 : str = r'') -> None:
    """
    Imprime na tela a mensagem de problema encontrada durante a execução e a adiciona num arquivo
    de texto referente aos problemas encontrados na etapa 1.
    :param string_problema: String da descrição do problema encontrado durante a execução de algum
    processo ao decorrer da execução.
    :param n_programa: Número do programa que está executando este código.
    :param caminho_pasta_execs_etapa_2: String do caminho referente a pasta da etapa 2 no Google Drive, aonde o
    arquivo de texto dos avisos deve ser salvo.
    :return: None, não há retornos nessa função.
    """
    with open(os.path.join(caminho_pasta_execs_etapa_2,f'Avisos programa {n_programa}.txt'),'a',encoding='utf-8') as f:
        f.write(string_problema+'\n\n'+('*'*100))
        f.close()
    print(string_problema)
