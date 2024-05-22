# Visualizações WOKE

Acessando este diretório você conseguirá rodar programas destinados a exibição dos resultados de múltiplas formas dos nossos modelos treinados.

## Passo 1 - Escolher o tipo de treinamento

Ao configurar o ambiente será pedido para você selecionar o tipo de treinamento, aonde:
- **com_series_temporais**: Treinamentos separados por intervalos de datas, que podem ser comparados entre si a fim de analisar mudanças entre as relações das palavras ao decorrer do tempo, por exemplo, quero analisar as relações entre as palavras num escopo do Repositório Institucional inteiro (todas as coleções) entre 2003 e 2024, verificando os resultados para cada instante "t" (que no nosso caso pode ser organizado em intervalo de anos, não especificamente um ano) de treinamento.
- **sem_series_temporais**: Treinamentos realizados com uma data inicial e final fixas, os quais servem para analisar "globalmente" algum escopo específico, por exemplo, análise de todo corpus do Repositório Institucional desde 2003 até 2024.

## Passo 2 - Escolher o escopo de treinos

Depois de escolher o tipo de treinamento, deve-se optar por algum dos escopos oferecidos, todas as coleções, coleções específicas, etc.

## Passo 3 - Escolher o modo utilizado no treinamento

Se o modo de treino escolhido foi com séries temporais, seja solicitado que informe em que modo as séries temporais foram construídas:

- **Incremental**: Começou-se com um modelo base (geralmente de 2003 até 2006) e depois passou-se a incrementar corpus em treinos futuros, ou seja, adicionou-se um corpus de, por exemplo, 2007 a 2008 e atualizou-se o treinamento passado (que antes possuia só os textos referentes à 2003 e 2006). Este processo continua até a data final, 2024.
- **Temporal**: Começou-se também com um modelo base (geralmente de 2003 até 2006) e depois passou-se a treinar mais modelos abrindo a janela temporal, ou seja, o próximo treinamento vai ser, por exemplo, de 2003 até 2008, o seguinte de 2003 até 2010, e assim por diante até chegar em 2003 à 2024. Este modo utilizado é o mais indicado para não se lidar com o "esquecimento catastrófico" causado pela atualização das redes neurais em modelos de linguagem natural.

## Passo 4 - Escolher os modelos disponíveis

Nós treinamos diversos modelos com diferentes parâmetros e escolhemos os melhores. Nesta etapa será solicitado que escolha um desses modelos que se saíram melhor dentre todos os outros que treinamos.

## Passo 5 - Escolher quais intervalos de anos serão contemplados na visualização

Agora você já pode escolher se quer visualizar o resultado para todos os modelos disponíveis ou somente para um conjunto específicos de modelos (aconselhamos que você sempre opte por todos, a menos que esteja fazendo uma pesquisa bem específica).

## Passo 6 - Aguardar os downloads dos arquivos referentes ao modelo escolhido

Nesta etapa você deve ter um pouco de paciência, pois em alguns minutos você já terá em mãos um modelo quentinho, pronto para ser utilizado! Basta só esperar que ele seja baixado adequadamente e os arquivos descompactados!

## Passo 7 - Escolher as visualizações que você quer gerar com o modelo escolhido!

Agora você finalmente está apto para explorar nosso modelo, escolha qual visualização você gostaria de gerar e divirta-se pesquisando e aprendendo mais sobre PLN na UFSC!

### Visualizações disponíveis:

- **Gráfico das Similaridades ao decorrer do tempo:**

![Imagem](Similaridades para modelos de 2003 até 2023.png)

- **Vizinhos mais próximos ao decorrer do tempo:**

- **Mapa de calor das similaridades ao decorrer do tempo:**
Faça um estudo a respeito das palavras que mais são similares dentre o conjunto de palavras que você desejar com uma visualização bonita!

- **Frequência de Palavras ao decorrer do tempo:**
Analise as palavras mais utilizadas ao decorrer do tempo!

- **Mudança vetorial ao decorrer do tempo:**
O quão mudado o vetor da palavra "gato" está depois de uma década?
    - **Similaridade entre um vetor no instante "t" e o mesmo vetor num instante "t" + "delta t":**
    asjdasijd
    - **Mudança nos vizinhos mais próximos**
    asjfailfj

