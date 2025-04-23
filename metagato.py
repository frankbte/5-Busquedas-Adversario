from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo

""" El metagato es una variante del juego del gato,
    este sigue las reglas basicas, pero con algunas 
    modificaciones:
    
    1. El tablero ya no es 3x3, ahora tenemos un tablero
    de 9x9 dividido en 9 secciones, cada una de 3x3. Es decir,
    tenemos un juego de gato en cada celda. El obejito es
    ganar en el tablero grande, formando una linea con de 
    3 tableros pequeños ganados.
    
    El estado inicial se vería algo así:
    
    0   1  2  |   9 10 11  |  18 19 20
    3   4  5  |  12 13 14  |  21 22 23
    6   7  8  |  15 16 17  |  24 25 26
    ----------+------------+------------
    27 28 29  |  36 37 38  |  45 46 47
    30 31 32  |  39 40 41  |  48 49 50
    33 34 35  |  42 43 44  |  51 52 53
    ----------+------------+------------
    54 55 56  |  63 64 65  |  72 73 74
    57 58 59  |  66 67 68  |  75 76 77
    60 61 62  |  69 70 71  |  78 79 80

    Reglas para jugar:

    1. El lugar donde juegas en el tablero pequeño determina
    a qué tablero pequeño tu oponente tiene que jugar en su siguiente turno.

    Por ejemplo: si se juega en la celda central de un tablero pequeño,
    el oponente tiene que jugar en el tablero pequeño central en su turno.

    Si se juega en la esquina superior derecha de un tablero pequeño,
    el oponente juega en el tablero dela esquina superior derecha del tablero grande.

    2. Si sucede que al jugador le toca jugar en un tablero ya lleno,
    puede ejegir jugar en cualquier otro tablero que esté disponible.

"""

class MetaGato(ModeloJuegoZT2):
    def inicializa(self):
        pass
