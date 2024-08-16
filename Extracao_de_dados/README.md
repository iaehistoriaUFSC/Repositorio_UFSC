# Extração de Dados - Projeto WOKE

Inicialmente, planejamos a extração de dados do site do Repositório Institucional da UFSC usando técnicas de Web Scraping. Porém, depois de conversar com o TI responsável pelo servidor que hospeda o site do RI, este nos comunicou que preferia que utilizássemos o Protocolo OAI-PMH para extrair os metadados diretamente do DSpace (software que armazena os dados do RI da UFSC).

Tendo isso em vista, acabamos desenvolvendo códigos de raspagem via Web Scraping, mas descontinuamos o processo por este meio. Atualmente a extração foi feita via Protocolo OAI-PMH, seguindo as boas práticas que o TI solicitou.

Ao longo da extração os arquivos de informações dos metadados e os textos extraídos dos trabalhos foram salvos em pastas do Google Drive. Desta forma os membros do grupo de estudos puderam contribuir para validar o processo e verificar a eficiência do método utilizado.

Ao final foi gerado uma [Planilha de Metadados](https://docs.google.com/spreadsheets/d/1YqitjS2qVczIYMwx9JtEsM0No3Cg_46EXObhiOGpiEI/edit?usp=sharing) organizados e um [Relatório em PDF](https://drive.google.com/file/d/132hHPHH3xQ4E_iAHeNkc1a7aNlhWT1JP/view?usp=sharing) com o desempenho da extração.

## Desenvolvedores

- [Igor Caetano de Souza](https://github.com/IgorCaetano): Todos os processos
- [Davi Alves de Azevedo](https://github.com/daviaaze): Melhoria na extração de texto de arquivo PDF.
