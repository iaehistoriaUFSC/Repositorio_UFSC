# Infomação sobre as Visualizações disponíveis para o WOKE

## 1 - Gráfico das similaridades ao decorrer do tempo

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  <h4>Exemplo de uso</h4>

  <p>Caso exista interesse em avaliar a similaridade entre o token "gênero" e outros tokens de seu interesse ao decorrer do tempo, podemos usar esta visualização. Primeiro escolhemos o token central e depois os tokens que terão sua similaridade calculada com este token central. Neste exemplo estaremos interessados em observar as similaridades de gênero com etnia, raça, identidade, estudos de gênero, classe, classe social, categoria, tribo, grupo e sexualidade. As palavras selecionadas são simplesmente para fins didáticos. Abaixo podemos ver a visualização gerada.</p>

  <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/Sim_WOKE_1_CFH_w2v_inc_2003_2024_genero.png?raw=true" alt="imggrafsim" />

  <p>Dessa forma podemos dizer que no início da série temporal os tokens que tinham maior similaridade com gênero, dos tokens selecionados, foram: etnia, raça, estudos de gênero, sexualidade e classe social, em ordem decrescente.
  Ao final da série temporal vemos que não houve mudanças tão significativas, tanto para os tokens mais similares quanto para os menos similares. Houve apenas leves mudanças de posição entre o top 1, top 3, etc.</p>

</details>

## 2 - Vizinhos mais próximos ao decorrer do tempo (.png e .txt)

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  
  Esta visualização possui geração de imagem (arquivo .png), mas também pode gerar texto (arquivo .txt) com informações mais detalhadas e maior funcionalidade.

  <h4>Exemplo de uso</h4>

  <p>Caso exista interesse em avaliar os vizinhos mais próximos (mais similares) de um determinado token, podemos usar esta visualização. Primeiro escolhemos se vamos querer gerar apenas uma visualização dos top 10 vizinhos mais próximos para cada série temporal ou se vamos querer gerar um arquivo de texto podendo ter uma quantidade maior de vizinhos mais próximos e podendo avaliar os vizinhos mais próximos de mais de um token ao mesmo tempo, por exemplo avaliar os vizinhos mais próximos de "carro" e "automóvel". Vamos supor que temos interesse em saber os vizinhos mais próximos ao decorrer do tempo para o token "etnia" e vamos gerar resultados das duas formas.</p>

  <h5>Com geração de imagem</h5>
  <figure>
    <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/VP_WOKE_1_CFH_2003_2010_w2v_inc_etnia.png?raw=true" alt="imgvizprox1" />
    <figcaption>Resultado para o primeiro modelo da série.</figcaption>
  </figure>

  <figure>
    <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/VP_WOKE_1_CFH_2014_2016_w2v_inc_etnia.png?raw=true" alt="imgvizprox2" />
    <figcaption>Resultado para o modelo mais ao meio da série.</figcaption>
  </figure>

  <figure>
    <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/VP_WOKE_1_CFH_2020_2024_w2v_inc_etnia.png?raw=true" alt="imgvizprox3" />
    <figcaption>Resultado para o último modelo da série.</figcaption>
  </figure>
  
  <h5>Com geração de texto</h5>
  Escolhendo os tokens centrais como "etnia" e "etnias" (obtendo também a sua forma no plural) e escolhendo 20 vizinhos mais próximos, teremos as seguintes respostas nos arquivos de texto referentes aos mesmo modelos visualizados a cima:

  <h6>VP_WOKE_1_CFH_2003_2010_w2v_inc.txt</h6>
  Lista dos TOP 20 vizinhos mais próximos de etnia, etnias:

  1. étnica: 0.7338260412216187
  2. étnicas: 0.7208661437034607
  3. descendências: 0.6878007650375366
  4. raça: 0.6646744608879089
  5. etnicamente: 0.6503458619117737
  6. étnicos: 0.6483527421951294
  7. étnico: 0.6303802132606506
  8. miscigenar: 0.6284468173980713
  9. afro-descendentes: 0.6252454519271851
  10. gênero: 0.597994863986969
  11. ucranianos: 0.588929295539856
  12. descendentes: 0.5856320261955261
  13. afrodescendente: 0.5792911052703857
  14. afro-brasileira: 0.5781661868095398
  15. dialetos: 0.5733134746551514
  16. classe_social: 0.5717697739601135
  17. raciais: 0.5646035671234131
  18. ucraniana: 0.5617498755455017
  19. procedências: 0.5615004301071167
  20. trentinos: 0.5601247549057007


  <h6>VP_WOKE_1_CFH_2014_2016_w2v_inc.txt</h6>
  Lista dos TOP 20 vizinhos mais próximos de etnia, etnias:

  1. étnicas: 0.6517886519432068
  2. raça: 0.6482296586036682
  3. étnicos: 0.6354309320449829
  4. étnica: 0.6191620230674744
  5. étnico: 0.6112656593322754
  6. classe_social: 0.5692297220230103
  7. nacionalidades: 0.5602165460586548
  8. nacionalidade: 0.5549836754798889
  9. gênero: 0.536987841129303
  10. raciais: 0.5367445349693298
  11. culturas: 0.5364434123039246
  12. credos: 0.5198298692703247
  13. etnicidade: 0.5167660117149353
  14. indígena: 0.511545717716217
  15. descendências: 0.5066790580749512
  16. racial: 0.5017944574356079
  17. étnico-raciais: 0.5017296075820923
  18. etnocentrismo: 0.5005885362625122
  19. línguas: 0.49701908230781555
  20. indígenas: 0.4935998022556305

 
 <h6>VP_WOKE_1_CFH_2020_2024_w2v_inc.txt</h6>
  Lista dos TOP 20 vizinhos mais próximos de etnia, etnias:

  1. raça: 0.7234798073768616
  2. étnicas: 0.6266407370567322
  3. étnica: 0.5975705981254578
  4. subordinações: 0.5958067178726196
  5. étnico: 0.5905644297599792
  6. classe_social: 0.5904056429862976
  7. etnicidade: 0.5849472880363464
  8. marcadores: 0.5842293500900269
  9. nacionalidade: 0.5686661005020142
  10. gênero: 0.5666171908378601
  11. étnico-racial: 0.5598510503768921
  12. étnicos: 0.551025390625
  13. étnico-: 0.5481338500976562
  14. povos: 0.5458667874336243
  15. interseccionalidades: 0.5398861765861511
  16. descendências: 0.5300548672676086
  17. culturas: 0.5298485159873962
  18. indígena: 0.5192650556564331
  19. autodeclaram: 0.5190275311470032
  20. intersecções: 0.5173969864845276

  <p>Dessa forma podemos analisar se o campo semântico mudou muito, quais foram os tokens que estavam no início, meio e final da série temporal, se houve aparição de algum token um pouco mais diferente no campo semântico, além de visualizar também o grau de similaridade que o primeiro e o último tiveram ao decorrer do tempo para com o token central analisado.</p>
</details>


## 3 - Rede dinâmica dos campos semânticos ao decorrer do tempo

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  <h4>Exemplo de uso</h4>

  <p>Esta visualização é uma variação da visualização de cima de campo semântico, com mais decorações na imagem gerada (e geração somente de uma imagem), mas menos informações (valor das similaridades).
  Vamos supor que queremos analisar, agora, o campo semântico ao decorrer do tempo do token "aborto". Mas vamos focar no campo semântico num geral, sem se ater tanto ao mais similar ou menos similar, apenas aos tokens que o compõem o campo.</p>

  <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/RD_CS_aborto_WOKE_1_CFH_w2v_inc.png?raw=true" alt="imgrededin" />

  <p>Podemos também analisar as mudanças nos campos semânticos do token central ao decorrer do tempo.</p>

</details>

## 4 - Mapa de calor das similaridades ao decorrer do tempo

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  <h4>Exemplo de uso</h4>

  <p>Nesta visualização podemos também ter uma boa visão sobre a mudança das similaridades de um conjunto de tokens com relação à um token central, ao decorrer do tempo. Vamos supor que queremo analisar as similaridades que "nazismo" tem com os tokens: fascismo, totalitarismo, democracia, hitler e nazista ao longo da série temporal.</p>

  <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/Mapa_de_Calor_para_nazismo.png?raw=true" alt="imgmapacalor" />

  <p>Aqui vemos que as cores mais frias representam uma menor similaridade e as cores mais quentes uma maior similaridade. Podemos buscar onde se encontram tais padrões de cores de forma mais intensa e realizar estudos de casos a respeito dos tokens e de seus períodos no mapa de calor.</p>

</details>


## 5 - Estratos do Tempo

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  <h4>Exemplo de uso</h4>

  <p>Nesta visualização podemos também ter uma boa visão sobre a mudança dos campos semânticos de um ou mais tokens ao decorrer do tempo, tendo também a informação dos tokens que mais tiveram sua similaridade com o token central seguidos dos outros tokens que também tiveram alta similaridade. Vamos supor que queremos analisar o campo semântico e o seu top 1 vizinhos mais próximo ao longo da série temporal dos tokens "racismo" e "racista" (poderíamos optar também por buscar por apenas um token central, mas nesse caso vamos usar dois).</p>

  <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/Estratos_do_Tempo_para_racismo_racista.png?raw=true" alt="imgestratostempo" />

  <p>Aqui vemos que é uma espécie de mapa de calor, mas vertical, ou seja, as cores mais frias representam uma menor similaridade e as cores mais quentes uma maior similaridade. Podemos buscar onde se encontram tais padrões de cores de forma mais intensa e realizar estudos de casos a respeito dos tokens e de seus períodos no mapa de calor, além de visualizar com clareza os top 10 vizinhos que compõe o campo semântico do(s) token(s) pesquisado(s).</p>

</details>


## 6 - Vetores de Palavras

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  <h4>Exemplo de uso</h4>

  <p>Nesta visualização podemos observar, vetorialmente, as semelhanças entre os tokens que desejarmos analisar. Vamos supor que queremos analisar a dispersão dos vetores no espaço vetorial dos seguintes vetores de palavras: política, história, ética, teoria, fatos, acontecimentos, psicologia, biologia, matemática, física, cálculo e probabilidade.</p>

  <figure>
    <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/Vetores_de_palavras_para_WOKE_4_UFSC_2003_2006_w2v.png?raw=true" alt="imgvetpalav1" />
    <figcaption>Resultado para o primeiro modelo da série.</figcaption>
  </figure>

  <figure>
    <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/Vetores_de_palavras_para_WOKE_4_UFSC_2023_2024_w2v.png?raw=true" alt="imgvetpalav2" />
    <figcaption>Resultado para o último modelo da série.</figcaption>
  </figure>

  <p>Dessa forma podemos ver a relação que os tokens selecionados tem entre si: quem fica mais próximo de quem, quem fica mais distante, se ocorre mudanças dessas posições ao longo do tempo ou não, etc. Vale destacar que as imagens podem apresentar palavras a menos se o token não estiver presente em todos os modelos da série temporal. Ainda, os tokens serão dispersados conforme as palavras selecionadas, ou seja, não é porque um token apareceu próximo de outro que eles terão, necessariamente, similaridade entre si alta, pois esta visualização leva em consideração somente o espaço vetorial formado pelas palavras selecionadas. Em outras palavras: Se X está próximo de Y e distante de Z, X e Y não possuem, necessariamente, similaridade alta entre si, mas mostra que X está mais similar à Y do que à Z.</p>

</details>


## 7 - Comparação entre Palavras

<details>
  <summary><b>Informações <i>(clique para expandir)</i></b></summary>
  <h4>Exemplo de uso</h4>

  <p>Esta é uma das visualizações que explora um dos maiores potenciais de modelos Word2Vec: as analogias. Com elas podemos criar relações entre um token e outro e tentar replicar esta mesma relação com base em outro token para verificar o resultado. Para ficar mais didático, o exemplo mais popular é: "homem" está para "rei", assim como "mulher" está para o que? O modelo responderá adequadamente se a resposta for "rainha". Da mesma forma, analisando um pouco melhor a potencialidade desta funcionalidade: "homem" está para "mulher" assim como "tio" está para o que? Esperamos que seja tia, pois a relação que foi estipulada de "homem" até "mulher" é uma relação de gênero, a mesma relação deve ser aplicada a "tio" para encontrar "tia". Aconselha-se que se faça a análise dos vizinhos mais próximos dos tokens que serão utilizados na pesquisa, para verificar se o modelo está "entendendo bem" sobre o que está sendo tratado.</p>

  <img src="https://github.com/iaehistoriaUFSC/Repositorio_UFSC/blob/main/Word_Embeddings/Visualizacoes/img_src/Comparação Entre Palavras para WOKE_1_CFH_2017_2019_w2v_inc.png?raw=true" alt="imganalogia" />

  <p>Dessa forma podemos capturar de forma mais concreta possíveis viéses nos corpus utilizados para treinar os modelos, além de verificar a acurácia dos mesmos. É possível também estudar as mudanças de resultados ao longo do tempo.</p>

</details>

