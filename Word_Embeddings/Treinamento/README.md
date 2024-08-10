# Treinamento de modelos WOKE

Após construído o corpus de textos pré-processado, podemos partir para a etapa do tão aguardado treinamento dos modelos!

Nesta etapa tivemos a estratégia de realizar múltiplos treinamentos (gerando múltiplos modelos) com alternância de parâmetros. Ou seja, realizamos muitos treinos cada um com parâmetros diferentes. Isso foi pensado para maximizar a potencialidade de modelos treinados no nosso corpus de documentos. Dessa forma não estaremos fadados a modelos ruins por conta de uma má escolha de parâmetros no treinamento. 

Por exemplo: não adianta setar o parâmetro de *vector_size* (quantidade de dimensões dos vetores) muito alto se você tem um corpus muito pequeno, isso tende a gerar uma generalização muito abrupta das informações extraídas para cada token no modelo. 

Sendo assim, realizando diversos treinamentos com os mais variados valores nos parâmetros de treino, podemos depois avaliar o desempenho de cada modelo treinado por meio de pontuações em questões (analogias) com base nos seus resultados obtidos e os esperados. Depois basta escolhermos os modelos que melhor pontuaram e começar a construir as séries temporais.

Para construção das séries temporais necessitamos de um modelo base, que será a primeira série temporal que originará as demais. Nesse sentido para melhorar a acurácia dos múltiplos treinamentos pensamos em botar uma quantidade de textos adequada para este primeiro recorte temporal, da seguinte forma:

- Modelo UFSC: contempla textos escritos de 2003 até 2006.
- Modelo CFH: contempla textos escritos de 2003 até 2010.
- Modelo HST: contempla textos escritos de 2003 até 2010.
- Modelo SAUDE-CORPO: contempla textos escritos de 2003 até 2010.

Essas informações foram usadas para construir as baterias de treinos nesses diferentes corpus de textos. Depois de executada as baterias, validado os modelos e escolhido os que melhor desempenharam, partimos para continuação dos treinamentos para geração de mais séries temporais. Temos dois modos de construir o restante das séries:

- Incremental: Atualiza o treino anterior com um corpus de textos novo.
- Temporal: Adiciona um novo treino com um corpus de textos estendido.

Depois de construídas as séries temporais (realizados os treinamentos seguintes), transformamos os arquivos de modelo em arquivos de wordvectors, formatos mais leves e que carregam em si o que de fato usamos na hora de realizar as operações para visualizar os resultados. Esse processo de transformação é importante para baixar os modelos depois no programa de Visualizações de Resultados de forma mais rápida e também não ocupar tanto espaço na RAM do sistema na hora de carregar os modelos para realizar as operações quando for feita a construção de alguma visualização.

Abaixo podemos observar uma imagem que ilustra os processos executados para sair do corpus de textos pré-processados até os modelos em séries temporais:

![imgvizprox](https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Treinamento/img_src/img_processos_treinamentos.jpg?raw=true)
