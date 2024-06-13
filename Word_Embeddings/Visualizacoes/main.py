from visualizacoes_woke import *

def main():    
    organizarAmbiente()
    parar_programa = False

    limparConsole()
    tipo_treinamento = escolherTipoTreinamento()
    while tipo_treinamento != '0' and not parar_programa:
        limparConsole()
        treinamento = escolherTreinamento(pasta_tipo_treinamento=tipo_treinamento)
        if treinamento == '0':
            parar_programa = True
            break
        while treinamento != '-1' and not parar_programa:                     
            limparConsole()
            modo_treinado = escolherModoTreinado(caminho_pasta_treino=treinamento)
            if modo_treinado == 0:
                parar_programa = True
                break
            while modo_treinado != '-1' and not parar_programa:            
                limparConsole()
                modelo = escolherModelos(caminho_pasta_modo_treino=modo_treinado)
                if modelo == '0':
                    parar_programa = True
                    break
                while modelo != '-1' and not parar_programa:                    
                    limparConsole()

                    descompactarPastaModelos(modelo,excluir_zip=True)

                    limparConsole()

                    caminhos_modelos_temporais_escolhidos = escolherModelosTemporais(modelo)
                    if caminhos_modelos_temporais_escolhidos == '0':
                        print('PARAR PROGRAMA TRUE')
                        parar_programa = True
                        break
                    while caminhos_modelos_temporais_escolhidos not in ['-1','0'] and not parar_programa:                        

                        modelos_carregados = carregarModelos(lista_caminhos_modelos_temporais=caminhos_modelos_temporais_escolhidos)

                        limparConsole()

                        acao = escolherAcao(os.path.basename(tipo_treinamento))        
                        if acao == '0':
                            parar_programa = True
                            break
                        while acao != '-1' and not parar_programa:
                            limparConsole()
                            if os.path.basename(tipo_treinamento) == 'Com séries temporais':
                                if acao == 'Gráfico das similaridades ao decorrer do tempo':
                                    SimilaridadesAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Vizinhos mais próximos ao decorrer do tempo':
                                    VizinhosMaisProximosAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Mapa de calor das similaridades ao decorrer do tempo':
                                    MapaDeCalorSimilaridadesAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Estratos do Tempo':
                                    EstratosDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Frequência de Palavras ao decorrer do tempo':
                                    FrequenciaDePalavrasAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Vetores de Palavras':
                                    VetoresDePalavrasAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Comparação entre Palavras':
                                    ComparacaoEntrePalavrasAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Mudança de Palavras ao decorrer do tempo':
                                    MudancaDePalavrasAoDecorrerDoTempo(modelos_treinados=modelos_carregados)
                                elif acao == 'Rede dinâmica dos campos semânticos ao decorrer do tempo':
                                    RedeDinamicaCampoSemantico(modelos_treinados=modelos_carregados)
                                elif acao == 'Elemento que não combina dentre os demais':
                                    ElementoQueNaoCombina(modelos_treinados=modelos_carregados)
                                else:
                                    break                                
                            acao = escolherAcao(os.path.basename(tipo_treinamento))
                            if acao == '0':
                                parar_programa = True
                                break
                        if not parar_programa:
                            limparConsole()
                            caminhos_modelos_temporais_escolhidos = escolherModelosTemporais(modelo)
                        else:
                            break
                    if not parar_programa:
                        limparConsole()
                        modelo = escolherModelos(caminho_pasta_modo_treino=modo_treinado)
                    else:
                        break
                if not parar_programa:
                    limparConsole()
                    modo_treinado = escolherModoTreinado(caminho_pasta_treino=treinamento)
                else:
                    break
            if not parar_programa:
                limparConsole()
                treinamento = escolherTreinamento(pasta_tipo_treinamento=tipo_treinamento)
            else:
                break
        if not parar_programa:
            limparConsole()
            tipo_treinamento = escolherTipoTreinamento()
        else:
            break       

    limparConsole()

    print('\n\n\tPrograma finalizado!\n\n')
