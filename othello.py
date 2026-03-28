import juegos_simplificado as js
from othello_mapas import MAPA_ADYACENCIA as MAPA_ADY
import minimax

class Othello(js.JuegoZT2):
    
    def inicializa(self):
        # -1 es blanco, 1 es negro
        tablero = [0 for _ in range(8 * 8)]
        tablero[27] = -1
        tablero[28] = 1
        tablero[35] = 1
        tablero[36] = -1

        return tuple(tablero)
        
    def jugadas_legales(self, s, j):
        
        jugadas_legales = []

        for casilla in range(64):
            if s[casilla] != 0:
                continue
            
            if not self._checar_captura(s, casilla, j):
                continue

            jugadas_legales.append(casilla)

        return jugadas_legales if jugadas_legales != [] else [None]
    
    def _checar_captura(self, s, casilla, j):
        """
        True si en alguna dirección desde casilla hay una línea del
        oponente cerrada por una ficha del jugador.
        """
        for direccion, vecino in MAPA_ADY[casilla].items():
            
            if s[vecino] != -j:
                continue
            
            aux = vecino
            
            while direccion in MAPA_ADY[aux]:
                
                siguiente = MAPA_ADY[aux][direccion]

                if s[siguiente] == j:
                    return True
                
                if s[siguiente] != -j:
                    break
                
                aux = siguiente

        return False

# TODO: Combinar _checar_captura y _fichas_a_voltear para no loopear dos veces

    def _fichas_a_voltear(self, s, casilla, j):
        """
        Identifica para una casilla cuales fichas voltea una acción
        """
        fichas_a_voltear = []

        for direccion, vecino in MAPA_ADY[casilla].items():
            
            if s[vecino] != -j:
                continue

            aux = vecino
            temp = [vecino]

            while direccion in MAPA_ADY[aux]: 
                siguiente = MAPA_ADY[aux][direccion]
                
                if s[siguiente] == -j:
                    temp.append(siguiente)
    
                elif s[siguiente] == j:
                    fichas_a_voltear.extend(temp)
                    break
                    
                elif s[siguiente] == 0:
                    break

                aux = siguiente

        return fichas_a_voltear

    def sucesor(self, s, a, j):
        if a is None:
            return s
        
        s = list(s)
        s[a] = j
        
        fichas = self._fichas_a_voltear(s, a, j)
        for i in fichas:
            s[i] = j

        return tuple(s)
    
    def ganancia(self, s):
        sum_s = sum(s)

        if sum_s > 0:
            return 1
        
        elif sum_s < 0: 
            return -1

        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        
        elif 1 not in s or -1 not in s:
            return True
        
        elif self.jugadas_legales(s, 1) == [None] and self.jugadas_legales(s, -1) == [None]:
            return True
        
        return False

class InterfaceOthello(js.JuegoInterface):

    # Para este prototipo O es blanco, X es negro. Se tiene que hacer que negro siempre empiece.
    def muestra_estado(self, s):
        """
        Muestra el estado del juego
        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' for x in s]
        print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 ')
        for i in range(8):
            print('|'.join(a[8 * i:8 * (i + 1)]))
            print('---+---+---+---+---+---+---+---\n')
    
    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego
        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

def evalua_aleatorio(estado):
    from random import uniform
    """
    PARA PRUEBAS
    Definitivamente evalua
    """
    return uniform(-1, 1)

 # Heurísticas de:
 # https://doi.org/10.1007/978-1-4842-3357-3_16

def dif_piezas(estado):
    blanco = estado.count(-1)
    negro = estado.count(1)

    dif = abs(blanco - negro)
    suma = blanco + negro

    return dif / suma

def dif_piezas_2(estado):
    blanco = estado.count(-1)
    negro = estado.count(1)

    #dif = abs(blanco - negro)
    suma = blanco + negro

    if negro > blanco:
        return 100 * negro / suma
    elif negro < blanco:
        return 100 * blanco / suma
    else:
        return 0
    
def ocupacion_esquinas(estado):
    from othello_mapas import ESQUINAS
    blanco = 0
    negro = 0

    for esquina in ESQUINAS:
        if estado[esquina] == 0:
            continue
        elif estado[esquina] == -1:
            blanco += 1
        elif estado[esquina] == 1:
            negro += 1
    
    return 25*negro - 25*blanco
    
if __name__ == '__main__':

    # Negro siempre empieza, entonces J2 es el humano por ahora.
    cfg = {
        "Jugador 1": "Negamax",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",   #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10,
        "ordena": None,    #Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": ocupacion_esquinas       #Puede ser None o una función f(estado) -> número entre -1 y 1
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        
        elif cadena == "Tiempo":
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceOthello(
        Othello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("OTHELLO")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()