# Repositório de códigos do Grupo de Estudos e Pesquisa em IA e História da UFSC

## 🎯 Objetivo do projeto
Treinar modelos de Word Embeddings com textos puramente acadêmicos, extraídos dos PDFs de trabalhos da comunidade de Teses e Dissertações do Repositório Institucional da Universidade Federal de Santa Catarina a fim de analisar conceitos, semântica e análise diacrônica destes mesmos.

## 📃 Etapas

## Extração de Dados
A primeira etapa foi desenvolver um conjunto de programas para a raspagem e armazenamento dos dados. Tendo isso em vista, criou-se uma sessão dedicada exclusivamente para os códigos e arquivos gerados nesta parte de extração de dados. *Vale destacar que alguns arquivos estão presentes somente no Google Drive do Grupo de Estudos, o qual está armazenando os textos extraídos e os metadados em formato de planilha. Como a quantidade de textos armazenados passa de 30.000, optou-se por deixá-los somente no Drive, sem cloná-los para o GitHub. Arquivos voltados para análise das etapas ficará disponível na pasta de "Resultados".*

## Pré-processamento dos textos extraídos
Feita a coleta dos textos, partiu-se para a etapa de pré-processamento dos mesmos, a qual consistiu-se em limpar, tokenizar e armazenar os textos pré-processados, prontos para alimentarem o treinamento.

## Treinamento
Depois de coletar e pré-processar os textos, está na hora de iniciar o treinamento. Optou-se por utilizar o método Word2Vec juntamente com um método de múltiplos treinamentos (treinos com alternância de parâmetros) analisando sempre o modelo que melhor performar diante de "perguntas" (analogias) e de similaridade de palavras com base na realidade.

## Visualização dos resultados
Em posse dos arquivos referentes aos modelos treinados, pode-se gerar diversas visualizações, tais como: mapa de calor, rede dinâmica de nuvem de palavras, gráficos mostrando as tendências de mudança semântica para uma determinada palavra comparada à outras demais, etc.

# 💻 Ambiente de execução dos programas

*Utilizamos o Google Colabolatory integrado ao Github como ambiente de programação, os códigos são escritos em Python utilizando diversas bibliotecas. 
Para gerenciamento de novas versões do código, utilizamos uma extensão para o Google Chrome chamada "Open in colab", dessa forma pode-se acessar as pastas e arquivos que se deseje, diretamente no Github e utilizar a extensão para abrir e alterar.*

*Em casos de novos notebooks, pode-se abrir diretamente o Google Colab e quando desejar salvar o documento, basta clicar no menu superior esquerdo em "Arquivo" e depois em "Salvar uma cópia no GitHub". Para isso é necessário ser colaborador do projeto, e os commits devem ser feitos a partir da conta pessoal do colaborador.*

# 🗂️ Sobre o repositório:

O repositório possue duas pastas centrais: uma voltada para os códigos utilizados nas etapas de Extração de Dados e outro voltado para o Processamento de Linguagem Natural proposto para pré-processamento, treinamento de modelos Word Embeddings e visualização de resultados.

# Sobre o Grupo

## Desenvolvedores:

### [Igor Caetano de Souza](https://github.com/IgorCaetano)
Programador que deu início aos códigos e permanece construindo e realizando a manutenção em todos os códigos de todas as etapas. Atualmente (2023-2024) atua como bolsista de iniciação científica do projeto voltado para a área da programação.

### [Davi Alves de Azevedo](https://github.com/daviaaze)
Programador que contribuiu na parte de extração de textos dos PDFs melhorando e otimizando os códigos já existentes.

### [Vinicius X. Tobias](https://github.com/vinixavi95)
Programador que contribuiu na abertura deste GitHub.

## Integrantes ativos

### [Rodrigo Bragio Bonaldo](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4209056A4&tokenCaptchar=03AFcWeA5mNySD1bB8-44suhAf6wXHaeJkZLMV9JEps8ckh-kMlHjaVCr9ZYjv8TvcZoYQS2ABv5aUfJuSXOeQ3PEC2JBuId5Lc6t273aYrHUV2huTHma6J8ggAlRP0skhZUVjc0x_zcS0aFxWDE5LUPrEh9jj6soDobbKK3EzICpMNoeBnG2PqyKDeY1O4WxcBW847pwZtjftElwnoIDtR-r8lP_AoskjyGjcC7BWckaGqhqi3wiBeQZTP0TiBqCaSe2sQyLo0gW0mzUldZ521R6liuHe1BhcjcYVnNeewyPRNXI1RfoQmvDvM69HjI6lf9RJxPNLsjwUuE1zlxwk68fs-_Vn3RMZ8yn4qSBqx6ZNvHd-J1cnaSQOP4nvWJmXP-FDfbwj2x01KZBL8tF1pOFnze8XgZjoe6BD0OyHVtxw8mfVbOt8mdiybYwLh5D-mQBPoB1zDWTcAQfHRzj08DxwA0ABgh59pbBzFC0gEJdPRG9Fsz43oDpvbQdsQDeLrrQt87na0Q2VHEHc-2zqYzLS8QdolZ20MyVXezQSFe9sn3rr6R6nMCCpoJ3GQoEbRasG8VHlMBn6NYllesESWCWivLNL-C6NxbJCv9BXOjSJ7yXSZB5f375iPgpjLJC4bU8nLPOEtlPb_qG4FTByU37P-PH_u_AmpWgdyAdUA0nHJWC5v6yTcnpgTtE9MJ6rmYAlkyds31ECdh2Ls9t4l4M0c947Tb-YJbwaOP74OxTX-BaMHs1vafI)
Coordenador e fundador do Grupo de Estudos e Pesquisa em IA e História da UFSC
### [Franciele Dias da Silva](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K1168805H4&tokenCaptchar=03AFcWeA5PIVEVcrplocdHcP5Il2xMEv-IW0yrvQfttwawBmiFRUjEhpsycGqQok3VU7egWtXpWX-i1cdxKz41gNtTZcq3Sb6_L_ZXzoIfPxH4BJ5VzgFAUIIyUvZqehmbqLXt_7yfrboIJR1FpP6qi2KFLuHJz_X0zj7pOnU5AEL3WIeoKayoMcgl7QRi0_93b92bksPOGrE-cczFjmfoOj3fB7ng3bO5IqJQOSN7V5iKjA1pSLnhJ49eGBXx4HXPaEl2kRTYc-_VTCqy4a2mRG_qimEbPv7-EXb9KXNMBEqFq9xAOw1nrRKPliKXu0WPW6141GITIiZw7sREjquDiYb8MPEma_0_JHxP9cfgqyBQjekgSxSWC5j3jtDFYF0f5XIZMpD1iCx0FcjapZ8iONysOxrhxI_BA2W0JMPI_RbqnDiX1DGyZ99B2sC6WUUAIITcqpvKPOJBidA9I2qjiG9l9wsNxbT-3x7iWtM2I5PSqIs5nJDaPqZVKcIatROltmn-nP2EpPfK5eTh0zieEuTMYjM8_IC9jpvcb564jT3bRMHSnpCWVKlKMd28tJrhssQgO6ELMG-Rp2qfcJ7XGB7Arqo2NLdyYSF-C9jB5P6sPeWR8VRIWUiGIjjYhoEeok8xsJ-a0v2jbLEYnUEy_znMAhnQ17VHu10DWSVmyDeHDNc_hNi3oOKhC-Oa0mTqfNBIQF6i92I15CFlR23aYO2ipEk3HhGXh9G6y4jjBr9D-rnog8xNtTYSzhJj_hSEZ7bqxUaZT6kp)
Bolsista de iniciação científica do projeto voltada para o processamento de linguagem natural aplicado à história
### Mateus Borsatti
### Carlos
### Eric
### Almir
### Sara
### Jader

## Integrantes inativos
### Ana
### Ícaro
### Matheus
