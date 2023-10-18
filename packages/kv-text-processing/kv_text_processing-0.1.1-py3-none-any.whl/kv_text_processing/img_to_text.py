import os
from typing import Optional
import pytesseract
import cv2


def extract_text_from_article(img_dir: str = None,
                              article_title: str = None,
                              save_file: bool = True) -> Optional[str]:
    """
    This function uses tesseract to perform OCR on the images contained in the provided directory. It
    returns the ocr'd text as a string, as well as saves the text to a txt file.

    :param img_dir: The directory containing the images to be ocr'd
    :param article_title: The title of the article, used for the file name.
    :param save_file: Boolean determining whether the file is saved.
    :return: Optional String
    """

    text = ""  # Create a blank string to store the ocr'd text
    for img in sorted(os.listdir(img_dir)):

        # Open the file using cv2, and convert from BGR to RGB format
        img = cv2.imread(img_dir + '/' + img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # use tesseract to extract the text from image and append it to the text variable
        text += pytesseract.image_to_string(img)

    if save_file:
        write_text_to_file(text=text, file_name=article_title + ".txt")

    return text

def extract_text_from_image(img_path: str = None,
                            file_name: str = None,
                            save_file: bool = True) -> Optional[str]:
    """
    This function uses tesseract to perform OCR on a single image. It returns the OCR'd text as a string,
    and optionally can save the contents to a .txt file.
    :param img_path: The file path for the image to be OCR'd
    :param file_name: The name of the save file
    :param save_file: Boolean determining whether the file is saved.
    :return: Optional String
    """

    if img_path is None:
        raise UserWarning("No Image file supplied. Please provide an image file.")

    text = ""

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Change channel order

    # use tesseract to extract the text from image and append it to the text variable
    text += pytesseract.image_to_string(img)

    if save_file:
        write_text_to_file(text=text, file_name=file_name + ".txt")

    return text

def clean_extracted_text(text: str) -> str:
    """
    This function takes extracted text and strips unnecessary new lines and hyphens.

    :param text: The string to be cleaned
    :return: the cleand String
    """

    # Remove all the new lines
    text = text.replace('\n', ' ').replace('- ', '')

    return text


def write_text_to_file(text: str,
                       file_name: str = None) -> None:
    """
    This function takes a string input and saves it to a text file.
    :param text: The string to be saved
    :param file_name: The name of the file
    :return: None
    """

    # Write the text to a file
    with open(file_name, 'w') as f:
        f.write(text)
        f.close()
