def eea(a, b, x, y):
    if a == 0:
        x[0] = 0
        y[0] = 1
        return b

    x1, y1 = [0], [0]
    gcd = eea(b % a, a, x1, y1)

    x[0] = y1[0] - (b // a) * x1[0]
    y[0] = x1[0]

    return gcd


class Hill:
    def __init__(self):
        pass

    @staticmethod
    def create_matrix(text):
        ltext = list(map(int, text.split()))
        if len(ltext) != 4:
            return -1
        else:
            return [ltext[0:2], ltext[2:]]

    @staticmethod
    def det_matrix(matrix):
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return det

    @staticmethod
    def prune_text(text):
        ltext = []

        for char in text:
            if char.isalpha():
                ltext.append(char.upper())

        if len(ltext) % 2 != 0:
            ltext.append("X")

        return "".join(ltext)

    @staticmethod
    def gcd_validation(det):
        x, y = [1], [1]
        if eea(det % 26, 26, x, y) != 1:
            return -1
        return 0

    @staticmethod
    def gen_inverse(matrix):
        det = Hill.det_matrix(matrix)
        x, y = [0], [0]
        eea(det % 26, 26, x, y)
        det_inv = x[0] % 26

        f_row = [matrix[1][1] * det_inv, -matrix[0][1] * det_inv]
        s_row = [-matrix[1][0] * det_inv, matrix[0][0] * det_inv]
        attach_matrix = [f_row, s_row]
        return [[((x % 26) + 26) % 26 for x in piece] for piece in attach_matrix]

    def encrypt(self):
        ord_message = [ord(char) - 65 for char in self.message]
        enc_list = []

        for i in range(len(ord_message) // 2):
            a = (
                ord_message[2 * i] * self.matrix[0][0]
                + ord_message[2 * i + 1] * self.matrix[1][0]
            ) % 26
            b = (
                ord_message[2 * i] * self.matrix[0][1]
                + ord_message[2 * i + 1] * self.matrix[1][1]
            ) % 26
            enc_list.append(a)
            enc_list.append(b)
        enc_message = "".join([chr(char + 65) for char in enc_list])

        return enc_message

    def decrypt(self):
        ord_message = [ord(char) - 65 for char in self.message]
        inv_matrix = self.gen_inverse(self.matrix)

        dec_list = []
        for i in range(len(ord_message) // 2):
            a = (
                ord_message[2 * i] * inv_matrix[0][0]
                + ord_message[2 * i + 1] * inv_matrix[1][0]
            ) % 26
            b = (
                ord_message[2 * i] * inv_matrix[0][1]
                + ord_message[2 * i + 1] * inv_matrix[1][1]
            ) % 26
            dec_list.append(a)
            dec_list.append(b)
        dec_message = "".join([chr(char + 65) for char in dec_list])

        return dec_message

    def compute(self, mode, message, matrix):
        self.matrix = self.create_matrix(matrix)

        if self.matrix == -1:
            return -1

        self.det = self.det_matrix(self.matrix)

        if self.det == 0:
            return -2

        if self.gcd_validation(self.det) == -1:
            return -3

        self.message = self.prune_text(message)

        if mode == "encrypt":
            print("Encriptar")
            return self.encrypt()
        elif mode == "decrypt":
            print("Desencriptar")
            return self.decrypt()


def main():
    hill = Hill()

    while True:
        mode = input(
            "Escriba 0 para encriptar, 1 o cualquier otro carácter para desencriptar: "
        )
        mode = "encrypt" if mode == "0" else "decrypt"

        message = input("Escriba el mensaje que desea encriptar/desencriptar: ")
        matrix = input(
            """Inserte la matriz 2x2 que usará como clave para la ejecución del programa, \nsepare los números con espacios:\n"""
        )

        proc_message = hill.compute(mode, message, matrix)

        if proc_message == -1:
            print("La matriz insertada no cumple con las dimensiones requeridas (2x2)")
        elif proc_message == -2:
            print("La matriz insertada no tiene matriz inversa")
        elif proc_message == -3:
            print("La matriz insertada no tiene inversa modular (gcd(det A, 26) != 1)")
        else:
            print(f"El mensaje procesado es {proc_message}")


if __name__ == "__main__":
    main()
