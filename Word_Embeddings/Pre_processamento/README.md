# Pré-processamento WOKE UFSC

## Objetivo

Esta etapa tem como objetivo pré-processar os textos extraídos dos trabalhos podendo ser com o reconhecimento de entidades no texto (e posterior tokenização destas entidades) e sem reconhecimento de entidades no texto (tokenizando palavra por palavra). Ambas possuem a lematização de verbos implementada.

Para otimizar o tempo e integrar mais os membros do Grupo de Estudos e Pesquisa em IA e História da UFSC foi projetado execuções "paralelas" para se pré-processar o máximo de textos num mesmo período de tempo. Desta forma, estruturou-se o código de execução do pré-processamento pensando em separar e organizar os trabalhos entre os programas que estiverem executando o pré-processamento. Para mais informações detalhadas sobre este processo, por favor leia as células de texto e os comentários presentes no arquivo de notebook *Programa_Oficial_FINAL_de_Pre_processamento_WOKE_UFSC.ipynb*.

*Observação: Destacamos aqui que a execução foi pensada sempre em ser realizada via Google Colab, por meio de contas que possuam acesso às pastas que armazenam os arquivos de textos extraídos.*


## Ferramentas utilizadas
- Segmentação de frases: [NLTK](https://www.nltk.org/)
- Reconhecimento de entidades na frase: [spaCy](https://spacy.io/models/pt)
- POS Tag para reconhecer verbos na frase: [spaCy](https://spacy.io/models/pt)
- Lematizador de verbos: [pt-br-verbs-lemmatizer](https://pypi.org/project/pt-br-verbs-lemmatizer/)
- Limpeza/padronização/formatação do texto:[ferramentas-basicas-pln](https://pypi.org/project/ferramentas-basicas-pln/)
- Armazenamento de arquivos pré-processados: MessagePack ([msgpack](https://github.com/msgpack/msgpack-python))
- Algumas bibliotecas básicas do Python também foram necessárias como: *os*, *string*, *re* e *time*.

## Desenvolvedor

- [Igor Caetano de Souza](https://github.com/IgorCaetano)