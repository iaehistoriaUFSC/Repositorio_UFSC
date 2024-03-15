# Descrição do Programa - Etapa 1 - Extração de Dados

Neste programa será coletado, via protocolo OAI-PMH, os **metadados** dos trabalhos presentes nas coleções da comunidade de *[Teses e Dissertações do Repositório Institucional da UFSC](https://repositorio.ufsc.br/handle/123456789/74645)*.

Para executar tal comunicação, estaremos enviando requisições para o link da interface que opera com o protocolo OAI-PMH: "[https://repositorio.ufsc.br/oai/](https://repositorio.ufsc.br/oai/)".

Na documentação, observa-se que o link de requisição é formado por campos. Resumidamente, escolheremos o campo de *ListRecords* (para coletar toda listagem de trabalhos), no formato de metadados *xoai* (para recebermos dados a respeito dos arquivos do trabalho na resposta). Passaremos o número da coleção dentro de Teses e Dissertações com o parâmetro "set=col_123456789" e, ao final, iremos adicionar o número da coleção (curso) que queremos coletar os metadados. Desta forma, tem-se o seguinte padrão de requisição:

*https://repositorio.ufsc.br/oai/request?verb=ListRecords&metadataPrefix=xoai&set=col_123456789_numero_colecao*


*   A resposta para tal requisição vem no formato XML e usou-se uma biblioteca, *xmltodict*, para passar o XML para o formato de dicionário Python, o qual temos mais familiaridade na hora de buscar as informações.
*   As respostas não ultrapassam 100 resultados, por isso foi desenvolvida uma lógica com um "resumptionToken" o qual vai dar acesso as outras respostas (de 100 em 100), até chegar no final dos trabalhos da respectiva coleção.





Ao final, armazenamos todos os metadados em um dicionário Python para a coleção em questão e salvamos esses dicionários num arquivo ".joblib" numa pasta do Google Drive para ser acessado posteriormente na Etapa 2.

---

*Observação: Foram feitas tentativas de restringir as datas de publicação dos trabalhos (de 2003 até 2024), mas as respostas eram as mesmas que sem o filtro de tais datas na requisição. Então optou-se por deixar a requisição sem o filtro de datas e filtrá-las durante o processamento.*

---

## Atenção:
- **Arquivo _main.py_ destinado apenas para execução em ambientes fora do Google Colab.
Já o arquivo _Código Atualizado para execução no Colab.ipynb_ é destinado para execuções dentro do Google Colab.**
- **Atenção para execuções fora do Colab: muitos programas dependem de arquivos que estão armazenados em outras pastas do Google Drive, ou seja, para uma execução fora do Colab sem erros, verifique se os arquivos que forem procurados se encontram disponíveis no seu ambiente de execução.**
