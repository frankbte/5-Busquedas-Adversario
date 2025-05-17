from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores, minimax
from minimax import jugador_negamax
from minimax import minimax_iterativo

import random

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
        """ Representamos el estado como un diccionario con 3 llaves donde,
            tablero: representa la lista de los 9 tableros pequeños
            global: represtenta el tablero grande, para tener control de quien gana la partida
            activo: tablero acitvo para el siguiente jugador. Si es None, se puede jugar en cualquier tablero,
                    de otra forma un numero del 0 al 8 representa el tablero en que se puede jugar."""
        
        estado = {
            "tablero": [[[0]*3 for _ in range(3)] for _ in range(9)],
            "global": [[0]*3 for _ in range(3)],
            "activo": None
        }
        jugador_inicial = 1 #jugador inicial por defecto
        return estado, jugador_inicial

    def jugadas_legales(self, s, j):
        jugadas = [] #lista para guardar las jugadas legales
        tablero = s["tablero"]
        tablero_activo = s["activo"]
        
        #si no hay un tablero activo, se puede jugar en cualquiera que no esté ganado
        tableros_validos = []
        if tablero_activo is None: #si no hay tablero activo, se puede jugar en cualquiera
            for i in range(9):
                if not self.tablero_completo(tablero[i]): #checamos si no está completo
                    tableros_validos.append(i)
        else: 
            if not self.tablero_completo(tablero[tablero_activo]): #checamos si podemos jugar en el tablero activo
                tableros_validos = [tablero_activo]
            else: #si el tablero activo está completo, se puede jugar en cualquier otro
                for i in range(9):
                    if not self.tablero_completo(tablero[i]):
                        tableros_validos.append(i)

        #buscamos las posiciones vacías dentro de los tableros válidos
        for t in tableros_validos:
            for fila in range(3):
                for col in range(3):
                    if tablero[t][fila][col] == 0:
                        jugadas.append((t, fila, col))
        return jugadas


    def transicion(self, s, a, j):
        nuevo_estado = {
            "tablero": [[fila[:] for fila in tablero] for tablero in s["tablero"]],
            "global": [fila[:] for fila in s["global"]],
            "activo": s["activo"]
        }
        
        tablero_idx, fila, columna = a
        #creamos una copia del estado actual
        nuevo_estado["tablero"][tablero_idx][fila][columna] = j

        #revisamos si el tablero pequeño ya se ganó
        tablero_actual = nuevo_estado["tablero"][tablero_idx]
        if self.gana_tablero(tablero_actual, j):
            nuevo_estado["global"][tablero_idx // 3][tablero_idx % 3] = j

        #actualizamos el tablero activo
        siguiente_tablero = fila * 3 + columna

        #revisamos si el siguiente tablero ya está ganado o lleno
        tablero_siguiente = nuevo_estado["tablero"][siguiente_tablero] if 0 <= siguiente_tablero < 9 else None
        if tablero_siguiente:
            lleno = all(celda != 0 for fila in tablero_siguiente for celda in fila)
            ganado = nuevo_estado["global"][siguiente_tablero // 3][siguiente_tablero % 3] != 0
        else:
            lleno = True
            ganado = True

        if lleno or ganado:
            nuevo_estado["activo"] = None  # Puede jugar en cualquier tablero disponible
        else:
            nuevo_estado["activo"] = siguiente_tablero

        return nuevo_estado
    
    def tablero_completo(self, tablero):
        for fila in tablero:
            for celda in fila:
                if celda == 0:
                    return False
        return True
    
    def gana_tablero(self, tablero, jugador):
        """Revisamos si el jugador ganó en un tablero pequeño 3x3"""
        for fila in tablero:
            if all(celda == jugador for celda in fila):
                return True
        for col in range(3):
            if all(fila[col] == jugador for fila in tablero):
                return True
        
        if all(tablero[i][i] == jugador for i in range(3)):
            return True
        if all(tablero[i][2-i] == jugador for i in range(3)):
            return True
        return False


    def terminal(self, s):
        # Si hay un ganador, el juego terminó
        if self.ganancia(s) != 0:
            return True
        
        # Verificar si hay al menos un sub-tablero sin ganador y sin empate
        for i in range(3):
            for j in range(3):
                if s["global"][i][j] == 0:
                    return False  # Hay al menos un espacio disponible

        # Si no hay espacios en el global, el juego terminó en empate
        return True

    def ganancia(self, s):
        global_tablero = s["global"]
        
        # Revisar filas
        for fila in global_tablero:
            if fila[0] == fila[1] == fila[2] != 0:
                return fila[0]
        
        # Revisar columnas
        for col in range(3):
            if global_tablero[0][col] == global_tablero[1][col] == global_tablero[2][col] != 0:
                return global_tablero[0][col]
        
        # Revisar diagonales
        if global_tablero[0][0] == global_tablero[1][1] == global_tablero[2][2] != 0:
            return global_tablero[0][0]
        if global_tablero[0][2] == global_tablero[1][1] == global_tablero[2][0] != 0:
            return global_tablero[0][2]
        
        # Si no hay ganador, devolver 0
        return 0


        
def pprint_gato(s):
    simbolos = {1: 'X', -1: 'O', 0: ' '}
    tableros = s["tablero"]

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

# ──────────────────────────────────────────────────────────────────────────────
#  Funciones de apoyo para jugar Meta‑Gato en modo manual
# ──────────────────────────────────────────────────────────────────────────────

def pprint_metagato(s):
    """Imprime el estado de los 9 tableros pequeños y el tablero global."""
    signos = {0: ".", 1: "X", 2: "O"}
    tableros = s["tablero"]

    # Dibujamos los 9 tableros en una cuadrícula 3×3
    for bloque_fila in range(3):
        for fila in range(3):
            linea = []
            for bloque_col in range(3):
                idx = bloque_fila * 3 + bloque_col
                for col in range(3):
                    linea.append(signos[tableros[idx][fila][col]])
                if bloque_col < 2:
                    linea.append("│")          # separador vertical entre tableros
            print(" ".join(linea))
        if bloque_fila < 2:
            print("─" * 23)                   # separador horizontal entre filas de tableros

    # Tablero global (para ver quién ha ganado cada sub‑tablero)
    print("\nTablero global:")
    for fila in s["global"]:
        print(" ".join(signos[c] for c in fila))
    print()  # línea en blanco al final


def jugador_manual_metagato(juego, s, j):
    """
    Jugador manual para Meta‑Gato.
    
    El usuario puede introducir:
        • Tres números separados por espacio  ->  tablero fila columna
        • Un índice de la lista mostrada      ->  número simple
    """
    jugada = None
    print("Estado actual:")
    pprint_metagato(s)

    if s["activo"] is None:
        print("Puedes jugar en *cualquier* tablero no terminado.")
    else:
        print(f"Debes jugar en el tablero pequeño {s['activo']}.")

    print("Turno del jugador:", j, "(X = 1, O = 2)")
    jugadas = juego.jugadas_legales(s, j)

    # Mostramos las jugadas con un índice para que sea más cómodo elegir
    print("Jugadas legales:")
    for idx, (t, f, c) in enumerate(jugadas):
        print(f"  {idx:2d}: tablero {t}, fila {f}, col {c}")

    while jugada not in jugadas:
        entrada = input(
            "\n→ Escribe 'tablero fila col' (e.g. 4 1 2) o el número de índice: "
        ).strip().split()

        try:
            # Caso 1: un solo número ⇒ lo interpretamos como índice
            if len(entrada) == 1:
                idx = int(entrada[0])
                jugada = jugadas[idx]  # se lanza IndexError si idx no válido

            # Caso 2: tres números ⇒ (tablero, fila, col)
            elif len(entrada) == 3:
                t, f, c = map(int, entrada)
                jugada = (t, f, c)

            else:
                raise ValueError

        except (ValueError, IndexError):
            print("Entrada no válida. Intenta de nuevo…")
            jugada = None  # forzamos repetir el bucle

        if jugada not in jugadas:
            print("→ Esa jugada no es legal en este momento.")

    return jugada

def jugador_aleatorio_metagato(juego, s, j):
    """
    Jugador aleatorio para el juego del MetaGato.
    """
    jugadas = juego.jugadas_legales(s, j)
    return random.choice(jugadas)

def jugador_minimax_metagato(juego, s, j):

    return minimax(juego, s, j)


def juega_Metagato(jugador='X'):
    """
    Juega el juego del gato

    """
    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = MetaGato()
    
    print("El juego del gato")
    print(f"Las 'X' siempre empiezan y tu juegas con {jugador}")
    
    estado, jugador = juego.inicializa()

    while not juego.terminal(estado):
        if jugador == 1:
            accion = jugador_manual_metagato(juego, estado, jugador)
        else:
            accion = jugador_aleatorio_metagato(juego, estado, jugador)

        estado = juego.transicion(estado, accion, jugador)
        jugador = 3 - jugador  # alternar 1 ↔ 2

        
if __name__ == '__main__':
    juega_Metagato('O')

"""
if __name__ == "__main__":
    juego = MetaGato()
    estado, jugador_inicial = juego.inicializa()

    #estado inicial
    print("Estado inicial del juego:")
    pprint_gato(estado)

    #el jugador inicial hace su jugada
    accion = (0, 1, 1)  # (tablero, fila, columna)
    print(f"Jugador {jugador_inicial} hace jugada en {accion}")
    estado = juego.transicion(estado, accion, jugador_inicial)
    pprint_gato(estado)

    # Cambio manual de jugador (esto por mientras desarrollo la heuristica)
    jugador_siguiente = -jugador_inicial

    # Jugador 2 hace su jugada
    accion = (1, 2, 0)
    print(f"Jugador {jugador_siguiente} hace jugada en {accion}")
    estado = juego.transicion(estado, accion, jugador_siguiente)
    pprint_gato(estado)

    # Continuamos...
    accion = (2, 0, 0)
    print(f"Jugador {jugador_inicial} hace jugada en {accion}")
    estado = juego.transicion(estado, accion, jugador_inicial)
    pprint_gato(estado)

    accion = (3, 1, 1)
    print(f"Jugador {jugador_siguiente} hace jugada en {accion}")
    estado = juego.transicion(estado, accion, jugador_siguiente)
    pprint_gato(estado)

    # Verificar si el juego ha terminado
    if juego.terminal(estado):
        print("El juego ha terminado.")
    else:
        print("El juego no ha terminado.")
    
    # Verificar quién es el ganador (si hay)
    ganador = juego.ganancia(estado)
    if ganador != 0:
        print(f"El ganador es el jugador: {ganador}")
    else:
        print("No hay ganador aún.")

    
"""