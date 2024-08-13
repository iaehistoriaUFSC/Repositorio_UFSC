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

### [Rodrigo Bragio Bonaldo](http://lattes.cnpq.br/2967207698672476)
Coordenador e fundador do Grupo de Estudos e Pesquisa em IA e História da UFSC.

### [Franciele Dias da Silva](http://lattes.cnpq.br/8272002719032465)
Bolsista de iniciação científica do projeto voltada para o processamento de linguagem natural aplicado à história. Contribuiu nas discussões e nas validações referentes ao desenvolvimento de todas as etapas dos programas do WOKE.

### [Mateus Freitas Borsatti](https://lattes.cnpq.br/1731957464761445)
Um dos membros mais ativos desde a criação do grupo, contribuiu na idealização do projeto WOKE, assim como nas discussões e nas validações referentes ao desenvolvimento de todas as etapas. Além disso será o autor do primeiro estudo utilizando o WOKE como ferramenta historiográfica.

### [Éric Gabriel Kundlatsch](http://lattes.cnpq.br/3926071140042328)

### Carlos

### Almir

### Sara

### Jader

## Integrantes inativos
### Ana

### Ícaro

### Matheus

