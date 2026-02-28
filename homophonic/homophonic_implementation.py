import random as rd


class Homophonic:
    def __init__(self, numbers, chars):
        self.layout = self.gen_layout(numbers, chars)

    @staticmethod
    def gen_layout(numbers, chars):
        numbers = list(range(numbers))
        rd.shuffle(numbers)

        letters = [chr(i + 65) for i in range(chars)]

        assign = {letter: [numbers[i]] for i, letter in enumerate(letters)}

        remainder = numbers[len(letters) :]
        for number in remainder:
            letter = rd.choice(letters)
            assign[letter].append(number)

        return assign

    @staticmethod
    def prune_text(mode, text):
        if mode == "encrypt":
            ltext = []
            for char in text:
                if char.isalpha():
                    ltext.append(char.upper())
            return ltext
        else:
            ltext = text.split(" ")
            for element in ltext:
                if element.isdigit() != 1:
                    ltext.remove(element)
            return ltext

    def encrypt(self):
        enc_list = []
        for char in self.message:
            num = rd.choice(self.layout.get(char))
            enc_list.append(num)
        return " ".join([str(x) for x in enc_list])

    def decrypt(self):
        dec_list = []

        for enc_num in self.message:
            for char, nums in self.layout.items():
                if int(enc_num) in nums:
                    dec_list.append(char)
                    break

        return "".join(dec_list)

    def compute(self, mode, message):
        self.message = self.prune_text(mode, message)
        if mode == "encrypt":
            print("Encriptar")
            return self.encrypt()
        elif mode == "decrypt":
            print("Desencriptar")
            return self.decrypt()
        else:
            return -1


def main():
    rd.seed(42)
    homophonic = Homophonic(100, 26)
    while True:
        mode = input(
            "Ingrese 0 si desea encriptar, 1 o cualquier otro caracter si desea desencriptar: "
        )
        mode = "encrypt" if mode == "0" else "decrypt"

        message = input("Inserte el mensaje que desea encriptar/desencriptar: ")

        proc_message = homophonic.compute(mode, message)
        print(f"El mensaje procesado es {proc_message}")


if __name__ == "__main__":
    main()
