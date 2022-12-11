from PIL import Image
import pytesseract
import sys

# given the file, uses OCR to get the text
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

if __name__ == "__main__":
    # get the filename from the command line argument
    filename = sys.argv[1]

    lines = ocr_core(filename)


    with open(f"outputs/{filename[7:-3]}txt", 'w') as f:
        f.write(lines)