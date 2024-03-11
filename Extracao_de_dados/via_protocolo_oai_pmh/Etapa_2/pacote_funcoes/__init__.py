try:
    from .funcoes_auxiliares import *
    from .funcoes_extracao_texto import *
    from .variaveis_utilizadas import *
    from .main_function import main
except ImportError as e:
    from funcoes_auxiliares import *
    from funcoes_extracao_texto import *
    from variaveis_utilizadas import *
    from main_function import main