from visualizacoes_woke import *

tipo_treinamento = escolherTipoTreinamento()
limparConsole()

treinamento = escolherTreinamento(tipo_treinamento)
limparConsole()
print(treinamento,'ESCOLHIDO')
modelo = escolherModelos(caminho_pasta_treino=treinamento)
limparConsole()
print(modelo,'ESCOLHIDO')

descompactarPastaModelos(modelo,excluir_zip=True)

limparConsole()

caminhos_modelos_temporais_escolhidos = escolherModelosTemporais(modelo)
for m in caminhos_modelos_temporais_escolhidos:
    print(os.path.basename(m))

modelos_carregados = carregarModelos(lista_caminhos_modelos_temporais=caminhos_modelos_temporais_escolhidos)

limparConsole()

acao = ''

while acao != '0':
    acao = escolherAcao(os.path.basename(tipo_treinamento))
    limparConsole()
    if acao == 'Similaridades ao decorrer do tempo':
        SimilaridadeSemanticaAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
    elif acao == 'Campos Semânticos ao decorrer do tempo':
        campoSemanticoAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
    elif acao == 'Mapa de calor das similaridades ao decorrer do tempo':
        pass
    
    acao = escolherAcao(os.path.basename(tipo_treinamento))