from .funcoes_planilha_metadados import gerarPlanilhaDeMetadados, caminho_pasta_planilhas, caminho_pasta_dicts
from .funcoes_relatorio_pdf import gerarDicionarioDeFalhas, gerarRelatorioPDF, os
from .funcoes_arquivos_txt_detalhados import gerarTxtAvisosDetalhadosCadaColecao

def main(escolha_relatorio_pdf : bool = True,
         escolha_arquivos_txt : bool = True,
         escolha_planilha_metadados : bool = True):
    """
    Função destinada a organizar as chamadas das funções referentes aos processos de 
    geração automatizada de relatório PDF, planilha de metadados e arquivos de textos 
    detalhados.

    Parâmetros:
    -----------
    - param escolha_planilha_metadados: Bool que decidirá se a execução do processo de 
    geração de planilha de metadados será executado (True) ou não (False).
    - param escolha_relatorio_pdf: Bool que decidirá se a execução do processo de 
    geração de relatório PDF será executado (True) ou não (False).
    - param escolha_arquivos_txt: Bool que decidirá se a execução do processo de 
    geração de arquivos de texto detalhados será executado (True) ou não (False).
    """

############# Planilha de Metadados #############
    
    if escolha_planilha_metadados:

        # caminho_pasta_dicts = r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Extração de Dados/via API DSpace Protocolo OAI-PMH/Etapa 1/Dicts'

        if os.path.exists(caminho_pasta_dicts):
            lista_de_dicionarios = [os.path.join(caminho_pasta_dicts,arquivo) for arquivo in sorted(os.listdir(caminho_pasta_dicts)) if arquivo.endswith('.joblib')]
            nome_da_planilha = 'Metadados_Colecoes_Automatizada_final.xlsx'
            status_geracao_planilha, msg_geracao_planilha = gerarPlanilhaDeMetadados(lista_de_dicionarios=lista_de_dicionarios,
                                                                                    caminho_pasta_planilhas=caminho_pasta_planilhas,
                                                                                    nome_da_planilha=nome_da_planilha)
            if status_geracao_planilha:
                print('\n\n\tPlanilha de Metadados gerada com sucesso!\n')
            else:
                print(f'\n\n\t! Problemas ao gerar planilha de metadados: {msg_geracao_planilha}')
        else:
            print(f'\n\n\t! Problemas ao gerar planilha de metadados: Pasta de dicts atualizados não encontrada... "{caminho_pasta_dicts}"')

############# Relatório PDF #############
            
    if escolha_relatorio_pdf:
        dic_falhas = gerarDicionarioDeFalhas()
        status_geracao_relatorio, msg_geracao_relatorio = gerarRelatorioPDF(dic_falhas=dic_falhas)

        if not status_geracao_relatorio:
            print('\n\n\t! Problema(s) ao gerar relatório PDF:', msg_geracao_relatorio)

############# Arquivos txt detalhados #############
            
    if escolha_arquivos_txt:
        gerarTxtAvisosDetalhadosCadaColecao()