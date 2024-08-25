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

### Igor Caetano de Souza *[(Perfil GitHub)](https://github.com/IgorCaetano)*
Estudante de graduação em Engenharia de Controle e Automação e programador que deu início à parte técnica do projeto WOKE (2023-2024) desenvolvendo códigos para todas as etapas de extração de dados, limpeza e pré-processamento, armazenamento, treinamento de modelos Word2Vec e visualização de dados. Além da construção, também realizou a manutenção e documentação dos códigos de todas essas etapas. Atuou em 2023.2 - 2024.2 como bolsista de iniciação científica do projeto voltado para a área da programação, mas também participava ativamente das discussões nas reuniões do grupo de estudos.

### Davi Alves de Azevedo *[(Perfil GitHub)](https://github.com/daviaaze)*
Estudante de graduação em História e programador que contribuiu na parte de extração de textos dos PDFs, melhorando e otimizando os códigos existentes.

### Vinicius X. Tobias *[(Perfil GitHub)](https://github.com/vinixavi95)*
Estudante de graduação em Ciência da Computação e programador que contribuiu na abertura deste GitHub.

## Integrantes ativos

### Rodrigo Bragio Bonaldo *[(Currículo Lattes)](http://lattes.cnpq.br/2967207698672476)*
Coordenador e fundador do Grupo de Estudos e Pesquisa em IA e História da UFSC.

### Franciele Dias da Silva *[(Currículo Lattes)](http://lattes.cnpq.br/8272002719032465)*
Estudante de graduação em História e bolsista de iniciação científica do projeto voltada para o processamento de linguagem natural aplicado à história. Desde o início, participou ativamente em discussões literárias sobre Processamento de Linguagem Natural (PLN), História e Inteligência Artificial, além de ter contribuído nas discussões e validações de todas as etapas do desenvolvimento dos modelos WOKE.

### Mateus Freitas Borsatti *[(Currículo Lattes)](https://lattes.cnpq.br/1731957464761445)*
Estudante de graduação em História e um dos membros mais ativos desde a criação do grupo, contribuiu na idealização do projeto WOKE, assim como nas discussões e nas validações referentes ao desenvolvimento de todas as etapas. Além disso será o autor do primeiro estudo utilizando o WOKE como ferramenta historiográfica.

### Éric Gabriel Kundlatsch *[(Currículo Lattes)](http://lattes.cnpq.br/3926071140042328)*

### Carlos

### Almir

### Sara

### Jader
Engenheiro de Controle e Automação que auxiliou em diversas tomadas de decisões no desenvolvimento do projeto na área de Processamento de Linguagem Natural, fornecendo diversos insights importantes do contexto da matemática envolvida na construção dos modelos Word Embbedings. Além disso, participa ativamente com opiniões construtivas e bem embasadas nas discussões das reuniões do grupo de estudos.

## Integrantes inativos
### Ana

### Ícaro

### Matheus

