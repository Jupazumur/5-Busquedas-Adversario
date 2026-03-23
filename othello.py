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
  
        jugadas_legales = []

        for casilla in range(64):
            if s[casilla] != 0:
                continue
            
            if not self._checar_captura(s, casilla, j):
                continue

            jugadas_legales.append(casilla)

        return jugadas_legales
    
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

# TODO: Combinar (de ser posible) _checar_captura y _fichas_a_voltear para no loopear dos veces

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
        s = list(s)
        s[a] = j
        
        fichas = self._fichas_a_voltear(s, a, j)
        for i in fichas:
            s[i] = j

        return tuple(s)
    
    def ganancia(self, s):
        if sum(s) > 0:
            return 1
        elif sum(s) < 0: 
            return -1
        else:
            return 0
    
    def terminal(self, s):
        # Es terminal en estas situaciones:
        # Tablero lleno
        # Jugador captura todas las fichas del oponente
        # No hay jugadas legales para ningun jugador
        
        if 0 not in s:
            return True
        
        elif 1 not in s or -1 not in s:
            return True
        
        elif self.jugadas_legales(s, 1) == self.jugadas_legales(s, -1) == []:
            return True
        
        return False