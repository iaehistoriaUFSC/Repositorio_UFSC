# Treinamento de modelos WOKE

Após construído o corpus de textos pré-processado, podemos partir para a etapa do tão aguardado treinamento dos modelos!

Nesta etapa tivemos a estratégia de realizar múltiplos treinamentos (gerando múltiplos modelos) com alternância de parâmetros. Ou seja, realizamos muitos treinos cada um com parâmetros diferentes. Isso foi pensado para maximizar a potencialidade de modelos treinados no nosso corpus de documentos. Dessa forma não estaremos fadados a modelos ruins por conta de uma má escolha de parâmetros no treinamento. 

Por exemplo: não adianta setar o parâmetro de *vector_size* (quantidade de dimensões dos vetores) muito alto se você tem um corpus muito pequeno, isso tende a gerar uma generalização muito abrupta das informações extraídas para cada token no modelo. 

Sendo assim, realizando diversos treinamentos com os mais variados valores nos parâmetros de treino, podemos depois avaliar o desempenho de cada modelo treinado por meio de pontuações em questões (analogias) com base nos seus resultados obtidos e os esperados. Depois basta escolhermos os modelos que melhor pontuaram e começar a construir as séries temporais.

Para construção das séries temporais necessitamos de um modelo base, que será a primeira série temporal que originará as demais. Nesse sentido para melhorar a acurácia dos múltiplos treinamentos pensamos em botar uma quantidade de textos adequada para este primeiro recorte temporal, da seguinte forma:

- Modelo **UFSC 2003-2006**: contempla textos escritos de 2003 até 2006 de todas as coleções/cursos da UFSC.
- Modelo **CFH-03-10**: contempla textos escritos de 2003 até 2010 das coleções/cursos do Centro de Filosofia e Ciências Humanas da UFSC.
- Modelo **HST-03-10**: contempla textos escritos de 2003 até 2010 da coleções/curso de História da UFSC.
- Modelo **SAUDE-CORPO-03-10**: contempla textos escritos de 2003 até 2010 das coleções/cursos referentes ao corpo humano e saúde do corpo no geral da UFSC.

Essas informações foram usadas para construir as baterias de treinos nesses diferentes corpus de textos. Depois de executada as baterias, validamos os modelos e escolhemos os que melhor desempenharam. Abaixo estão os links para acessar as planilhas de resultados dos múltiplos treinamentos para os diferentes corpus explorados:
- [Planilha resultados - WOKE UFSC 2003-2006](https://docs.google.com/spreadsheets/d/1BZGAcEixg35OT39wduayRawp9mGWA8Fr/edit?usp=sharing&ouid=107024036721805330434&rtpof=true&sd=true)
- [Planilha resultados - WOKE CFH-03-10](https://docs.google.com/spreadsheets/d/1RoUbxPGZDj3li13DxvZROuZZaSEf0BSu/edit?usp=sharing&ouid=107024036721805330434&rtpof=true&sd=true)
- [Planilha resultados - WOKE HST-03-10](https://docs.google.com/spreadsheets/d/14xs9bfIm0Sah3baT8EVBUmAedLPe2Uoa/edit?usp=sharing&ouid=107024036721805330434&rtpof=true&sd=true)
- [Planilha resultados - WOKE SAUDE-CORPO-03-10](https://docs.google.com/spreadsheets/d/1qe2DoJlfC-6HfP0PRtLka-aV8_Q00-EF/edit?usp=sharing&ouid=107024036721805330434&rtpof=true&sd=true)


Feitas as análises partimos para a continuação dos treinamentos para geração de mais séries temporais. Temos dois modos de construir o restante das séries:

- **Incremental**: Atualiza o treino anterior com um corpus de textos novo.
- **Temporal**: Adiciona um novo treino com um corpus de textos estendido.

Este treinamento "temporal" tem como objetivo remover a possibilidade de ocorrer o fenômeno de "esquecimento catastrófico" que acomete atualizações de redes neurais nos treinamentos de inteligências artificiais. Pois, na lógica utilizada no treino "temporal" não ocorre atualização, apenas adição de treinos com um corpus de textos maior a cada série temporal. Ainda, um dos desenvolvedores do gensim-Word2Vec abordou temas relacionados à atualização de treinamentos para modelos Word2Vec e o próprio esquecimento catastrófico em uma de suas respostas em fóruns de dúvidas: [word2vec gensim update learning rate - StackOverflow - Gordon Mohr (aka "gojomo")](https://stackoverflow.com/questions/51133162/word2vec-gensim-update-learning-rate).

Depois de construídas as séries temporais (realizados os treinamentos seguintes), transformamos os arquivos de modelo em arquivos de wordvectors, formatos mais leves e que carregam em si o que de fato usamos na hora de realizar as operações para visualizar os resultados. Esse processo de transformação é importante para baixar os modelos depois no programa de Visualizações de Resultados de forma mais rápida e também não ocupar tanto espaço na RAM do sistema na hora de carregar os modelos para realizar as operações quando for feita a construção de alguma visualização.

Abaixo podemos observar uma imagem que ilustra os processos executados para sair do corpus de textos pré-processados até os modelos em séries temporais:

![imgvizprox](https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Treinamento/img_src/img_processos_treinamentos.jpg?raw=true)

#### ❗ Importante: Para se ter como base de suas pesquisas os resultados do WOKE, é extremamente recomendado que você verifique os vizinhos mais próximos de todos os tokens que você está analisando em uma visualização de resultados. Pois isso garantirá que o modelo estará "entendendo bem" sobre o que está sendo abordado nas suas questões. Como você pode observar na planilha de resultados é muito difícil obter um modelo que acerte questões de todos os temas, por isso também recomendamos realizar a mesma análise nos outros modelos disponíveis para o seu mesmo corpus de interesse. ❗
Por exemplo: se você quiser realizar uma visualização de comparação entre palavras / analogias do tipo "homem está para rei assim como mulher está para o que?" Você deve buscar os vizinhos mais próximos de "homem", "rei" e "mulher" e ver se estão de acordo com o que você identifica como adequado. Depois, se você estiver usando o modelo 1 da UFSC, refaça esta visualização com o modelo 2, 3 e 4 (da UFSC também) para fins de comparação. Se as 4 visualizações não estiverem distantes podemos dizer que você está diante de um resultado confiável.
