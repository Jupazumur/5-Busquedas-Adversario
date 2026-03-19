import juegos_simplificado as js
#import minimax

class Othello(js.JuegoZT2):
    def inicializa(self):
        return tuple([0 for _ in range(8 * 8)])
        
    def jugadas_legales(self, s, j):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def sucesor(self, s, a, j):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def ganancia(self, s):
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0