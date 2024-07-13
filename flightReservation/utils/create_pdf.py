import os.path
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from datetime import datetime
from utils.constants import Attachment
import logging

def create_ticket(first_name, last_name, departure_city, arrival_city, time_of_departure):
    try:
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Arial_Bold.ttf')
        file_path = Attachment.ATTACHMENT_FILE_PATH.value
        if os.path.exists(file_path):
            os.remove(file_path) 
        documentTitle = 'Ticket'
        title = 'Neo-Fly: Fly like a bird!'
        data = [
            ["Ticket Number", "From", "To", "Departure Time"],
            [datetime.now().timestamp().__str__().replace('.',''), arrival_city, departure_city, time_of_departure]
        ]
        subTitle = f'Ticket for {departure_city} to {arrival_city}, {first_name} {last_name}'
        textLines = [ 
            f'Dear {first_name} {last_name},', 
            f"""Please find the ticket information below.""",
            f"""Ticket Number: NF-{datetime.now().timestamp().__str__().replace('.','')}""",
            f'From: {departure_city}             To: {arrival_city}',
            "",
            '',
            '',
            '',
            'Have a happy and safe journey.',
            '',
            '',
            'For any assistance please connect neofly.bibh@gmail.com',  
            '',
            '',
            f'Team NeoFly',
            f'© {datetime.today().year}'       
        ] 
        
        # image = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'neo_fly_logo.png')
        
        pdf = canvas.Canvas(file_path) 
        pdf.setTitle(documentTitle) 
        pdfmetrics.registerFont( 
        TTFont('abc', font_path) 
        ) 
    
        pdf.setFont('abc', 36) 
        pdf.drawCentredString(300, 770, title) 
        pdf.setFillColorRGB(0, 0, 255) 
        pdf.setFont("Helvetica-Bold", 24) 
        pdf.drawCentredString(290, 720, subTitle) 
        pdf.line(30, 710, 550, 710) 
        text = pdf.beginText(40, 680) 
        text.setFont("Helvetica", 18) 
        text.setFillColor(colors.black) 
        for line in textLines: 
            text.textLine(line) 
        pdf.drawText(text) 
        
        data = [
            ["Ticket Number", "From", "To", "Departure Time"],
            ["NF"+datetime.now().timestamp().__str__().replace('.',''), arrival_city, departure_city, time_of_departure]
        ]
        col_widths = [150, 100, 100, 150]
        row_heights = [30] * len(data)
        table = Table(data, colWidths=col_widths, rowHeights=row_heights)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        table.setStyle(style)
        x = 42
        y = 550
        table.wrapOn(pdf, 200, 200)
        table.drawOn(pdf, x, y)
        
        pdf.save() 
        
    except Exception as error:
        logging.error(error)
        
        
    

    
