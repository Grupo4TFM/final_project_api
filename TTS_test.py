import os
from gtts import gTTS
from PIL import Image
import pytesseract
from docx import Document
from PyPDF2 import PdfReader

# Configuración para pytesseract (asegúrate de que esté en tu PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Cambia la ruta si es necesario
# C:\Program Files\Tesseract-OCR\tesseract.exe
def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_word_file(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_pdf_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang='spa')  # Usa 'eng' para inglés
    return text

def process_file(file_path):
    if file_path.endswith('.txt'):
        text = read_text_file(file_path)
    elif file_path.endswith('.docx'):
        text = read_word_file(file_path)
    elif file_path.endswith('.pdf'):
        text = read_pdf_file(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(file_path)
    else:
        raise ValueError("Formato de archivo no soportado")

    # Convertir el texto a voz
    tts = gTTS(text, lang='es')
    audio_path = "output.mp3"
    tts.save(audio_path)
    print(f"Audio guardado en: {audio_path}")

def main():
    print("Selecciona el tipo de archivo para convertir a voz:")
    print("1. Archivo de texto (.txt)")
    print("2. Documento de Word (.docx)")
    print("3. PDF (.pdf)")
    print("4. Imagen con texto (.png, .jpg, .jpeg)")

    choice = input("Ingresa el número de tu elección: ")

    if choice in ['1', '2', '3', '4']:
        file_path = input("Ingresa la ruta completa del archivo: ").strip()
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print("La ruta del archivo no es válida.")
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()