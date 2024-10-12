import os

from heuristics.heuristics import Heuristics

"""
Maiko Ademir Nunes 30-09-2024
Este será o arquivo principal que importa e utiliza as funções das heurísticas.
"""


class PDFConverter(Heuristics):
    def __init__(self, pdf_folder):
        super().__init__(pdf_folder)
        self.pdf_folder = pdf_folder
        os.makedirs(self.pdf_folder, exist_ok=True)

    def convert_pdf_to_txt(self):
        """
        Converte todos os arquivos PDF em uma pasta para arquivos de texto.

        Args:
            pdf_folder (str): Caminho para a pasta contendo arquivos PDF.
        """
        for filename in os.listdir(self.pdf_folder):
            if filename.endswith('.pdf'):
                try:
                    pdf_path = os.path.join(pdf_folder, filename)
                    text = self.extract_text_from_pdf(pdf_path)
                    charset = self.detect_charset(text)
                    txt_filename = filename.replace('.pdf', '.txt')
                    txt_path = os.path.join(pdf_folder, txt_filename)
                    with open(txt_path, 'w', encoding=charset) as txt_file:
                        txt_file.write(text)
                    print(f"Converted {filename} to {txt_filename} with charset {charset}")
                except Exception as e:
                    print(f"Error converting {filename}: {e}")


if __name__ == "__main__":
    pdf_folder = 'pdf_folder'
    converter = PDFConverter(pdf_folder)
    converter.convert_pdf_to_txt()
