from make_query import *
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4
import docx

def read_file (filename):
    doc = docx.Document(filename)
    words = []
    for para in doc.paragraphs:
        words.append(para.text)
    loc = len(filename) - filename[::-1].find('/')
    for i in words:
        data = get_relevant_data(make_req(i))
        if data:
            create_pdf(data, i, filename[:loc])

def reduce_height (height, c):
    height -= 25
    if height <= 50:
        height = 791
        c.showPage()
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
        c.setFont('HeiseiMin-W3', 16)
        num = c.getPageNumber()
        c.drawString(545, 25, str(num))

    return height

def create_pdf (data, name, loc=''):
    c = canvas.Canvas(loc + name + ".pdf", pagesize=A4)
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    c.setFont('HeiseiMin-W3', 16)
    num = c.getPageNumber()
    c.drawString(545, 25, str(num))
    height = 791
    for i in data:
        for j in i:
            if type(j[1]).__name__ == 'list':
                c.drawString(75, height, j[0] + ':')
                height = reduce_height(height, c)
                for k in j[1]:
                    if type(k[1]).__name__ == 'list':
                        c.drawString(100, height, k[0])
                        height = reduce_height(height, c)
                        for m in k[1]:
                            if type(m).__name__ == 'dict':
                                m = m['url']
                            c.drawString(125, height, m)
                            height = reduce_height(height, c)
                    else:
                        c.drawString(100, height, k[0] + ' : ' + k[1])
                        height = reduce_height(height, c)
            else:
                c.drawString(75, height, j[0] + ' : ' + str(j[1]))
                height = reduce_height(height, c)
    c.save()
    print("Done!")