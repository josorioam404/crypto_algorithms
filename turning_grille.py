import argparse
import re


class TurningGrille:
    def __init__(self, dimension, rotation, holes):
        self.rotation = rotation
        self.dimension = dimension
        self.hole_list = self._parse_holes(holes)

    @staticmethod
    def _parse_holes(holes):
        rows = re.findall(r"\[.*?\]", holes)
        indexes = []
        for i, row in enumerate(rows):
            nums = re.findall(r"\d+", row)
            for n in nums:
                indexes.append((i, int(n)))
        return indexes

    @staticmethod
    def _prune_text(text, req_length):
        pruned = [c.upper() for c in text if c.isalpha()]
        pruned = pruned[:req_length]
        if len(pruned) < req_length:
            pruned.extend(["X"] * (req_length - len(pruned)))
        return "".join(pruned)

    @staticmethod
    def _rotate(holes, rotation, dimension):
        if rotation == "clockwise":
            holes = [(y, dimension - 1 - x) for (x, y) in holes]
            holes.sort()
            return holes
        elif rotation == "anti-clockwise":
            holes = [(dimension - 1 - y, x) for (x, y) in holes]
            holes.sort()
            return holes
        else:
            raise ValueError("Mode de ejecución inválido")

    def _encrypt(self, message):
        grid = [[""] * self.dimension for _ in range(self.dimension)]
        holes = self.hole_list.copy()

        pointer = 0

        for _ in range(4):
            for x, y in holes:
                if grid[x][y] == "":
                    grid[x][y] = message[pointer]
                    pointer += 1
            holes = self._rotate(holes, self.rotation, self.dimension)

        return "".join("".join(row) for row in grid)

    def _decrypt(self, message):
        grid = [
            list(message[i : i + self.dimension])
            for i in range(0, len(message), self.dimension)
        ]
        holes = self.hole_list.copy()

        dec_message = []
        for _ in range(4):
            for x, y in holes:
                dec_message.append(grid[x][y])
            holes = self._rotate(holes, self.rotation, self.dimension)

        return "".join(dec_message)

    def compute(self, mode, message):
        message = self._prune_text(message, self.dimension**2)
        if mode == "encrypt":
            return self._encrypt(message)
        elif mode == "decrypt":
            return self._decrypt(message)
        else:
            raise ValueError("Mode de ejecución inválido")


def main():
    parser = argparse.ArgumentParser(
        description="Programa de cifrado/descifrado usando Turning Grille"
    )
    parser.add_argument("dimension", type=int, help="Tamaño de la retícula")
    parser.add_argument(
        "rotation",
        choices=[1, 0],
        type=int,
        help="Dirección de la rotación (1 = clockwise, 0 = anti-clockwise)",
    )
    parser.add_argument(
        "mode",
        choices=[1, 0],
        type=int,
        help="Modo de ejecución (1 = cifrar, 0 = descifrar)",
    )
    parser.add_argument(
        "holes",
        help="Lista de hoyos ([1,2,3] [] [1,2] ...)",
    )
    parser.add_argument(
        "message",
        help="Mensaje a (des)cifrar",
    )

    args = parser.parse_args()
    dimension = args.dimension
    rotation = "clockwise" if args.rotation == 1 else "anti-clockwise"
    mode = "encrypt" if args.mode == 1 else "decrypt"
    holes = args.holes
    message = args.message

    turning_grille = TurningGrille(dimension, rotation, holes)

    print(
        f"El mensaje a {'encriptar' if mode == 'encrypt' else 'desencriptar'} es:\n{message}"
    )

    proc_message = turning_grille.compute(mode, message)
    print(
        f"El mensaje {'encriptado' if mode == 'encrypt' else 'desencriptado'} es:\n{proc_message}"
    )


if __name__ == "__main__":
    main()
