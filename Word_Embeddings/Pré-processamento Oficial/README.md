# Pré-processamento WOKE UFSC

## Objetivo

Esta etapa tem como objetivo pré-processar os textos extraídos dos trabalhos de duas maneiras: com o reconhecimento de entidades no texto (e posterior tokenização destas entidades) e sem reconhecimento de entidades no texto. Ambas possuem a lematização de verbos implementada.

## Ferramentas utilizadas
- Segmentação de frases: [NLTK](https://www.nltk.org/)
- Reconhecimento de entidades na frase: [spaCy](https://spacy.io/models/pt)
- POS Tag para reconhecer verbos na frase: [spaCy](https://spacy.io/models/pt)
- Lematizador de verbos:[pt-br-verbs-lemmatizer](https://pypi.org/project/pt-br-verbs-lemmatizer/)
- Limpeza do texto:[ferramentas-basicas-pln](https://pypi.org/project/ferramentas-basicas-pln/)
- Armazenamento: MessagePack ([msgpack](https://github.com/msgpack/msgpack-python))

## Desenvolvedor

- [Igor Caetano de Souza](https://github.com/IgorCaetano)