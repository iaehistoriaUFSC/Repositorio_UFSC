import os
import string

def criarDiretorioAuxiliar(caminho : str) -> None:
    if os.path.isfile(caminho):
        caminho = os.path.dirname(caminho)
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

if 'Etapa_2' not in diretorio_atual:
    diretorio_atual = criarDiretorioAuxiliar(os.path.join(diretorio_atual,'Etapa_2'))


minutos_para_limpar_lixeira = 5

string_dos_caracteres_especiais = string.punctuation

# caminho_pasta_dicts = caminho_pasta_dicts_atualizados = caminho_pasta_dicts_falhas = caminho_pasta_colecoes = string_dos_caracteres_especiais = lista_nomes_das_colecoes_para_este_programa = None

# if os.path.exists(os.path.join(os.path.dirname(diretorio_atual),'Etapa_1','Dicts')):
#   caminho_pasta_dicts = os.path.join(os.path.dirname(diretorio_atual),'Etapa_1','Dicts')
# else:
#   print('Problema ao buscar variável caminho_pasta_dicts\nDiretório não existe.')

# if os.path.exists(os.path.join(os.path.dirname(diretorio_atual),'Etapa_2','Dicts_atualizados')):
#   caminho_pasta_dicts_atualizados = os.path.join(os.path.dirname(diretorio_atual),'Etapa_2','Dicts atualizados')
# else:
#   print('Problema ao buscar variável caminho_pasta_dicts_atualizados\nDiretório não existe.')

# if os.path.exists(os.path.join(diretorio_atual,'Dicionário de Falhas')):
#   caminho_pasta_dicts_falhas = os.path.join(diretorio_atual,'Dicionário de Falhas')
# else:
#   print('Problema ao buscar variável caminho_pasta_dicts_falhas\nDiretório não existe.')

# if os.path.exists(os.path.join(os.path.dirname(diretorio_atual),'Resultados','Coleções')):
#   caminho_pasta_colecoes = os.path.join(os.path.dirname(diretorio_atual),'Resultados','Coleções')
# else:
#   print('Problema ao buscar variável caminho_pasta_colecoes\nDiretório não existe.')

# # if os.path.exists(r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Lista de caracteres especiais.joblib'):
# #   lista_de_caracteres_especiais = joblib.load(r'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Lista de caracteres especiais.joblib')
# #   string_dos_caracteres_especiais = ''.join(lista_de_caracteres_especiais)
# # else:
# #   print('Problema ao buscar variável lista_de_caracteres_especiais\nDiretório não existe.')
# string_dos_caracteres_especiais = string.punctuation

# if os.path.exists(os.path.join(diretorio_atual,'Dicionário de Execuções','dic_listagem_execs.joblib')):
#   if n_programa == 1 and n_dia == 4: ##### Só para testes ou correções ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
#     lista_nomes_das_colecoes_para_este_programa = ['Programa de Pós-Graduação em Ecossistemas Agrícolas e Naturais',
#                                                    'Programa de Pós-Graduação em Energia e Sustentabilidade',
#                                                    'Programa de Pós-Graduação em Direito (Mestrado Profissional)']
#     ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
#   else:
#     dic_listagem_execs = joblib.load(os.path.join(diretorio_atual,'Dicionário de Execuções','dic_listagem_execs.joblib'))
#     lista_nomes_das_colecoes_para_este_programa = dic_listagem_execs[f'Dia {n_dia}'][f'Programa {n_programa}'][1]
# else:
#   print('Problema ao buscar variável dic_listagem_execs\nDiretório não existe.')

# if caminho_pasta_dicts and caminho_pasta_dicts_atualizados and caminho_pasta_dicts_falhas and caminho_pasta_colecoes and string_dos_caracteres_especiais and lista_nomes_das_colecoes_para_este_programa:
#   print('\n\tVariáveis fixas carregadas com sucesso!\n')
# else:
#   print('\n\t--> Notifique um programador do Grupo de Estudos.')


caminho_pasta_execs = os.path.join(diretorio_atual,'Execs')


caminho_dicts_falhas = os.path.join(diretorio_atual,'Dicionário de Falhas')

