import glob
import pathlib
import os
import pandas as pd
from fpdf import FPDF

def generate(invoices_dir, pdfs_dir, image_path, product_id, product_name, amount_purchased, price_per_unit, total_price, excel_sheet_name = 'Sheet 1'):
    """
    :param invoices_dir:
    :param pdfs_dir:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :param excel_sheet_name:
    """

    invoice_paths = glob.glob(f'{invoices_dir}/*.xlsx')
    
    for invoice_path in invoice_paths:
        p = pathlib.Path(invoice_path)
        i_no, i_date = p.stem.split('-')

        df = pd.read_excel(invoice_path, sheet_name=excel_sheet_name)
        
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        pdf.set_font(family='Times', size=16, style='B')
        pdf.cell(w=50, h=8, txt=f'Invoice No.: {i_no}', ln=1)
        pdf.cell(w=50, h=8, txt=f'Date: {i_date}', ln=1)

        pdf.ln(6)

        # Add column headers
        columns = [ col.replace('_', ' ').title() for col in df.columns]
        pdf.set_font(family='Times', size=10, style='B')
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=65, h=8, txt=columns[1], border=1)
        pdf.cell(w=40, h=8, txt=columns[2], border=1, align='R')
        pdf.cell(w=30, h=8, txt=columns[3], border=1, align='R')
        pdf.cell(w=25, h=8, txt=columns[4], border=1, align='R', ln=1)

        # Add rows
        for i, row in df.iterrows():
            pdf.set_font(family='Times', size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=65, h=8, txt=row[product_name], border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount_purchased]), border=1, align='R')
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1, align='R')
            pdf.cell(w=25, h=8, txt=str(row[total_price]), border=1, align='R', ln=1)

        total_price_sum = df['total_price'].sum()
        pdf.set_font(family='Times', size=10, style='B')
        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=65, h=8, border=1)
        pdf.cell(w=40, h=8, border=1)
        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=25, h=8, border=1, txt=str(total_price_sum), align='R', ln=1)

        pdf.ln(6)

        # Add total sum sentence
        pdf.set_font(family='Times', size=12, style='B')
        pdf.cell(w=0, h=10, txt=f'The total price is {total_price_sum}', ln=1)

        pdf.ln(6)
        
        # Add company logo
        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=50, h=10, txt=f'Python with Anindya')
        pdf.image(image_path, w=10, h=10)

        if not os.path.exists(pdfs_dir):
            os.makedirs(pdfs_dir)
        pdf.output(f'{pdfs_dir}/{p.stem}.pdf')
