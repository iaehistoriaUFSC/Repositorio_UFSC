# Extração de dados do RI da UFSC por meio da interface/API/Protocolo OAI-PMH

Nesta pasta estão armazenados os códigos, em "sub-pastas", das etapas relacionadas à extração dos metadados e textos presentes nos PDFs dos trabalhos na comunidade de Teses e Dissertações do Repositório Institucional da UFSC.

Cada etapa tem seu próprio arquivo _README_, especificando mais detalhadamente os processos referentes aquela determinada etapa. Entretanto, podemos dar um resumo do que acontece em cada etapa:

### Etapa 1

- É nesta etapa que acontece a comunicação direta entre o nosso programa e a API do RI. Logo, é nela que coletamos os **metadados** de **Título, Autor, Resumo, Descrição, Assuntos, Língua, Tipo, Data** de upload no **repositório, Data** presente na **descrição, Link** da **página** do trabalho no site do RI e o **Link** do **PDF** do trabalho para cada trabalho presente em cada coleção presente na comunidade de Teses e Dissertações. Depois de obter e armazenar todos esses dados, incluindo os quantitativos referentes a esta etapa da extração, passamos para a Etapa 2.

<h4><i>Etapa 1_2</i></h4>

- Esta etapa surgiu depois da organização das etapas, por isso a numeração 1_2 (está entre a etapa 1 e a etapa 2). Percebeu-se a necessidade de gerar e armazenar uma variável que possuísse as informações referentes à organização das execuções dos diversos programas ao decorrer dos dias, armazenando assim uma lista de coleções que um determinado programa, num determinado dia, iria contemplar. Decidimos alocá-la em uma etapa diferente porque ela não faz parte nem do processo de extração de metadados (etapa 1) nem da extração do texto (etapa 2).

### Etapa 2

- Nesta etapa foram realizadas as extrações de textos e armazenamento em arquivos no formato ".txt" dos arquivos PDFs. Em posse dos links referentes aos PDFs, extraídos com os metadados, pode-se enviar requisições para estes links a fim de baixar o arquivo PDF, realizar a extração do texto, armazenar estes dados extraídos e depois deletamos o arquivo PDF do armazenamento do Drive. Alguns programas se encarregaram de esvaziar a lixeira do Drive para não sobrecarregar o espaço (que antes da atualização de plano era limitado).

### Etapa 3

- A geração da planilha de metadados e do relatório em PDF referentes à extração dos dados é feita nesta etapa. Organiza os dados estruturados armazenados pelas etapas anteriores em uma planilha Excel (".xlsx") e gera indicadores de desempenho referentes ao processo de extração de textos dos trabalhos num arquivo PDF em formato de relatório.

### Etapa 4

- Etapa extra para realização de validações referentes ao processo realizado de extração de dados do Repositório Institucional da UFSC.

## Atenção!
- Os arquivos devem ser executados tendo como pasta de trabalho as próprias pastas das etapas ou a pasta "via_protocolo_oai_pmh". Caso contrário o código não será executado da forma adequada;

- Cada etapa tem um requirements.txt diferente;
