import PyPDF2
def extract_text(file):
    """Reads an uploaded PDF and returns its content as a string."""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"