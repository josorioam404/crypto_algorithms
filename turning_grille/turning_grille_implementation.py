import sys


class TurningGrille:
    def __init__(self, dimension, rotation, hole_list):
        self.dimension = dimension
        self.rotation = rotation
        self.turning_grille = [[" "] * dimension for _ in range(dimension)]
        self.hole_list = self.parse_hole_list(hole_list)

    @staticmethod
    def parse_hole_list(hole_list):
        indexes = []
        rows = hole_list.split(";")
        for i, row in enumerate(rows):
            row = row.strip("[]")
            cells = row.split(",")
            pair = [(i, int(x)) for x in cells if x.isdigit()]
            indexes.extend(pair)
        return indexes

    def populate_turning_grille(self, mode, message):
        if mode == "encrypt":
            pad = 0
            for turn in range(4):
                for i, (x, y) in enumerate(self.hole_list):
                    if self.turning_grille[x][y] != " ":
                        pad += 1
                    else:
                        self.turning_grille[x][y] = message[
                            i + (turn * len(self.hole_list) - pad)
                        ]
                self.hole_list = self.rotate_list(
                    self.dimension, self.rotation, self.hole_list
                )

        elif mode == "decrypt":
            for i, char in enumerate(message):
                self.turning_grille[i // self.dimension][i % self.dimension] = char

    @staticmethod
    def prune_message(text, req_length):
        pruned = []
        for char in text:
            if char.isalpha():
                pruned.append(char.upper())
        pruned = pruned[:req_length]
        if len(pruned) != req_length:
            pruned.extend(["X"] * (req_length - len(pruned)))
        return "".join(pruned)

    @staticmethod
    def rotate_list(dimension, rotation, num_list):
        if rotation == "clockwise":
            num_list = [(y, dimension - 1 - x) for (x, y) in num_list]
        else:
            num_list = [(dimension - 1 - y, x) for (x, y) in num_list]
        num_list.sort()
        return num_list

    def encrypt(self, message):
        self.populate_turning_grille("encrypt", message)
        return "".join("".join(x) for x in self.turning_grille)

    def decrypt(self, message):
        self.populate_turning_grille("decrypt", message)
        dec_list = []
        for turn in range(4):
            for x, y in self.hole_list:
                dec_list.append(self.turning_grille[x][y])
            self.hole_list = self.rotate_list(
                self.dimension, self.rotation, self.hole_list
            )

        return "".join(dec_list)

    def compute(self, mode, message):
        message = self.prune_message(message, self.dimension**2)
        if mode == "encrypt":
            return self.encrypt(message)
        elif mode == "decrypt":
            return self.decrypt(message)
        else:
            return "ERROR: Invalid mode"


def main():
    error_message = """No se introdujeron los parámetros necesarios para el programa.
        Parámetros:
        1) Tamaño de la retícula.
        2) Dirección de rotación (1 - clockwise, 0 - anticlockwise).
        3) Modo de ejecución (1 - ciframiento, 0 - desciframiento).
        4) Lista de hoyos (asegurese de usar comillas, formato (cada conjunto entre [] simboliza una fila):"[1,2,3];[];[4,5];...").
        5) Mensaje a (de)cifrar.
            """

    if len(sys.argv) != 6:
        print(error_message)
        return -1

    dimension = int(sys.argv[1])

    if sys.argv[2] == "1":
        rotation = "clockwise"
    elif sys.argv[2] == "0":
        rotation = "anti-clockwise"
    else:
        print("ERROR: No se introdujo un modo de ejecución válido")
        print(error_message)
        return -1

    if sys.argv[3] == "1":
        print(f"Se introdujo modo = {sys.argv[3]}, ciframiento")
        mode = "encrypt"
    elif sys.argv[3] == "0":
        print(f"Se introdujo modo = {sys.argv[3]}, desciframiento")
        mode = "decrypt"
    else:
        print("ERROR: No se introdujo un modo de ejecución válido")
        print(error_message)
        return -1

    hole_list = sys.argv[4]
    message = sys.argv[5]

    turning_grille = TurningGrille(dimension, rotation, hole_list)
    if turning_grille == -1:
        print("ERROR: No se introdujo el número de hoyos requeridos")
        print(error_message)

    print(f"""
    El tamaño de la grilla giratoria es {dimension}x{dimension}
    El modo de ejecución es {mode} y la dirección de rotación es {rotation}
    El mensaje que se procesará es {message}
    """)

    proc_message = turning_grille.compute(mode, message)
    print(f"El mensaje procesado es {proc_message}")


if __name__ == "__main__":
    main()
