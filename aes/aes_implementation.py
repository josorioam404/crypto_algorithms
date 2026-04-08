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
    parser.add_argument("input", help="Input image")
    parser.add_argument("key_size", help="Key size", choices=[128, 192, 256], type=int)
    args = parser.parse_args()

    key_size = args.key_size

    print(f"Executing with key of {key_size} bits")

    # IMAGE TO BYTES
    bytes_img = img_to_bytes(args.input)
    print(f"First 10 bytes of the original image: {bytes_img[:10]}")

    key = KEYS[key_size].encode("utf-8")

    aes_enc = pyaes.AESModeOfOperationCTR(key)

    # IMAGE BYTES TO ENCRYPTED BYTES
    enc_bytes_img = aes_enc.encrypt(bytes_img)

    print(f"First 10 enc with AES bytes of the image: {enc_bytes_img[:10]}")

    # ENCRYPTED BYTES TO BASE64
    base64_enc_bytes_img = base64.b64encode(enc_bytes_img)
    print(
        f"First 10 base64 encoded chars of the enc bytes of the image: {base64_enc_bytes_img[:10]}"
    )

    # BASE64 TO BITS
    bits_enc_img = "".join(format(byte, "08b") for byte in base64_enc_bytes_img)
    print(f"First 10 bits of the enc image: {bits_enc_img[:10]}")

    # BITS TO BASE64
    base64_enc_bytes_img = bytes(
        int(bits_enc_img[i : i + 8], 2) for i in range(0, len(bits_enc_img), 8)
    )
    print(
        f"First 10 base64 encoded chars of the enc bytes of the image: {base64_enc_bytes_img[:10]}"
    )

    # BASE64 TO BYTES
    enc_bytes_img = base64.b64decode(base64_enc_bytes_img)
    print(
        f"First 10 base64 decoded chars of the enc bytes of the image: {enc_bytes_img[:10]}"
    )

    # NEW INSTANCE FOR COUNTER RESET
    aes_dec = pyaes.AESModeOfOperationCTR(key)

    # ENC BYTES TO DEC BYTES
    dec_bytes_img = aes_dec.decrypt(enc_bytes_img)
    print(f"First 10 bytes dec with AES bytes of the image: {dec_bytes_img[:10]}")

    # OPEN IMAGE
    image = Image.open(io.BytesIO(dec_bytes_img))
    image.show()


if __name__ == "__main__":
    main()
