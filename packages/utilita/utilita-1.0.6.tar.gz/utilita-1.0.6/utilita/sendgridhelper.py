
from typing import Dict
import sendgrid
from sendgrid.helpers import mail
import re
import base64
import io
import os
import zipfile as zf
import openpyxl as xl
import datetime
from utilita import excel, date_fns

"""
Usage: Use this to send a sendgrid email in the most common ways we need

"""


class SendgridHelper:
    def __init__(self, sendgrid_api_key=None, from_email=None):
        self.from_email = from_email
        self.sendgrid_api_key = sendgrid_api_key

        assert not [x for x in (sendgrid_api_key, from_email) if x is None], f"Must have a sendgrid_api_key and from_email"

    def config_email(self, subject, recipients, body):
        self.client = sendgrid.SendGridAPIClient(api_key = self.sendgrid_api_key)
        self.msg = sendgrid.helpers.mail.Mail()
        self.msg.from_email = sendgrid.helpers.mail.Email(self.from_email.get('email'), self.from_email.get('name'))
        
        self.p = sendgrid.helpers.mail.Personalization()
        self.p.subject = subject
        self.recipients = recipients

        if isinstance(self.recipients, Dict):
            to_emails = get_email_address_list(self.recipients.get('to'))
            for e in to_emails:
                self.p.add_to(sendgrid.helpers.mail.Email(e))

            cc_emails = get_email_address_list(self.recipients.get('cc', []))
            for e in cc_emails:
                self.p.add_cc(sendgrid.helpers.mail.Email(e))

            bcc_emails = get_email_address_list(self.recipients.get('bcc', []))
            for e in bcc_emails:
                self.p.add_bcc(sendgrid.helpers.mail.Email(e))

        else:
            to_emails = get_email_address_list(self.recipients)
            for d in to_emails:
                self.p.add_to(sendgrid.helpers.mail.Email(d))


        self.msg.add_personalization(self.p)

        self.msg.add_content(
            sendgrid.helpers.mail.Content(
                'text/html',
                body
            )
        )

    def send_email(self):
        try:
            response = self.client.client.mail.send.post(request_body = self.msg.get())
            return response
        except Exception() as e:
            return e


    def attach_df_as_csv(self, file_obj, df_filename=None, compressed=True):
        """Attach a pandas dataframe as a csv file

        Params:
            file_obj: dict in the format of {"df": [dataframe], "zip_filename": "[filename as string]"}
                {"df": unmapped_df, "zip_filename": f"uber_unmappable_transactions for {date}"}

            df_filename:

            compressed=True: compress the file as a zip file.
        """
        df = file_obj.get("df")
        zip_filename=file_obj.get("zip_filename")
        
        assert not [x for x in (df, zip_filename) if x is None], "df==None and zip_filename==None must not be true."
        
        zip_filename = zip_filename.replace('.zip','')

        if df_filename is None: df_filename = zip_filename
        df_filename = df_filename.replace('.csv','')

        zip_bytes = df_to_zipfile_bytes(df, df_filename+".csv")
        zip_bytes.seek(0)
        report_bytes = zip_bytes.read()

        self.msg.add_attachment(
            attachment_from_bytes(
            file_name = zip_filename+".zip",
            file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            file_bytes = report_bytes
            )
        )


    def attach_single_df_as_csv(self, df, df_filename, compressed=False) -> None:
        """Attach a pandas dataframe as a csv file

        Params:
            df: dataframe object

            df_filename: what to name the file. 

            compressed=True: compress the file as a zip file. If True, the compressed file name is the same as the df filename.

        Returns:
            Nothing, as it gets added to the object.
        """
        
        if compressed==True:
            zip_filename = df_filename.replace('.zip','')
            df_filename = df_filename.replace('.csv','')

            zip_bytes = df_to_zipfile_bytes(df=df, df_filename=df_filename+'.csv')
            zip_bytes.seek(0)
            report_bytes = zip_bytes.read()
            
            attach_filename = df_filename+'.zip'
            attach_mime_type = 'application/zip'

        else:
            csv_bytes = df_to_csv_bytes(df=df)
            attach_filename = df_filename+'.csv'
            attach_mime_type = 'text/csv'
            report_bytes = csv_bytes.read()

        self.msg.add_attachment(
            attachment_from_bytes(
            file_name = attach_filename,
            file_type = attach_mime_type,
            file_bytes = report_bytes
            )
        )

    def attach_excel_file_from_path(self, excel_path):
        wb = xl.load_workbook(excel_path)
        excel_bytes = excel.workbook_to_bytes(wb)
        file_name = os.path.basename(excel_path)
        self.attach_excel_file_from_bytes(excel_bytes, file_name)

    def attach_excel_file_from_bytes(self, excel_bytes, file_name):
        self.msg.add_attachment(
            attachment_from_bytes(
                file_name = file_name,
                file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                file_bytes = excel_bytes
            )
        )

def get_email_address_list(address_string):
    if isinstance(address_string, str):
        address_string = re.split(r',|;', address_string)

    return [x.strip() for x in address_string]

def attachment_from_bytes(file_name, file_type, file_bytes):
    a = mail.Attachment()
    a.disposition = mail.Disposition('attachment')
    a.file_type = mail.FileType(file_type)
    a.file_name = mail.FileName(file_name)
    data_64 = str(base64.b64encode(file_bytes).decode('utf-8'))
    a.file_content = mail.FileContent(data_64)
    return a

def df_to_zipfile_bytes(df, df_filename):
    file_obj = io.BytesIO()
    x = zf.ZipFile(file=file_obj, mode='w', compression=zf.ZIP_DEFLATED, compresslevel=5) #winrar "normal" compression
    x.writestr(zinfo_or_arcname=df_filename ,data=df.to_csv(index=False)) #filename of the 
    x.close()

    return file_obj

def df_to_csv_bytes(df):
    file_obj = io.BytesIO(initial_bytes=df.to_csv(index=False).encode('utf-8'))
    file_obj.seek(0)

    return file_obj