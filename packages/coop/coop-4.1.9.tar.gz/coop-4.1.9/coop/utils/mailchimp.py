import sentry_sdk
from django.conf import settings
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

if hasattr(settings, "MAILCHIMP_API_KEY") and hasattr(settings, "MAILCHIMP_USERNAME"):
    client = MailChimp(settings.MAILCHIMP_API_KEY, settings.MAILCHIMP_USERNAME)
else:
    client = None


def subscribe_user(email, data={}, list_id=settings.MAILCHIMP_LIST_ID):
    if not client:
        sentry_sdk.capture_message("Mailchimp client improperly configured")
        return False
    try:
        email = email.lower()
        data.update(
            {
                "status_if_new": "subscribed",
                "email_address": email,
            }
        )
        client.lists.members.create_or_update(list_id, email, data)
        return True
    except MailChimpError as e:
        # Swallow the error but let us know
        sentry_sdk.capture_exception(e)
        return False
