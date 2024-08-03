# Pré-processamento WOKE UFSC

## Objetivo

Esta etapa tem como objetivo pré-processar os textos extraídos dos trabalhos podendo ser com o reconhecimento de entidades no texto (e posterior tokenização destas entidades) e sem reconhecimento de entidades no texto (tokenizando palavra por palavra). Ambas possuem a remoção de stopwords e a lematização de verbos implementadas. Esta etapa criará um corpus de textos pré-processados que ao invés de arquivos txt terá arquivos msgpack os quais estarão armazenando os tokens pré-processados. Além disso foi estipulado que tokens devem ter ao menos 2 letras e que as frases devem possuir ao menos 5 palavras para entrar para o corpus pré-processado. 

Geralmente costuma-se pré-processar na etapa de treinamento dos modelos, mas como estamos querendo sempre otimizar os tempos de execução e explorar ao máximo cada etapa dos processos de construção de modelos Word Embeddings, optamos por construir um corpus de textos pré-processados que será, posteriormente, usado para treinar os modelos. Desta forma não será necessário pré-processar texto por texto antes de alimentá-lo no treinamento, bastará alimentar com o conteúdo do seu arquivo do texto já pré-processados.

Para otimizar o tempo e integrar mais os membros do Grupo de Estudos e Pesquisa em IA e História da UFSC foi projetado execuções "paralelas" para se pré-processar o máximo de textos num mesmo período de tempo. Desta forma, estruturou-se o código de execução do pré-processamento pensando em separar e organizar os trabalhos entre os programas que estiverem executando o pré-processamento. Para mais informações detalhadas sobre este processo, por favor leia as células de texto e os comentários presentes no arquivo de notebook *[Programa_Oficial_FINAL_de_Pre_processamento_WOKE_UFSC.ipynb](https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Pre_processamento/Programa_Oficial_FINAL_de_Pre_processamento_WOKE_UFSC.ipynb)*.

*Observação: Destacamos aqui que a execução foi pensada sempre em ser realizada via Google Colab, por meio de contas que possuam acesso às pastas que armazenam os arquivos de textos extraídos.*


## Ferramentas utilizadas
- Segmentação de frases: [NLTK](https://www.nltk.org/)
- Reconhecimento de entidades na frase: [spaCy](https://spacy.io/models/pt)
- POS Tag para reconhecer verbos na frase: [spaCy](https://spacy.io/models/pt)
- Lematizador de verbos: [pt-br-verbs-lemmatizer](https://pypi.org/project/pt-br-verbs-lemmatizer/)
- Limpeza/padronização/formatação do texto: [ferramentas-basicas-pln](https://pypi.org/project/ferramentas-basicas-pln/)
- Armazenamento de arquivos pré-processados: [msgpack](https://github.com/msgpack/msgpack-python)
- Algumas bibliotecas básicas do Python também foram necessárias como: *os*, *string*, *re* e *time*.

## Desenvolvedor

- [Igor Caetano de Souza](https://github.com/IgorCaetano)

## Melhorias nesta etapa

Se aprofundando um pouco mais na [documentação](https://radimrehurek.com/gensim/models/word2vec.html) do algoritmo Word2Vec via biblioteca gensim, percebeu-se que, para corpus grandes, pode-se utilizar um parâmetro no treinamento chamado de "corpus_file" ao invés de alimentar o treinamento pelo parâmetro "sentences" (que atualmente é usado para alimentar o treino com as frases do corpus. Retirando o trecho que explica essa otimização no treinamento da documentação, tem-se:

_"corpus_file (str, optional) – Path to a corpus file in LineSentence format. You may use this argument instead of sentences to get **performance boost**. Only one of sentences or corpus_file arguments need to be passed (or none of them, in that case, the model is left uninitialized)."_

Para tal feito, é necessário pré-processar no "formato" [LineSentence](https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.LineSentence), ao invés do formato utilizado de lista de lista de tokens.
