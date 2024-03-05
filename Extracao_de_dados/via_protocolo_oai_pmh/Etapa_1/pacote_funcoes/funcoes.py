import os
import time
import re
from typing import Dict
import requests
from bs4 import BeautifulSoup
import xmltodict
from unidecode import unidecode
import joblib

os_name = os.name

def limparConsole():
    """
    Função responsável por limpar a tela do console. Ela já considera, usando a bibliteca OS 
    o seu sistema operacional para executar o comando mais adequado.
    """
    if os_name == 'posix':
        os.system('clear')
    elif os_name == 'nt':
        os.system('cls')

def criarDiretorio(caminho : str) -> None:
    """
    Função que cria o diretório, caso ele não exista.

    Parâmetros:
    -----------
    - param caminho: String contendo o caminho para o diretório que será analisado.
    """
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        return caminho
    else:
        return caminho

def ObterDiretorioAtual() -> str:
    """
    Essa função retornará o diretório atual da pasta de trabalho que está executando o 
    script em questão.

    Retorno:
    -------
    - return: String contendo o caminho total até a pasta de trabalho que está executando 
    este script.
    """
    return os.getcwd()

if 'Etapa_1' in ObterDiretorioAtual():
    caminho_pasta_etapa_1 = ObterDiretorioAtual()
else:
    caminho_pasta_etapa_1 = os.path.join(ObterDiretorioAtual(),'Etapa_1')

caminho_pasta_dicts = criarDiretorio(os.path.join(caminho_pasta_etapa_1,'Dicts'))

caminho_pasta_lista_colecoes = criarDiretorio(os.path.join(caminho_pasta_etapa_1,'Lista_de_colecoes'))

padrao_regex_data = re.compile(r'^(\d{4})')

padrao_regex_data_descricao = re.compile(r'Florianópolis,\s*(\d{4})')


def enviarRequisicao(link : str) -> tuple[bool, requests.Response] | tuple[bool, str]:
    """
    Realiza o envio de uma requisição por meio de um link informado,
    analisa se o código de status da resposta é do tipo "OK" (200) e retorna,
    em caso afirmativo, um booleano "True" e a resposta da requisição ou, em caso
    negativo, um booleano "False" e uma string com o código de status da resposta.

    Parâmetros:
    -----------
    - param link: URL/link da requisição que será enviada.
    
    Retorno:
    --------
    - return: Tupla com o status do processo (True ocorreu tudo certo e False
    aconteceu algo indesejado) e uma string. Em caso do status ser True, a string
    será a própria resposta da requisição, em caso de False, a string será o
    erro identificado no processo de enviar a requisição e esperar a resposta.
    """
    try:
        response = requests.get(url=link)
        if response.status_code == 200:
            return True, response
        else:
            return False, f'Status code != 200: response.status_code = {str(response.status_code)}'
    except Exception as e:
        erro = f'{e.__class__.__name__}: {str(e)}'
        return False, erro

def criarListaDeColecoes(link_colecoes: str) -> tuple[bool, list] | tuple[bool, str]:
    """
    Faz a criação de uma lista com todas as coleções encontradas no site do
    Repositório Institucional da UFSC na comunidade de Teses e Dissertações.
    Tal lista contém tupla(s) com 3 posições, do tipo:
    ('Nome da coleção','Número da coleção',Número de trabalhos publicados),
    ou seja, com os tipos: [(str, str, int)].

    Parâmetros:
    -----------
    - param link_colecoes: URL/link da página da comunidade de Teses e Dissertações
    do Repositório Institucional da UFSC.
    
    Retornos:
    ---------
    - return: Lista contendo tuplas que armazenam as informações das coleções
    presentes na página da comunidade de Teses e Dissertações do RI da UFSC.
    """
    status_requisicao_colecoes, response_colecoes = enviarRequisicao(link=link_colecoes)

    if status_requisicao_colecoes:

        soup = BeautifulSoup(response_colecoes.content,'html.parser')
        campo_links_colecoes = soup.find('div', attrs={'class':'ds-static-div secondary'})
        if campo_links_colecoes:
            colecoes = campo_links_colecoes.find_all('li',class_=re.compile('ds-artifact-item'))
            if colecoes:
                lista_de_colecoes = []
                for colecao in colecoes:
                    nome_colecao = numero_publicacoes = numero_colecao = None

                    nome_colecao = colecao.find('a')
                    if nome_colecao:
                        nome_colecao = str(nome_colecao.text).strip()

                    numero_publicacoes = colecao.find('span')
                    if numero_publicacoes:
                        numero_publicacoes = str(numero_publicacoes.text).strip().replace('[','').replace(']','')
                        if numero_publicacoes.isdigit():
                          numero_publicacoes = int(numero_publicacoes)

                    numero_colecao = colecao.find('a')
                    numero_colecao = str(numero_colecao['href'])
                    lista_numero_colecao = numero_colecao.split('/')
                    numero_colecao = lista_numero_colecao[-1]

                    if nome_colecao and numero_publicacoes and numero_colecao:
                      lista_de_colecoes.append((nome_colecao,numero_colecao,numero_publicacoes))

                return True, lista_de_colecoes

            else:
              return False, 'Campo "colecoes" não localizado corretamente'
        else:
            return False, 'Campo "links_colecoes" não localizado corretamente'
    else:
      return False, response_colecoes

def comunicarComAPI(link : str) -> tuple[bool, dict] | tuple[bool, str]:
    """
    Realiza a comunicação com a interface OAI-PMH do RI da UFSC para coletar a
    resposta (em XML) e transformá-la em um dicionário Python.

    Parâmetros:
    -----------
    - param link: URL/Link da requisição que será enviada para a interface.
    
    Retornos:
    ---------
    - return: Tupla contendo o status do processo (True para indicar que deu tudo
    certo e False para indicar que não ocorreu como desejado) e o dicionário
    da resposta (em caso afirmativo do status) ou uma string com o erro
    encontrado (em caso negativo do status).
    """
    print('\n\n\t--> Enviando requisição para API...\n')
    status_requisicao_api, response_api = enviarRequisicao(link=link)
    if status_requisicao_api:
        try:
            dic_xml = xmltodict.parse(response_api.content)
            return True, dic_xml
        except Exception as e:
            erro = f'Erro "{e.__class__.__name__}": {str(e)}'
            return False, erro
    else:
        return False, response_api

def formatarNomeArquivoColecao(nome_colecao : str) -> str:
    """
    Realiza a formatação do nome da coleção proveniente do site do RI
    e passa para uma notação mais amigável no contexto de nomes de
    arquivos (sem caractéres especiais, "/", ":", "-", "ç", "~", etc...), para
    evitar qualquer conflito ou prejuízo por conta da nomenclatura.

    Parâmetros:
    -----------
    - param nome_colecao: Nome da coleção proveniente do site.
    
    Retornos:
    ---------
    - return: Nome da coleção formatado para salvar e "manusear" adequadamente
    o(s) arquivo(s).
    """
    nome_colecao_formatado = re.sub(r'[^\w]', '_', unidecode(nome_colecao))
    nome_colecao_formatado = nome_colecao_formatado.replace('__','_')
    if nome_colecao_formatado.endswith('_'):
        nome_colecao_formatado = nome_colecao_formatado[:len(nome_colecao_formatado)-1]
    nome_colecao_formatado = nome_colecao_formatado.replace('Programa_de_Pos_Graduacao_em_','')
    return nome_colecao_formatado

def validaFormatoDicXML(dic_xml : dict) -> bool:
    """
    Realiza a validação do dicionário retornado da comunicação com a
    interface do RI UFSC.

    Parâmetros:
    -----------
    - param dic_xml: Dicionário XML retornado da comunicação com a
    interface depois da transformação XML --> dict.
    
    Retornos:
    ---------
    - return: Booleano indicando se o dicionário em questão tem ou não
    todos os campos esperados na resposta para a adequada coleta dos
    metadados. True quer dizer que o dicionário contém os campos
    adequadamente e False quer dizer que faltou algum campo necessário
    no processo para encontrar as informações dentro do dicionário de
    resposta.
    """
    if isinstance(dic_xml,dict):
        if 'OAI-PMH' in dic_xml.keys():
            if isinstance(dic_xml['OAI-PMH'],dict):
                if 'ListRecords' in dic_xml['OAI-PMH'].keys():
                    if isinstance(dic_xml['OAI-PMH']['ListRecords'],dict):
                        if 'record' in dic_xml['OAI-PMH']['ListRecords'].keys():
                            if isinstance(dic_xml['OAI-PMH']['ListRecords']['record'],list) or isinstance(dic_xml['OAI-PMH']['ListRecords']['record'],dict):
                                return True
    return False

def encontrarDataNaDescricao(data_descricao : str) -> str:
    """
    Encontra uma data na descrição dos trabalhos presente na página
    do RI referente ao trabalho. Tem como base que o formato de data
    na descrição é do tipo "Florianópolis, 2024", por exemplo, ou
    qualquer outro ano, com 4 dígitos em sequência, ao final da descrição,
    caso exista.

    Parâmetros:
    -----------
    - param data_descricao: String contendo toda a descrição do trabalho
    proveniente da comunicação com a interface.

    Retornos:
    ---------
    - return: Data contendo os 4 dígitos, caso encontrada ou "N.I." em
    caso de não identificação da data na descrição (sem correspondência
    entre o padrão de data e a string da descrição).
    """

    correspondencias_data_descricao = padrao_regex_data_descricao.search(data_descricao[len(data_descricao)-len('Florianópolis,  0000.'):])

    data_desc = 'N.I.'
    if correspondencias_data_descricao:
        data_descricao = correspondencias_data_descricao.group(1)
        correspondencias_data_desc = padrao_regex_data.search(data_descricao)
        if correspondencias_data_desc:
            data_desc = correspondencias_data_desc.group(1)
    return data_desc

def encontrarPDFNaListagemDeArquivos(listagem_de_arquivos : list) -> str:
    """
    Em caso de encontrar mais de um arquivo na seção de arquivos do trabalho,
    encontra o arquivo que for PDF ou o arquivo PDF, dentre outros arquivos
    PDFs, que tiver o maior tamanho.

    Parâmetros:
    -----------
    - param listagem_de_arquivos: Lista contendo os dicionários que representam
    os campos dos arquivos em questão.
    
    Retornos:
    ---------
    - return: String contendo o link do PDF do trabalho ou "N.I." caso não
    encontre um arquivo PDF ("application/pdf").
    """
    link_pdf = 'N.I.'
    lista_de_pdfs = []
    for info_arquivo in listagem_de_arquivos:
        pdf_encontrado = False
        if isinstance(info_arquivo,dict):
            if 'field' in info_arquivo.keys():
                if isinstance(info_arquivo['field'],list):
                    listagem_campo_info_arquivo = info_arquivo['field']
                    for campo_info_arquivo in (listagem_campo_info_arquivo):
                        if isinstance(campo_info_arquivo,dict):
                            if '@name' in campo_info_arquivo.keys() and '#text' in campo_info_arquivo.keys():
                                if campo_info_arquivo['@name'] == 'format' and campo_info_arquivo['#text'] == 'application/pdf':
                                    pdf_encontrado = True
                                if pdf_encontrado:
                                    if campo_info_arquivo['@name'] == 'size':
                                        tamanho_pdf_encontrado = campo_info_arquivo['#text'].strip()
                                        if tamanho_pdf_encontrado.isdigit():
                                            tamanho_pdf_encontrado = float(tamanho_pdf_encontrado)
                                    if campo_info_arquivo['@name'] == 'url':
                                        link_pdf_encontrado = campo_info_arquivo['#text'].strip()
        if pdf_encontrado:
            lista_de_pdfs.append((tamanho_pdf_encontrado,link_pdf_encontrado))

    if lista_de_pdfs:
        tamanho_maior_de_pdf = 0
        link_maior_pdf = ''

        for pdf_encontrado_listado in lista_de_pdfs:
            tamanho_pdf = pdf_encontrado_listado[0]
            link_do_pdf = pdf_encontrado_listado[1]

            if tamanho_pdf > tamanho_maior_de_pdf:
                tamanho_maior_de_pdf = tamanho_pdf
                link_maior_pdf = link_do_pdf

        link_pdf = str(link_maior_pdf)

    return link_pdf

def processarDicXML(dic : Dict[str,list], dic_xml : dict) -> Dict[str,list]:
    """
    Percorre todo dicionário de resposta da interface (antigo XML) encontrando
    os campos dos metadados, coletando as informações presentes nesses campos
    e as adicionando no dicionário "dic" passado como argumento dessa função
    (o atualizando). Caso algum metadado não for propriamente encontrado, é
    preenchido como "N.I." (Não Identificado).

    Parâmetros:
    -----------
    - param dic: Dicionário de entrada, no qual será preenchido/adicionado os
    metadados encontrados no dicionário de resposta da interface "dic_xml".
    - param dic_xml: Dicionário retornado da comunicação com a interface do RI,
    após transformação de "XML" para "dict".
    
    Retornos:
    ---------
    - return: Dicionário "dic" passado como entrada atualizado, depois da
    coleta dos metadados presentes no dicionário de entrada "dic_xml".
    """
    if isinstance(dic_xml['OAI-PMH']['ListRecords']['record'],list):
      lista_de_trabalhos_dic_xml = dic_xml['OAI-PMH']['ListRecords']['record']
    elif isinstance(dic_xml['OAI-PMH']['ListRecords']['record'],dict):
      lista_de_trabalhos_dic_xml = [dic_xml['OAI-PMH']['ListRecords']['record']]
    else:
      lista_de_trabalhos_dic_xml = []

    for trabalho in lista_de_trabalhos_dic_xml:

       titulo = autor = resumo = descricao = assuntos = lingua = data_rep = data_desc = tipo = link = link_pdf = 'N.I.'

       if isinstance(trabalho,dict):
            if 'metadata' in trabalho.keys():

                if 'metadata' in trabalho['metadata'].keys():

                    if 'element' in trabalho['metadata']['metadata'].keys():
                        dic_trabalho_metadados = trabalho['metadata']['metadata']['element']

                        if isinstance(dic_trabalho_metadados,list):
                            for campo in dic_trabalho_metadados:
                                if isinstance(campo,dict):
                                    if 'element' in campo.keys() and '@name' in campo.keys():
                                        if campo['@name'] == 'dc':
                                            campo_metadados_info_gerais = campo['element']
                                            if isinstance(campo_metadados_info_gerais,list):
                                                for metadado in campo_metadados_info_gerais:
                                                    if isinstance(metadado,dict):
                                                        if '@name' in metadado.keys() and 'element' in metadado.keys():

                                                            if metadado['@name'] == 'contributor':
                                                                if isinstance(metadado['element'],list):
                                                                    listagem_contribuintes =  metadado['element']
                                                                    for contribuinte in listagem_contribuintes:
                                                                        if isinstance(contribuinte,dict):
                                                                            if '@name' in contribuinte.keys() and 'element' in contribuinte.keys():
                                                                                if contribuinte['@name'] == 'author':
                                                                                        if isinstance(contribuinte['element'],dict):
                                                                                            if 'field' in contribuinte['element'].keys():
                                                                                                if isinstance(contribuinte['element']['field'],dict):
                                                                                                    if '#text' in contribuinte['element']['field'].keys():
                                                                                                        autor = str(contribuinte['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                                        # print(autor)
                                                                                                        break
                                                                elif isinstance(metadado['element'],dict):
                                                                    if '@name' in metadado['element'].keys() and 'element' in metadado['element'].keys():
                                                                        if metadado['element']['@name'] == 'author' and isinstance(metadado['element']['element'],dict):
                                                                            if 'field' in metadado['element']['element'].keys():
                                                                                if isinstance(metadado['element']['element']['field'],dict):
                                                                                    if '#text' in metadado['element']['element']['field'].keys():
                                                                                        autor = str(metadado['element']['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                        # print(autor)


                                                            elif metadado['@name'] == 'date':
                                                                if isinstance(metadado['element'],list):
                                                                    listagem_datas =  metadado['element']
                                                                    for data in listagem_datas:
                                                                        if isinstance(data,dict):
                                                                                if '@name' in data.keys() and 'element' in data.keys():
                                                                                    if data['@name'] == 'issued':
                                                                                        if isinstance(data['element'],dict):
                                                                                            if 'field' in data['element']:
                                                                                                if isinstance(data['element']['field'],dict):
                                                                                                    if '#text' in data['element']['field'].keys():
                                                                                                        correspondencias = padrao_regex_data.search(str(data['element']['field']['#text']).strip())
                                                                                                        if correspondencias:
                                                                                                            data_rep = correspondencias.group(1)
                                                                                                            # print(data_rep)
                                                                                                        break

                                                            elif metadado['@name'] == 'identifier':
                                                                if isinstance(metadado['element'],list):
                                                                    listagem_identificadores =  metadado['element']
                                                                    for identificador in listagem_identificadores:
                                                                        if isinstance(identificador,dict):
                                                                                if '@name' in identificador.keys() and 'element' in identificador.keys():
                                                                                    if identificador['@name'] == 'uri':
                                                                                        if isinstance(identificador['element'],dict):
                                                                                            if 'field' in identificador['element'].keys():
                                                                                                if isinstance(identificador['element']['field'],dict):
                                                                                                    if '#text' in identificador['element']['field'].keys():
                                                                                                        link = str(identificador['element']['field']['#text']).strip()
                                                                                                        # print(link)
                                                                                                        break

                                                            elif metadado['@name'] == 'description':
                                                                if isinstance(metadado['element'],list):
                                                                    listagem_descricoes =  metadado['element']
                                                                    for dic_descricao in listagem_descricoes:
                                                                        if isinstance(dic_descricao,dict):
                                                                            if '@name' in dic_descricao.keys() and 'field' in dic_descricao.keys():
                                                                                if isinstance(dic_descricao['field'],dict):
                                                                                    if '#text' in dic_descricao['field'].keys():
                                                                                        descricao = str(dic_descricao['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                        # print(descricao)
                                                                                        data_desc = encontrarDataNaDescricao(data_descricao=descricao)

                                                                            elif '@name' in dic_descricao.keys() and 'element' in dic_descricao.keys():
                                                                                if dic_descricao['@name'] == 'abstract':
                                                                                    if isinstance(dic_descricao['element'],dict):
                                                                                        if 'field' in dic_descricao['element']:
                                                                                            if isinstance(dic_descricao['element']['field'],dict):
                                                                                                if '#text' in dic_descricao['element']['field'].keys():
                                                                                                    resumo = str(dic_descricao['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                                    # print(resumo)
                                                                                                    break
                                                                                            elif isinstance(dic_descricao['element']['field'],list):
                                                                                                if isinstance(dic_descricao['element']['field'][0],dict):
                                                                                                    if '#text' in dic_descricao['element']['field'][0].keys():
                                                                                                        resumo = str(dic_descricao['element']['field'][0]['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                                        # print(resumo)
                                                                                                        break
                                                                                    elif isinstance(dic_descricao['element'],list):
                                                                                        if isinstance(dic_descricao['element'][0],dict):
                                                                                            if 'field' in dic_descricao['element'][0].keys():
                                                                                                if isinstance(dic_descricao['element'][0]['field'],dict):
                                                                                                    if '#text' in dic_descricao['element'][0]['field'].keys():
                                                                                                        resumo = str(dic_descricao['element'][0]['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                                        # print(resumo)
                                                                                                        break
                                                                elif isinstance(metadado['element'],dict):
                                                                    if 'field' in metadado['element'].keys():
                                                                        if isinstance(metadado['element']['field'],dict):
                                                                            if '#text' in metadado['element']['field'].keys():
                                                                                descricao = str(metadado['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                # print(descricao)
                                                                    elif '@name' in metadado['element'].keys() and 'element' in metadado['element'].keys():
                                                                        if metadado['element']['@name'] == 'abstract' and isinstance(metadado['element']['element'],dict):
                                                                            if 'field' in metadado['element']['element'].keys():
                                                                                if isinstance(metadado['element']['element']['field'],dict):
                                                                                    if '#text' in metadado['element']['element']['field'].keys():
                                                                                        resumo = str(metadado['element']['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                        # print(resumo)




                                                            elif metadado['@name'] == 'language':
                                                                if isinstance(metadado['element'],dict):
                                                                    if 'element' in metadado['element'].keys():
                                                                        if isinstance(metadado['element']['element'],dict):
                                                                            if 'field' in metadado['element']['element'].keys():
                                                                                if isinstance(metadado['element']['element']['field'],dict):
                                                                                    if '#text' in metadado['element']['element']['field'].keys():
                                                                                        lingua = str(metadado['element']['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                        # print(lingua)


                                                            elif metadado['@name'] == 'subject':
                                                                if isinstance(metadado['element'],dict):
                                                                    if 'element' in metadado['element'].keys():
                                                                        if isinstance(metadado['element']['element'],dict):
                                                                            if 'field' in metadado['element']['element'].keys():
                                                                                if isinstance(metadado['element']['element']['field'],list):
                                                                                    listagem_assuntos = metadado['element']['element']['field']
                                                                                    assuntos = ''
                                                                                    for assunto in listagem_assuntos:
                                                                                        if isinstance(assunto,dict):
                                                                                            if '@name' in assunto.keys() and '#text' in assunto.keys():
                                                                                                if assunto['@name'] == 'value':
                                                                                                    assuntos += str(assunto['#text']).strip().encode('utf-8').decode('utf-8')+', '
                                                                                    assuntos = assuntos[:len(assuntos)-2].strip()
                                                                                    # print(assuntos)
                                                                                elif isinstance(metadado['element']['element']['field'],dict):
                                                                                    if '#text' in metadado['element']['element']['field'].keys():
                                                                                        assuntos = str(metadado['element']['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                        # print(assuntos)

                                                            elif metadado['@name'] == 'title':
                                                                if isinstance(metadado['element'],dict):
                                                                    if 'field' in metadado['element'].keys():
                                                                        if isinstance(metadado['element']['field'],dict):
                                                                            if '#text' in metadado['element']['field'].keys():
                                                                                titulo = str(metadado['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                # print(titulo)

                                                            elif metadado['@name'] == 'type':
                                                                if isinstance(metadado['element'],dict):
                                                                    if 'field' in metadado['element'].keys():
                                                                        if isinstance(metadado['element']['field'],dict):
                                                                            if '#text' in metadado['element']['field'].keys():
                                                                                tipo = str(metadado['element']['field']['#text']).strip().encode('utf-8').decode('utf-8')
                                                                                # print(tipo)





                                        elif campo['@name'] == 'bundles':
                                            if isinstance(campo['element'],dict):
                                                if 'element' in campo['element'].keys():
                                                    if isinstance(campo['element']['element'],dict):
                                                        if 'element' in campo['element']['element'].keys():
                                                            if isinstance(campo['element']['element']['element'],dict):
                                                                if 'field' in campo['element']['element']['element'].keys():
                                                                    if isinstance(campo['element']['element']['element']['field'],list):
                                                                        listagem_info_arquivos = campo['element']['element']['element']['field']
                                                                        for info_arquivo in listagem_info_arquivos:
                                                                            if isinstance(info_arquivo,dict):
                                                                                if '@name' in info_arquivo.keys() and '#text' in info_arquivo.keys():
                                                                                    if info_arquivo['@name'] == 'url':
                                                                                        if info_arquivo['#text'].strip().endswith('.pdf'):
                                                                                            link_pdf = str(info_arquivo['#text']).strip()
                                                                                            # print(link_pdf)
                                                            elif isinstance(campo['element']['element']['element'],list):
                                                                listagem_info_arquivos = campo['element']['element']['element']
                                                                link_pdf = encontrarPDFNaListagemDeArquivos(listagem_de_arquivos=listagem_info_arquivos)


                                            elif isinstance(campo['element'],list):
                                                for elemento_do_campo_arquivo in campo['element']:
                                                    campo_pdf = False
                                                    if isinstance(elemento_do_campo_arquivo,dict):
                                                        if 'field' in elemento_do_campo_arquivo.keys():
                                                            if isinstance(elemento_do_campo_arquivo['field'],dict):
                                                                if '#text' in elemento_do_campo_arquivo['field']:
                                                                    if str(elemento_do_campo_arquivo['field']['#text']).strip() == 'ORIGINAL':
                                                                        campo_pdf = True
                                                        if campo_pdf:
                                                            if 'element' in elemento_do_campo_arquivo.keys():
                                                                if isinstance(elemento_do_campo_arquivo['element'],dict):
                                                                    if 'element' in elemento_do_campo_arquivo['element'].keys():
                                                                        if isinstance(elemento_do_campo_arquivo['element']['element'],dict):
                                                                            if 'field' in elemento_do_campo_arquivo['element']['element'].keys():
                                                                                if isinstance(elemento_do_campo_arquivo['element']['element']['field'],list):
                                                                                    for item_arquivo in elemento_do_campo_arquivo['element']['element']['field']:
                                                                                        if isinstance(item_arquivo,dict):
                                                                                            if '@name' in item_arquivo.keys() and '#text' in item_arquivo.keys():
                                                                                                if item_arquivo['@name'] == 'url' and item_arquivo['#text'].strip().endswith('.pdf'):
                                                                                                    link_pdf = str(item_arquivo['#text']).strip()
                                                                                                    # print(link_pdf)
                                                                                                    break


                                                if isinstance(campo['element'][0],dict):
                                                    if 'element' in campo['element'][0].keys():
                                                        if isinstance(campo['element'][0]['element'],dict):
                                                            if 'element' in campo['element'][0]['element'].keys():
                                                                if isinstance(campo['element'][0]['element']['element'],dict):
                                                                    if 'field' in campo['element'][0]['element']['element'].keys():
                                                                        if isinstance(campo['element'][0]['element']['element']['field'],list):
                                                                            listagem_info_arquivos = campo['element'][0]['element']['element']['field']
                                                                            for info_arquivo in listagem_info_arquivos:
                                                                                if isinstance(info_arquivo,dict):
                                                                                    if '@name' in info_arquivo.keys() and '#text' in info_arquivo.keys():
                                                                                        if info_arquivo['@name'] == 'url':
                                                                                            if info_arquivo['#text'].strip().endswith('.pdf'):
                                                                                                link_pdf = str(info_arquivo['#text']).strip()
                                                                                                # print(link_pdf)
                                                                                                break


                dic['Título'].append(titulo)
                dic['Autor'].append(autor)
                dic['Resumo'].append(resumo)
                dic['Descrição'].append(descricao)
                dic['Assuntos'].append(assuntos)
                dic['Língua'].append(lingua)
                dic['Ano repositório'].append(data_rep)
                dic['Ano descrição'].append(data_desc)
                dic['Tipo'].append(tipo)
                dic['Link página'].append(link)
                dic['Link PDF'].append(link_pdf)

    return dic

def printarAdicionandoProblemaNumTxt(string_problema : str, caminho_pasta_etapa_1 : str) -> None:
    """
    Imprime na tela a mensagem de problema encontrada durante a execução e a adiciona num arquivo
    de texto referente aos problemas encontrados na etapa 1.
    
    Parâmetros:
    -----------
    - param string_problema: String da descrição do problema encontrado durante a execução de algum
    processo ao decorrer da execução.
    - param caminho_pasta_etapa_1: String do caminho referente a pasta da etapa 1 no Google Drive, aonde o
    arquivo de texto dos problemas deve ser salvo.
    
    Retornos:
    ---------
    - return: None, não há retornos nessa função.
    """
    try:
        with open(os.path.join(caminho_pasta_etapa_1,'Problemas_etapa_1.txt'),'a',encoding='utf-8') as f:
            f.write(string_problema+'\n\n'+('*'*100))
            f.close()
        
    except Exception as e:
        erro = f'{e.__class__.__name__}: {str(e)}'
        print(f'\nProblema ao salvar arquivo de texto contendo falhas desta etapa:\n\t-->{erro}\n')
    finally:
        print(string_problema)

def main():
    """
    Função principal a qual se encarregará de fazer as chamadas para as outras funções na sequência adequada.

    Parâmetros:
    -----------
    - param exec_google_colab: Bool que decidirá se a execução será feita no Colab ou em outro ambiente de 
    execução.
    """
    print('\n\n\tColetando informações das coleções do repositório (nome, número para API, número de publicações)...')
    time.sleep(2)
    link_pagina_repositorio_colecoes = 'https://repositorio.ufsc.br/handle/123456789/74645'

    status_lista_de_colecoes, lista_de_colecoes = criarListaDeColecoes(link_colecoes=link_pagina_repositorio_colecoes)
    if status_lista_de_colecoes:

        if lista_de_colecoes:

            joblib.dump(lista_de_colecoes,os.path.join(caminho_pasta_lista_colecoes,'lista_de_colecoes.joblib'))

            qtd_total_colecoes = len(lista_de_colecoes)

            for contagem, colecao in enumerate(lista_de_colecoes): # [0:30]
                print(contagem+1,'de',qtd_total_colecoes)
                print('\nColeção:',colecao[0])

                nome_colecao, numero_colecao, numero_publicacoes = colecao

                dic = {'Título':[],'Autor':[],'Resumo':[],'Descrição':[],'Assuntos':[],'Língua':[],'Tipo':[],'Ano repositório':[],'Ano descrição':[],'Link página':[],'Link PDF':[]}

                link = 'https://repositorio.ufsc.br/oai/request?verb=ListRecords&metadataPrefix=xoai&set=col_123456789_'+numero_colecao

                status_requisicao, dic_xml = comunicarComAPI(link=link)

                if status_requisicao:
                    limparConsole()
                    if validaFormatoDicXML(dic_xml=dic_xml):
                        dic_atualizado = processarDicXML(dic=dic,dic_xml=dic_xml)

                        if 'resumptionToken' in dic_xml['OAI-PMH']['ListRecords'].keys():
                            if isinstance(dic_xml['OAI-PMH']['ListRecords']['resumptionToken'],dict):
                                while '#text' in dic_xml['OAI-PMH']['ListRecords']['resumptionToken']:
                                    limparConsole()
                                    print('\n\nIndo para próxima página de resultados...')
                                    link = 'https://repositorio.ufsc.br/oai/request?verb=ListRecords&resumptionToken='+str(dic_xml['OAI-PMH']['ListRecords']['resumptionToken']['#text']).strip()

                                    status_requisicao, dic_xml_atualizado = comunicarComAPI(link=link)
                                    if status_requisicao:
                                        if validaFormatoDicXML(dic_xml=dic_xml_atualizado):
                                            dic_atualizado = processarDicXML(dic=dic_atualizado,dic_xml=dic_xml_atualizado)
                                            dic_xml = dic_xml_atualizado
                                        else:
                                            break
                                    else:
                                        break

                        if len(dic_atualizado['Link página']) > 0:
                            print('\n\n\tSalvando dicionário...\n\n')
                            nome_arquivo_dic = formatarNomeArquivoColecao(nome_colecao=nome_colecao)
                            joblib.dump(dic_atualizado,os.path.join(caminho_pasta_dicts,f'{nome_arquivo_dic}.joblib'))
                    else:
                        problema = f'\nProblemas validando dicionário XML recebido da API: "{link}" da coleção "{colecao}"\n\n{dic_xml}'
                        printarAdicionandoProblemaNumTxt(string_problema=problema,caminho_pasta_etapa_1=caminho_pasta_etapa_1)
                else:
                    problema = f'Problemas enviando requisição para o link: "{link}" referente a coleção "{colecao}\n\n{dic_xml}'
                    printarAdicionandoProblemaNumTxt(string_problema=problema,caminho_pasta_etapa_1=caminho_pasta_etapa_1)
                    if "timeout" in problema.lower():
                      print('\n! Encerrando programa por conta do Timeout.\n')
                      break
                
        else:
            problema = f'A lista de coleções está vazia.\nVerifique se houve alguma mudança na página HTML do Repositório: "{link_pagina_repositorio_colecoes}"'
            printarAdicionandoProblemaNumTxt(string_problema=problema,caminho_pasta_etapa_1=caminho_pasta_etapa_1)
    else:
        problema = f'Problema(s) na criação da lista de coleções via webscraping da página do RI na comunidade de Teses e Dissertações.\n{lista_de_colecoes}'
        printarAdicionandoProblemaNumTxt(string_problema=problema,caminho_pasta_etapa_1=caminho_pasta_etapa_1)

    print('\n\n\t--> Programa finalizado <--\n\n')
