try:
    from google.colab import output
    # from google.colab import drive
    # drive.mount('/content/drive')
except Exception:
    GOOGLE_COLAB = False
else:
    GOOGLE_COLAB = True
finally:
    import gdown
    import platform
    import zipfile
    import shutil
    from weasyprint import HTML
    import os
    import msgpack
    import re
    import gc

OS_ATUAL = platform.system()
CAMINHO_EXEC_ATUAL = os.getcwd()
if GOOGLE_COLAB:
  CAMINHO_SKINNER = r'/content/SKINNER_files'
else:
  CAMINHO_SKINNER = os.path.join(CAMINHO_EXEC_ATUAL,'SKINNER_files')
CAMINHO_PLANILHA_METADADOS = os.path.join(CAMINHO_SKINNER,'planilha_metadados_woke.xlsx')

def organizarAmbienteExecucao():
  """
  Função responsável por realizar a criação da pasta central do SKINNER.
  Tal pasta será utilizada para armazenar os arquivos baixados para 
  um determinado modelo, bem como para armazenar os resultados da 
  busca dos tokens que deseja-se analisar.
  """
  global CAMINHO_SKINNER
  try:
    os.makedirs(CAMINHO_SKINNER,exist_ok=True)
  except Exception:
    return False
  else:
    return True

def coletar_ID_link_Dive(link_drive : str) -> str|None:
  """
  Função responsável por coletar o ID de um arquivo ou pasta do Drive
  com base no seu link de compartilhamento.

  ### Parâmetros:
  - link_drive: String contendo o link de compartilhamento do arquivo.
  
  ### Retornos:
  - String contendo o ID do arquivo ou None, caso a captura não seja
  bem sucedida.
  """
  padrao_regex = r'\/d\/(.+)/'
  busca = re.search(padrao_regex,link_drive)
  if busca:
    return busca.group(1)
  else:
    return None

def baixarArquivoDrive(link_drive : str,
                       caminho_destino : str,
                       silencio : bool = False) -> bool:
  """
  Função responsável por baixar um arquivo presente no ambiente
  do Google Drive (com acesso liberado) e trazê-lo para o ambiente
  de execução do programa.

  ### Parâmetros:
  - link_drive: String contendo o link de compartilhamento do arquivo.
  - caminho_destino: String contendo o caminho completo (incluindo nome
  e extensão do arquivo) no ambiente de execução onde deseja armazenar.
  - silencio: Bool para printar (True) ou não (False) informações sobre 
  este processo.

  ### Retornos:
  - Bool para validar o êxito (True) ou não (False) da execução deste
  processo.
  """
  try:
    ID_arquivo = coletar_ID_link_Dive(link_drive)
    if ID_arquivo:
      # URL no formato que o gdown utiliza para baixar arquivos do Google Drive por meio do ID
      url = f'https://drive.google.com/uc?export=download&id={ID_arquivo}'
      os.makedirs(os.path.dirname(caminho_destino),exist_ok=True)
      # Execução do processo de baixar o arquivo do Drive e trazê-lo para este ambiente de execução
      gdown.download(url, caminho_destino, quiet=silencio)
    else:
      print('Erro ao identificar ID do arquivo pelo link.')
      return False
  except Exception as e:
    if not silencio:
      print(f'Erro na hora de baixar arquivo do Drive: {e.__class__.__name__}: {str(e)}')
    return False
  else:
    return True

def descompactarPasta(caminho_pasta : str, excluir_zip : bool = True, silencio : bool = True):
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
            if not silencio:
                print(f'Descompactando {i+1} de {qtd_zips}')
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(caminho_pasta)
            if excluir_zip:
                if not silencio:
                    print('Tentando remover',arquivo)
                os.remove(arquivo)

def limparConsole():
    """
    Função responsável por limpar a tela de output/console.
    """
    global GOOGLE_COLAB
    global OS_ATUAL
    if GOOGLE_COLAB: # Se estivermos executando no Colab, melhor utilizar a função própria para limpar o output neste ambiente
        output.clear()
    elif OS_ATUAL.lower() == 'windows': # Se for Windows
        os.system('cls')
    else:   # Se for MAC/Linux
        os.system('clear')

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

def ConstrucaoContexto(nome_modelo : str,tokens : list[str], pasta_modelos : str) -> dict:
  tokens = [token.lower().strip() for token in tokens]

  caminho_arquivos = os.path.join(pasta_modelos,nome_modelo)
  if os.path.exists(caminho_arquivos):
    dic_analise_completa = {token : {'Geral':{'Ocorrencias_totais':0,'Tokens':{}}} for token in tokens}

    caminhos_dicionarios = [os.path.join(caminho_arquivos,nome_dic_colecao) for nome_dic_colecao in os.listdir(caminho_arquivos) if nome_dic_colecao.startswith('dic') and nome_dic_colecao.endswith('.msgpack')]
    for caminho_dic in caminhos_dicionarios:
      nome_colecao = os.path.basename(caminho_dic).replace('dic_','').replace('.msgpack','')
      dic_colecao = abrirArquivoMsgPack(caminho_dic)
      dic_analise_colecao = {token : {'Total_ocorrencias_colecao':0,'Geral_colecao':{},'Trabalhos':[],'Contexto':[],'Total_ocorrencias_Trabalho':[]} for token in tokens}
      for token in tokens:
        for trabalho in dic_colecao.keys():
          if token in dic_colecao[trabalho]['tokens_centrais'].keys():
            dic_analise_colecao[token]['Trabalhos'].append((trabalho,dic_colecao[trabalho]['metadados']))
            dic_analise_colecao[token]['Contexto'].append(dic_colecao[trabalho]['tokens_centrais'][token])
            dic_analise_colecao[token]['Total_ocorrencias_Trabalho'].append([0])
            for token_contexto in dic_colecao[trabalho]['tokens_centrais'][token].keys():
              if token_contexto in dic_analise_colecao[token]['Geral_colecao'].keys():
                dic_analise_colecao[token]['Geral_colecao'][token_contexto] += dic_colecao[trabalho]['tokens_centrais'][token][token_contexto]
              else:
                dic_analise_colecao[token]['Geral_colecao'][token_contexto] = dic_colecao[trabalho]['tokens_centrais'][token][token_contexto]
              dic_analise_colecao[token]['Total_ocorrencias_Trabalho'][-1][-1] += dic_colecao[trabalho]['tokens_centrais'][token][token_contexto]
              dic_analise_colecao[token]['Total_ocorrencias_colecao'] += dic_colecao[trabalho]['tokens_centrais'][token][token_contexto]

        dic_analise_colecao[token]['Geral_colecao'] = dict(sorted(dic_analise_colecao[token]['Geral_colecao'].items(), key=lambda item: item[1], reverse=True))
        dic_analise_completa[token][nome_colecao] = dic_analise_colecao[token]

        for token_contexto in dic_analise_colecao[token]['Geral_colecao'].keys():
          if token_contexto in dic_analise_completa[token]['Geral']['Tokens'].keys():
            dic_analise_completa[token]['Geral']['Tokens'][token_contexto] += dic_analise_colecao[token]['Geral_colecao'][token_contexto]
          else:
            dic_analise_completa[token]['Geral']['Tokens'][token_contexto] = dic_analise_colecao[token]['Geral_colecao'][token_contexto]
          dic_analise_completa[token]['Geral']['Ocorrencias_totais'] += dic_analise_colecao[token]['Geral_colecao'][token_contexto]


    for token in dic_analise_completa.keys():
      dic_analise_completa[token]['Geral']['Tokens'] = dict(sorted(dic_analise_completa[token]['Geral']['Tokens'].items(), key=lambda item: item[1], reverse=True))

    return dic_analise_completa
  else:
    return None

def gerarHTML(titulo : str,
              quebra_de_linha_tamanho_da_imagem : str,
              capa : str,
              conteudo_depois_da_capa : str,
              conteudo_tokens : str,
              conteudo_tokens_aprofundado: str,
              style_css_src : str,
              imagem_src : str) -> str:

    template_html = f'''
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        <link rel="stylesheet" href="{style_css_src}">
    </head>
    <body>

        <img src="{imagem_src}" alt="Imagem de exemplo" style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 100%; height: auto;">
        {quebra_de_linha_tamanho_da_imagem}
        {capa}
        {conteudo_depois_da_capa}
        {conteudo_tokens}
        {conteudo_tokens_aprofundado}
    </body>
    </html>
    '''
    return template_html

def escreverDocHTML(caminho_arquivo_html : str,
                    template_html : str):
    """
    Geração do documento HTML que será usado como template para geração do
    relatório em PDF.

    :param caminho_arquivo_html: String referente ao caminho para salvar a string
    do template do conteúdo HTML completo.
    :param template_html: String contendo o HTML completo para geração do
    relatório em PDF.
    :return: None, não há retornos nessa função.
    """
    try:
        if not caminho_arquivo_html.endswith('.html'):
          caminho_arquivo_html += '.html'
        with open(caminho_arquivo_html, 'w') as f:
            f.write(template_html)
            f.close()
    except Exception as e:
        erro = f'{e.__class__.__name__}: {str(e)}'
        return False, erro
    else:
        return True, ''

def gerarQuebraDeLinhasDoTamanhoDaImagem() -> str:
    """
    Gera uma string, para compor a string geral do HTML, que faz a quebra de
    linhas até que o texto que irá ser escrito posteriormente não fique embaixo
    da imagem presente na capa.

    :param None: Não há parametros para esta função.
    :return: String HTML com as devidas quebras de linhas.
    """
    string_html = '<br>'*35
    return string_html

def gerarTextoCapa() -> str:
  string_html = '''<br><h1>Semantic Knowledge and Interpretation Navigator for Nurturing Exact References<br>WOKE - UFSC</h1>
        <br><br><br><br>
        <p style="text-align: center;">Desenvolvido por: Igor Caetano de Souza
        <br>Grupo de Estudos e Pesquisa em IA e História - UFSC</p>
        '''
  return string_html

def gerarConteudoDepoisDaCapa(nome_modelo : str,tokens_pesquisados : list[str]) -> str:

  string_html = f'''<div class="quebra-de-pagina"><hr class="linha-vermelha"><h2>Resumo da pesquisa</h2><hr class="linha-vermelha"><br><h3>Modelo analisado:<hr class="linha-cinza"><br></h3><p>{nome_modelo}</p>
  <br></hr><br>
  </div>'''
  return string_html

def gerarConteudoTokensInicial(tokens : list[str]) -> str:
  listagem_tokens = ''
  for i,token in enumerate(tokens):
    listagem_tokens += f'<li><a href="#token{i}">{token}</a></li>'
  string_html = f'''
  <h3>Tokens pesquisados</h3><hr class="linha-cinza">
          <ul>
              {listagem_tokens}
          </ul>
  '''
  return string_html

def obterPorcentagemContribuicao(total : int, contribuicao : int):
  if total != 0:
    return str(round(((contribuicao*100)/total),2))+'%'
  else:
    return 0

def gerarConteudoTop20TokensContexto(total_de_ocorrencias_contexto_token : int,tokens_totais_de_contexto : dict) -> str:
  string_html = '<h3>TOP 20 TOKENS DE CONTEXTO QUE MAIS CONTRIBUIRAM PARA FORMAÇÃO DO VETOR:</h3><br><p>'

  for token_contexto in list(tokens_totais_de_contexto.keys())[:20]:
    string_html += f'{token_contexto}: {obterPorcentagemContribuicao(total=total_de_ocorrencias_contexto_token,contribuicao=tokens_totais_de_contexto[token_contexto])}<br>'
  string_html += f'<br>20 de um total de {len(tokens_totais_de_contexto.keys())}</p>'

  return string_html

def gerarContribuicaoColecoes(total_de_ocorrencias_contexto_token,token : str, n_token : int, dic_analise_token : dict) -> str:
  string_html = f'<div><h3>Coleções e suas respectivas porcentagens de contribuição na construção de contexto para "{token}"</h3>'

  string_html += '<ul>'
  for c,colecao in enumerate([col for col in dic_analise_token.keys() if col != 'Geral']):
    string_html += f'<li><a href="#token{n_token}colecao{c}">{colecao}: {obterPorcentagemContribuicao(total=total_de_ocorrencias_contexto_token,contribuicao=dic_analise_token[colecao]["Total_ocorrencias_colecao"])}</a></li>'
  string_html += '</ul></div></div>'

  return string_html

def gerarContribuicaoTrabalhos(token : str,
                               n_token : int,
                               dic_analise_token : dict) -> str:
  string_html = ''
  for n_colecao,colecao in enumerate([col for col in dic_analise_token.keys() if col != 'Geral']):
    string_html += f'<div class="quebra-de-pagina"><hr class="linha-cinza"><h3 id="token{str(n_token)}colecao{str(n_colecao)}">{token} - {colecao}</h3><hr class="linha-cinza">'
    # string_html += f'<div class="quebra-de-pagina">Trabalhos e suas respectivas porcentagens de contribuição para coleção "{colecao}"'

    string_html += f'Trabalhos e suas respectivas porcentagens de contribuição para coleção "{colecao}"<ul>'
    for n_trab,dados in enumerate(zip(dic_analise_token[colecao]['Trabalhos'],dic_analise_token[colecao]['Contexto'],dic_analise_token[colecao]['Total_ocorrencias_Trabalho'])):
      nome_trabalho,dic_metadados_trabalho = dados[0]
      dic_tokens_contexto_trabalho = dados[1]
      total_ocorrencias_trabalho = dados[2][0]
    # for n_trab,(nome_trabalho,dic_metadados_trabalho),dic_tokens_contexto_trabalho,total_ocorrencias_trabalho in enumerate(zip(dic_analise_token[colecao]['Trabalhos'],dic_analise_token[colecao]['Contexto'],dic_analise_token[colecao]['Total_ocorrencias_Trabalho'])):
      assuntos = dic_metadados_trabalho['assuntos']
      string_html += f'<li><a href="#token{str(n_token)}colecao{str(n_colecao)}trabalho{str(n_trab)}">{nome_trabalho}: {obterPorcentagemContribuicao(total=dic_analise_token[colecao]["Total_ocorrencias_colecao"],contribuicao=total_ocorrencias_trabalho)}</a><br>Assuntos: {assuntos}</li><br>'
    string_html += '</ul></div>'

    for n_trab,dados in enumerate(zip(dic_analise_token[colecao]['Trabalhos'],dic_analise_token[colecao]['Contexto'],dic_analise_token[colecao]['Total_ocorrencias_Trabalho'])):
      nome_trabalho,dic_metadados_trabalho = dados[0]
      dic_tokens_contexto_trabalho = dados[1]
      total_ocorrencias_trabalho = dados[2][0]
      link_pagina = dic_metadados_trabalho['link_pagina']
      link_pdf = dic_metadados_trabalho['link_pdf']
      assuntos = dic_metadados_trabalho['assuntos']
      string_html += f'<h4 id="token{str(n_token)}colecao{str(n_colecao)}trabalho{str(n_trab)}">{nome_trabalho} / <a href="{link_pagina}" target="_blank">Link para página no RI</a> / <a href="{link_pdf}" target="_blank">Link para o PDF</a></h4>'
      string_html += '<h7>Tokens de contexto e suas ocorrências:<br>'
      for token_contexto,ocorrencia in dic_tokens_contexto_trabalho.items():
        string_html += f'{token_contexto}: {ocorrencia}<br>'
      string_html += '</h7>'
  return string_html

def gerarConteudoTokensAprofundado(dic_analise : dict, tokens : list[str]) -> str:

  string_html = ''
  for i,token in enumerate(tokens):
    string_html += f'''<div><div class="quebra-de-pagina"><hr class="linha-vermelha"><h2 id="token{i}">{token}</h2><hr class="linha-vermelha">

    {gerarConteudoTop20TokensContexto(total_de_ocorrencias_contexto_token=dic_analise[token]['Geral']['Ocorrencias_totais'],
                                      tokens_totais_de_contexto=dic_analise[token]['Geral']['Tokens'])}
    </div>

    {gerarContribuicaoColecoes(total_de_ocorrencias_contexto_token=dic_analise[token]['Geral']['Ocorrencias_totais'],
                               token=token,
                               n_token=i,
                               dic_analise_token=dic_analise[token])}

    {gerarContribuicaoTrabalhos(token=token,n_token=i,dic_analise_token=dic_analise[token])}'''

  return string_html



def obterResultadoSKINNER(tokens_desejados : list[str], nome_modelo_atual : str, pasta_modelos_atual : str) -> bool:


  caminho_arquivo_html=f'/content/SKINNER_files/HTMLs/html_SKINNER_{nome_modelo_atual}_{"_".join(tokens_desejados)}.html'
  caminho_arquivo_relatorio_pdf = f'/content/SKINNER_files/PDFs/PDF_SKINNER_{nome_modelo_atual}_{"_".join(tokens_desejados)}.pdf'

  os.makedirs(os.path.dirname(caminho_arquivo_html),exist_ok=True)
  os.makedirs(os.path.dirname(caminho_arquivo_relatorio_pdf),exist_ok=True)

  img_src = r'/content/Repositorio_UFSC/Word_Embeddings/SKINNER/src/SKINNER.jpg'
  css_src = r'/content/Repositorio_UFSC/Word_Embeddings/SKINNER/src/style_skinner.css'

  dic_analise = ConstrucaoContexto(nome_modelo=nome_modelo_atual,tokens=tokens_desejados,pasta_modelos=pasta_modelos_atual)

  template_html = gerarHTML(titulo='SKINNER - WOKE',
                            quebra_de_linha_tamanho_da_imagem=gerarQuebraDeLinhasDoTamanhoDaImagem(),
                            capa=gerarTextoCapa(),
                            conteudo_depois_da_capa=gerarConteudoDepoisDaCapa(nome_modelo=nome_modelo_atual,tokens_pesquisados=tokens_desejados),
                            conteudo_tokens=gerarConteudoTokensInicial(tokens=tokens_desejados),
                            conteudo_tokens_aprofundado=gerarConteudoTokensAprofundado(dic_analise=dic_analise,tokens=tokens_desejados),
                            style_css_src=css_src,
                            imagem_src=img_src)

  status_geracao_HTML, msg_geracao_HTML = escreverDocHTML(caminho_arquivo_html=caminho_arquivo_html, template_html=template_html)

  if status_geracao_HTML:

      html = HTML(filename=caminho_arquivo_html)
      print("\n\n\tDocumento HTML gerado com sucesso!\n\n\tGerando PDF.\n\t--> Por favor aguarde...")

      pdf = html.write_pdf(caminho_arquivo_relatorio_pdf)
      
      # Tentativa de mitigar o uso de RAM após conclusão do processo
      del html
      del pdf
      gc.collect()

      limparConsole()

      print("\n\n\tRelatório PDF gerado com sucesso!\n\n")
      return True

  else:
    print(f'\n\n\tHTML não conseguiu ser gerado com sucesso...\n\tErro encontrado: {msg_geracao_HTML}\n\n')
    return False

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

DIC_INFO = {'HST-03-10':{'Incremental':{'Modelo 1':{'WOKE_1_HST_2003_2010_w2v_inc':'https://drive.google.com/file/d/1buTOFyyervBYLBjG3wiQb3Qs6I_vauKz/view?usp=drive_link',
                                                    'WOKE_1_HST_2011_2013_w2v_inc':'https://drive.google.com/file/d/1DpaWixw4Lc6K3vV43tvn-8pseHXo1HGQ/view?usp=drive_link',
                                                    'WOKE_1_HST_2014_2016_w2v_inc':'https://drive.google.com/file/d/1JurGTCfCwsZA7EmxDCNMxVpC9n7T2ReU/view?usp=drive_link',
                                                    'WOKE_1_HST_2017_2019_w2v_inc':'https://drive.google.com/file/d/19pahUKlkzdS6zV6e_ftLhJxUmd8QeGSY/view?usp=drive_link',
                                                    'WOKE_1_HST_2020_2024_w2v_inc':'https://drive.google.com/file/d/1PcTpFlmo5BeQRsFZe7LIjNqpeCgcG-qH/view?usp=drive_link'},
                                        'Modelo 2':{'WOKE_2_HST_2003_2010_w2v_inc':'https://drive.google.com/file/d/14Cvf3DO2OvN8Pnmn45tRrJzDK0hVx6pE/view?usp=drive_link',
                                                    'WOKE_2_HST_2011_2013_w2v_inc':'https://drive.google.com/file/d/1ZIzZDjCElCBASZ6NL3fxVeRL6OFe8bU0/view?usp=drive_link',
                                                    'WOKE_2_HST_2014_2016_w2v_inc':'https://drive.google.com/file/d/1rRRHX_L2myu8zU5-VtFsAzuRz_m-qG8L/view?usp=drive_link',
                                                    'WOKE_2_HST_2017_2019_w2v_inc':'https://drive.google.com/file/d/1u7TEyoppHYcW7424M5tGgGgg3riS6rDv/view?usp=drive_link',
                                                    'WOKE_2_HST_2020_2024_w2v_inc':'https://drive.google.com/file/d/12Zmn7b9WZWfgFM1VhbFhItGQksP-32Oh/view?usp=drive_link'},
                                        'Modelo 3':{'WOKE_3_HST_2003_2010_w2v_inc':'https://drive.google.com/file/d/1XPsrUWhptWoR-AIi081lnAWWIxi2I17a/view?usp=drive_link',
                                                    'WOKE_3_HST_2011_2013_w2v_inc':'https://drive.google.com/file/d/17KESdkvs7LLHuNkjUEUGFpzkUIrdowEk/view?usp=drive_link',
                                                    'WOKE_3_HST_2014_2016_w2v_inc':'https://drive.google.com/file/d/1SsrsRMoRMF0bocTN54EWRthoPgmfU9VQ/view?usp=drive_link',
                                                    'WOKE_3_HST_2017_2019_w2v_inc':'https://drive.google.com/file/d/1S-8NOm-zADDCfZ0KlkP06mC7rfM51QJq/view?usp=drive_link',
                                                    'WOKE_3_HST_2020_2024_w2v_inc':'https://drive.google.com/file/d/1ZxCihGqv_lJo4PusbxpAGmUzC1NcCWZW/view?usp=drive_link'},
                                        'Modelo 4':{'WOKE_4_HST_2003_2010_w2v_inc':'https://drive.google.com/file/d/1brVnbnG5pop5ykp51kfG90j9lQAH42W4/view?usp=drive_link',
                                                    'WOKE_4_HST_2011_2013_w2v_inc':'https://drive.google.com/file/d/1FNWc2slsMnBLjaB6crZnHOtIbee5U1p_/view?usp=drive_link',
                                                    'WOKE_4_HST_2014_2016_w2v_inc':'https://drive.google.com/file/d/1HL7kV5zaM-NorMF9-9Pb0RzKrigyRlQy/view?usp=drive_link',
                                                    'WOKE_4_HST_2017_2019_w2v_inc':'https://drive.google.com/file/d/1dskJkxgF2FTHJuR59Zuv3ZsipTzJ9Toh/view?usp=drive_link',
                                                    'WOKE_4_HST_2020_2024_w2v_inc':'https://drive.google.com/file/d/1JIgDrcANXH8cQ-UZ69zrLvZQg9EbJEu3/view?usp=drive_link'}},
                           'Temporal':{'Modelo 1':{'WOKE_1_HST_2003_2010_w2v_tmp':'https://drive.google.com/file/d/1xeAPIw5Ig7STWGa1Mz3H5FQH_bEivc11/view?usp=drive_link',
                                                   'WOKE_1_HST_2003_2013_w2v_tmp':'https://drive.google.com/file/d/1nBRxx2LrP2iQqqNA2WVGJzdzs8_HMNQt/view?usp=drive_link',
                                                   'WOKE_1_HST_2003_2016_w2v_tmp':'https://drive.google.com/file/d/1si7yZXSPMR8MQLUpI-BmAzawrhIrdRo1/view?usp=drive_link',
                                                   'WOKE_1_HST_2003_2019_w2v_tmp':'https://drive.google.com/file/d/1eSZcYUrwLzrtowW8Sh7XOU-2_vzXXZbU/view?usp=drive_link',
                                                   'WOKE_1_HST_2003_2024_w2v_tmp':'https://drive.google.com/file/d/14TCdXvAzvfqGYN5Dd79dcQH4isZqQXA9/view?usp=drive_link'},
                                       'Modelo 2':{'WOKE_2_HST_2003_2010_w2v_tmp':'https://drive.google.com/file/d/18HLJovqZFX5Me7XDRhLucDuH6RAfcN8A/view?usp=drive_link',
                                                   'WOKE_2_HST_2003_2013_w2v_tmp':'https://drive.google.com/file/d/1x_XLe87DhfrVU02i-winZcc1kjehFQ6V/view?usp=drive_link',
                                                   'WOKE_2_HST_2003_2016_w2v_tmp':'https://drive.google.com/file/d/15W4NUd3rpWBApj3MssIDVg2TWMDv05Am/view?usp=drive_link',
                                                   'WOKE_2_HST_2003_2019_w2v_tmp':'https://drive.google.com/file/d/1ZUODZbWJvMfx4A1MeTuariuBOJEAAfYL/view?usp=drive_link',
                                                   'WOKE_2_HST_2003_2024_w2v_tmp':'https://drive.google.com/file/d/1N5DhoTNHQPjhQ--SyN_lfERLgqjNuuWs/view?usp=drive_link'},
                                       'Modelo 3':{'WOKE_3_HST_2003_2010_w2v_tmp':'https://drive.google.com/file/d/138B74s4_ynjsW1sUEAuXF8aB-tfusohE/view?usp=drive_link',
                                                   'WOKE_3_HST_2003_2013_w2v_tmp':'https://drive.google.com/file/d/1oSNi9irYTxUXirXis1k7k52oKsCbGaR5/view?usp=drive_link',
                                                   'WOKE_3_HST_2003_2016_w2v_tmp':'https://drive.google.com/file/d/1QUFP2I_ZSdH7kVpnxsXO4SFmjvWLrbIq/view?usp=drive_link',
                                                   'WOKE_3_HST_2003_2019_w2v_tmp':'https://drive.google.com/file/d/1lcI99eB2m-EVVwJ1DWeRYhzf6xEKGFW9/view?usp=drive_link',
                                                   'WOKE_3_HST_2003_2024_w2v_tmp':'https://drive.google.com/file/d/1Liy-UONaIXx993ustruGZUDxRRBg3P2L/view?usp=drive_link'},
                                       'Modelo 4':{'WOKE_4_HST_2003_2010_w2v_tmp':'https://drive.google.com/file/d/1y_kRWkXRxxnQaTpXHz92V0g7GXeWIqCG/view?usp=drive_link',
                                                   'WOKE_4_HST_2003_2013_w2v_tmp':'https://drive.google.com/file/d/14R_6zS4FVu58IygURAnvCMuhFRyuQnLc/view?usp=drive_link',
                                                   'WOKE_4_HST_2003_2016_w2v_tmp':'https://drive.google.com/file/d/1eW0oJfFUCewrWzemJxEMPCkY9YNqVMDJ/view?usp=drive_link',
                                                   'WOKE_4_HST_2003_2019_w2v_tmp':'https://drive.google.com/file/d/1eNKpmpuCc9Legi2HStX2NoQqC7CQICdC/view?usp=drive_link',
                                                   'WOKE_4_HST_2003_2024_w2v_tmp':'https://drive.google.com/file/d/1lCYA4obqoWRy2_TMG9sMB4v77ihhhYuk/view?usp=drive_link'}}},
              'CFH-03-10':{'Incremental':{'Modelo 1':{'WOKE_1_CFH_2003_2010_w2v_inc':'https://drive.google.com/file/d/1_-lhKN5zK_mzXyzuG-ZTpmHs7OHpK0mc/view?usp=drive_link',
                                                      'WOKE_1_CFH_2011_2013_w2v_inc':'https://drive.google.com/file/d/1uGhlY7odmcAVeK6z5JE7EPQ5ORn224Mz/view?usp=drive_link',
                                                      'WOKE_1_CFH_2014_2016_w2v_inc':'https://drive.google.com/file/d/1BHFzfZABpXUxmZRenqI3pQVt5Wt5NYmP/view?usp=drive_link',
                                                      'WOKE_1_CFH_2017_2019_w2v_inc':'https://drive.google.com/file/d/1ltLfOyMAHa1KKfdgcoEtqWUt7L74YhEH/view?usp=drive_link',
                                                      'WOKE_1_CFH_2020_2024_w2v_inc':'https://drive.google.com/file/d/1PHzr330Q3oqLyrmFYnyIkpPjbkXk-s5Z/view?usp=drive_link'},
                                          'Modelo 2':{'WOKE_2_CFH_2003_2010_w2v_inc':'https://drive.google.com/file/d/1glYpHxXdAdMgRZ5KU5J7zJBEjmSpQx9e/view?usp=drive_link',
                                                      'WOKE_2_CFH_2011_2013_w2v_inc':'https://drive.google.com/file/d/1Iv7Yj5KYcnZ0yyjLAbx6o3ByylJPknQk/view?usp=drive_link',
                                                      'WOKE_2_CFH_2014_2016_w2v_inc':'https://drive.google.com/file/d/1nCiE-hIKYENCDOgIgY5LUuFMP_o4V07d/view?usp=drive_link',
                                                      'WOKE_2_CFH_2017_2019_w2v_inc':'https://drive.google.com/file/d/1avJ2wI2tkEKPjw4u02c8u6o3V7pHYupv/view?usp=drive_link',
                                                      'WOKE_2_CFH_2020_2024_w2v_inc':'https://drive.google.com/file/d/1EKXnHgsUMqP9AvITBVjzyescDKldkkPx/view?usp=drive_link'}},
                           'Temporal':{'Modelo 1':{'WOKE_1_CFH_2003_2010_w2v_tmp':'https://drive.google.com/file/d/1B6RmZIaFasZrmTUGPr1l9n6ISSj4XXrh/view?usp=drive_link',
                                                   'WOKE_1_CFH_2003_2013_w2v_tmp':'https://drive.google.com/file/d/1Noy8xft-tT5Du5MdPoVO_a7c1ghiHzp_/view?usp=drive_link',
                                                   'WOKE_1_CFH_2003_2016_w2v_tmp':'https://drive.google.com/file/d/1t1JAYVaASeHF3g0Y5nEScZnfLhbUu5kU/view?usp=drive_link',
                                                   'WOKE_1_CFH_2003_2019_w2v_tmp':'https://drive.google.com/file/d/1U_4x5Fc7c2uNS-6B3iE5zDSfnii_l6Tt/view?usp=drive_link',
                                                   'WOKE_1_CFH_2003_2024_w2v_tmp':'https://drive.google.com/file/d/1lSdNqxgWcxGZ5UMmjelZ79Z8lDMYQc3g/view?usp=drive_link'}}},
              'SAUDE-CORPO-03-10':{'Incremental':{'Modelo 1':{'WOKE_1_SAUDE-CORPO_2003_2010_w2v_inc':'https://drive.google.com/file/d/1SZx99koZsTg83agzDI92KJ6QmYItbi0B/view?usp=drive_link',
                                                              'WOKE_1_SAUDE-CORPO_2011_2013_w2v_inc':'https://drive.google.com/file/d/1ThhH9z5qSV6-coPkIMLGSyK_by7NWlRk/view?usp=drive_link',
                                                              'WOKE_1_SAUDE-CORPO_2014_2016_w2v_inc':'https://drive.google.com/file/d/1ThhH9z5qSV6-coPkIMLGSyK_by7NWlRk/view?usp=drive_link',
                                                              'WOKE_1_SAUDE-CORPO_2017_2019_w2v_inc':'https://drive.google.com/file/d/1jVjUEyftT9rL8erfjVqlaGD3vZys4wnR/view?usp=drive_link',
                                                              'WOKE_1_SAUDE-CORPO_2020_2024_w2v_inc':'https://drive.google.com/file/d/1BYhXPETd22wflcrPNjXRmlUwOLQlYLk5/view?usp=drive_link'},
                                                  'Modelo 2':{'WOKE_2_SAUDE-CORPO_2003_2010_w2v_inc':'https://drive.google.com/file/d/1ETzJ-9MmVg3ZuJDH6NqEuQZ8ph66Z1jB/view?usp=drive_link',
                                                               'WOKE_2_SAUDE-CORPO_2011_2013_w2v_inc':'https://drive.google.com/file/d/1LXOkLaWfDIhFTFLQyI2BJjDeKkg6OtN-/view?usp=drive_link',
                                                               'WOKE_2_SAUDE-CORPO_2014_2016_w2v_inc':'https://drive.google.com/file/d/1KLh91ALb5hMhI72ql5xkfcgq8SYCHqXs/view?usp=drive_link',
                                                               'WOKE_2_SAUDE-CORPO_2017_2019_w2v_inc':'https://drive.google.com/file/d/17oU7PL3vMr6H5ZRb8F23zjVl5CgjMlq2/view?usp=drive_link',
                                                               'WOKE_2_SAUDE-CORPO_2020_2024_w2v_inc':'https://drive.google.com/file/d/1DALBOpEJ48Y5rQob9OQ91FLN69O9oe79/view?usp=drive_link'},
                                                  'Modelo 3':{'WOKE_3_SAUDE-CORPO_2003_2010_w2v_inc':'https://drive.google.com/file/d/1WX5xALxWktUNZbZbcg-pi3gPQOwW524I/view?usp=drive_link',
                                                              'WOKE_3_SAUDE-CORPO_2011_2013_w2v_inc':'https://drive.google.com/file/d/1f244d8GUvL61T8p5SzUcaQR0a_yF8kAU/view?usp=drive_link',
                                                              'WOKE_3_SAUDE-CORPO_2014_2016_w2v_inc':'https://drive.google.com/file/d/1mgoSYa6OuyMRiDM6i23Pg-7z6voeKkfR/view?usp=drive_link',
                                                              'WOKE_3_SAUDE-CORPO_2017_2019_w2v_inc':'https://drive.google.com/file/d/1zGG3Ft9yiT4mz9kb6Ez8Cv4D2R7gzk3-/view?usp=drive_link',
                                                              'WOKE_3_SAUDE-CORPO_2020_2024_w2v_inc':'https://drive.google.com/file/d/1tY9wNtvqeYmKzRH2WARcHIcErr9894jd/view?usp=drive_link'}},
                                   'Temporal':{'Modelo 1':{'WOKE_1_SAUDE-CORPO_2003_2010_w2v_tmp':'https://drive.google.com/file/d/1Lh-n-clH5j75nfbr8LOOEifx58V2Mifl/view?usp=drive_link'},
                                                'Modelo 2':{'WOKE_2_SAUDE-CORPO_2003_2010_w2v_tmp':'https://drive.google.com/file/d/1lt7I6rY-qSQjDpKOVApwG4sLET2qUcv7/view?usp=drive_link'},
                                                'Modelo 3':{'WOKE_3_SAUDE-CORPO_2003_2010_w2v_tmp':'https://drive.google.com/file/d/1XuSp3Bm6EEL1Je6cSLhvC3rJNrIUZGDK/view?usp=drive_link'}}},
              'UFSC 2003 - 2006': {'Incremental':{'Modelo 1':{'WOKE_1_UFSC_2003_2006_w2v_inc':'https://drive.google.com/file/d/1BoaGPBYaF0SDCSxRS4hrnOHOJsKuIgSe/view?usp=drive_link'}},
                                   'Temporal':{}}}

def SKINNER():
  global DIC_INFO
  while True:

    print('Escolha o corpus de treino utilizado no modelo:\n\n')
    corpus_disponiveis = list(DIC_INFO.keys())
    for i,corpus_disponivel in enumerate(corpus_disponiveis):
      print(f'{i+1} - {corpus_disponivel}')
    print('0 - Encerrar programa')
    resposta_corpus = formatarEntrada(input('\nDigite o número referente a sua escolha: '))
    if resposta_corpus != '0':
      try:
        while not resposta_corpus.isdigit() or resposta_corpus not in [str(i) for i in range(1,len(corpus_disponiveis)+1)]:
          resposta_corpus = formatarEntrada(input('\nPor favor, digite uma resposta válida: '))
        resposta_corpus = corpus_disponiveis[int(resposta_corpus)-1]

        limparConsole()
        print('Você escolheu o corpus:',resposta_corpus,'\n')
        print('Agora escolha qual o modo treinado:\ninc --> Incremental\ntmp --> Temporal\n\n')
        modos_disponiveis = list(DIC_INFO[resposta_corpus].keys())
        for i,modo_disponivel in enumerate(modos_disponiveis):
          print(f'{i+1} - {modo_disponivel}')
        print('-1 - Voltar para o início')
        resposta_modo = formatarEntrada(input('\nDigite o número referente a sua escolha: '))
        if resposta_modo != '-1':
          while not resposta_modo.isdigit() or resposta_modo not in [str(i) for i in range(1,len(modos_disponiveis)+1)]:
            resposta_modo = formatarEntrada(input('\nPor favor, digite uma resposta válida: '))
          resposta_modo = modos_disponiveis[int(resposta_modo)-1]

          limparConsole()
          print('Você escolheu o modo de treinamento:',resposta_modo,'\n')
          top_modelos = list(DIC_INFO[resposta_corpus][resposta_modo].keys())
          if top_modelos:
            print('Agora escolha a numeração do Modelo:\n\n')
            for i,top_modelo in enumerate(top_modelos):
              print(f'{i+1} - {top_modelo}')
            print('-1 - Voltar para o início')
            resposta_top_modelo = formatarEntrada(input('\nDigite o número referente a sua escolha: '))
            if resposta_top_modelo != '-1':
              while not resposta_top_modelo.isdigit() or resposta_top_modelo not in [str(i) for i in range(1,len(top_modelos)+1)]:
                resposta_top_modelo = formatarEntrada(input('\nPor favor, digite uma resposta válida: '))
              resposta_top_modelo = top_modelos[int(resposta_top_modelo)-1]

              limparConsole()
              print('Você escolheu:',resposta_top_modelo,'\n')
              print('Agora escolha a série temporal a ser utilizada:\n\n')
              series_temporais = list(DIC_INFO[resposta_corpus][resposta_modo][resposta_top_modelo].keys())
              for i,serie_temporal in enumerate(series_temporais):
                print(f'{i+1} - {serie_temporal}')
              print('-1 - Voltar para o início')
              resposta_serie_temporal = formatarEntrada(input('\nDigite o número referente a sua escolha: '))
              if resposta_serie_temporal != '-1':
                while not resposta_serie_temporal.isdigit() or resposta_serie_temporal not in [str(i) for i in range(1,len(series_temporais)+1)]:
                  resposta_serie_temporal = formatarEntrada(input('\nPor favor, digite uma resposta válida: '))
                resposta_serie_temporal = series_temporais[int(resposta_serie_temporal)-1]

                limparConsole()
                print('Você escolheu a série temporal para o modelo:',resposta_serie_temporal,'\n')
                print('Configurando arquivos do modelo...')

                link_arquivos_modelo_drive = DIC_INFO[resposta_corpus][resposta_modo][resposta_top_modelo][resposta_serie_temporal]

                pasta_arquivos_modelo_atual = os.path.join(CAMINHO_SKINNER,resposta_corpus,resposta_modo,resposta_top_modelo)
                if not os.path.exists(os.path.join(pasta_arquivos_modelo_atual,resposta_serie_temporal)):
                  baixarArquivoDrive(link_drive=link_arquivos_modelo_drive,caminho_destino=os.path.join(pasta_arquivos_modelo_atual,'pasta_modelo_atual.zip'))
                  descompactarPasta(caminho_pasta=pasta_arquivos_modelo_atual)
                elif os.path.exists(os.path.join(pasta_arquivos_modelo_atual,'pasta_modelo_atual.zip')):
                  for caminho_arquivo in [os.path.join(pasta_arquivos_modelo_atual,arq) for arq in os.listdir(pasta_arquivos_modelo_atual) if os.path.isfile(os.path.join(pasta_arquivos_modelo_atual,arq)) and arq != 'pasta_modelo_atual.zip']:
                    os.remove(caminho_arquivo)
                  for caminho_pasta in [os.path.join(pasta_arquivos_modelo_atual,pasta) for pasta in os.listdir(pasta_arquivos_modelo_atual) if os.path.isdir(os.path.join(pasta_arquivos_modelo_atual,pasta))]:
                    shutil.rmtree(caminho_pasta)
                  descompactarPasta(caminho_pasta=pasta_arquivos_modelo_atual)
                else:
                  pass

                limparConsole()
                print('Você escolheu a série temporal para o modelo:',resposta_serie_temporal,'\n')
                print('Escolha um ou mais tokens a serem buscados:\n\nATENÇÃO:\n- O token precisa existir no modelo para a busca acontecer.\n- Confira a digitação antes de pressionar a tecla Enter.\n\n')
                print('-1 - Voltar para o início')
                token = formatarEntrada(input('Digite um token: '))
                if token != '-1':
                  tokens_desejados = []
                  while token != '0':
                    tokens_desejados.append(token)
                    token = formatarEntrada(input('Digite mais um token (0 para parar): '))
                  limparConsole()
                  print('\n\n\tTokens escolhidos para execução da busca no SKINNER:',', '.join(tokens_desejados))
                  print('\n\t--> Construção do HTML e posterior PDF iniciada. Por favor, aguarde!\n\n')

                  obterResultadoSKINNER(tokens_desejados=tokens_desejados,
                                        nome_modelo_atual=resposta_serie_temporal,
                                        pasta_modelos_atual=pasta_arquivos_modelo_atual)
                else:
                  limparConsole()
              else:
                limparConsole()
            else:
              limparConsole()
          else:
            print('Ainda não possuímos arquivos para este(s) modelo(s).\nPor favor, aperte Enter para voltar para o início.')
            input('\n')
        else:
          limparConsole()
      except Exception as e:
        print(f'\n\n\t! Ocorreu um erro inesperado... :/\n\n\t! Se você gostaria de contatar um programador do Grupo de Estudos, informe o seguinte erro:\n\n\t! {e.__class__.__name__}: {str(e)}\n\n\t! Junto com o nome do modelo e os tokens buscados.\n\n\t! Pedimos desculpas pelo ocorrido :/\n\n')
    else:
      limparConsole()
      print('\n\n\tPrograma finalizado.\n\n')
      break


