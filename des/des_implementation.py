import base64
import pyDes
from PIL import Image
import io


def base64_img_encoding(path):
    with open(path, "rb") as image_file:
        image_bytes = image_file.read()
        encoded = base64.b64encode(image_bytes)
    return encoded


def base64_img_decoding(encoded_string):
    decoded_string = base64.b64decode(encoded_string)
    return decoded_string


def main():
    base64_enc_image = base64_img_encoding("puppy.jpg")
    print(f"First 10 base64 characters of the original image: {base64_enc_image[:10]}")

    des = pyDes.des(
        b"password",
        pyDes.CBC,
        IV=b"\0\0\0\0\0\0\0\0",
        pad=None,
        padmode=pyDes.PAD_PKCS5,
    )

    enc_image = des.encrypt(base64_enc_image)
    print(f"First 10 characters of the encoded image: {enc_image[:10]}")
    dec_image = des.decrypt(enc_image)
    print(f"First 10 base64 characters of the decoded image: {dec_image[:10]}")

    raw_image_bytes = base64_img_decoding(dec_image)
    image = Image.open(io.BytesIO(raw_image_bytes))
    image.show()


if __name__ == "__main__":
    main()
