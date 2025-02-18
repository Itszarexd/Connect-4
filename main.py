import tkinter as tk
from tkinter import messagebox
import pickle 

class GUI:
    ROWS = 6
    COLS = 7
    SAVE_FILE = "conecta4_checkpoint.pkl" 

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.title("Conecta 4")
        self.root.configure(bg="darkblue")

        self.label2 = tk.Label(self.root, text="Conecta 4", font=('Arial', 17), bg="black", fg="white", height=2)
        self.label2.pack(fill="x")
        
        self.label = tk.Label(self.root, text="Turno: Jugador 1 (Rojo)", font=('Arial', 16), bg="black", fg="white")
        self.label.pack(fill="x")
        
        self.play_button = tk.Button(self.root, text="Play", height=2, width=12, command=self.partida)
        self.play_button.place(x=180, y=200)

        
        self.restart_button = tk.Button(self.root, text="Restart", height=2, width=12, command=self.reiniciar_partida)
        self.restart_button.place(x=300, y=200)

        self.turno = 1
        self.tablero = [[0] * self.COLS for _ in range(self.ROWS)] 
        
        self.cargar_checkpoint()

        self.root.mainloop()

    def partida(self):
        self.root.configure(bg="white")
     
        self.buttonframe = tk.Frame(self.root, bg="grey")
        self.buttonframe.pack(fill='both', expand=True)

        for i in range(self.COLS):
            self.buttonframe.columnconfigure(i, weight=1)

        self.botones = []

        for r in range(self.ROWS):
            fila_botones = []
            for c in range(self.COLS):
                btn = tk.Button(self.buttonframe, height=2, width=5, bg="white",
                                command=lambda col=c: self.colocar_ficha(col))
                btn.grid(row=r, column=c, sticky="WE")
                fila_botones.append(btn)
            self.botones.append(fila_botones)

        self.restart_button = tk.Button(self.root, text="Restart", height=2, width=12, command=self.reiniciar_partida)
        self.restart_button.place(x=250, y=350)

        
        self.actualizar_interfaz()

        

    def colocar_ficha(self, col):
        for row in range(self.ROWS-1, -1, -1):
            if self.tablero[row][col] == 0:
                self.tablero[row][col] = self.turno
                color = "red" if self.turno == 1 else "yellow"
                self.botones[row][col].configure(bg=color)

                if self.verificar_ganador(row, col):
                    ganador = "Jugador 1 (Rojo)" if self.turno == 1 else "Jugador 2 (Amarillo)"
                    messagebox.showinfo("Fin del juego", f"¡{ganador} ha ganado!")
                    self.deshabilitar_tablero()
                else:
                    self.turno = 3 - self.turno 
                    self.label.config(text=f"Turno: Jugador {self.turno} ({'Rojo' if self.turno == 1 else 'Amarillo'})")

                self.guardar_checkpoint()  
                return

    def verificar_ganador(self, fila, col):
        jugador = self.tablero[fila][col]

        def contar(dx, dy):
            """Cuenta fichas en una dirección (dx, dy) y su opuesta (-dx, -dy)."""
            total = 1
            for d in [1, -1]:
                x, y = fila + dx * d, col + dy * d
                
                while 0 <= x < self.ROWS and 0 <= y < self.COLS and self.tablero[x][y] == jugador:
                    total += 1
                    x += dx * d
                    y += dy * d
            return total

        return (contar(1, 0) >= 4 or contar(0, 1) >= 4 or contar(1, 1) >= 4 or contar(1, -1) >= 4)

    def deshabilitar_tablero(self):
        """Deshabilita todos los botones tras una victoria."""
        for fila in self.botones:
            for btn in fila:
                btn.config(state="disabled")

    def reiniciar_partida(self):
        self.tablero = [[0] * self.COLS for _ in range(self.ROWS)]
        self.turno = 1
        self.label.config(text="Turno: Jugador 1 (Rojo)")

        for fila in self.botones:
            for btn in fila:
                btn.config(bg="white", state="normal")

        self.borrar_checkpoint()

    def actualizar_interfaz(self):
        """Restaura el estado del tablero en la interfaz tras cargar un checkpoint."""
        colores = {0: "white", 1: "red", 2: "yellow"}
        for r in range(self.ROWS):
            for c in range(self.COLS):
                self.botones[r][c].configure(bg=colores[self.tablero[r][c]])

    def guardar_checkpoint(self):
        """Guarda el estado actual del juego en un archivo."""
        estado = {"tablero": self.tablero, "turno": self.turno}
        with open(self.SAVE_FILE, "wb") as f:
            pickle.dump(estado, f)

    def cargar_checkpoint(self):
        """Carga el estado del juego desde un archivo si existe."""
        try:
            with open(self.SAVE_FILE, "rb") as f:
                estado = pickle.load(f)
                self.tablero = estado["tablero"]
                self.turno = estado["turno"]
                self.label.config(text=f"Turno: Jugador {self.turno} ({'Rojo' if self.turno == 1 else 'Amarillo'})")
        except FileNotFoundError:
            pass  

    def borrar_checkpoint(self):
        """Borra el archivo de checkpoint al reiniciar el juego."""
        import os
        if os.path.exists(self.SAVE_FILE):
            os.remove(self.SAVE_FILE)

def main():
    GUI()

if __name__ == '__main__':
    main()