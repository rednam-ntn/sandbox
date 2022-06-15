#%%
from pdf2image import convert_from_bytes
import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import json


#%%


def convert_pdf_to_gray_img(
    pdfPath, words_pdf=[], WIDTH=1600, HEIGHT=2200, dpi=300, forkey=False, toGray=True,
):
    """ return a gray image array for cv2 processing """
    # outName = pdfPath.split('/')[-1].split('.')[0]
    try:
        with open(pdfPath, "rb") as file:
            f = file.read()
            images = convert_from_bytes(f, dpi=dpi)
            if forkey:
                if len(words_pdf) >= 2:
                    if len(words_pdf[1]) <= 3:
                        images = [images[0]]
                    else:
                        pass
                else:
                    pass

            full_image = []
            for image in images:
                openCV_img = np.array(image.convert("RGB"))
                # convert RGB to BGR
                openCV_img = openCV_img[:, :, ::-1].copy()
                # convert to grayscale
                if toGray:
                    openCV_img = cv2.cvtColor(openCV_img, cv2.COLOR_BGR2GRAY)
                openCV_img = cv2.resize(openCV_img, (WIDTH, HEIGHT))

                if isinstance(full_image, list):
                    full_image = openCV_img
                else:
                    full_image = np.vstack((full_image, openCV_img))
    except Exception as e:
        print(e)
        full_image = []

    return full_image


#%%


full_image = convert_pdf_to_gray_img("test.pdf")
print(full_image.shape)
img = Image.fromarray(full_image)
img
#%%

buffered = BytesIO()
img.save(buffered, format="PNG")
img_byte = base64.b64encode(buffered.getvalue())
img_str = img_byte.decode()
#%%

decoded_img = Image.open(BytesIO(base64.b64decode(str.encode(img_str))))
decoded_img


# %%
array_decoded_img = np.asarray(decoded_img)
print(array_decoded_img.shape)


# %%
