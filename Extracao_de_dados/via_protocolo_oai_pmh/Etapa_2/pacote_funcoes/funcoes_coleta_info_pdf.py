import re
import fitz
try:
    from funcoes_auxiliares import validarDicTextoExtraido, padronizarTextoDoBloco
except ImportError as e:
    from .funcoes_auxiliares import validarDicTextoExtraido, padronizarTextoDoBloco

def procurarPaginaDosAgradecimentos(texto_bloco_analisado : str):
    if 'agradecimentos' in texto_bloco_analisado[:(len('agradecimentos')+1)]:
        return True
    return False

def procurarPaginaDoResumo(texto_bloco_analisado : str):
    if 'resumo' in texto_bloco_analisado[:(len('resumo')+1)]:
        return True
    return False

def procurarPaginaDasListas(texto_bloco_analisado : str):
    texto_bloco_analisado_formatado = texto_bloco_analisado.replace('listas','lista')
    if 'lista de figura' in texto_bloco_analisado_formatado[:(len('lista de figuras')+1)] or 'lista de quadro' in texto_bloco_analisado_formatado[:(len('lista de quadros')+1)] or 'lista de gráfico' in texto_bloco_analisado_formatado[:(len('lista de gráficos')+1)] or 'lista de tabela' in texto_bloco_analisado_formatado[:(len('lista de tabelas')+1)] or 'lista de abreviatura' in texto_bloco_analisado_formatado[:(len('lista de abreviaturas')+1)] or 'lista de símbolo' in texto_bloco_analisado_formatado[:(len('lista de símbolos')+1)] or 'lista de sigla' in texto_bloco_analisado_formatado[:(len('lista de siglas')+1)] or 'lista de equaç' in texto_bloco_analisado_formatado[:(len('lista de equações')+1)] or 'lista de ilustra' in texto_bloco_analisado_formatado[:(len('lista de ilustrações')+1)] or 'lista de anexo' in texto_bloco_analisado_formatado[:(len('lista de anexos')+1)]:
        return True
    return False

def procurarPaginaDoSumario(texto_bloco_analisado : str):
    if 'sumário' in texto_bloco_analisado[:(len('sumário')+1)]:
        return True
    return False

def procurarPaginaDaIntroducao(texto_bloco_analisado : str):
    if 'introdução' in texto_bloco_analisado[:(len('introdução')+1)]:
        return True
    return False

def encontrarPrimeiraPaginaPrimaria(dicionario_de_posicoes : dict):
    pagina_inicial_1 = 0
    if dicionario_de_posicoes['agradecimentos'] and dicionario_de_posicoes['resumo']:
      if dicionario_de_posicoes['agradecimentos'] < dicionario_de_posicoes['resumo']:
        pagina_inicial_1 = dicionario_de_posicoes['agradecimentos']
      else:
        pagina_inicial_1 = dicionario_de_posicoes['resumo']
    elif dicionario_de_posicoes['agradecimentos']:
        pagina_inicial_1 = dicionario_de_posicoes['agradecimentos']
    elif dicionario_de_posicoes['resumo']:
        pagina_inicial_1 = dicionario_de_posicoes['resumo']

    return pagina_inicial_1

def encontrarUltimaPaginaPrimaria(dicionario_de_posicoes : dict, quantidade_de_paginas : int):
    pagina_final_1 = quantidade_de_paginas
    if dicionario_de_posicoes['lista de x'] and dicionario_de_posicoes['sumario']:
        if dicionario_de_posicoes['lista de x'] < dicionario_de_posicoes['sumario']:
            pagina_final_1 = dicionario_de_posicoes['lista de x']
        else:
            pagina_final_1 = dicionario_de_posicoes['sumario']

    elif dicionario_de_posicoes['lista de x']:
        pagina_final_1 = dicionario_de_posicoes['lista de x']

    elif dicionario_de_posicoes['sumario']:
        pagina_final_1 = dicionario_de_posicoes['sumario']

    return pagina_final_1

def encontrarPrimeiraPaginaSecundaria(dicionario_de_posicoes : dict,pagina_final_1 : int):
    pagina_inicial_2 = pagina_final_1
    if dicionario_de_posicoes['resumo'] and dicionario_de_posicoes['lista de x'] and dicionario_de_posicoes['sumario']:
        if dicionario_de_posicoes['resumo'] > dicionario_de_posicoes['lista de x'] and dicionario_de_posicoes['resumo'] > dicionario_de_posicoes['sumario']:
            pagina_inicial_2 = dicionario_de_posicoes['resumo']
        elif dicionario_de_posicoes['introducao']:
            pagina_inicial_2 = dicionario_de_posicoes['introducao']

    elif dicionario_de_posicoes['introducao']:
        pagina_inicial_2 = dicionario_de_posicoes['introducao']

    return pagina_inicial_2

def listarPaginasParaExtrairTextoPDF(caminho_do_pdf : str,
                                     string_dos_caracteres_especiais : str = '''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''):
    lista_de_paginas_para_extrair_texto = []
    dic_posicoes = {'agradecimentos':None,'resumo':None,'lista de x':None,'sumario':None,'introducao':None}
    try:
        doc = fitz.open(caminho_do_pdf)

        for i in range(len(doc)):
            page = doc[i]

            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:
                texto_bloco = ''
                for l in b["lines"]:
                    texto_linha = ''
                    for s in l["spans"]:
                        texto_linha += s['text']
                    texto_bloco += str(texto_linha).strip()

                if texto_bloco.strip() != '' and len(texto_bloco.strip()) > 3:
                    texto_bloco_analisado = padronizarTextoDoBloco(texto_bloco=texto_bloco,string_dos_caracteres_especiais=string_dos_caracteres_especiais)

                    if not dic_posicoes['agradecimentos']:
                        if procurarPaginaDosAgradecimentos(texto_bloco_analisado=texto_bloco_analisado):
                            dic_posicoes['agradecimentos'] = i
                    if not dic_posicoes['resumo']:
                        if procurarPaginaDoResumo(texto_bloco_analisado=texto_bloco_analisado):
                            dic_posicoes['resumo'] = i
                    if not dic_posicoes['lista de x']:
                        if procurarPaginaDasListas(texto_bloco_analisado=texto_bloco_analisado):
                            dic_posicoes['lista de x'] = i
                    if not dic_posicoes['sumario']:
                        if procurarPaginaDoSumario(texto_bloco_analisado=texto_bloco_analisado):
                            dic_posicoes['sumario'] = i
                    if not dic_posicoes['introducao']:
                        if procurarPaginaDaIntroducao(texto_bloco_analisado=texto_bloco_analisado):
                            dic_posicoes['introducao'] = i
                    break

        quantidade_de_paginas_doc = len(doc)

        doc.close()

        pagina_inicial_1 = encontrarPrimeiraPaginaPrimaria(dicionario_de_posicoes=dic_posicoes)

        pagina_final_1 = encontrarUltimaPaginaPrimaria(dicionario_de_posicoes=dic_posicoes,quantidade_de_paginas=quantidade_de_paginas_doc)

        pagina_inicial_2 = encontrarPrimeiraPaginaSecundaria(dicionario_de_posicoes=dic_posicoes,pagina_final_1=pagina_final_1)

        pagina_final_2 = quantidade_de_paginas_doc

        if pagina_inicial_1 != 0 and pagina_inicial_2 != 0 and pagina_final_1 != quantidade_de_paginas_doc-1:
            lista_de_paginas_1 = list(range(pagina_inicial_1,pagina_final_1))
            lista_de_paginas_2 = list(range(pagina_inicial_2,pagina_final_2))
            lista_de_paginas_para_extrair_texto = lista_de_paginas_1+lista_de_paginas_2
            lista_de_paginas_para_extrair_texto = list(set(lista_de_paginas_para_extrair_texto))
        else:
            lista_de_paginas_para_extrair_texto = list(range(len(doc)))

        return lista_de_paginas_para_extrair_texto
    except Exception as e:
        return []

def encontrarDataPubNaPagina(texto_pagina : str):
    ano_capa = None
    # correspondencias = re.compile(r'\d{4}').findall(texto_pagina)
    correspondencias = re.compile(r'\b\d{4}\b').findall(texto_pagina)
    if correspondencias:
        correspondencia_data = correspondencias[-1]
        if int(correspondencia_data) > 1900 and int(correspondencia_data) < 2030:
          ano_capa = correspondencia_data
    return ano_capa

def encontrarDataPubNaPaginaDeOutraForma(pagina):
    texto_total_pagina = pagina.get_text()
    if texto_total_pagina:
        texto_para_analise = texto_total_pagina.lower().replace(',','').replace('.','').replace('(sc)','').replace('sc','').replace('santa catarina','').replace(' de','').replace('-','').replace('–','').replace('/','').replace('brasil','').replace('br','')
        correspondencias_data_publicacao = re.findall(r'\n\nflorianópolis\s+\b\d{4}\b|\s{4}\nflorianópolis\s+\b\d{4}\b|\n\nararanguá\s+\b\d{4}\b|\s{4}\nararanguá\s+\b\d{4}\b|\n\nblumenau\s+\b\d{4}\b|\s{4}\nblumenau\s+\b\d{4}\b|\n\ncuritibanos\s+\b\d{4}\b|\s{4}\ncuritibanos\s+\b\d{4}\b|\n\njoinville\s+\b\d{4}\b|\s{4}\njoinville\s+\b\d{4}\b', texto_para_analise)
        if correspondencias_data_publicacao:
            resultado_processamento_data_de_outra_forma = correspondencias_data_publicacao[-1].replace('\n','').strip()
            return encontrarDataPubNaPagina(texto_pagina=resultado_processamento_data_de_outra_forma)
    return False

def encontrarDataPubNoPDF(caminho_pdf : str):
    try:
        doc = fitz.open(caminho_pdf)
        for i in range(0,3):
            page = doc[i]
            texto_extraido = page.get_text('dict')
            if validarDicTextoExtraido(dic_texto_extraido=texto_extraido):
                resultado_processamento_data = processaBlocos(text_page=texto_extraido)
                if resultado_processamento_data:
                    return True, int(resultado_processamento_data), ''
                else:
                    resultado_processamento_data_de_outra_forma = encontrarDataPubNaPaginaDeOutraForma(pagina=page)
                    if resultado_processamento_data_de_outra_forma:
                        return True, int(resultado_processamento_data_de_outra_forma), ''
            # else:
            #     return False, 0, 'Formato de dicionário extraído da página INVÁLIDO.'
        doc.close()
    except Exception as e:
        erro = f'Erro "{e.__class__.__name__}": {str(e)}'
        return False, 0, erro
    return False, 0 , 'Não foi possível identificar o ano na capa do PDF'
    # return False, 0

def processaBlocos(text_page : dict):
    texto_da_pagina = []
    for b in text_page['blocks']:
        if isinstance(b,dict):
          if 'lines' in b.keys():
            texto_bloco = ''
            for l in b['lines']:
                if isinstance(l,dict):
                  if 'spans' in l.keys():
                    texto_linha = ''
                    for s in l['spans']:
                        texto_linha += s['text']
                    if texto_linha.strip() != '':
                        # texto_bloco += texto_linha
                        texto_bloco += texto_linha.strip() + ' '
            if texto_bloco.strip() != '':
                texto_da_pagina.append(texto_bloco)

    if len(texto_da_pagina) > 0:
        possivel_texto_com_data = ''
        if len(texto_da_pagina) > 1:
            # ultimo_texto = texto_da_pagina[-1]
            ultimo_texto = texto_da_pagina[-1].lower().replace('(sc)','').replace('sc','').replace('santa catarina','').replace(' de','').replace('-','').replace('–','').replace('/','').replace('brasil','').replace('br','')
            if 'florianópolis' in ultimo_texto:
                if len(ultimo_texto) < len('Florianópolis, fevereiro de 2003'):
                    ultimo_texto = texto_da_pagina[-2] + texto_da_pagina[-1]
            elif 'araranguá' in ultimo_texto:
                if len(ultimo_texto) < len('Araranguá, fevereiro de 2003'):
                    ultimo_texto = texto_da_pagina[-2] + texto_da_pagina[-1]
            elif 'blumenau' in ultimo_texto:
                if len(ultimo_texto) < len('Blumenau, fevereiro de 2003'):
                    ultimo_texto = texto_da_pagina[-2] + texto_da_pagina[-1]
            elif 'curitibanos' in ultimo_texto:
                if len(ultimo_texto) < len('Curitibanos, fevereiro de 2003'):
                    ultimo_texto = texto_da_pagina[-2] + texto_da_pagina[-1]
            elif 'joinville' in ultimo_texto:
                if len(ultimo_texto) < len('Joinville, fevereiro de 2003'):
                    ultimo_texto = texto_da_pagina[-2] + texto_da_pagina[-1]
            possivel_texto_com_data = ultimo_texto
        else: # len(texto_da_pagina) == 1 (só um bloco de texto)
            texto_para_analise = texto_da_pagina[0].lower().replace('(sc)','').replace('sc','').replace('santa catarina','').replace(' de','').replace('-','').replace('–','').replace('/','').replace('brasil','').replace('br','')
            if 'florianópolis' in texto_para_analise[len(texto_para_analise)-len('Florianópolis, fevereiro de 2003'):]:
                possivel_texto_com_data = texto_para_analise[len(texto_para_analise)-len('Florianópolis, fevereiro de 2003'):]
            elif 'araranguá' in texto_para_analise[len(texto_para_analise)-len('Araranguá, fevereiro de 2003'):]:
                possivel_texto_com_data = texto_para_analise[len(texto_para_analise)-len('Araranguá, fevereiro de 2003'):]
            elif 'blumenau' in texto_para_analise[len(texto_para_analise)-len('Blumenau, fevereiro de 2003'):]:
                possivel_texto_com_data = texto_para_analise[len(texto_para_analise)-len('Blumenau, fevereiro de 2003'):]
            elif 'curitibanos' in texto_para_analise[len(texto_para_analise)-len('Curitibanos, fevereiro de 2003'):]:
                possivel_texto_com_data = texto_para_analise[len(texto_para_analise)-len('Curitibanos, fevereiro de 2003'):]
            elif 'joinville' in texto_para_analise[len(texto_para_analise)-len('Joinville, fevereiro de 2003'):]:
                possivel_texto_com_data = texto_para_analise[len(texto_para_analise)-len('Joinville, fevereiro de 2003'):]

        if possivel_texto_com_data != '':
            resultado_analise = encontrarDataPubNaPagina(possivel_texto_com_data)
            if resultado_analise:
                return resultado_analise
            else:
                return False
        else:
            return False
    else:
        return False
    