import juegos_simplificado as js
from othello_mapas import MAPA_ADYACENCIA as MAPA_ADY
#import minimax

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
        # Para que una jugada sea legal:
        #    > Debe estar vacia (s[casilla] == 0).
        #    > Ser adyacente a una pieza del oponente en al menos una dirección.
        #    > Tener una pieza del jugador actual al final de una línea continua 
        #      de piezas del oponente empezando de esa casilla adyacente.
    
        jugadas_legales = []

        for casilla in range(64):
            if s[casilla] != 0:
                continue
            
            if self._checar_adyacentes(s[casilla], j):
                continue

            # TODO: anadir metodo para checar la ultima

        return jugadas_legales

    def _checar_adyacentes(casilla, j):
        """
        Checa las casillas adyacentes de una casilla.
        True si hay una ficha del oponente en una casilla adyacente.
        """
        casillas_adyacentes = MAPA_ADY[casilla].values()

        for casilla_destino in casillas_adyacentes:
            if casilla_destino == -j:
                return True

    def sucesor(self, s, a, j):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def ganancia(self, s):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0