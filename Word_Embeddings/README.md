# Etapas voltadas para Processamento de Linguagem Natural

Aqui procuramos construir Word Embeddings, ou representações vetoriais de palavras presentes em um determinado corpus de textos.

Tentaremos não se aprofundar tanto na "matemática" por trás de todos os processos, mas, à grosso modo, iremos transformar cada palavra em uma forma matemática ("compreensível" para máquinas). Para realizar tal feito utilizamos o algoritmo [Word2Vec disponibilizado pela biblioteca gensim](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html) da linguagem de programação **Python**. 

Para realização de análise semântica por meio de Word Embeddings, precisamos treinar modelos (optamos por utilizar o algoritmo Word2Vec para realização de tais treinamentos) e depois visualizar os resultados (gerando imagens). Tendo isso em vista, foi desenvolvido diversos programas escritos em Python, na seguinte ordem:

1. **Pré-processamento dos textos extraídos:** para treinar modelos Word2Vec precisamos que os textos estejam "tokenizados"/pré-processados. Como queremos otimizar ao máximo o tempo treinando, optamos por criar um corpus de textos pré-processado, o qual contemplou todos os textos extraídos, mas agora já tokenizados.
2. **Treinamento de modelos:** com o corpus de textos pré-processados, podemos treinar diversos modelos nas mais diversas variações de corpus utilizados para alimentar esses treinamentos, optando por coleções e anos específicos. Além de construir também séries temporais com treinamentos em sequência.
3. **Visualização dos resultados:** depois de obter modelos, podemos visualizar, gerando imagens, os resultados desses modelos.

As pastas neste diretório dão acesso à documentação específica de todas estas etapas, bem como todos os arquivos de código e arquivos auxiliares utilizados para estes processos. Além das etapas propriamente ditas, também está disponibilizado um diretório voltado para o processo de contabilização de tokens no corpus de textos extraídos.

Se você não conhece modelos Word2Vec e suas potencialidades, resumidamente, o algoritmo cria um espaço vetorial, o qual agrupa vetores. Cada vetor nesse espaço vetorial faz referência à uma palavra nos textos utilizados para alimentar o treinamento desse modelo. Os vetores, nesse espaço vetorial, tendem a estar alocados de forma que palavras semanticamente parecidas estejam próximas umas das outras enquanto palavras semanticamente diferentes estejam distantes entre si, pois utiliza como base teórica a [Hipótese Distribucional](https://brasileiraspln.com/livro-pln/1a-edicao/parte5/cap10/cap10.html#:~:text=A%20sem%C3%A2ntica%20distribucional%20%C3%A9%20ancorada,ter%20significado%20similar%20ou%20aproximado.).

Dessa forma podemos analisar as palavras (vetores) e verificar quem são seus "vizinhos mais próximos", ou seja, quais outras palavras (vetores) estão mais próximas dessa palavra que estamos analisando. Por exemplo, se analisarmos a palavra "morango", provavelmente teremos como palavras mais próximas à ela: banana, maçã, abacaxi, uva, etc. Sendo assim, podemos analisar *clusters* que, nesse caso, seria um campo semântico de frutas.

Essa possibilidade de analisar campos semânticos construídos no espaço vetorial consegue ir além de simples relações sintáticas ou contextuais e demonstram a grande potencialidade de modelos Word2Vec.

Além disso, podemos também realizar "operações semânticas" como as promissoras **analogias**, as quais estão mais detalhadas na etapa de *Treinamento*.
