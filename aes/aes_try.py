import base64
import pyaes
from PIL import Image
import io
import argparse

KEYS = {
    128: "THIS_IS_MY_KEY!!",
    192: "THIS_IS_MY_KEY!!_APPROVE",
    256: "THIS_IS_MY_KEY!!_DO_YOU_APPROVE?",
}


def img_to_bytes(path):
    with open(path, "rb") as image_file:
        image_bytes = image_file.read()
    return image_bytes


def main():
    parser = argparse.ArgumentParser(description="Img path receiver")
    parser.add_argument("key_size", help="Key size", type=int)
    parser.add_argument("message", help="Message")
    args = parser.parse_args()

    message = args.message

    # IMAGE TO BYTES
    print(f"Message is {message}")

    key = KEYS[args.key_size].encode("utf-8")
    print(key)

    aes_enc = pyaes.AESModeOfOperationCTR(key)

    enc_message = aes_enc.encrypt(message.encode("utf-8"))
    print(f"The enc_message is {enc_message}")

    aes_dec = pyaes.AESModeOfOperationCTR(key)

    dec_message = aes_dec.decrypt(enc_message)
    print(f"The dec_message is {dec_message}")


if __name__ == "__main__":
    main()
