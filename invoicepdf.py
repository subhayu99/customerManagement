# Importing Required Module
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak
import datetime
import os
    
try:
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()
    directory = "invoices"
    parent_dir = primary_ext_storage
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path)
except:
    try:
        path = "invoices"
        os.mkdir(path)
    except:
        path = ""

def invoice(
    invoice_num,
    customer,
    paid,
    booking_date,
    check_in,
    check_out,
    heads,
    items):

    invoice_name = f"{invoice_num}-{customer.lower().replace(' ', '-',)}-{booking_date.replace('/', '-')}"
    #invoice_name = os.path.join(primary_external_storage_path(), f"{invoice_num}-{customer.lower().replace(' ', '-',)}-{booking_date.replace('/', '-')}")
    c = canvas.Canvas(os.path.join(path, f"{invoice_name}.pdf"),pagesize=(597.6,842.4),bottomup=0)
    # Logo Section
    # Setting th origin to (10,40)
    c.translate(20,140)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("logo.png",0,0,width=120,height=110)
    # Again Inverting Scale For strings instring lower pythonsertion
    c.scale(1,-1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(35,-100)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold",15)
    c.setFillColorRGB(0.3,0.3,0.3)
    # Inserting the name of the company
    c.drawString(100,10,"SAND CASTLES BEACH CAMP")
    # Changing the font size for Specifying Address
    c.setFont("Helvetica",10)
    c.drawString(100,25,"Salt Ghery, Baliara, Mousuni Island")
    c.drawString(100,38,"Namkhana, WB")
    c.drawString(100,51,"Mobile: 9163750545")
    c.drawString(100,64,"Landline: 9330246505")
    c.drawString(100,77,"www.sandcastlesmousuni.com")
    c.drawString(100,90,"sandcastlesmousuni@gmail.com")

    c.setFont("Helvetica-Bold",10)
    c.drawRightString(505,25,"INVOICE")
    c.setFont("Helvetica",10)
    c.drawRightString(505,36,invoice_num)
    c.setFont("Helvetica-Bold",10)
    c.drawRightString(505,51,"DATE")
    c.setFont("Helvetica",10)
    c.drawRightString(505,62,booking_date)
    c.setFont("Helvetica-Bold",10)
    c.drawRightString(505,77,"BALANCE DUE")

    # Line Seprating the page header from the body
    c.setLineWidth(0)
    c.line(-25,110,505,110)

    c.setFillColorRGB(.15,.15,.2)
    c.setFont("Helvetica-Bold",9)
    c.drawString(-20,137,"BILL TO")
    c.setFont("Helvetica-Bold",12)
    c.drawString(-20,152,customer)

    c.setFillColorRGB(0.15,0.15,0.15)
    c.line(-25,170,505,170)

    c.setFont("Helvetica-Bold",9)
    c.drawString(-20,185,"DESCRIPTION")
    c.drawString(300,185,"RATE")
    c.drawString(380,185,"QTY")
    c.drawString(462,185,"AMOUNT")
    c.line(-25,195,505,195)

    c.translate(-20,155)

    total = 0
    for item in items:
        count = 0
        for i in range(4):
            if i == 0:
                c.setFont("Helvetica-Bold",10)
                c.drawString(0,55, item[i])
            elif i == 1:
                c.setFont("Helvetica",10)
                c.drawString(0,67, item[i])
            elif i == 2:
                c.setFont("Helvetica",10)
                c.drawRightString(345,55, "INR "+"%.2f" % float(item[i]))
            elif i == 3:
                c.setFont("Helvetica",10)
                c.drawRightString(418,55, item[i])
        rate = float(item[2])
        qty = float(item[3])
        total += rate*qty
        c.drawRightString(520,55, "INR "+"%.2f" % (rate*qty))
        count += 28
        c.translate(0,count)

    c.line(-3,52,523,52)
    c.setFont("Helvetica",10)
    c.drawString(265,68, "TOTAL")
    c.drawString(265,84, "PAID")
    c.setFont("Helvetica",9)
    c.drawRightString(520,97, datetime.date.today().strftime("%d/%m/%Y"))
    c.setFont("Helvetica-Bold",10)
    c.setFillColorRGB(0.2,0.2,0.2)
    c.drawRightString(520,68, "INR "+"%.2f" % total)
    c.drawRightString(520,84, "- INR "+"%.2f" % float(paid))

    c.drawString(265,119, "BALANCE DUE")
    c.setFont("Helvetica-Bold",13)
    due = total-float(paid)
    c.drawRightString(520,120, "INR "+"%.2f" % due)
    c.setLineWidth(0)
    c.line(262,103,523,103)

    c.setFillColorRGB(0.3,0.3,0.3)
    c.setFont("Helvetica",10)
    c.drawRightString(525,-66-((len(items))*28),"INR "+"%.2f" % due)
    c.setFillColorRGB(0.2,0.2,0.2)

    c.translate(0,100)

    c.setFont("Helvetica-Bold",13)
    c.drawString(0,0,"Payment Instructions")
    c.setFillColorRGB(0.25,0.25,0.25)
    c.setFont("Helvetica-Bold",9)
    c.drawString(0,21,"OTHER")
    c.setFillColorRGB(0.2,0.2,0.2)
    c.setFont("Helvetica",10)
    c.drawString(0,35,"Rest of the payment must be paid in cash.")
    c.drawString(0,47,"at the time of check in.")
    c.setLineWidth(0)
    c.line(0,80,240,80)

    c.translate(0,0)
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("sign.png",410,-200,width=120,preserveAspectRatio=True)
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    c.setFont("Helvetica-Bold",10)
    c.drawRightString(520,150,"DATE SIGNED")
    c.setFont("Helvetica",11)
    c.drawRightString(520,164, datetime.date.today().strftime("%d/%m/%Y"))

    c.setFont("Helvetica",11)
    c.drawString(0,115,"CONFIRMATION RECEIPT")
    c.drawString(0,140,"Booking Date: "+booking_date)
    c.drawString(0,165,"Check In:    "+check_in)
    c.drawString(0,180,"Check Out: "+check_out)
    c.drawString(0,205,"Total Heads: "+heads)

    c.setFillColorRGB(0.35,0.35,0.35)
    c.setFont("Helvetica-Bold",11)
    c.drawString(0,235,"Each and every guest must provide their original")
    c.drawString(0,250,"government ID proof at the time of check in.")

    c.setFont("Helvetica-Bold",11)
    c.drawString(0,279,"Cancellation & Reschedule Policy")
    c.setFillColorRGB(0.25,0.25,0.25)
    c.setFont("Helvetica",11)
    c.drawString(0,296,"1. Before 10 days: Deduct 10% of total billing amount or")
    c.drawString(0,310,"Free Reschedule")
    c.drawString(0,326,"2. From 10 days to before 7 days: Deduct 20% of total")
    c.drawString(0,340,"billing amount or 10% reschedule charge will be applicable.")
    c.drawString(0,356,"3. From 7 days to before 3 days: Deduct 30% of total billing")
    c.drawString(0,370,"amount or 20% reschedule charge will be applicable.")
    c.drawString(0,386,"4. Within 3 days (72 hrs): No refund or 30% reschedule")
    c.drawString(0,400,"charge will be applicable.")

    # End the Page and Start with new
    c.showPage()
    P = PageBreak()
    P.drawOn(c, 0, 0)

    c.translate(36, 0)
    c.setFillColorRGB(0.35,0.35,0.35)
    c.setFont("Helvetica-Bold",11)
    c.drawString(0,52,"Train Route")
    c.setFont("Helvetica-BoldOblique",11)
    c.drawString(35,70,"Namkhana")
    c.drawString(226,85,"7mile")
    c.drawString(0,100,"Hujjuti Kheyaghat or 10mile Patibunia Kheyaghat.")
    c.drawString(74,115,"Chenoi")
    c.drawString(205,115,"Mousuni")
    c.drawString(0,130,"Island.")
    c.drawString(173,145,"Sand Castles")
    c.drawString(0,160,"Beach camp.")
    c.setFillColorRGB(0.25,0.25,0.25)
    c.setFont("Helvetica",11)
    c.drawString(0,70,"Reach                    by train.")
    c.drawString(0,85,"From namkhana book toto/magic van to reach ")
    c.drawString(0,115,"Cross the river              by boat and reach ")
    c.drawString(0,145,"From there take a toto to reach our ")

    c.translate(0, 148)
    c.setFillColorRGB(0.35,0.35,0.35)
    c.setFont("Helvetica-Bold",11)
    c.drawString(0,52,"Bus Route")
    c.setFont("Helvetica-BoldOblique",11)
    c.drawString(78,70,"Bus of Bakkhali")
    c.drawString(191,70,"Dharmatala/")
    c.drawString(0,85,"Anywhere")
    c.drawString(165,85,"10 Mile Bazar")
    c.drawString(159,100,"Patibunia Ghat")
    c.setFont("Helvetica",11)
    c.drawString(0,70,"You can take a                              from ")
    c.drawString(0,85,"                   and get off the bus at ")
    c.drawString(0,100,"From there take a Toto to reach ")
    c.drawString(0,115,"(AC bus is also available)")

    c.translate(0, 115)
    c.setFont("Helvetica-Bold",11)
    c.drawString(0,40,"Car Parking (7Mile Hujjuter Ghat):")
    c.setFont("Helvetica",11)
    c.drawString(0,58,"Riya Parking - 90027 74035")

    # Saving the PDF
    c.save()


if __name__ == "__main__":
    invoice_num = "SND4333"
    customer = "Subhayu Kumar Bala"
    paid = "3500.00"
    booking_date = "01/01/2022"
    check_in = "12:00 PM"
    check_out = "10:00 AM"
    heads = "6"
    items = [
        [
            "XL Adv Tent (For 2 heads)", 
            "Including food", 
            "2400.00", 
            "3"
        ], 
        [
            "Adv Tent (For 1 head)", 
            "Including food", 
            "1600.00", 
            "2"
        ], 
        [
            "Group Castle (For 5 heads)", 
            "Including food & AC", 
            "5800.00", 
            "1"
        ]
    ]
    invoice(invoice_num, customer, paid, booking_date, check_in, check_out, heads, items)