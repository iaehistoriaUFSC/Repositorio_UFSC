import pdfplumber  # Importa a biblioteca pdfplumber, que é usada para manipular arquivos PDF.

"""
Maiko Ademir Nunes 30-09-2024
Este arquivo contém a função para verificar se um PDF é digitalizado.
"""

def is_scanned_pdf(pdf_path):
    """
    Verifica se um PDF é digitalizado.

    Args:
        pdf_path (str): Caminho para o arquivo PDF.

    Returns:
        bool: True se o PDF for digitalizado, False caso contrário.
    """
    with pdfplumber.open(pdf_path) as pdf:  # Abre o arquivo PDF especificado pelo caminho usando pdfplumber.
        for page in pdf.pages:  # Itera por todas as páginas do PDF.
            if page.images:  # what is happening if the page has an image in the header?
                # what if the image contains a graph as an image
                # the problem are the books that are scanned
                # the problem is not the image itself
                return True  # Se a página contém imagens, retorna True indicando que o PDF é digitalizado.
            if page.extract_text():  # Tenta extrair texto da página.
                return False  # Se conseguir extrair texto, retorna False indicando que o PDF não é digitalizado.


    return True  # Se nenhuma página contém texto e todas têm imagens, retorna True indicando que o PDF é digitalizado.
