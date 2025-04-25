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
    el oponente juega en el tablero central del tablero grande.

    Si se juega en la esquina superior derecha de un tablero pequeño,
    el oponente juega en el tablero de la esquina superior derecha del tablero grande.

    2. Si sucede que al jugador le toca jugar en un tablero ya lleno,
    puede ejegir jugar en cualquier otro tablero que esté disponible.

"""

"""Clase que representa el juego del metagato"""
class MetaGato(ModeloJuegoZT2):
    def inicializa(self):
        estado = {
            "tablero": [[[0]*3 for _ in range(3)] for _ in range(9)],
            "global": [[0]*3 for _ in range(3)],
            "activo": None
        }
        jugador_inicial = 1
        return estado, jugador_inicial

    def jugadas_legales(self, s, j):
        jugadas = []
        tableros = s["tableros"]
        tablero_activo = s["activo"]
        
        # Si no hay un tablero activo, se puede jugar en cualquiera que no esté ganado
        tableros_validos = []
        if tablero_activo is None:
            for i in range(9):
                if not self.tablero_completo(tableros[i]):
                    tableros_validos.append(i)
        else:
            if not self.tablero_completo(tableros[tablero_activo]):
                tableros_validos = [tablero_activo]
            else:
                for i in range(9):
                    if not self.tablero_completo(tableros[i]):
                        tableros_validos.append(i)

        # Buscar posiciones vacías dentro de los tableros válidos
        for t in tableros_validos:
            for fila in range(3):
                for col in range(3):
                    if tableros[t][fila][col] == 0:
                        jugadas.append((t, fila, col))
        return jugadas


    def transicion(self, s, a, j):
        pass

    def terminal(self, s):
        pass

    def ganancia(self, s):
        pass

def pprint_gato(s):
    simbolos = {1: 'X', -1: 'O', 0: ' '}
    tableros = estado["tablero"]

    def fila_de_superfila(i):
        fila = ""
        for bloque in range(3):
            idx = i // 3 * 3 + bloque
            fila += " | ".join(simbolos[x] for x in tableros[idx][i % 3])
            if bloque < 2:
                fila += " || "
        return fila

    for super_fila in range(3):
        for fila in range(3):
            print(fila_de_superfila(super_fila * 3 + fila))
        if super_fila < 2:
            print("=" * 35)

def tablero_completo(self, tablero):
    for fila in tablero:
        for celda in fila:
            if celda == 0:
                return False
    return True


if __name__ == '__main__':
    juego = MetaGato()
    estado, jugador = juego.inicializa()

    estado["tablero"][0][0][0] = 1   # X
    estado["tablero"][0][0][1] = -1  # O
    estado["tablero"][4][1][1] = 1   # X en el centro del tablero central
    pprint_gato(estado)


    