import plotly.graph_objects as go
import numpy as np

# Pontos no espaço 3D
homem = np.array([2, 6, 10])
rei = np.array([6, 8, 11])
mulher = np.array([4, 2, 7])
rainha = np.array([8, 4, 8])

# Vetores representando as relações
vetor_h_r = rei - homem
vetor_m_r = rainha - mulher

# Pontos adicionais próximos a "rainha"
palavras_relacionadas = [rainha + np.array([x, y, z]) for x, y, z in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]]

# Cria a figura
fig = go.Figure()

# Plota os pontos
fig.add_trace(go.Scatter3d(x=[homem[0]], y=[homem[1]], z=[homem[2]], mode='markers', marker=dict(color='blue', size=5), name='Homem'))
fig.add_trace(go.Scatter3d(x=[rei[0]], y=[rei[1]], z=[rei[2]], mode='markers', marker=dict(color='red', size=5), name='Rei'))
fig.add_trace(go.Scatter3d(x=[mulher[0]], y=[mulher[1]], z=[mulher[2]], mode='markers', marker=dict(color='blue', size=5), name='Mulher'))
fig.add_trace(go.Scatter3d(x=[rainha[0]], y=[rainha[1]], z=[rainha[2]], mode='markers', marker=dict(color='red', size=5), name='Rainha'))

# Plota os pontos adicionais próximos a "rainha" e adiciona legendas
legendas_palavras_relacionadas = ['Majestade','Princesa','Realeza','Coroa','Rainhas','Coroa']
for i, p in zip(legendas_palavras_relacionadas, palavras_relacionadas):
    fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode='markers', marker=dict(color='orange', size=2), name=i))

# Plota as setas
# fig.add_trace(go.Cone(x=[homem[0]], y=[homem[1]], z=[homem[2]], u=[vetor_h_r[0]], v=[vetor_h_r[1]], w=[vetor_h_r[2]], colorscale='Viridis', sizemode='absolute', sizeref=0.5, name='Vetor de ligação'))
# fig.add_trace(go.Cone(x=[mulher[0]], y=[mulher[1]], z=[mulher[2]], u=[vetor_m_r[0]], v=[vetor_m_r[1]], w=[vetor_m_r[2]], colorscale='Viridis', sizemode='absolute', sizeref=0.5))
fig.add_trace(go.Scatter3d(x=[homem[0],homem[1],homem[2]],y=[rei[0],rei[1],rei[2]], marker= dict(size=10),line = dict( color = "black",width = 6)))

# Configuração dos rótulos dos eixos
fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z', xaxis_range=[0,13], yaxis_range=[0,9], zaxis_range=[0,13]))

# Adiciona uma legenda
fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Remover os eixos
fig.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False))

# Exibe o gráfico
fig.show()
