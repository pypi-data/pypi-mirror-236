

def pdf_text(filepath):
    import pdfplumber
    delimiter = '\n'
    with pdfplumber.open(filepath) as pdf:
        # 获取 页数据
        page_contents = [page.extract_text() for page in pdf.pages]
        return delimiter.join(page_contents)


def doc_text(filepath):
    import docx
    doc = docx.Document(filepath)
    text = ''
    for part in doc.paragraphs:
        _ = part.text.strip()
        if _:
            text += '\n' + _

    return text.strip()