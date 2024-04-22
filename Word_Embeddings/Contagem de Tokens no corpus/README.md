# Contador de Tokens no corpus - WOKE UFSC

## Objetivos 

Este programa foi destinado a contar a quantidade de tokens presentes nos trabalhos coletados do Repositório Institucional da UFSC.

## Método utilizado
Este programa foi replicado para mais outros 11 programas, totalizando um total de 12 programas, os quais foram executados "em paralelo", por meio de outras contas do Google. Cada usuário do Colab pode executar apenas 3 programas simultaneamente, logo essa abordagem foi aplicada para otimizar melhor o tempo de execução desta contagem.

## Adendos
A lógica de contar o tamanho do vocabulário foi aplicada para cada trabalho, porém a lista de tokens não foi salva, impossibilitando de contabilizar o tamanho do vocabulário total (somatório de todos os textos). Ou seja, a informação da quantidade de tokens no vocabulário (com e sem stopwords sendo contadas) está sendo armazenada no arquivo referente ao número de tokens para cada trabalho, porém esta restrito a cada trabalho, não podendo ser calculado apropriadamente o tamanho exato do vocabulário total do corpus.

Tendo isso em vista apenas as informações de contagem normal de todos os tokens foi considerada para obter o somatório total de tokens de todos os textos, a qual totalizou em:
- 1.220.839.374 contando stopwords
- 826.526.579 não contando stopwords
