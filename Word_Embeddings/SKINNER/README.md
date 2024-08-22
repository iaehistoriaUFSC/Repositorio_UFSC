# 🔍 Semantic Knowledge and Interpretation Navigator for Nurturing Exact References

## SKINNER - WOKE - UFSC 

O algoritmo Semantic Knowledge and Interpretation Navigator for Nurturing Exact References (SKINNER) foi desenvolvido com o intuito de clarear, na medida do possível, as construções de contexto dos vetores de palavras atribuídas dentro de algumas etapas do algoritmo Word2Vec com base na co-ocorrência de palavras e suas respectivas frequências. Para tal feito, pensou-se em replicar tais etapas e armazenar as informações obtidas.
Sendo assim, destaca-se que o escopo de análise com base no SKINNER se dá por meio de modelos individuais, ou seja, devemos escolher um modelo para então analisar o processo de construção de contexto com base na co-ocorrência das palavras utilizadas para alimentar seu treinamento.

Podemos resumir o desenvolvimento deste algoritmo da seguinte forma:
- **Coleta de informações do modelo utilizado**: Após escolher o modelo que terá sua análise disponibilizada, verifica-se qual foi o tamanho da janela de contexto utilizada no treinamento, bem como os tokens presentes no vocabulário do modelo e o intervalo de datas contemplado pelo treinamento do mesmo.
- **Coleta de informações a respeito da co-ocorrência de palavras no corpus**: Depois de obter o vocabulário (palavras únicas que entraram para o treinamento) e o tamanho da janela (quantidade de tokens que serão analisados na frase toda ao redor de um token central/alvo para montar contexto), pode-se partir para construção de contexto com base nas frases presentes no corpus (no recorte temporal utilizado no treino) e nas palavras que entraram para o treinamento dentro dessas frases. Além da construção do contexto propriamente dita, os arquivos foram estruturados de tal forma que preservou-se a estruturação das pastas que armazenam os arquivos de textos no corpus de documentos, podendo assim organizá-lo com base na coleção, trabalho e nos metadados do trabalho (assuntos, link para página no repositório e link para o PDF que teve seu texto extraído).
- **Construção de contexto**: Após feita a geração dos arquivos referentes as informações de co-ocorrência (cada arquivo fazendo referencia a uma coleção/curso utilizada no treinamento), pode-se então navegar entre eles construindo o contexto para um determinado conjunto de tokens.
- **Geração de PDF**: E, por fim, depois de construído contexto para os tokens que deseja-se analisar, pode-se, então, gerar o PDF contendo todas as informações organizadas.

### Exemplo
Para melhor compreender o processo de construção de contexto, imagine um exemplo em que o modelo que se queira analisar tem as seguintes características:
-  Foi treinado com uma janela de tamanho 2;
- Possui um vocabulário com esses tokens: "gênero","importância","textos","explora","textual","inclusão","artigo", "aborda", "borboleta", "sofá".

Agora imagine que estamos no meio de uma análise de um trabalho e vamos passar pela seguinte frase:

"O artigo explora a inclusão de gênero em textos dentro dos estudos de gênero."

*Observação: a frase de exemplo não está tokenizada tão pouco pré-processada, foi deixada em seu "formato cru" apenas para fins didáticos, pois as frases no corpus de textos pré-processado utilizado para os treinamentos dos modelos WOKE se apresentariam de outra forma, removendo stopwords, lematizando verbos, etc.*

Voltando à análise, como estamos interessados apenas nos tokens que, de fato, entraram para o treinamento do modelo analisado, filtramos a frase para apenas conter os tokens que existem no modelo:

"artigo explora inclusão gênero textos gênero"

Feita a filtragem da frase passamos a analisar token por token de forma a deixá-lo como token central/alvo na análise, buscando assim as palavras que o cercam na janela usada pelo treinamento:

- artigo:
    - explora: 1
    - inclusão: 1
- explora:
    - artigo: 1
    - inclusão: 1
    - gênero: 1
- inclusão:
    - artigo: 1
    - explora: 1
    - gênero: 1
    - textos: 1
- gênero:
    - explora: 1
    - inclusão: 1
    - textos: 2

Note que os itens listados a cima fornecem a informação dos tokens centrais e seus respectivos tokens de contexto com suas respectivas frequências de ocorrências. Além disso, veja que gênero apareceu 2 vezes na mesma frase, dessa forma sua contagem é atualizada na frase atual, com seu token de contexto "textos" com 2 ocorrências.

Não considerou-se que os próprios tokens centrais aparecessem em seus tokens de contexto (no caso "gênero" não foi considerado um token de contexto para "gênero", por mais que aparecesse dentro da janela de contexto).
A lógica do filtro nas frases foi validado por análise de respostas no fórum Stack Overflow disponível no link: [How is Word2Vec min_count applied](https://stackoverflow.com/questions/50723303/how-is-word2vec-min-count-applied).


### Observações e Melhorias

O projeto SKINNER ainda está em fase de testes, totalmente funcional, mas não totalmente otimizado. Ainda pode-se melhorá-lo da seguinte forma:
- Filtro para não pesquisar palavras fora do vocabulário;
- Exibição, no PDF, apenas das coleções e trabalhos que tiveram contribuição, de fato, na construção de contexto para determinado token (atualmente a coleção/trabalho aparece com 0% e um espaço vazio);
- Ordenação da maior porcentagem para a menor porcentagem de contribuição na listagem de coleções e na listagem de trabalhos.
- Possibilidade de geração apenas de arquivo HTML com navegação via menu lateral como resultado final, pois o HTML é gerado muito mais rápido que o arquivo PDF.

Embora exista a possibilidade da realização de tais melhorias, é importante destacar que este projeto teve como principal objetivo acender uma luz dentro da "caixa-preta" que assombra o processo de construção de modelos de inteligência artificial, tendo como maior foco, especificamente, modelos de processamento de linguagem natural. 
Dito isso, pode-se dizer que o resultado atual do SKINNER já mostrou grandes potencialidades na busca por referências dentro do corpus de textos utilizados diante de resultados obtidos por tais modelos.

## Desenvolvedor

- Igor Caetano de Souza *[(Perfil GitHub)](https://github.com/IgorCaetano)*
