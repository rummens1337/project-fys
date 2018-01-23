class Sendmail:
    def __init__(self,email,subject,filename,code,taal):
        #voor versturen van de E-mail
        import smtplib
        #MIME staat voor "Multipurpose Internet Mail Extension"
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        #
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

        if(taal == 1):
            body = ('''
Bedankt voor het gebruiken van de fotokiosk!
Uw foto is als bijlage toegevoegd in deze E-mail.
        
Mocht de foto niet als bijlage zijn toegevoegd, dan kunt u de
foto op de volgende manier verkrijgen:
1. Noteer deze code: ''' + code + '''
2. Ga naar: www.rummens1337.nl
3. Voer uw code in
4. Download uw foto
            ''')
        else:
            body = ('''
Thank you for using the photobooth!
Your photo is added as an attachment in this E-mail.
        
If somehow the photo is not added as an attachment,
You can download your photo by following these steps:
1. Write down this code: ''' + code + '''
2. Go to: www.rummens1337.nl
3. Enter your code
4. Download your photo
            ''')
            
            
        #Voegt de body toe aan msg object als text/plain
        msg.attach(MIMEText(body,'plain'))
        
        #voegt foto toe als attachment
        attachment = open(self.filename,'rb')

        #maakt van de foto een MIMEBase object
        part = MIMEBase('application','octect-stream')
        part.set_payload((attachment).read())
        
        #encode het MIMEBase object in base64
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= Corendon.jpg")
        
        #voegt de attachment toe aan het msg object
        msg.attach(part)
        
        #maakt van msg een string, en voegt deze toe aan text.
        text = msg.as_string()
        
        #instellingen voor het versturen van de email
        server = smtplib.SMTP('smtp.live.com',25)
        server.starttls()
        server.login('corendonfys@hotmail.com','IT103@FYS')

        #verstuurd de email naar de gebruiker, ook een kopie naar ons
        server.sendmail(email_from,email_from,text)
        
        #verbreekt de verbinding.
        server.quit()