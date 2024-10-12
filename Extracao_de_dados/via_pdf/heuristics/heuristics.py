import chardet
import pdfplumber


class Heuristics:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_from_pdf(self, pdf_path):
        """
        Extrai texto de um arquivo PDF.

        Args:
            pdf_path (str): Caminho para o arquivo PDF.

        Returns:
            str: Texto extraído do PDF.
        """
        text = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    lines = page_text.split('\n')
                    formatted_lines = []
                    for line in lines:
                        if self._is_title(line):
                            formatted_lines.append('\n\n' + line + '\n\n')
                        else:
                            formatted_lines.append(line)
                    page_text = ' '.join(formatted_lines)

                    page_text = page_text.replace('\n\n', '<PARAGRAPH>').replace('\n', ' ').replace('<PARAGRAPH>',
                                                                                                    '\n\n')
                    text += page_text + '\n\n'
        return text.strip()

    def _is_title(self, line):
        """
        Verifica se uma linha é um título.

        Args:
            line (str): Linha de texto.

        Returns:
            bool: True se a linha for um título, False caso contrário.
        """
        return line.isupper() and len(line.split()) < 10

    def detect_charset(self, text):
        """
        Detecta a codificação de um texto.
    
        Args:
            text (str): Texto para detectar a codificação.
    
        Returns:
            str: Codificação detectada.
        """
        result = chardet.detect(text.encode())
        return result['encoding']
