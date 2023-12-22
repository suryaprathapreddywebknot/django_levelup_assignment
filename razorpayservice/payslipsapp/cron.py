# import os
# import json
# from django.core.mail import EmailMessage
# from reportlab.pdfgen import canvas
# from django.conf import settings
# from .models import Payslips
# from .serializers import PayslipGetSerializer
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # def create_pdf(payslip):
# #     pdf_filename = f"{payslip['user']['name']}.pdf"
# #     with canvas.Canvas(pdf_filename) as pdf:
# #         pdf.drawString(100, 800, f"Payslip for {payslip['user']['name']}\n")
# #         pdf.drawString(100, 780, f"Salary: {payslip['salary']}\n")
# #         pdf.drawString(100, 760, f"Deductions: {payslip['deductions']}\n")
# #     return pdf_filename

# # def send_email_with_pdf(pdf_filename, recipient_email):
# #     subject = 'Payslip'
# #     message = 'Please find attached the Payslip report.'
# #     from_email = 'spreddy8951@gmail.com'  # Replace with your Gmail email address
# #     password = 'gbkyywsfriovfblc'  # Replace with your Gmail password
# #     to_email = recipient_email

# #     # Create a MIME object
# #     msg = MIMEMultipart()
# #     msg['From'] = from_email
# #     msg['To'] = to_email
# #     msg['Subject'] = subject
# #     body = message
# #     msg.attach(MIMEText(body, 'plain'))

# #     # Attach the PDF file
# #     with open(pdf_filename, 'rb') as attachment:
# #         part = MIMEBase('application', 'octet-stream')
# #         part.set_payload(attachment.read())
# #         encoders.encode_base64(part)
# #         part.add_header('Content-Disposition', f"attachment; filename= {pdf_filename}")
# #         msg.attach(part)

# #     # Connect to the SMTP server and send the email
# #     try:
# #         server = smtplib.SMTP('smtp.gmail.com', 587)
# #         server.starttls()
# #         server.login(from_email, password)
# #         text = msg.as_string()
# #         server.sendmail(from_email, to_email, text)
# #         server.quit()
# #         print(f"Email sent to {to_email} successfully!")
# #     except Exception as e:
# #         print(f"Error sending email to {to_email}: {e}")

def generate_payslip(payslip,data):
    print('Cron is running')
    file_path = f"/{payslip['user']['name']}.txt"

    try:
        with open(file_path, 'w') as f:
            f.write(f"Payslip for {payslip['user']['name']}\n")
            f.write(f"Salary: {payslip['salary']}\n")
            f.write(f"Deductions: {payslip['deductions']}\n")
            f.write(f"Email: {payslip['user']['email']}\n")
            f.write(f"data: {data}\n")
    except Exception as e:
        print(f"Error creating payslip for {payslip['user']['name']}: {e}")

# def SendPayslip():
#     payslips = Payslips.objects.select_related('user').all()
#     serializer = PayslipGetSerializer(payslips, many=True)
    
#     for payslip_data in serializer.data:
#         pass

import boto3
from botocore.exceptions import NoCredentialsError
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Payslips
from .serializers import PayslipGetSerializer

def generate_payslip_pdf(payslip_data):
    # Create a PDF using reportlab or another library
    pdf_content = BytesIO()
    p = canvas.Canvas(pdf_content)
    # Add content to the PDF using p.drawString, p.drawInlineImage, etc.
    p.drawString(100, 100, f"Salary: {payslip_data['salary']}")
    p.showPage()
    p.save()
    pdf_content.seek(0)
    return pdf_content

def upload_to_s3(pdf_content, file_name):
    # Upload the PDF to S3
    s3 = boto3.client('s3', aws_access_key_id='AKIAW5F5B2AIZ7PJXN55', aws_secret_access_key='q3GrRfuRy4YPdOWHKrTiUxUJkzeFI5psT')
    try:
        s3.upload_fileobj(pdf_content, 'leveluprazorpay', file_name)
        return f'https://leveluprazorpay.s3.amazonaws.com/{file_name}'
    except NoCredentialsError:
        print('Credentials not available')
        return None

def send_payslip_email(user_email, payslip_pdf):    
    # Send an email with the payslip attached
    subject = 'Your Monthly Payslip'
    message = 'Please find attached your monthly payslip.'
    from_email = 'spreddy8951@gmail.com'  # Update with your email
    recipient_list = [user_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        # html_message=render_to_string('email_template.html'),  # Optional: Use a template for HTML content
        fail_silently=False,
        attachment=[('payslip.pdf', payslip_pdf, 'application/pdf')],
    )

def SendPayslip():
    payslips = Payslips.objects.select_related('user').all()
    serializer = PayslipGetSerializer(payslips, many=True)

    for payslip_data in serializer.data:
        # test
        # Step 1: Generate PDF
        payslip_pdf = generate_payslip_pdf(payslip_data)

        # Step 2: Store PDF in S3
        file_name = f'payslip_{payslip_data["user"]["name"]}.pdf'
        s3_url = upload_to_s3(payslip_pdf, file_name)
        generate_payslip(payslip_data,s3_url)

        if s3_url:
            # Step 3: Append S3 URL to payslip_docs list in the database
            payslip_instance = Payslips.objects.get(user=payslip_data['user']['id'])
            payslip_instance.payslip_docs.append(s3_url)
            payslip_instance.save()

            # Step 4: Send PDF to user through email
            user_email = payslip_data['user']['email']
            send_payslip_email(user_email, payslip_pdf)
            
