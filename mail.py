import smtplib
from logger import getLogger
from sql import update_miqaat

logger = getLogger()


def send_email(miqaat):
    user = "a"
    pwd = "a"
    recipient = "a"
    subject = "Pass open for " + miqaat.name
    body = "Pass open for " + miqaat.name

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        logger.info("Sent mail successfully")
        update_miqaat(miqaat)
    except Exception as e:
        logger.error("error: " + str(e))
