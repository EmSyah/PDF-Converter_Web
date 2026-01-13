from pdf2docx import Converter
from docx2pdf import convert

def convert_my_files():
    print("1. PDF to Word")
    print("2. Word to PDF")
    choice = input("Choose 1 or 2: ")

    if choice == "1":
        pdf_name = input("Enter the PDF filename (e.g., test.pdf): ")
        cv = Converter(pdf_name)
        cv.convert("converted_word.docx")
        cv.close()
        print("Done! Check your folder for 'converted_word.docx'")
    
    elif choice == "2":
        word_name = input("Enter the Word filename (e.g., test.docx): ")
        convert(word_name, "converted_pdf.pdf")
        print("Done! Check your folder for 'converted_pdf.pdf'")

if __name__ == "__main__":
    convert_my_files()
    