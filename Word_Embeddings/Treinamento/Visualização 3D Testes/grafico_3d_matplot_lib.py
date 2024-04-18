import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

# Cria a figura e o subplot 3D
fig = plt.figure(facecolor='white')
ax = fig.add_subplot(111, projection='3d', facecolor='white')

# Plota os pontos
ax.scatter(homem[0], homem[1], homem[2], color='blue', s=50, label='Homem')
ax.scatter(rei[0], rei[1], rei[2], color='red', s=50, label='Rei')
ax.scatter(mulher[0], mulher[1], mulher[2], color='blue', s=50, label='Mulher')
ax.scatter(rainha[0], rainha[1], rainha[2], color='red', s=50, label='Rainha')

legendas_palavras_relacionadas = ['Majestade','Princesa','Realeza','Coroa','Rainhas','Coroa']

for i,p in zip(legendas_palavras_relacionadas, palavras_relacionadas):
    ax.scatter(p[0], p[1], p[2], color='orange', s=20)
    ax.text(p[0]+0.15, p[1]+0.15, p[2]+0.15, i, color='black', ha='center', va='center',fontsize='6')


# Plota as setas
ax.quiver(homem[0], homem[1], homem[2], rei[0]-homem[0], rei[1]-homem[1], rei[2]-homem[2], color='cyan', label='Vetor de ligação')
ax.quiver(mulher[0], mulher[1], mulher[2], rainha[0]-mulher[0], rainha[1]-mulher[1], rainha[2]-mulher[2], color='cyan')

# Configuração dos rótulos dos eixos
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim([0,13])
ax.set_ylim([0,9])
ax.set_zlim([0,13])

ax.text(homem[0]+0.15, homem[1]+0.15, homem[2]+0.15, 'Homem', color='black', ha='center', va='center',fontsize='8')
ax.text(rei[0]+0.15, rei[1]+0.15, rei[2]+0.15, 'Rei', color='black', ha='center', va='center',fontsize='8')
ax.text(mulher[0]+0.15, mulher[1]+0.15, mulher[2]+0.15, 'Mulher', color='black', ha='center', va='center',fontsize='8')
ax.text(rainha[0]+0.15, rainha[1]+0.15, rainha[2]+0.15, 'Rainha', color='black', ha='center', va='center',fontsize='8')


# Remover o grid de fundo
ax.grid(False)

# Remover os eixos
ax.set_axis_off()

# Adiciona uma legenda
plt.legend()

# Exibe o gráfico
plt.show()
