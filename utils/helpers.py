import pdfplumber
from PyPDF2 import PdfReader
import docx2txt
from fastapi import HTTPException
import io

class Helpers():
    def convert_pdf_to_md(self,filepath):
        markdown_lines = []
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for line in lines:
                        stripped_line = line.strip()
                        if stripped_line:
                            # Detect main headings
                            if stripped_line.isupper() and len(stripped_line.split()) < 10:
                                markdown_lines.append(f'# {stripped_line}')
                            # Detect subheadings (capitalize first letter)
                            elif stripped_line.istitle() and len(stripped_line.split()) < 10:
                                markdown_lines.append(f'## {stripped_line}')
                            # Detect bullet points
                            elif stripped_line.startswith(('- ', '* ', '+ ')):
                                markdown_lines.append(stripped_line)
                            else:
                                markdown_lines.append(stripped_line)
        
        # Combine all markdown lines with double newlines to create paragraphs
        md_text = "\n\n".join(markdown_lines)
        
        # Save the markdown text to a file
        md_path = filepath.replace('.pdf', '.md')
        with open(md_path, 'w', encoding='utf-8') as md_file:
            md_file.write(md_text)

        file_path = md_path 
        file_contents = ""
        # Read the file and store its contents in a variable
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        return file_contents


    def extract_text_from_file(self,content, content_type):
        if content_type == "application/pdf":
            text = ""
            with io.BytesIO(content) as pdf_file:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text()
        elif content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            with io.BytesIO(content) as docx_file:
                text = docx2txt.process(docx_file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return text