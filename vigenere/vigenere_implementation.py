import sys


class Vigenere:
    def __init__(self, t, key):
        self.tableau = self.generateTableau()
        self.t = int(t)
        self.key = key.upper()

    @staticmethod
    def generateTableau():
        matrix = []
        for i in range(26):
            row = []
            for j in range(26):
                char = ord("A") + (i + j) % 26
                row.append(chr(char))
            matrix.append(row)
        return matrix

    @staticmethod
    def generateKeyword(t, key, length):
        keyword = []
        l = len(key)
        read = l
        while length > 0:
            frame = ""
            for i in range(t):
                frame += key[l - read]
                read -= 1
                if read == 0:
                    read = l
            keyword.append(frame)
            length -= t
        return keyword

    @staticmethod
    def pruneText(text):
        pruned_text = ""
        for char in text:
            if char.isalpha():
                pruned_text += char.upper()
        return pruned_text

    @staticmethod
    def generateLtext(t, message):
        ltext = []
        length = len(message)
        l = length
        count = 0
        while length > 0:
            frame = ""
            for i in range(t):
                if (i + t * count) >= l:
                    frame += "X"
                else:
                    frame += message[i + t * count]
            count += 1
            ltext.append(frame)
            length -= t
        return ltext

    def encrypt(self, message):
        plaintext = self.generateLtext(self.t, message)
        enc_message = []
        for i in range(len(self.keyword)):
            frame = ""
            for j in range(self.t):
                x = ord(self.keyword[i][j]) - 65
                y = ord(plaintext[i][j]) - 65
                frame += self.tableau[x][y]
            enc_message.append(frame)
        enc_text = ["".join(piece) for piece in enc_message]
        enc_text = " ".join(enc_text)
        return enc_text

    def decrypt(self, message):
        enc_message = self.generateLtext(self.t, message)
        dec_message = []
        for i in range(len(self.keyword)):
            frame = ""
            for j in range(self.t):
                x = ord(self.keyword[i][j]) - 65
                y = ord(enc_message[i][j]) - 65
                frame += self.tableau[0][(y - x) % 26]
            dec_message.append(frame)
        dec_text = ["".join(piece) for piece in dec_message]
        dec_text = " ".join(dec_text)
        return dec_text

    def compute(self, mode, message):
        message = self.pruneText(message)
        self.keyword = self.generateKeyword(self.t, self.key, len(message))
        if mode == 0:
            return self.encrypt(message)
        else:
            return self.decrypt(message)


def main():
    if len(sys.argv) < 5:
        print("""No se introdujeron los parámetros necesarios para el programa.
        Parámetros:
        1) Modo de ejecución (0 para ciframiento, cualquier otro para desciframiento)
        2) Clave de ejecución del algoritmo.
        3) Parámetro t para ejecución del algoritmo.
        4) Mensaje a cifrar/descifrar, puede contener espacios.
            """)
        return -1

    if int(sys.argv[1]) == 0:
        print(f"Se introdujo modo = {sys.argv[1]}, ciframiento")
    else:
        print(f"Se introdujo modo = {sys.argv[1]}, desciframiento")
    print(f"La clave en ejecución es {sys.argv[2]}")
    print(f"El parámetro t para vigenere es {sys.argv[3]}")
    message = "".join(sys.argv[4:])
    print(f"El mensaje que se procesará es {message}")

    vigenere = Vigenere(sys.argv[3], sys.argv[2])
    processed_message = vigenere.compute(int(sys.argv[1]), message)
    print(f"El mensaje obtenido tras el procesamiento es {processed_message}")


if __name__ == "__main__":
    main()
