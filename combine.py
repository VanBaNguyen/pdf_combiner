import os
import PyPDF2

def combine_pdfs_in_folder(folder_path, output_filename):
    # List all PDF files in the folder, sorted alphabetically
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    pdf_files.sort()

    merger = PyPDF2.PdfMerger()
    for pdf in pdf_files:
        full_path = os.path.join(folder_path, pdf)
        merger.append(full_path)

    merger.write(output_filename)
    merger.close()

if __name__ == "__main__":
    folder = 'pdfs'
    output_pdf = 'combined.pdf'
    combine_pdfs_in_folder(folder, output_pdf)
    print(f"Combined PDF saved as {output_pdf}")
