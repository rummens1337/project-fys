class sendmail:
    def __init__(self,email,subject,filename,code):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders
        
        #input voor de klasse
        self.email_to = email
        self.subject = subject
        self.filename = filename
        self.code = code
        
        email_from = 'corendonfys@hotmail.com'
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = self.email_to
        msg['Subject'] = self.subject

        body = ('''
Bedankt voor het gebruiken van de fotokiosk!
Uw foto is als bijlage toegevoegd in deze E-mail.
        
Mocht de foto niet als bijlage zijn toegevoegd dan kunt u de
foto op de volgende manier verkrijgen:
1. Noteer deze code: ''' + code + '''
2. Ga naar: www.rummens1337.nl
3. Voer uw code in
4. Download uw foto
        ''')
        msg.attach(MIMEText(body,'plain'))

        filename = self.filename
        attachment = open(self.filename,'rb')

        part = MIMEBase('application','octect-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.live.com',25)
        server.starttls()
        server.login('corendonfys@hotmail.com','IT103@FYS')

        server.sendmail(email_from,email_from,text)
        server.quit()