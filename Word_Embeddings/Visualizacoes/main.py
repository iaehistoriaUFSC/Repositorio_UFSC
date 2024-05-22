from visualizacoes_woke import *

def main():
    organizarAmbiente()

    tipo_treinamento = escolherTipoTreinamento()
    limparConsole()

    treinamento = escolherTreinamento(pasta_tipo_treinamento=tipo_treinamento)
    limparConsole()

    modo_treinado = escolherModoTreinado(caminho_pasta_treino=treinamento)
    limparConsole()

    modelo = escolherModelos(caminho_pasta_modo_treino=modo_treinado)
    limparConsole()

    descompactarPastaModelos(modelo,excluir_zip=True)

    limparConsole()

    caminhos_modelos_temporais_escolhidos = escolherModelosTemporais(modelo)
    # for m in caminhos_modelos_temporais_escolhidos:
    #     print(os.path.basename(m))

    modelos_carregados = carregarModelos(lista_caminhos_modelos_temporais=caminhos_modelos_temporais_escolhidos)

    limparConsole()

    acao = escolherAcao(os.path.basename(tipo_treinamento))        

    while acao != 'Sair':
        limparConsole()
        if acao == 'Gráfico das similaridades ao decorrer do tempo':
            SimilaridadesAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
        elif acao == 'Vizinhos mais próximos ao decorrer do tempo':
            VizinhosMaisProximosAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
        elif acao == 'Mapa de calor das similaridades ao decorrer do tempo':
            MapaDeCalorSimilaridadesAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
        elif acao == 'Frequência de Palavras ao decorrer do tempo':
            FrequenciaDePalavrasAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
        else:
            break
        acao = escolherAcao(os.path.basename(tipo_treinamento))

    limparConsole()

    print('\n\n\tPrograma finalizado!\n\n')
