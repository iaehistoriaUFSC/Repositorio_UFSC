import os
import joblib
from weasyprint import HTML

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

def criarDiretorio(caminho : str) -> None:
    if os.path.isfile(caminho):
        caminho = os.path.dirname(caminho)
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        return caminho
    else:
        return caminho

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
caminho_arquivo_relatorio_pdf = os.path.join(caminho_pasta_relatorio_pdf,'Relatório - Extração de Dados WOKE_final.pdf')
caminho_arquivo_html = os.path.join(caminho_pasta_arquivos_geracao_relatorio_pdf,'HTML_relatorio_final.html')

dic_erros_amostrados = {'Problema ao ler/abrir PDF (provavelmente arquivo corrompido)':['"FileDataError": cannot open broken document',
                                                                                        '"EmptyFileError": cannot open empty document',
                                                                                        '"IndexError": page 0 not in document'],
                        'Problema ao ler/abrir PDF (provavelmente PDF muito pequeno)':['"IndexError": page 1 not in document',
                                                                                       '"IndexError": page 2 not in document']}


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

def gerarQuebraDeLinhasDoTamanhoDaImagem() -> str:
    """
    Gera uma string, para compor a string geral do HTML, que faz a quebra de
    linhas até que o texto que irá ser escrito posteriormente não fique embaixo
    da imagem presente na capa.

    :param None: Não há parametros para esta função.
    :return: String HTML com as devidas quebras de linhas.
    """
    string_html = '<br>'*30
    return string_html

def preencherQuantidadesRelatorioPDF(dic_falhas : dict) -> tuple[int,int,int,int,int,int,int,int,int,int]:
    """
    Dá valor as variáveis de quantidades que serão utilizados na página depois
    da capa do PDF.

    :param dic_falhas: Dicionário de falhas da coleção em questão.
    :return: Tupla com 6 elementos sendo eles a quantidade de coleções analisadas,
    quantidade total de trabalhos no site, quantidade total de trabalhos
    provenientes da comunicação com a API, quantidade total de trabalhos com
    avisos, quantidade total de trabalhos que tiveram seu texto extraido e a
    quantidade total de trabalhos analisados, respectivamente.
    """

    quantidade_total_de_colecoes_site = quantidade_total_de_trabalhos_site = quantidade_de_colecoes_analisadas = 0
    quantidade_total_de_trabalhos_site_analisados = quantidade_total_trabalhos_api = 0
    quantidade_total_de_trabalhos_com_avisos_fora_do_recorte = quantidade_total_de_trabalhos_com_texto_extraido_geral = 0
    quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte = quantidade_total_de_trabalhos_analisados = 0
    quantidade_total_de_trabalhos_com_avisos_geral = quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte = 0
    quantidade_total_de_trabalhos_com_texto_extraido_fora_do_recorte = quantidade_total_de_trabalhos_com_texto_extraido_geral = 0
    quantidade_total_de_trabalhos_analisados_dentro_do_recorte = quantidade_total_de_trabalhos_analisados_fora_do_recorte = 0
    lista_colecoes_site = joblib.load(caminho_lista_colecoes_site)

    for colecao_site in lista_colecoes_site:
        quantidade_total_de_trabalhos_site += colecao_site[2]
        quantidade_total_de_colecoes_site += 1

    for colecao in dic_falhas['Coleções'].keys():
        quantidade_de_colecoes_analisadas += 1
        quantidade_de_trabalhos_analisados_dentro_do_recorte = dic_falhas["Coleções"][colecao]["Número de trabalhos analisados"]['Possivelmente dentro do recorte']
        quantidade_de_trabalhos_analisados_fora_do_recorte = dic_falhas["Coleções"][colecao]["Número de trabalhos analisados"]['Fora do recorte']
        quantidade_de_trabalhos_com_avisos_dentro_do_recorte = len(dic_falhas['Coleções'][colecao]['Avisos']['Possivelmente dentro do recorte']['Erro'])
        quantidade_de_trabalhos_com_avisos_fora_do_recorte = len(dic_falhas['Coleções'][colecao]['Avisos']['Fora do recorte']['Erro'])

        quantidade_total_de_trabalhos_analisados_dentro_do_recorte += quantidade_de_trabalhos_com_avisos_dentro_do_recorte
        quantidade_total_de_trabalhos_analisados_fora_do_recorte += quantidade_de_trabalhos_com_avisos_fora_do_recorte

        quantidade_total_de_trabalhos_site_analisados += dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs site"]
        quantidade_total_trabalhos_api += dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs dic"]
        quantidade_total_de_trabalhos_analisados += quantidade_de_trabalhos_analisados_dentro_do_recorte + quantidade_de_trabalhos_analisados_fora_do_recorte

        quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte += quantidade_de_trabalhos_com_avisos_dentro_do_recorte
        quantidade_total_de_trabalhos_com_avisos_fora_do_recorte += quantidade_de_trabalhos_com_avisos_fora_do_recorte
        quantidade_total_de_trabalhos_com_avisos_geral += quantidade_de_trabalhos_com_avisos_dentro_do_recorte + quantidade_de_trabalhos_com_avisos_fora_do_recorte

        quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte += quantidade_de_trabalhos_analisados_dentro_do_recorte - quantidade_de_trabalhos_com_avisos_dentro_do_recorte
        quantidade_total_de_trabalhos_com_texto_extraido_fora_do_recorte += quantidade_de_trabalhos_analisados_fora_do_recorte - quantidade_de_trabalhos_com_avisos_fora_do_recorte
        quantidade_total_de_trabalhos_com_texto_extraido_geral += (quantidade_de_trabalhos_analisados_dentro_do_recorte - quantidade_de_trabalhos_com_avisos_dentro_do_recorte) + (quantidade_de_trabalhos_analisados_fora_do_recorte - quantidade_de_trabalhos_com_avisos_fora_do_recorte)

        # quantidade_total_de_trabalhos_com_texto_extraido_geral += quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte + quantidade_total_de_trabalhos_com_texto_extraido_fora_do_recorte

    resposta_quantidades = (quantidade_total_de_colecoes_site,
                            quantidade_total_de_trabalhos_site,
                            quantidade_de_colecoes_analisadas,
                            quantidade_total_de_trabalhos_site_analisados,
                            quantidade_total_trabalhos_api,
                            quantidade_total_de_trabalhos_analisados,
                            quantidade_total_de_trabalhos_com_avisos_geral,
                            quantidade_total_de_trabalhos_com_texto_extraido_geral,
                            quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte,
                            quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
                            quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte,
                            quantidade_total_de_trabalhos_com_avisos_fora_do_recorte,
                            quantidade_total_de_trabalhos_analisados_fora_do_recorte,
                            quantidade_total_de_trabalhos_com_texto_extraido_fora_do_recorte)

    return resposta_quantidades

def gerarCapa() -> str:
    """
    Gera uma string, para compor a string geral do HTML, referente a capa do
    relatório.

    :param None: Não há parametros para esta função.
    :return: String HTML com as características da capa.
    """
    string_html = '''<h1>Relatório das etapas<br>Extração de Dados<br>WOKE - UFSC</h1>
        <br><br><br><br><br><br><br><br><br><br>
        <p style="text-align: center;">Desenvolvido por: Igor Caetano de Souza
        <br>Grupo de Estudos e Pesquisa em IA e História - UFSC</p>'''
    return string_html

def colorir(texto : str,
            cor_escolhida : str,
            tag_cor_verde : str = '<cor_verde>',
            tag_cor_vermelha : str = '<cor_vermelha>',
            tag_cor_laranja : str = '<cor_laranja>') -> str:
    """
    Colore o texto fornecido da cor escolhida, adicionando as tags do CSS referentes a
    a cor.

    :param texto: String do texto a ser colorido de verde.
    :param cor_escolhida: String referente uma das cores: verde, vermelho ou laranja.
    :param tag_cor_verde: String contendo a "tag" da cor verde desejada
    declarada no arquivo Style CSS.
    :param tag_cor_vermelha: String contendo a "tag" da cor vermelha desejada
    declarada no arquivo Style CSS.
    :param tag_cor_laranja: String contendo a "tag" da cor laranja desejada
    declarada no arquivo Style CSS.
    :return: String do texto fornecido com a tag de inicio e fim referente a cor
    escolhida embutida.
    """
    tag_inicio = tag_final = ''
    cor_escolhida = cor_escolhida.lower()
    if cor_escolhida in ['verde','esverdeada']:
        tag_inicio = tag_cor_verde
        tag_final = tag_cor_verde[0]+'/'+tag_cor_verde[1:]
    elif cor_escolhida in ['vermelha','vermelho']:
        tag_inicio = tag_cor_vermelha
        tag_final = tag_cor_vermelha[0]+'/'+tag_cor_vermelha[1:]
    elif cor_escolhida in ['laranja','alaranjado','alaranjada']:
        tag_inicio = tag_cor_laranja
        tag_final = tag_cor_laranja[0]+'/'+tag_cor_laranja[1:]
    string_html = tag_inicio+texto+tag_final
    return string_html

def GerarInicioDaStringHTMLParaTituloColecao(colecao : str) -> str:
    string_html = f'''
        <div>
        <hr class="linha-vermelha">
        <h2>{colecao}</h2>
        <hr class="linha-vermelha">
        '''
    return string_html

lista_de_erros_conhecidos = ['Ano encontrado na capa do PDF é menor que 2003',
                             'Link do PDF não foi identificado',
                             'Língua não é português',
                             'Não foi possível identificar o ano na capa do PDF',
                             'Problema ao fazer download do PDF']
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

    if erro_amostrado not in lista_de_erros_conhecidos:
      erro_amostrado = 'Erro desconhecido'

    return erro_amostrado

def inserirQuantidadesTotalDeErrosNaColecaoStringHTML(dic_colecao : dict,
                                                      dic_falhas_totais : dict) -> tuple[str, dict]:
    string_html = ''
    lista_bruta_de_erros = dic_colecao['Avisos']['Possivelmente dentro do recorte']["Erro"]+dic_colecao['Avisos']['Fora do recorte']["Erro"]

    lista_de_erros = sorted(list(set(lista_bruta_de_erros)))

    dic_erros_amostrados_contagem = {}

    for erro in lista_de_erros:
        erro_amostrado = exibirErrosAmostrados(erro=erro)
        # contagem_erro = dic_colecao["Erro"].count(erro)
        contagem_erro = lista_bruta_de_erros.count(erro)
        if erro_amostrado in dic_erros_amostrados_contagem.keys():
            dic_erros_amostrados_contagem[erro_amostrado] += contagem_erro
        else:
            dic_erros_amostrados_contagem[erro_amostrado] = contagem_erro
        if erro_amostrado not in list(dic_falhas_totais.keys()):
            dic_falhas_totais[erro_amostrado] = contagem_erro
        else:
            dic_falhas_totais[erro_amostrado] += contagem_erro

    for erro_amostrado in sorted(list(dic_erros_amostrados_contagem.keys())):
        string_html += f'''<h4>{erro_amostrado}: {dic_erros_amostrados_contagem[erro_amostrado]}</h4>'''

    return string_html,dic_falhas_totais

def inserirMetricasColecaoNaStringHTML(quantidade_total_trabalhos_analisados_colecao_geral : int,
                                       quantidade_total_trabalhos_com_avisos : int,
                                       texto_taxa_aproveitamento_colecao_geral : str,
                                       quantidade_total_de_trabalhos_analisados_dentro_do_recorte : int,
                                       quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte : int,
                                       texto_taxa_aproveitamento_colecao_dentro_do_recorte : str) -> str:

    string_html = f'''<ul><h3><li>Métricas desta coleção no geral:</li></h3></ul>
        <h4>Quantidade de trabalhos analisados: {quantidade_total_trabalhos_analisados_colecao_geral}</h4>
        <h4>Quantidade de trabalhos com avisos: {quantidade_total_trabalhos_com_avisos}</h4>
        <h4>Taxa de aproveitamento dos trabalhos analisados: {texto_taxa_aproveitamento_colecao_geral}</h4>
        <hr class="linha-cinza">
        <ul><h3><li>Métricas desta coleção <i>dentro</i> do nosso recorte:</li></h3></ul>
        <h4>Quantidade de trabalhos analisados: {quantidade_total_de_trabalhos_analisados_dentro_do_recorte}</h4>
        <h4>Quantidade de trabalhos com avisos: {quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte}</h4>
        <h4>Taxa de aproveitamento dos trabalhos analisados: {texto_taxa_aproveitamento_colecao_dentro_do_recorte}</h4>
        <hr class="linha-cinza">
        <ul><h3><li>Quantidade total de cada erro encontrado nesta coleção:</li></h3></ul>
        '''
    return string_html

def inserirObservacaoQuantidadesDiferentesColecaoNaStringHTML(n_publicacoes_site : int,
                                                              n_publicacoes_api : int):
    diferenca = n_publicacoes_site - n_publicacoes_api
    if diferenca > 1:
        trabs_negativos = colorir(texto=f'-{diferenca} trabalhos',cor_escolhida='vermelha')
    else:
        trabs_negativos = colorir(texto=f'-{diferenca} trabalho',cor_escolhida='vermelha')
    string_html = f'''
    <h4><i><b>Observação: Número de trabalhos retornados da API é menor que o número de trabalhos publicados no site do repositório: {n_publicacoes_site} / {n_publicacoes_api}  {trabs_negativos}</b></i></h4>
    '''
    return string_html

def gerarConteudoColecoes(dic_falhas : dict,
                          dic_falhas_totais : dict,
                          colecao : str) -> tuple[str, dict]:
    """
    Gera uma string, para compor a string geral do HTML, referente ao conteúdo de
    uma determinada coleção com base no seu dicionário de falhas e gera também um
    dicionário de falhas totais, o qual é atualizado e
    depois retornado.

    :param dic_falhas: Dicionário de falhas da coleção em questão.
    :param dic_falhas_totoais: Dicionário que está armazenando os avisos e suas
    quantidades totais considerando todas as coleções.
    :param colecao: Coleção que está sendo analisada as falhas.
    :return: Tupla contendo a string HTML da coleção em questão e o
    dicionário de falhas totais atualizado após passar pelas falhas presentes
    nesta mesma coleção.
    """
    string_html = ''
    dic_colecao_atual = dic_falhas['Coleções'][colecao]
    n_publicacoes_site = dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs site"]
    n_publicacoes_api = dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs dic"]

    quantidade_total_de_trabalhos_analisados_dentro_do_recorte = dic_colecao_atual["Número de trabalhos analisados"]['Possivelmente dentro do recorte']
    quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte = len(dic_colecao_atual['Avisos']['Possivelmente dentro do recorte']['Erro'])

    quantidade_total_trabalhos_analisados_colecao = quantidade_total_de_trabalhos_analisados_dentro_do_recorte + dic_colecao_atual["Número de trabalhos analisados"]['Fora do recorte']
    quantidade_total_trabalhos_com_avisos = quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte + len(dic_colecao_atual['Avisos']['Fora do recorte']['Erro'])
    quantidade_total_trabalhos_com_texto_extraido = quantidade_total_trabalhos_analisados_colecao - quantidade_total_trabalhos_com_avisos

    taxa_aproveitamento_colecao_geral = calcularTaxaAproveitamento(quantidade_total=quantidade_total_trabalhos_analisados_colecao,
                                                                    quantidade_obtida=quantidade_total_trabalhos_com_texto_extraido)

    texto_taxa_aproveitamento_colecao_geral = analisarTaxaDeAproveitamento(taxa_aproveitamento=taxa_aproveitamento_colecao_geral)

    quantidade_total_trabalhos_analisados_colecao_dentro_do_recorte = dic_colecao_atual["Número de trabalhos analisados"]['Possivelmente dentro do recorte']
    quantidade_total_trabalhos_com_texto_extraido_dentro_do_recorte = quantidade_total_trabalhos_analisados_colecao_dentro_do_recorte - len(dic_colecao_atual['Avisos']['Possivelmente dentro do recorte']['Erro'])

    taxa_aproveitamento_colecao_dentro_do_recorte = calcularTaxaAproveitamento(quantidade_total=quantidade_total_trabalhos_analisados_colecao_dentro_do_recorte,
                                                                                quantidade_obtida=quantidade_total_trabalhos_com_texto_extraido_dentro_do_recorte)

    texto_taxa_aproveitamento_colecao_dentro_do_recorte = analisarTaxaDeAproveitamento(taxa_aproveitamento=taxa_aproveitamento_colecao_dentro_do_recorte)

    if len(dic_colecao_atual['Avisos']['Possivelmente dentro do recorte']['Erro']) > 0 or len(dic_colecao_atual['Avisos']['Fora do recorte']['Erro']) > 0:
        string_html += GerarInicioDaStringHTMLParaTituloColecao(colecao)



        string_html += inserirMetricasColecaoNaStringHTML(quantidade_total_trabalhos_analisados_colecao_geral=quantidade_total_trabalhos_analisados_colecao,
                                                          quantidade_total_trabalhos_com_avisos=quantidade_total_trabalhos_com_avisos,
                                                          texto_taxa_aproveitamento_colecao_geral=texto_taxa_aproveitamento_colecao_geral,
                                                          quantidade_total_de_trabalhos_analisados_dentro_do_recorte=quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
                                                          quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte=quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte,
                                                          texto_taxa_aproveitamento_colecao_dentro_do_recorte=texto_taxa_aproveitamento_colecao_dentro_do_recorte)

        string_html_para_adicionar, dic_falhas_totais = inserirQuantidadesTotalDeErrosNaColecaoStringHTML(dic_colecao=dic_colecao_atual,
                                                                                                          dic_falhas_totais=dic_falhas_totais)
        string_html += string_html_para_adicionar

        if n_publicacoes_site > n_publicacoes_api:

            string_html += inserirObservacaoQuantidadesDiferentesColecaoNaStringHTML(n_publicacoes_site=n_publicacoes_site,
                                                                                     n_publicacoes_api=n_publicacoes_api)
        string_html += '</div>'

    elif n_publicacoes_site > n_publicacoes_api:
        string_html += GerarInicioDaStringHTMLParaTituloColecao(colecao)

        string_html += inserirMetricasColecaoNaStringHTML(quantidade_total_trabalhos_analisados_colecao_geral=quantidade_total_trabalhos_analisados_colecao,
                                                          quantidade_total_trabalhos_com_avisos=quantidade_total_trabalhos_com_avisos,
                                                          texto_taxa_aproveitamento_colecao_geral=texto_taxa_aproveitamento_colecao_geral,
                                                          quantidade_total_de_trabalhos_analisados_dentro_do_recorte=quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
                                                          quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte=quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte,
                                                          texto_taxa_aproveitamento_colecao_dentro_do_recorte=texto_taxa_aproveitamento_colecao_dentro_do_recorte)

        string_html += inserirObservacaoQuantidadesDiferentesColecaoNaStringHTML(n_publicacoes_site=n_publicacoes_site,
                                                                                     n_publicacoes_api=n_publicacoes_api)
        string_html += '</div>'

    return string_html, dic_falhas_totais

def analisarTaxaDeAproveitamento(taxa_aproveitamento : float) -> str:
    """
    Realiza a análise do valor da taxa de aproveitamento encontrada,
    a transformando numa string com a cor verde, caso seu valor seja maior ou
    igual a 90; laranja caso o valor esteja entre 75 e 89 e vermelha caso esteja
    abaixo de 75.

    :param taxa_aproveitamento: Float referente a taxa de aproveitamento
    calculada.
    :return: String contendo a taxa de aproveitamento, com vírgulas e "%", na
    cor mais adequada para seu valor.
    """
    string_taxa_aproveitamento = str(taxa_aproveitamento).replace('.',',')+'%'
    if taxa_aproveitamento >= 90:
        string_taxa_aproveitamento = colorir(texto=string_taxa_aproveitamento,cor_escolhida='verde')
    elif taxa_aproveitamento < 90 and taxa_aproveitamento >= 75:
        string_taxa_aproveitamento = colorir(texto=string_taxa_aproveitamento,cor_escolhida='laranja')
    else:
        string_taxa_aproveitamento = colorir(texto=string_taxa_aproveitamento,cor_escolhida='vermelha')
    return string_taxa_aproveitamento

def calcularTaxaAproveitamento(quantidade_total : int,
                               quantidade_obtida : int) -> float:
    dividendo = quantidade_obtida*100
    divisor = quantidade_total
    if divisor != 0:
      resultado = dividendo/divisor
    else:
      resultado = 0
    return round(resultado,2)

def gerarConteudoErrosTotais(dic_falhas_totais : dict) -> str:
    """
    Gera uma string, para compor a string geral do HTML, referente ao conteúdo
    da parte dos erros totais analisados considerando todas as coleções
    analisadas.

    :param dic_falhas_totais: Dicionário que contém as informações de todos os
    erros e a quantidade respectiva deles em todas as coleções analisadas.
    :return: String HTML referente ao conteúdo das falhas/avisos totais gerais.
    """
    string_html = '<ul><h4><li>Quantidade total de cada erro encontrado durante as execuções:</li></h4></ul>'
    for chave_erro in sorted(dic_falhas_totais.keys()):
        string_html += f'''
        <h5>{chave_erro}: {colorir(texto=str(dic_falhas_totais[chave_erro]),cor_escolhida='vermelha')}</h5>
        '''
    return string_html

def gerarConteudoDepoisDaCapa(quantidade_total_de_trabalhos_site_analisados : int,
                              quantidade_de_colecoes_analisadas : int,
                              quantidade_total_trabalhos_api : int,
                              quantidade_total_de_trabalhos_analisados : int,
                              quantidade_total_de_trabalhos_com_texto_extraido_geral : int,
                              quantidade_total_de_trabalhos_com_avisos_geral : int,
                              taxa_aproveitamento_geral : float,
                              quantidade_total_de_trabalhos_analisados_dentro_do_recorte : int,
                              quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte : int,
                              taxa_aproveitamento_dentro_do_recorteo : float,
                              conteudo_erros_totais : str,
                              quantidade_total_de_colecoes_site : int,
                              quantidade_total_de_trabalhos_site : int,
                              quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte : int,
                              quantidade_total_de_trabalhos_com_avisos_fora_do_recorte : int) -> str:
    """
    Gera uma string, para compor a string geral do HTML, referente ao conteúdo
    que será exibido depois da capa, ou seja, a primeira página do relatório.
    Este conteúdo abordará o resumo das principais quantidades a serem
    observadas.

    :param quantidade_total_de_trabalhos_site_analisados: Quantidade total de trabalhos no
    site do Repositório Institucional da UFSC para uma determinada coleção.
    :param quantidade_total_trabalhos_api: Quantidade total de trabalhos
    provenientes da comunicação com a API, de uma determinada coleção.
    :param quantidade_total_de_trabalhos_analisados: Quantidade total de
    trabalhos que o programa analisou.
    :param quantidade_total_de_trabalhos_com_texto_extraido_geral: Quantidade total de
    trabalhos que tiveram seus textos extraídos.
    :param quantidade_total_de_trabalhos_com_avisos_geral: Quantidade total de
    trabalhos que não tiveram seus textos extraídos, ou seja, tiveram algum
    aviso.
    :param taxa_aproveitamento: Taxa referente ao aproveitamento dos trabalhos
    que foram analisados com os trabalhos que, de fato, tiveram seus textos
    extraídos.
    :param conteudo_erros_totais: Quantidade total de erros somando todas os
    trabalhos de todas as coleções analisadas.
    :param quantidade_de_colecoes_analisadas: Quantidade total de coleções que o
    programa analisou.
    :return: String HTML com o conteúdo do resumo das principais quantidades.
    """

    taxa_aproveitamento_geral = calcularTaxaAproveitamento(quantidade_total = quantidade_total_de_trabalhos_analisados,
                                                           quantidade_obtida = quantidade_total_de_trabalhos_com_texto_extraido_geral)

    texto_taxa_aproveitamento_geral = analisarTaxaDeAproveitamento(taxa_aproveitamento=taxa_aproveitamento_geral)


    quantidade_total_de_trabalhos_analisados_dentro_do_recorte = quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte + quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte

    taxa_aproveitamento_dentro_do_recorte = calcularTaxaAproveitamento(quantidade_total = quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
                                                                       quantidade_obtida = quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte)

    texto_taxa_aproveitamento_dentro_do_recorte = analisarTaxaDeAproveitamento(taxa_aproveitamento=taxa_aproveitamento_dentro_do_recorte)

    string_html = f'''<div>
        <hr class="linha-vermelha">
        <h2>Resumo das etapas de Extração de Dados do Repositório Institucional da UFSC<h2>
        <hr class="linha-vermelha">
        <h4>Link referente à comunidade analisada:<br><a href="https://repositorio.ufsc.br/handle/123456789/74645" target="_blank">https://repositorio.ufsc.br/handle/123456789/74645</a></h4>
        <h4>Link referente à API utilizada (interface do Protocolo OAI-PMH):<br><a href="https://repositorio.ufsc.br/oai" target="_blank">https://repositorio.ufsc.br/oai</a></h4>
        <i>Formato dos metadados compartilhados: xoai</i>
        <hr class="linha-vermelha">
        <ul><h3><li>Quantidades totais no site do Repositório Institucional da UFSC</li></h3></ul>
        <h4>Quantidade total de coleções: {quantidade_total_de_colecoes_site}</h4>
        <h4>Quantidade total trabalhos na comunidade "Teses e Dissertações": {quantidade_total_de_trabalhos_site}</h4>
        <hr class="linha-vermelha"></div>
        <div>
        <ul><h3><li>Quantidades analisadas ao decorrer da extração</li></h3></ul>
        <h4>Quantidade de coleções: {quantidade_de_colecoes_analisadas}</h4>
        <h4>Quantidade de trabalhos: {quantidade_total_de_trabalhos_analisados}</h4>
        <h4>Quantidade total de trabalhos recebidos da API: {quantidade_total_trabalhos_api}</h4>
        <h4>Quantidade de trabalhos perdidos na comunicação com a API: {colorir(texto=str(quantidade_total_de_trabalhos_site-quantidade_total_trabalhos_api),cor_escolhida='vermelha')}</h4>
        <hr class="linha-vermelha">
        </div>
        <div>
        <ul><h3><li>Quantidades <i>gerais</i> referentes à extração</li></h3></ul>
        <h4>Quantidade total de trabalhos analisados: {quantidade_total_de_trabalhos_analisados}</h4>
        <h4>Quantidade total de trabalhos com texto extraído: {quantidade_total_de_trabalhos_com_texto_extraido_geral}</h4>
        <h4>Quantidade total de trabalhos que não tiveram seus textos extraídos: {colorir(texto=str(quantidade_total_de_trabalhos_com_avisos_geral),cor_escolhida='vermelha')}</h4>
        <h4>Taxa de aproveitamento dos textos de <b>todos</b> os trabalhos analisados: {texto_taxa_aproveitamento_geral}</h4>
        <ul><h3><li>Quantidades <i>dentro do nosso recorte</i> referentes à extração</li></h3></ul>
        <h4>Quantidade total de trabalhos com texto extraído: {quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte}</h4>
        <h4>Quantidade total de trabalhos que não tiveram seus textos extraídos: {colorir(texto=str(quantidade_total_de_trabalhos_analisados_dentro_do_recorte-quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte),cor_escolhida='vermelha')}</h4>
        <h4>Taxa de aproveitamento dos textos <b>dentro do nosso recorte</b>: {texto_taxa_aproveitamento_dentro_do_recorte}
        <h4>
        <hr class="linha-vermelha">
        </div>
        <div>
        {conteudo_erros_totais}
        <hr class="linha-vermelha">
        <br>
        </div>'''
    return string_html

def gerarConteudoColecoesBemSucedidas(dic_falhas: dict) -> str:
    """
    Gera uma string, para compor a string geral do HTML, referente ao conteúdo
    da parte das coleções que não tiveram erros/avisos ao decorrer das execuções
    dos programas das etapas de extração de dados.

    :param dic_falhas: Dicionário de falhas da coleção em questão.
    :return: String para ser concatenada a string geral do HTML.
    """
    string_conteudo_colecoes_bem_sucedidas = ''
    for colecao in dic_falhas['Coleções']:
        if len(dic_falhas['Coleções'][colecao]['Avisos']['Possivelmente dentro do recorte']['Erro']) == 0 and len(dic_falhas['Coleções'][colecao]['Avisos']['Fora do recorte']['Erro']) == 0 and dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs site"] == dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs dic"]:
            string_conteudo_colecoes_bem_sucedidas = '''<div class="quebra-de-pagina"></div>
                <div>
                <h2>Lista de coleções que não tiveram avisos ao decorrer das etapas de extração de dados</h2>
                <hr class="linha-vermelha">
                <br>
                <ul>'''
            break

    if string_conteudo_colecoes_bem_sucedidas != '':
        for colecao in dic_falhas['Coleções']:
            if len(dic_falhas['Coleções'][colecao]['Avisos']['Possivelmente dentro do recorte']['Erro']) == 0 and len(dic_falhas['Coleções'][colecao]['Avisos']['Fora do recorte']['Erro']) == 0 and dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs site"] == dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs dic"]:
                string_conteudo_colecoes_bem_sucedidas += f'<li><h4> {colecao} [{dic_falhas["Coleções"][colecao]["Número de publicações"]["N pubs dic"]}]</h4></li>'
        string_conteudo_colecoes_bem_sucedidas += '</ul></div>'
    else:
        string_conteudo_colecoes_bem_sucedidas = '''<div class="quebra-de-pagina"></div>
            <div>
            <hr class="linha-vermelha">
            <h2>Lista de coleções que não tiveram avisos ao decorrer das etapas de extração de dados</h2>
            <hr class="linha-vermelha">
            <br>
            <h4>Infelizmente não teve coleção que não foi gerado algum tipo de aviso/falha na hora da extração de metadados/texto PDF.'''
    return string_conteudo_colecoes_bem_sucedidas

def gerarHTML(titulo : str,
              quebra_de_linha_tamanho_da_imagem : str,
              capa : str,
              conteudo_depois_da_capa : str,
              conteudo_colecoes : str,
              conteudo_colecoes_bem_sucedidas: str) -> str:
    """
    Gera uma string que representa o conteúdo HTML que será passado para a
    geração do PDF, tendo como base as seguintes partes:
    - Imagem da capa
    - Conteúdo escrito da capa (título, nome do grupo e desenvolvedor)
    - Conteúdo da primeira página, após a capa (resumo das quantidades)
    - Conteúdo das coleções (avisos gerais)

    :param titulo: Título do arquivo PDF.
    :param style_css_src: Caminho até o arquivo CSS referente ao style do HTML
    para geração do PDF.
    :param imagem_src: Caminho até a imagem que será inserida na capa.
    :param quebra_de_linha_tamanho_da_imagem: String do conteúdo HTML referente
    as quebras de linha necessárias para não escrever o título do relatório
    abaixo da imagem na capa.
    :param capa: String do conteúdo HTML referente a capa.
    :param conteudo_depois_da_capa: String do conteúdo HTML referente a primeira
    página depois da capa.
    :param conteudo_colecoes: String do conteúdo HTML referente as coleções e
    seus respectivos avisos e quantidades de tais avisos.
    :return: String do template do conteúdo HTML completo para geração do
    relatório em PDF.
    """
    template_html = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        <link rel="stylesheet" href="{style_css_src}">
    </head>
    <body>
        <!-- Adiciona a imagem antes do título -->
        <img src="{imagem_src}" alt="Imagem de exemplo" style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 100%; height: auto;">
        {quebra_de_linha_tamanho_da_imagem}
        {capa}
        {conteudo_depois_da_capa}
        {conteudo_colecoes}
        {conteudo_colecoes_bem_sucedidas}
    </body>
    </html>
    """
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
        with open(caminho_arquivo_html, 'w') as f:
            f.write(template_html)
            f.close()
    except Exception as e:
        erro = f'{e.__class__.__name__}: {str(e)}'
        return False, erro
    else:
        return True, ''

def gerarRelatorioPDF(dic_falhas : dict) -> tuple[bool, str]:
    """
    Gera, de fato, o relatório em PDF com base num template de um documento HTML.

    :param dic_falhas: Dicionário de falhas de todas as coleções agrupadas num
    dicionário só.
    :param caminho_pasta_arquivos_geracao_relatorio_pdf: String referente ao
    caminho até a pasta com os arquivos para geração do PDF.
    :param style_css_src: Caminho até o arquivo CSS referente ao style do HTML
    para geração do PDF.
    :param imagem_src: Caminho até a imagem que será inserida na capa.
    :param caminho_pasta_relatorio_pdf: Caminho até a pasta que será salvo o
    arquivo do relatório em PDF.
    :param caminho_arquivo_relatorio_pdf: Caminho que será salvo o arquivo do
    relatório em PDF.
    :param caminho_arquivo_html: String referente ao caminho para salvar a string
    do template do conteúdo HTML completo.
    :param caminho_lista_colecoes_site: Caminho para o arquivo que contém as
    informações das coleções provenientes diretamente do site do RI da UFSC, na
    comunidade de Teses e Dissertações.
    """
    print('\nIniciando criação do relatório automatizado...\n')
    try:
        titulo = 'Relatório - Extração de Dados - WOKE - UFSC'

        quebra_de_linha_tamanho_da_imagem = gerarQuebraDeLinhasDoTamanhoDaImagem()

        capa = gerarCapa()



        (quantidade_total_de_colecoes_site,
         quantidade_total_de_trabalhos_site,
         quantidade_de_colecoes_analisadas,
         quantidade_total_de_trabalhos_site_analisados,
         quantidade_total_trabalhos_api,
         quantidade_total_de_trabalhos_analisados,
         quantidade_total_de_trabalhos_com_avisos_geral,
         quantidade_total_de_trabalhos_com_texto_extraido_geral,
         quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte,
         quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
         quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte,
         quantidade_total_de_trabalhos_com_avisos_fora_do_recorte,
         quantidade_total_de_trabalhos_analisados_fora_do_recorte,
         quantidade_total_de_trabalhos_com_texto_extraido_fora_do_recorte) = preencherQuantidadesRelatorioPDF(dic_falhas=dic_falhas)

        taxa_aproveitamento_geral = calcularTaxaAproveitamento(quantidade_total=quantidade_total_de_trabalhos_analisados,
                                                               quantidade_obtida=quantidade_total_de_trabalhos_com_texto_extraido_geral)

        taxa_aproveitamento_dentro_do_recorteo = calcularTaxaAproveitamento(quantidade_total=quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
                                                                            quantidade_obtida=quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte)

        conteudo_colecoes = ''

        dic_falhas_totais = {}

        for colecao in sorted(dic_falhas['Coleções'].keys()):
            conteudo_colecao, dic_falhas_totais = gerarConteudoColecoes(dic_falhas=dic_falhas, dic_falhas_totais=dic_falhas_totais, colecao=colecao)
            conteudo_colecoes += conteudo_colecao

        conteudo_erros_totais = gerarConteudoErrosTotais(dic_falhas_totais=dic_falhas_totais)

        conteudo_depois_da_capa = gerarConteudoDepoisDaCapa(quantidade_total_de_trabalhos_site_analisados=quantidade_total_de_trabalhos_site_analisados,
                                                            quantidade_de_colecoes_analisadas=quantidade_de_colecoes_analisadas,
                                                            quantidade_total_trabalhos_api=quantidade_total_trabalhos_api,
                                                            quantidade_total_de_trabalhos_analisados=quantidade_total_de_trabalhos_analisados,
                                                            quantidade_total_de_trabalhos_com_texto_extraido_geral=quantidade_total_de_trabalhos_com_texto_extraido_geral,
                                                            quantidade_total_de_trabalhos_com_avisos_geral=quantidade_total_de_trabalhos_com_avisos_geral,
                                                            taxa_aproveitamento_geral=taxa_aproveitamento_geral,
                                                            quantidade_total_de_trabalhos_analisados_dentro_do_recorte=quantidade_total_de_trabalhos_analisados_dentro_do_recorte,
                                                            quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte=quantidade_total_de_trabalhos_com_texto_extraido_dentro_do_recorte,
                                                            taxa_aproveitamento_dentro_do_recorteo=taxa_aproveitamento_dentro_do_recorteo,
                                                            conteudo_erros_totais=conteudo_erros_totais,
                                                            quantidade_total_de_colecoes_site=quantidade_total_de_colecoes_site,
                                                            quantidade_total_de_trabalhos_site=quantidade_total_de_trabalhos_site,
                                                            quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte=quantidade_total_de_trabalhos_com_avisos_dentro_do_recorte,
                                                            quantidade_total_de_trabalhos_com_avisos_fora_do_recorte=quantidade_total_de_trabalhos_com_avisos_fora_do_recorte)


        conteudo_colecoes_bem_sucedidas = gerarConteudoColecoesBemSucedidas(dic_falhas=dic_falhas)

        template_html = gerarHTML(titulo=titulo,
                                  quebra_de_linha_tamanho_da_imagem=quebra_de_linha_tamanho_da_imagem,
                                  capa=capa,
                                  conteudo_depois_da_capa=conteudo_depois_da_capa,
                                  conteudo_colecoes=conteudo_colecoes,
                                  conteudo_colecoes_bem_sucedidas=conteudo_colecoes_bem_sucedidas)

        status_geracao_HTML, msg_geracao_HTML = escreverDocHTML(caminho_arquivo_html=caminho_arquivo_html, template_html=template_html)

        if status_geracao_HTML:

            html = HTML(filename=caminho_arquivo_html)
            print("\nDocumento HTML gerado com sucesso!")

            pdf = html.write_pdf(caminho_arquivo_relatorio_pdf)
            print("\n\n\tRelatório PDF gerado com sucesso!\n")

            return True, ''
        else:
            return False, f'Problema ao gerar template_html em "gerarRelatorioPDF":\n{msg_geracao_HTML}'

    except Exception as e:
        erro = f'Erro "{e.__class__.__name__}": {str(e)}'
        return False, erro
