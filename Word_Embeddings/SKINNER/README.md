# 🔍 Semantic Knowledge and Interpretation Navigator for Nurturing Exact References

## SKINNER - WOKE - UFSC 

O algoritmo Semantic Knowledge and Interpretation Navigator for Nurturing Exact References (SKINNER) foi desenvolvido com o intuito de clarear, na medida do possível, as construções de contexto dos vetores de palavras atribuídas dentro de algumas etapas do algoritmo Word2Vec com base na co-ocorrência de palavras e suas respectivas frequências. Para tal feito, pensou-se em replicar tais etapas e armazenar as informações obtidas.
Sendo assim, destaca-se que o escopo de análise com base no SKINNER se dá por meio de modelos individuais, ou seja, deve-se escolher um modelo para então analisar o processo de construção de contexto com base na co-ocorrência das palavras utilizadas para alimentar seu treinamento.

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

### Importante
- Não considerou-se que os próprios tokens centrais aparecessem em seus tokens de contexto (no exemplo, "gênero" não foi considerado um token de contexto para "gênero", por mais que aparecesse dentro da janela de contexto).
- A lógica do filtro nas frases foi validado por análise de respostas no fórum Stack Overflow disponível no link: [How is Word2Vec min_count applied](https://stackoverflow.com/questions/50723303/how-is-word2vec-min-count-applied).
- Modelos em que as séries temporais foram construídas utilizando o modo "Incremental" tiveram seus arquivos construídos para o SKINNER apenas contemplando o recorte temporal da atualização de treinamento, ou seja, se você optar por analisar o modelo "WOKE_1_CFH_2011_2013_w2v_inc", por exemplo, o SKINNER terá construídos arquivos com base nos arquivos de textos pré-processados da coleção do CFH, durante os anos 2011 e 2013. Se você optar pelo modelo treinado usando o modo "Temporal", no caso "WOKE_1_CFH_2003_2013_w2v_tmp", então você terá acesso à arquivos que foram construídos usando textos de 2003 até 2013.
- A viabilidade de tal desenvolvimento de algoritmo se deu, principalmente, pela disponibilidade de acesso ao corpus de documentos que constituiu o treinamento dos modelos WOKE. Ademais, a estruturação das pastas tornou toda a análise possível: pasta raiz -> pasta da coleção -> pasta do ano -> pasta do trabalho -> arquivos de textos (pré-processados).

### Observações e Melhorias

O projeto SKINNER ainda está em fase de testes, totalmente funcional, mas não totalmente otimizado, logo pode-se observar prováveis erros de uso excessivo de memória RAM ao pesquisar um conjunto muito grande de tokens ou utilizar modelos muito pesados. Algumas melhorias para o SKINNER estão pontuadas na pasta "Melhorias".

## Sobre os arquivos

Nesta página você terá acesso ao notebook responsável pela construção dos arquivos utilizados pelo SKINNER na hora de apresentar os contextos ("SKINNER_Construção_de_arquivos.ipynb"), ao notebook que executa propriamente dito a aplicação do SKINNER ("Notebook_SKINNER_WOKE_UFSC.ipynb") e na pasta "src" você terá acesso ao arquivo "main.py", onde está o código responsável pelo agrupamento, organização e exibição dos resultados do SKINNER.

## Desenvolvedor

- Igor Caetano de Souza *[(Perfil GitHub)](https://github.com/IgorCaetano)*
