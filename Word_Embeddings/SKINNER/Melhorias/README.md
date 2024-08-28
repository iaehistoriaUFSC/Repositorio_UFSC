O projeto SKINNER ainda não teve sua versão final lançada, mas já possui uma versão de testes totalmente funcional, mas não totalmente otimizada.

Não é tão difícil ter seu ambiente de execução desconectado (no caso da utilização do Google Colab) por conta da utilização máxima da RAM disponível no sistema. Isso se deve principalmente pelo armazenamento excessivo de dados dentro da RAM, causado pelas grandes quantidades de informação que são catalogadas, organizadas e armazenadas ao decorrer do processo de construção do HTML e, principalmente, do documento PDF. Logo, ao pesquisar um conjunto muito grande de tokens ou utilizar modelos muito pesados você pode se deparar com este cenário inoportuno. Mas já temos alguns pontos em mente para melhorar o algoritmo ainda mais e para tirá-lo da versão de testes:

- Filtro para não pesquisar palavras fora do vocabulário;
- Possibilidade de geração apenas de arquivo HTML com navegação via menu lateral como resultado final, pois o HTML é gerado muito mais rápido que o arquivo PDF;
- Armazenar as informações para construção do HTML numa pasta temporária no disco e depois percorrê-la coletando as informações e deletando os arquivos temporários;
- Utilização de objetos geradores dentro do código em funções específicas para não carregar informações desnecessariamente e só chamá-las quando forem de fato usadas (por exemplo, criar um gerador para cada token que esteja se pesquisando, evitando de carregar todas as informações de todos os tokens pesquisados numa mesma variável do tipo dicionário);
- Exibição, no PDF, apenas das coleções e trabalhos que tiveram contribuição, de fato, na construção de contexto para determinado token (atualmente a coleção/trabalho aparece com 0% e um espaço vazio);
- Ordenação da maior porcentagem para a menor porcentagem de contribuição na listagem de coleções e na listagem de trabalhos.


**Embora exista a possibilidade da realização de tais melhorias, é importante destacar que este projeto teve como principal objetivo acender uma luz dentro da "caixa-preta" que assombra o processo de construção de modelos de inteligência artificial, tendo como maior foco, especificamente, modelos de processamento de linguagem natural. 
Dito isso, pode-se dizer que o resultado atual do SKINNER já mostrou grandes potencialidades na busca por referências dentro do corpus de textos utilizados diante de resultados obtidos por tais modelos.**