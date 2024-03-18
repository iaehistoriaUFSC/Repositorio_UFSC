# Etapa 1_2 da Extração de Dados do RI da UFSC

Percebemos a necessidade de alocar um espaço especial para um processo que ainda não tinha sido desenvolvido: organizar todas as coleções em seus respectivos programas em seus respectivos dias, a fim de não passar duas ou mais vezes pela mesma coleção e otimizar bem nosso tempo para não ficar executando diversos programas madrugada à dentro.

Já havíamos feito uma estimativa, por cima, de quanto tempo levava para extrair o texto de um trabalho. Então, tendo essa estimativa em mente, calculamos quanto tempo gostaríamos de ficar executando os programas (o T.I. responsável pelo RI avisou que um horário adequado para realização da coleta seria depois das 18h, então das 18h até umas 23h / 23h30 no máximo) e vimos que, para rodar um programa por 5h, este passaria em, aproximadamente, 2.800 trabalhos.

Com isso, dividimos as coleções pensando em não ultrapassar 2.800 trabalhos em cada programa para os 6 programas diferentes ao decorrer dos dias em um dicionário do tipo:

```python
dic_listagem_execs = {'Dia 1':{'Programa 1':[0,[]],'Programa 2':[0,[]],'Programa 3':[0,[]],'Programa 4':[0,[]],'Programa 5':[0,[]],'Programa 6':[0,[]]},
                    'Dia 2':{'Programa 1':[0,[]],'Programa 2':[0,[]],'Programa 3':[0,[]],'Programa 4':[0,[]],'Programa 5':[0,[]],'Programa 6':[0,[]]},
                    'Dia 3':{'Programa 1':[0,[]],'Programa 2':[0,[]],'Programa 3':[0,[]],'Programa 4':[0,[]],'Programa 5':[0,[]],'Programa 6':[0,[]]},
                    'Dia 4':{'Programa 1':[0,[]],'Programa 2':[0,[]],'Programa 3':[0,[]],'Programa 4':[0,[]],'Programa 5':[0,[]],'Programa 6':[0,[]]},
                    'Dia 5':{'Programa 1':[0,[]],'Programa 2':[0,[]],'Programa 3':[0,[]],'Programa 4':[0,[]],'Programa 5':[0,[]],'Programa 6':[0,[]]},
                    'Dia 6':{'Programa 1':[0,[]],'Programa 2':[0,[]],'Programa 3':[0,[]],'Programa 4':[0,[]],'Programa 5':[0,[]],'Programa 6':[0,[]]}}
```

Aonde:
```python
{'Dia 1':{'Programa 1':[0,[]]}}
```
faz menção à o programa 1, no dia 1, passaria por 0 trabalhos e sua listagem de coleções está vazia.

Depois, só desenvolvemos uma lógica para alocar as coleções na lista para o determinado programa no determinado dia que ficasse entre 2.600 e 2.800 trabalhos.

As coleções que ultrapassassem 2.800 trabalhos, seriam executadas em um único programa, com o programador cuidando para executar este programa mais cedo do que os outros.
