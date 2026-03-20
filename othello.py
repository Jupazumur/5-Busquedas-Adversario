import juegos_simplificado as js
#import minimax


class Othello(js.JuegoZT2):

    # Diccionario de direcciones para el futuro
    DIRECCIONES = {
        (-1,  1), (0,  1), (1,  1),
        (-1,  0),          (1,  0),
        (-1, -1), (0, -1), (1, -1)
    }

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
            
                # TODO: anadir metodo para checar las ultimas dos

        return jugadas_legales

        #raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def sucesor(self, s, a, j):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def ganancia(self, s):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0