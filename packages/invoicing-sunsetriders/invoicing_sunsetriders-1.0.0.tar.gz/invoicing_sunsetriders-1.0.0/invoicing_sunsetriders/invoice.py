from fpdf import FPDF
import pandas as pd
import glob
from pathlib import Path
import os
import datetime as time



# # Get path of current file's directory
# current_file = Path(__file__)
# current_dir = current_file.parent

def generate(invoicesfolder="invoice_data", outputfolder="PDFs", product_id="product_id", product_name="product_name",
             amount_purchased="amount_purchased", price_per_unit="price_per_unit", total_price="total_price",
             logo="company_logo.jpg"):
    """
    This function generates printable pdf invoice receipts from .xlsx files.
    :param invoicesfolder:
    :param outputfolder:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :param logo:
    :return:
    """
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))



    # Construct the paths relative to the script directory
    invoicesfolder_path = os.path.join(script_dir, invoicesfolder)
    outputfolder_path = os.path.join(script_dir, outputfolder)
    logo_path = os.path.join(script_dir, logo)

    filepaths = glob.glob(f"{invoicesfolder_path}/*xlsx")

    for filepath in filepaths:
        pdf = FPDF(orientation="p", unit="mm", format="A4")
        pathname = Path(filepath).stem
        pdf.add_page()
        pdf.set_font(family="times", style="B", size=16)
        pdf.cell(w=50, h=8, txt="Invoice #" + pathname[0:5], ln=1)
        date = pathname[6:]
        parsed_date = time.datetime.strptime(date, '%Y.%m.%d')
        formatted_date = parsed_date.strftime("%m/%d/%Y")
        pdf.cell(w=50, h=8, txt="Date was: " + formatted_date, ln=1)
        pdf.ln(10)
        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        # Add header
        headers = list(df.columns)
        headers = [item.replace("_", " ").title() for item in headers]
        pdf.set_font(family="times", style="B", size=10)
        pdf.set_fill_color(178, 255, 255) # Celeste. Thanks https://rgbcolorcode.com/color/B3FFFF
        pdf.set_text_color(255, 178, 178) # Melon, the complement of Celeste.
        # Too light. Darker?
        pdf.set_text_color(255, 80, 80) # "Tomato". Going up actually makes a color lighter.
        pdf.cell(w=30, h=8, txt=headers[0], border=1, fill=True, align="C")
        pdf.cell(w=70, h=8, txt=headers[1], border=1, fill=True, align="C")
        pdf.cell(w=30, h=8, txt=headers[2], border=1, fill=True, align="C")
        pdf.cell(w=30, h=8, txt=headers[3], border=1, fill=True, align="C")
        pdf.cell(w=30, h=8, txt=headers[4], border=1, ln=1, fill=True, align="C")
        # Add rows
        for index, row in df.iterrows():
            pdf.set_fill_color(222, 255, 255)
            pdf.set_font(family="times", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1, align="C", fill=True)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1, align="C", fill=True)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1, align="C", fill=True)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1, align="C", fill=True)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1, align="C", fill=True)
            # To be supremely lazy, you can use win+shift+T to open the PowerToys text extractor, lol.

        # Adding the total total price
        pdf.cell(w=130, h=8, txt="", border=1, align="C", fill=True) # Its width is 30+70+30
        pdf.set_text_color(255, 60, 60)
        pdf.set_font(family="times", size=10)
        pdf.cell(w=30, h=8, txt=str("Total Invoice Cost:"), border=1, align="R", fill=True)
        pdf.cell(w=30, h=8, txt=str(df[total_price].sum()), border=1, ln=1, align="C", fill=True)
        # could also use invoice_nr = filename.split("-")[0], which is technically more scalable.
        # My method will break if you have an invoice that is more or less than 5 digits long.
        # Or even bettter, invoice, date = filename.split("-")



        # Add text to bottom of invoice
        pdf.ln(10)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("times", style="B", size = 14)
        pdf.cell(w=0, txt=f"The total cost of your invoice is ${df[total_price].sum()}.", ln=1)

        # Add company name and logo
        pdf.ln(10)
        pdf.set_text_color(255, 128, 0)
        pdf.set_font("times", style="BI", size=24)
        pdf.cell(w=70, h=12, txt=f"The Sunset Riders")
        pdf.image(logo_path, w=25)

        if not os.path.exists(outputfolder_path):
            os.mkdir(outputfolder_path)
        pdf.output(os.path.join(outputfolder_path, f"{pathname}.pdf"))

generate()