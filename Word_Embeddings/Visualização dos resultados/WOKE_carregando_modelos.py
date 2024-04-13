from WOKE_bibliotecas import *

print('\n\tCarregando os modelos pré-treinados baixados...')

caminho = '/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo'

# Carregando modelos WOKE Skip-Gram
try:
  print('\n\nCarregando modelos WOKE Skip-Gram...')
  word2vec_woke_hst_sg_1000 = joblib.load(caminho+'/word2vec_woke_hst_sg_1000.joblib').wv
  word2vec_woke_hst_sg_400 = joblib.load(caminho+'/word2vec_woke_hst_sg_400.joblib').wv
  word2vec_woke_hst_sg_700 = joblib.load(caminho+'/word2vec_woke_hst_sg_700.joblib').wv
except:
  print('\nProblema ao carregar modelos WOKE Skip-Gram.\n\t-->Verificar arquivo de "Problemas durante execução.txt"')
  erro = 'Descrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'  
  with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    f.write('Problema ao carregar modelos WOKE Skip-Gram'+'\n'+erro+'\n\n')
    f.close()
  time.sleep(2)
else:
  print('\n')
  print('-'*100)
  print('Modelos Skip-Gram 400D, 700D e 1000D do WOKE carregados com sucesso!')
  print('-'*100)

# Carregando modelos WOKE CBOW
try:
  print('\n\nCarregando modelos WOKE CBOW...')
  word2vec_woke_hst_cbow_1000 = joblib.load(caminho+'/word2vec_woke_hst_cbow_1000.joblib').wv
  word2vec_woke_hst_cbow_400 = joblib.load(caminho+'/word2vec_woke_hst_cbow_400.joblib').wv
  word2vec_woke_hst_cbow_700 = joblib.load(caminho+'/word2vec_woke_hst_cbow_700.joblib').wv
except:
  print('\nProblema ao carregar modelos WOKE CBOW.\n\t-->Verificar arquivo de "Problemas durante execução.txt"')
  erro = 'Descrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'  
  with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    f.write('Problema ao carregar modelos WOKE CBOW'+'\n'+erro+'\n\n')
    f.close()
  time.sleep(2)
else:
  print('\n')
  print('-'*100)
  print('Modelos CBOW 400D, 700D e 1000D do WOKE carregados com sucesso!')
  print('-'*100)


# Carregando modelo Nonce2Vec WOKE Skip-Gram
try:
  print('\n\nCarregando modelo N2V WOKE SKIP-GRAM...')
  nonce2vec_woke_hst_sg_400 = joblib.load(caminho+'/nonce2vec_woke_hst_sg_400.joblib').wv
except:
  print('\nProblema ao carregar modelo N2V WOKE SKIP-GRAM.\n\t-->Verificar arquivo de "Problemas durante execução.txt"')
  erro = 'Descrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'  
  with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    f.write('Problema ao carregar modelos WOKE CBOW'+'\n'+erro+'\n\n')
    f.close()
  time.sleep(2)
else:
  print('\n')
  print('-'*100)
  print('Modelo N2V WOKE SKIP-GRAM carregado com sucesso!')
  print('-'*100)

# Carregando modelo Nonce2Vec WOKE CBOW
try:
  print('\n\nCarregando modelo N2V WOKE CBOW...')
  nonce2vec_woke_hst_cbow_400 = joblib.load(caminho+'/nonce2vec_woke_hst_cbow_400.joblib').wv
except:
  print('\nProblema ao carregar modelo N2V WOKE CBOW.\n\t-->Verificar arquivo de "Problemas durante execução.txt"')
  erro = 'Descrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'  
  with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    f.write('Problema ao carregar modelos WOKE CBOW'+'\n'+erro+'\n\n')
    f.close()
  time.sleep(2)
else:
  print('\n')
  print('-'*100)
  print('Modelo N2V WOKE CBOW carregado com sucesso!')
  print('-'*100)


# Carregando info dos modelos
try:
  print('\n\nCarregando informação dos modelos...')
  info = joblib.load('/content/drive/MyDrive/Programa - Repositório Institucional UFSC/Word Embeddings/Treinamento do nosso modelo/Visualização dos resultados/info.joblib')
except:
  print('\nProblema ao carregar informação dos modelos.\n\t-->Verificar arquivo de "Problemas durante execução.txt"')
  erro = 'Descrição do erro --> '+str(sys.exc_info()[0].__name__)+": "+str(sys.exc_info()[1])+'.'  
  with open('Problemas durante execução.txt','a',encoding='utf-8') as f:
    f.write('Problema ao carregar informação dos modelos'+'\n'+erro+'\n\n')
    f.close()
  time.sleep(2)
else:
  print('\n')
  print('-'*100)
  print('Informações carregadas com sucesso!')
  print('-'*100)

time.sleep(2)