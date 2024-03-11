import re
import fitz
try:
    from funcoes_coleta_info_pdf import listarPaginasParaExtrairTextoPDF, encontrarDataPubNoPDF
except ImportError as e:
    from .funcoes_coleta_info_pdf import listarPaginasParaExtrairTextoPDF, encontrarDataPubNoPDF

def extrairTextoPDF(caminho_arquivo_pdf : str, lista_de_paginas_para_extrair_texto : list):
    try:
        doc = fitz.open(caminho_arquivo_pdf)
        texto_principal, notas_de_rodape = process_document(doc=doc,lista_de_paginas_para_extracao=lista_de_paginas_para_extrair_texto)
        # doc.save(f'{doc.name.split(".pdf")[0]}_annotaded.pdf')
        doc.close()
        return True, str(texto_principal), str(notas_de_rodape)
    except Exception as e:
        descricao_erro = f"{e.__class__.__name__}: {str(e)}"
        return False, descricao_erro, None

def process_document(doc, lista_de_paginas_para_extracao : list):
    texto_principal = ''
    notas_de_rodape = '\nNotas de rodapé:\n'
    if lista_de_paginas_para_extracao:
        lista_de_paginas_para_extracao_de_texto = lista_de_paginas_para_extracao
    else:
        lista_de_paginas_para_extracao_de_texto = list(range(len(doc)))

    for numero_pagina in lista_de_paginas_para_extracao_de_texto:
        texto_normal, texto_rodape = process_page(doc[numero_pagina])
        texto_principal += ' '.join(texto_normal).strip() + ' '
        notas_de_rodape += ' '.join(texto_rodape).strip() + ' '
    return extrai_texto(texto_principal), extrai_texto(notas_de_rodape)

def process_page(page):
    blocks = page.get_text("dict", flags=11)["blocks"]
    texto_normal = []
    texto_rodape = []
    for block in blocks:
        for line in block['lines']:
            for span in line['spans']:
                if is_texto_normal(span, block):
                    texto_normal.append(str(span['text']).strip())
                    # page.add_underline_annot(fitz.Rect(span['bbox']))
                elif is_texto_rodape(span, block):
                    texto_rodape.append(str(span['text']).strip())
                    # page.add_highlight_annot(fitz.Rect(span['bbox']))
    return texto_normal, texto_rodape

def is_texto_normal(span, block):
    return ((span['size'] >= 10.5 or (span['size'] >= 9.3 and block['bbox'][0] > 150)) and
            (len(span['text'].strip()) >= 3 or len(re.findall(r'[0-9][0-9]|[0-9]', span['text'].strip()[:2])) <= 0) and
            span['text'].strip() != '')

def is_texto_rodape(span, block):
    return (span['size'] < 10.5 and block['bbox'][0] < 150 and
            (len(span['text'].strip()) >= 3 or len(re.findall(r'[0-9][0-9]|[0-9]', span['text'].strip()[:2])) <= 0) and
            span['text'].strip() != '' and span['size'] > 7.5)

def extrai_texto(texto_extraido: str):
    return texto_extraido.encode('utf-8',errors='ignore').decode('utf-8')




def extrairTextoDoPDF(caminho_pdf : str,
                      string_dos_caracteres_especiais : str = '''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''):
  status_data_encontrada_pdf, ano_encontrado_capa, conteudo_msg_erro = encontrarDataPubNoPDF(caminho_pdf=caminho_pdf)
  if status_data_encontrada_pdf:
    ano_capa = ano_encontrado_capa
    if ano_capa > 2002:
      lista_de_paginas = listarPaginasParaExtrairTextoPDF(caminho_do_pdf=caminho_pdf,string_dos_caracteres_especiais=string_dos_caracteres_especiais)

      status_extracao_texto_pdf, texto_principal, notas_de_rodape = extrairTextoPDF(caminho_arquivo_pdf=caminho_pdf,lista_de_paginas_para_extrair_texto=lista_de_paginas)
      if status_extracao_texto_pdf:
        return True, texto_principal, notas_de_rodape, ano_capa
      else:
        return False, texto_principal, '', ano_capa
    else:
      return False, 'Ano encontrado na capa do PDF é menor que 2003', '', ano_capa
  else:
    return False, conteudo_msg_erro, '', 'N.I.'


def armazenarTextoExtraidoDoPDF(caminho_arquivo_txt : str, texto_extraido : str):
  try:
    with open(caminho_arquivo_txt,'w',encoding='utf-8') as f:
      f.write(texto_extraido)
      f.close()
    return True, ''
  except Exception as e:
    erro = f'Erro "{e.__class__.__name__}": {str(e)}'
    return False, erro