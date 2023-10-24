from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from emaildeliverability.settings import (
    get_password,
    get_server,
    get_timeout,
    get_user,
    get_interval,
    get_prefix
)
from imap_tools import MailBox, AND
from loguru import logger
import time


def emaildeliverability(request):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")

    subject = f"__{get_prefix()}_{dt_string}"
    logger.debug(f"Sending with subject: {subject}")
    mail = EmailMessage(
        subject=subject,
        body="test",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[get_user()],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )
    mail.send()

    t_end = time.time() + get_timeout()
    while time.time() < t_end:
        time.sleep(get_interval())
        with MailBox(get_server()).login(get_user(), get_password()) as mailbox:
            for msg in mailbox.fetch(AND(subject=f"{subject}")):
                logger.debug(
                    f"Message {msg.uid} {msg.date} {msg.subject} found in mailbox"
                )
                mailbox.delete(msg.uid)
                return HttpResponse("OK", status=200)

    return HttpResponse("KO", status=400)
