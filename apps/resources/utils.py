import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def add_watermark(input_pdf, watermark_text):
    output_pdf = io.BytesIO()
    packet = io.BytesIO()

    # Get the dimensions of the first page of the input PDF
    reader = PdfReader(input_pdf)
    first_page = reader.pages[0]
    mediabox = first_page.mediabox
    page_width = mediabox[2] - mediabox[0]
    page_height = mediabox[3] - mediabox[1]

    # Calculate center position
    x = int(float(page_width) * 0.15)
    y = int(float(page_height) * 0.12)

    # Create a PDF with the watermark text
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    can.setFont("Times-Roman", min(int(page_height / 12), int(page_width / 12)))  # Adjust font size as needed
    can.setFillColorRGB(0.216, 0.078, 0.078, alpha=0.2)

    # Rotate the canvas for the text
    can.saveState()
    can.translate(x, y)
    can.rotate(15)  # Rotate as desired

    # Calculate text width and height for repeated watermark
    text_width = can.stringWidth(watermark_text, "Times-Roman", int(page_height / 10))
    text_height = int(page_height / 10)

    # Calculate number of repetitions per page
    repetitions_x = int(float(page_width) / text_width) + 1
    repetitions_y = int(float(page_height) / text_height) + 1

    # Draw the watermark across all pages
    for page_num in range(len(reader.pages)):
        can.saveState()

        # Set position for each page
        for i in range(repetitions_x + 1):
            for j in range(repetitions_y + 1):
                can.drawString(i * text_width-200, j * text_height-300, watermark_text)

        can.restoreState()
        can.showPage()

    can.save()

    packet.seek(0)
    watermark = PdfReader(packet)
    watermark_page = watermark.pages[0]

    # Read the input PDF again
    input_pdf.seek(0)
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add watermark to each page
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.merge_page(watermark_page)
        writer.add_page(page)

    # Write the final output PDF
    writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf
