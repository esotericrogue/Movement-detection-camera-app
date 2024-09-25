import smtplib
import imghdr
from email.message import EmailMessage

password = "nope"
SENDER = "also nope"
RECEIVER = "noppest"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Foreign entity detected!"
    email_message.set_content("Some foreign object or person showed up!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, password)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email("images/*.png")