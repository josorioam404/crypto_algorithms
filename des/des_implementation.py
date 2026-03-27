import base64
import pyDes
from PIL import Image
import io


def img_to_bytes(path):
    with open(path, "rb") as image_file:
        image_bytes = image_file.read()
    return image_bytes


def main():
    # IMAGE TO BYTES
    bytes_img = img_to_bytes("puppy.jpg")
    print(f"First 10 bytes of the original image: {bytes_img[:10]}")

    des = pyDes.des(
        b"password",
        pyDes.CBC,
        IV=b"\0\0\0\0\0\0\0\0",
        pad=None,
        padmode=pyDes.PAD_PKCS5,
    )

    # IMAGE BYTES TO ENCRYPTED BYTES
    enc_bytes_img = des.encrypt(bytes_img)
    print(f"First 10 enc with DES bytes of the image: {enc_bytes_img[:10]}")

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

    # ENC BYTES TO DEC BYTES
    dec_bytes_img = des.decrypt(enc_bytes_img)
    print(f"First 10 bytes dec with DES bytes of the image: {dec_bytes_img[:10]}")

    # OPEN IMAGE
    image = Image.open(io.BytesIO(dec_bytes_img))
    image.show()


if __name__ == "__main__":
    main()
