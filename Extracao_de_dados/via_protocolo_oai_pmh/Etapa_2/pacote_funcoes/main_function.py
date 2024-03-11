import joblib, time, os
from typing import Any
try:
  from funcoes_auxiliares import criarGeradorDicts, formatarNomeArquivoColecao, encontrarAnoTrabalhoNosMetadados, printarAdicionandoProblemaNumTxt, limparLixeira, excluirPDF, encontrarAnoTrabalhoNosMetadados, baixarPDF, criarDiretorio
  from funcoes_extracao_texto import extrairTextoDoPDF, armazenarTextoExtraidoDoPDF
  from variaveis_utilizadas import diretorio_atual, caminho_pasta_execs, caminho_dicts_falhas, minutos_para_limpar_lixeira, string_dos_caracteres_especiais
except ImportError as e:
  from .funcoes_auxiliares import criarGeradorDicts, formatarNomeArquivoColecao, encontrarAnoTrabalhoNosMetadados, printarAdicionandoProblemaNumTxt, limparLixeira, excluirPDF, encontrarAnoTrabalhoNosMetadados, baixarPDF, criarDiretorio
  from .funcoes_extracao_texto import extrairTextoDoPDF, armazenarTextoExtraidoDoPDF
  from .variaveis_utilizadas import diretorio_atual, caminho_pasta_execs, caminho_dicts_falhas, minutos_para_limpar_lixeira, string_dos_caracteres_especiais


def main(n_programa : int,
         n_dia : int,
         drive_service : Any | None = None): # drive_service : Any | None = None
  

  start = time.time()

  caminho_pasta_dicts = caminho_pasta_dicts_atualizados = caminho_pasta_dicts_falhas = caminho_pasta_colecoes = lista_nomes_das_colecoes_para_este_programa = None

  if os.path.exists(os.path.join(os.path.dirname(diretorio_atual),'Etapa_1','Dicts')):
    caminho_pasta_dicts = os.path.join(os.path.dirname(diretorio_atual),'Etapa_1','Dicts')
  else:
    print('Problema ao buscar variável caminho_pasta_dicts\nDiretório não existe.')

  if not os.path.exists(os.path.join(diretorio_atual,'Dicts atualizados')):
    criarDiretorio(os.path.join(diretorio_atual,'Dicts atualizados'))
    # print('Problema ao buscar variável caminho_pasta_dicts_atualizados\nDiretório não existe.')
  caminho_pasta_dicts_atualizados = os.path.join(diretorio_atual,'Dicts atualizados')

  if not os.path.exists(os.path.join(diretorio_atual,'Dicionário de Falhas')):
    criarDiretorio(os.path.join(diretorio_atual,'Dicionário de Falhas'))
    # print('Problema ao buscar variável caminho_pasta_dicts_falhas\nDiretório não existe.')
  caminho_pasta_dicts_falhas = os.path.join(diretorio_atual,'Dicionário de Falhas')

  if os.path.exists(os.path.join(os.path.dirname(diretorio_atual),'Resultados','Coleções')):
    caminho_pasta_colecoes = os.path.join(os.path.dirname(diretorio_atual),'Resultados','Coleções')
  else:
    print('Problema ao buscar variável caminho_pasta_colecoes\nDiretório não existe.')

  if os.path.exists(os.path.join(os.path.dirname(diretorio_atual),'Etapa_1_2','Dicionário de Execuções','dic_listagem_execs.joblib')):
    if n_programa == 1 and n_dia == 4: ##### Só para testes ou correções ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
      lista_nomes_das_colecoes_para_este_programa = ['Programa de Pós-Graduação em Ecossistemas Agrícolas e Naturais',
                                                    'Programa de Pós-Graduação em Energia e Sustentabilidade',
                                                    'Programa de Pós-Graduação em Direito (Mestrado Profissional)']
      ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
    else:
      dic_listagem_execs = joblib.load(os.path.join(os.path.dirname(diretorio_atual),'Etapa_1_2','Dicionário de Execuções','dic_listagem_execs.joblib'))
      lista_nomes_das_colecoes_para_este_programa = dic_listagem_execs[f'Dia {n_dia}'][f'Programa {n_programa}'][1]
  else:
    print('Problema ao buscar variável dic_listagem_execs\nDiretório não existe.')

  if not (caminho_pasta_dicts and caminho_pasta_dicts_atualizados and caminho_pasta_dicts_falhas and caminho_pasta_colecoes and string_dos_caracteres_especiais and lista_nomes_das_colecoes_para_este_programa):
    print('\n\t--> Notifique um programador do Grupo de Estudos.')
  else:
    print('\n\tVariáveis fixas carregadas com sucesso!\n')
    

    lista_de_colecoes = joblib.load(os.path.join(os.path.dirname(diretorio_atual),'Etapa_1','Lista_de_colecoes','lista_de_colecoes.joblib'))

    lista_colecoes_para_este_programa = [formatarNomeArquivoColecao(nome_da_colecao) for nome_da_colecao in lista_nomes_das_colecoes_para_este_programa]

    lista_de_caminhos_dicts = [os.path.join(caminho_pasta_dicts,arquivo) for arquivo in os.listdir(caminho_pasta_dicts) if arquivo.replace('.joblib','') in lista_colecoes_para_este_programa]

    lista_geradores_dicts = criarGeradorDicts(lista_de_caminhos_dicionarios=lista_de_caminhos_dicts)

    caminho_pasta_exec = os.path.join(caminho_pasta_execs,f'Dia {str(n_dia)}')
    if not os.path.exists(caminho_pasta_exec):
      criarDiretorio(caminho_pasta_exec)

    txt_exec = ''

    if lista_de_caminhos_dicts and lista_de_colecoes:

      dic_falhas = {'Coleções':{}}

      # tamanho_total_lixeira = 0

      txt_exec += '\nColeções e quantidades de trabalhos analisados:\n\n'

      contagem_passagem_colecoes = 0

      for gerador_dic_colecao in lista_geradores_dicts:
        nome_colecao_dic = gerador_dic_colecao[0]

        qtd_total_de_colecoes_na_exec = len(lista_colecoes_para_este_programa)
        # contagem_passagem_colecoes = 0

        for colecao in lista_de_colecoes:
          nome_colecao_site = formatarNomeArquivoColecao(nome_colecao=colecao[0])
          # if nome_colecao_site.endswith(nome_colecao_dic):        #     Problema que gerou 2 coleções duplicadas no dic de falhas (Engenharia Química e Educação Física, pois tem curso de Química e Física com finais iguais, além de Enfermagem)
          if nome_colecao_site == nome_colecao_dic:
            txt_exec_colecao_atual = f'{str(colecao[0])}: '
            contagem_passagem_colecoes += 1
            numero_publicacoes_site = colecao[2]
            dic_colecao = gerador_dic_colecao[1]
            numero_publicacoes_dic = len(dic_colecao['Link página'])
            print('\n\n'+'*'*100)
            print('Coleção atual:',nome_colecao_site)
            print('Contagem:',contagem_passagem_colecoes,'de',qtd_total_de_colecoes_na_exec)

            # indice = 0
            if os.path.exists(os.path.join(caminho_pasta_dicts_atualizados,f'{nome_colecao_dic}.joblib')):
              print('Achei dict atualizado')
              dic_colecao_atualizado = joblib.load(os.path.join(caminho_pasta_dicts_atualizados,f'{nome_colecao_dic}.joblib'))
              dic_colecao_atualizado_encontrado = True
            else:
              dic_colecao_atualizado_encontrado = False
              print('Não achei dic_atualizado, começando um do zero')
              dic_colecao_atualizado = {'Título':[],'Autor':[],'Resumo':[],'Descrição':[],'Assuntos':[],'Língua':[],'Tipo':[],'Ano repositório':[],'Ano descrição':[],'Ano capa':[],'Link página':[],'Link PDF':[],'Texto extraído?':[]}
              for chave in dic_colecao.keys():
                dic_colecao_atualizado[chave] = dic_colecao[chave]        #[0:35] LIMITAR PARA TESTE #############################################################################################

              # Neste momento, falta preencher as chaves de "Ano capa" e "Texto extraído?" no dic_colecao_atualizado, que será feito na sequência...

            if os.path.exists(os.path.join(caminho_pasta_dicts_falhas,f'dic_falhas_programa_{n_programa}_dia_{n_dia}.joblib')):
              print('Achei dic de falhas para esse programa e dia!')
              dic_falhas = joblib.load(os.path.join(caminho_pasta_dicts_falhas,f'dic_falhas_programa_{n_programa}_dia_{n_dia}.joblib'))
            else:
              dic_falhas['Coleções'][colecao[0]] = {'Avisos':{'Possivelmente dentro do recorte':{'Trabalho':[], 'Erro':[], 'Link para o trabalho':[]},
                                                              'Fora do recorte':{'Trabalho':[], 'Erro':[], 'Link para o trabalho':[]}},
                                                    'Número de publicações':{},
                                                    'Número de trabalhos analisados':{'Possivelmente dentro do recorte':0,'Fora do recorte':0}}

            caminho_pasta_colecao = os.path.join(caminho_pasta_colecoes,nome_colecao_dic)

            if not os.path.exists(caminho_pasta_colecao):
              if criarDiretorio(caminho_pasta_colecao):
                print('\nDiretório da coleção:',caminho_pasta_colecao,'criado com sucesso.')
                pasta_colecao = True
              else:
                pasta_colecao = False
            else:
              pasta_colecao = True

            if pasta_colecao:
              cronometro_1min_inicio = time.time()

              qtd_trabalhos_analisados_colecao = 0

              qtd_trabalhos_encontrados_colecao = len(dic_colecao_atualizado['Link PDF'])

              for i in range(qtd_trabalhos_encontrados_colecao):
                link_pdf = dic_colecao['Link PDF'][i]

                if dic_colecao_atualizado_encontrado and link_pdf in dic_colecao_atualizado['Link PDF']:
                  pass
                else:
                  if colecao[0] not in dic_falhas['Coleções'].keys():
                    # dic_falhas['Coleções'][colecao[0]] = {'Trabalho':[],'Erro':[],'Link para o trabalho':[],'Número de publicações':{},'Número de trabalhos analisados':0}
                    dic_falhas['Coleções'][colecao[0]] = {'Avisos':{'Possivelmente dentro do recorte':{'Trabalho':[], 'Erro':[], 'Link para o trabalho':[]},
                                                                    'Fora do recorte':{'Trabalho':[], 'Erro':[], 'Link para o trabalho':[]}},
                                                          'Número de publicações':{},
                                                          'Número de trabalhos analisados':{'Possivelmente dentro do recorte':0,'Fora do recorte':0}}

                  # dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados'] += 1
                  # dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados'] = {'Possivelmente dentro do recorte':0,'Fora do recorte':0}

                  print('\n'+'-'*100)
                  print(f'Trabalho {i+1} de {qtd_trabalhos_encontrados_colecao}...')

                  qtd_trabalhos_analisados_colecao += 1
                  lingua_pdf = dic_colecao['Língua'][i]

                  ano_capa = 'N.I.'
                  resultado_texto_extraido = '-'
                  if link_pdf.strip() != 'N.I.':
                    if lingua_pdf.lower().strip() in ['por','pt','pt_br','br','por_br','português','portugues']:

                      caminho_arquivo_pdf_temporario = os.path.join(caminho_pasta_colecao,f'PDF_temporario_{i+1}_{n_programa}.pdf')

                      status_download_PDF, msg_download = baixarPDF(link_pdf=link_pdf,caminho_do_pdf=caminho_arquivo_pdf_temporario)
                      if status_download_PDF:
                        print(f'\nPDF temporário do Trabalho {i+1} da coleção {nome_colecao_dic} criado com sucesso.')

                        status_extracao_texto_pdf, texto_principal, notas_de_rodape, ano_capa = extrairTextoDoPDF(caminho_pdf=caminho_arquivo_pdf_temporario,string_dos_caracteres_especiais=string_dos_caracteres_especiais)
                        if status_extracao_texto_pdf:
                          print('Extração do texto concluída com sucesso.')
                          pasta_ano = False
                          if not os.path.exists(os.path.join(caminho_pasta_colecao,str(ano_capa))):
                            if criarDiretorio(os.path.join(caminho_pasta_colecao,str(ano_capa))):
                              pasta_ano = True
                          else:
                            pasta_ano = True

                          if pasta_ano:

                            caminho_pasta_trabalho = os.path.join(caminho_pasta_colecao,str(ano_capa),f'Trabalho {i+1}')

                            if criarDiretorio(caminho_pasta_trabalho):
                              print(f'\nDiretório do trabalho {i+1}:',caminho_pasta_trabalho,'criado com sucesso.')

                              caminho_arquivo_texto_extraido = os.path.join(caminho_pasta_trabalho,'texto_principal.txt')
                              status_armazenamento_texto_principal, msg_armazenamento_txt_principal = armazenarTextoExtraidoDoPDF(caminho_arquivo_txt=caminho_arquivo_texto_extraido,texto_extraido=texto_principal)
                              if status_armazenamento_texto_principal:
                                print('Texto principal extraído e armazenado com sucessso.')
                                resultado_texto_extraido = 'SIM'
                                dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados']['Possivelmente dentro do recorte'] += 1

                              else:
                                print('\n!Problema ao armazenar texto principal.')
                                print(msg_armazenamento_txt_principal)

                              caminho_arquivo_notas_de_rodape_extraida = os.path.join(caminho_pasta_trabalho,'notas_de_rodape.txt')
                              status_armazenamento_texto_principal, msg_armazenamento_notas_rodape = armazenarTextoExtraidoDoPDF(caminho_arquivo_txt=caminho_arquivo_notas_de_rodape_extraida,texto_extraido=notas_de_rodape)
                              if status_armazenamento_texto_principal:
                                print('Notas de rodapé extraídas e armazenadas com sucessso.')
                              else:
                                print('\n!Problema ao armazenar notas de rodapé.')
                                print(msg_armazenamento_notas_rodape)
                          else:
                            print('\n! Problema ao criar pasta do ano da capa.')


                        else:
                          print(f'\n! O texto do PDF não foi extraído: {texto_principal}.')
                          resultado_texto_extraido = 'NÃO'
                          chave_ano = encontrarAnoTrabalhoNosMetadados(ano_capa=str(ano_capa),ano_repositorio=dic_colecao['Ano repositório'][i],lingua=lingua_pdf)
                          dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Trabalho'].append(i+1)
                          dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Erro'].append(texto_principal)
                          dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Link para o trabalho'].append(dic_colecao['Link página'][i])
                          dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados'][chave_ano] += 1

                        tamanho_arquivo_pdf_temp = os.path.getsize(caminho_arquivo_pdf_temporario)

                        status_exclusao_PDF, msg_exclusao = excluirPDF(caminho_do_pdf=caminho_arquivo_pdf_temporario)
                        if status_exclusao_PDF:
                          print('\nPDF temporário excluído com sucesso.')
                          # tamanho_total_lixeira += tamanho_arquivo_pdf_temp

                        else:
                          print('\n! Erro ao excluir arquivo PDF temporário.')
                          print(msg_exclusao)
                          print('\n! Tentando excluir arquivo PDF temporário novamente...')
                          try:
                            os.remove(caminho_arquivo_pdf_temporario)
                            print('\nPDF temporário excluído com sucesso.')
                            # tamanho_total_lixeira += tamanho_arquivo_pdf_temp
                          except Exception as e:
                            print(f'\n! Erro ao tentar excluir usando os.remove() pela terceira vez: "{e.__class__.__name__}": {str(e)}')
                        cronometro_1min_fim = time.time()
                        if cronometro_1min_fim - cronometro_1min_inicio >= 60*minutos_para_limpar_lixeira and n_programa in [1,4]:
                            cronometro_1min_inicio = time.time()
                        # if tamanho_total_lixeira > 800000000 and n_programa in [1,4]: # Se a lixeira estiver com mais de 800MB
                            msg_limpar_lixeira = limparLixeira(drive_service=drive_service)
                            print(msg_limpar_lixeira)
                            # tamanho_total_lixeira = 0


                      else:
                        resultado_texto_extraido = 'NÃO'
                        string_problema = f'Problema ao fazer download do PDF com link: {link_pdf}.\nColeção: {nome_colecao_site}\nTrabalho: {i}\n{msg_download}'
                        printarAdicionandoProblemaNumTxt(string_problema=string_problema,caminho_pasta_execs_etapa_2=caminho_pasta_exec,n_programa=n_programa)
                        resultado_texto_extraido = 'NÃO'
                        chave_ano = encontrarAnoTrabalhoNosMetadados(ano_capa=str(ano_capa),ano_repositorio=dic_colecao['Ano repositório'][i],lingua=lingua_pdf)
                        dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Trabalho'].append(i+1)
                        dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Erro'].append('Problema ao fazer download do PDF')
                        dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Link para o trabalho'].append(dic_colecao['Link página'][i])
                        dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados'][chave_ano] += 1

                    else:
                      print('\n! Língua identificada não é português...')
                      resultado_texto_extraido = 'NÃO'
                      # chave_ano = encontrarAnoTrabalhoNosMetadados(ano_capa=str(ano_capa),ano_repositorio=dic_colecao['Ano repositório'][i],lingua=lingua_pdf)
                      chave_ano = 'Fora do recorte'
                      dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Trabalho'].append(i+1)
                      dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Erro'].append('Língua não é português')
                      dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Link para o trabalho'].append(dic_colecao['Link página'][i])
                      dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados'][chave_ano] += 1

                  else:
                    resultado_texto_extraido = 'NÃO'
                    chave_ano = encontrarAnoTrabalhoNosMetadados(ano_capa=str(ano_capa),ano_repositorio=dic_colecao['Ano repositório'][i],lingua=lingua_pdf)
                    dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Trabalho'].append(i+1)
                    dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Erro'].append('Link do PDF não foi identificado')
                    dic_falhas['Coleções'][colecao[0]]['Avisos'][chave_ano]['Link para o trabalho'].append(dic_colecao['Link página'][i])
                    dic_falhas['Coleções'][colecao[0]]['Número de trabalhos analisados'][chave_ano] += 1

                  dic_colecao_atualizado['Ano capa'].append(ano_capa)
                  dic_colecao_atualizado['Texto extraído?'].append(resultado_texto_extraido)
                  dic_falhas['Coleções'][colecao[0]]['Número de publicações'] = {'N pubs site':numero_publicacoes_site,'N pubs dic':numero_publicacoes_dic}

                  joblib.dump(dic_colecao_atualizado,os.path.join(caminho_pasta_dicts_atualizados,f'{nome_colecao_dic}.joblib'))
                  # joblib.dump(dic_falhas,f'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Extração de Dados/via API DSpace Protocolo OAI-PMH/Etapa 2/Dicionário de Falhas/dic_falhas_programa_{n_programa}_dia_{n_dia}.joblib')
                  joblib.dump(dic_falhas,os.path.join(caminho_dicts_falhas,f'dic_falhas_programa_{n_programa}_dia_{n_dia}.joblib'))

              txt_exec_colecao_atual += str(qtd_trabalhos_analisados_colecao)+'\n'
              txt_exec += txt_exec_colecao_atual

    end = time.time()

    duracao_exec = round((end-start),2)

    string_duracao = str(duracao_exec).replace('.',',')

    string_fim_da_execucao = f'\n\n\tDuração da execução: {string_duracao} segundos.\n\n'

    txt_exec += string_fim_da_execucao
    print(string_fim_da_execucao)

    caminho_arquivo_fim_de_exec = os.path.join(caminho_pasta_exec,f'Execucao {str(n_programa)}.txt')

    with open(caminho_arquivo_fim_de_exec,'w',encoding='utf-8') as f:
      f.write(f'Fim da exec. {n_programa}.\n\n{txt_exec}')
      f.close()

    if n_programa in [1,4]:
      print(f'\n\nIniciando temporizador para limpar lixeira de {minutos_para_limpar_lixeira} em {minutos_para_limpar_lixeira} minuto(s) enquanto os outros programa não terminam...')
      print('\t\t\t\t...')
      # lista_arquivos_fim_de_exec = os.listdir(f'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Extração de Dados/via API DSpace Protocolo OAI-PMH/Etapa 2/Execs/Dia {n_dia}')
      lista_arquivos_fim_de_exec = os.listdir(caminho_pasta_exec)
      if n_programa == 1:
        qtd_limpeza_lixeira = 0
        while not ('Execucao 1.txt' in lista_arquivos_fim_de_exec and 'Execucao 2.txt' in lista_arquivos_fim_de_exec and 'Execucao 3.txt' in lista_arquivos_fim_de_exec):
          msg_limpar_lixeira = limparLixeira(drive_service=drive_service)
          qtd_limpeza_lixeira += 1
          print(qtd_limpeza_lixeira, msg_limpar_lixeira)
          print('-'*100)
          time.sleep(60)
          # lista_arquivos_fim_de_exec = os.listdir(f'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Extração de Dados/via API DSpace Protocolo OAI-PMH/Etapa 2/Execs/Dia {n_dia}')
          lista_arquivos_fim_de_exec = os.listdir(caminho_pasta_exec)

      elif n_programa == 4:
        qtd_limpeza_lixeira = 0
        while not ('Execucao 4.txt' in lista_arquivos_fim_de_exec and 'Execucao 5.txt' in lista_arquivos_fim_de_exec and 'Execucao 6.txt' in lista_arquivos_fim_de_exec):
          msg_limpar_lixeira = limparLixeira(drive_service=drive_service)
          qtd_limpeza_lixeira += 1
          print(qtd_limpeza_lixeira, msg_limpar_lixeira)
          print('-'*100)
          time.sleep(60)
          # lista_arquivos_fim_de_exec = os.listdir(f'/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Extração de Dados/via API DSpace Protocolo OAI-PMH/Etapa 2/Execs/Dia {n_dia}')
          lista_arquivos_fim_de_exec = os.listdir(caminho_pasta_exec)

      print('\n\n\tRestante das execuções finalizadas!\n\n')