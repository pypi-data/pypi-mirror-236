from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_config():
    """
    Returns Emaildeliverability configuration in dictionary format. e.g:
    EMAIL_DELIVERABILITY = {
        'USER': 'test@test.com',
        ...
    }
    """
    return getattr(settings, "EMAIL_DELIVERABILITY", {})


def get_timeout():
    return get_config().get("TIMEOUT", 45)


def get_interval():
    return get_config().get("INTERVAL", 5)


def get_server():
    server = get_config().get("SERVER")

    if not server:
        raise ImproperlyConfigured(
            """Error you must define your destination imap server in the configuration dictionary e.g:
        EMAIL_DELIVERABILITY = {
            'SERVER': 'mail.test.com',
            ...
        }
        """
        )

    return server


def get_user():
    user = get_config().get("USER")

    if not user:
        raise ImproperlyConfigured(
            """Error you must define your destination imap user in the configuration dictionary e.g:
    EMAIL_DELIVERABILITY = {
        'USER': 'user@test.com',
        ...
    }
    """
        )

    return user


def get_password():
    password = get_config().get("PASSWORD")

    if not password:
        raise ImproperlyConfigured(
            """Error you must define your destination imap password in the configuration dictionary e.g:
    EMAIL_DELIVERABILITY = {
        'PASSWORD': 'password',
        ...
    }
    """
        )

    return password


def check_config():
    get_user()
    get_password()
    get_server()
