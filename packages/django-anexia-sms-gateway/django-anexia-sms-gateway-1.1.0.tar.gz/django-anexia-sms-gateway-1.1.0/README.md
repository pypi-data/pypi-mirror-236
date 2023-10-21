# Django Anexia SMS Gateway

A django module to send short messages via the [Anexia SMS gateway (ASGW)](https://www.anexia-engine.com/de/modul/sms-plattform-und-gateway).
It requires an active [Anexia Engine](https://www.anexia-engine.com/) subscription and a "ready to use" configured "sender" within [your web service](https://engine.anexia-it.com/sms/senders).

## Installation

Install using pip:

```
pip install django-anexia-sms-gateway
```

In the project's settings.py add the access token configuration:

```
# Anexia SMS Gateway settings (ASGW)
ASGW_ACTIVE = True
ASGW_API_TOKEN = "your-asgw-api-token"
```

## Usage

Call the `send_sms` method wherever you want to trigger a short message:
```
from django_anexia_sms_gateway.sms import send_sms

send_sms(message="SMS content", destination="+43123456789")
```

### Translation (message)

If you provide a translatable message string be sure to use `ugettext` ("gettext_lazy" would not be triggered on time):
```
from django.utils.translation import ugettext
from django_anexia_sms_gateway.sms import send_sms

send_sms(message=ugettext("Translatable SMS content"), destination="+43123456789")
```

### Recipient phone number (destination)

The recipient's phone number (=`destination`) must consist of prefix `+` followed by 1 to 14 digits. Otherwise the ASGW API will return an error.

#### Phone number on model
In case you store the phone number on a model (e.g. `User`), we recommend direct validation via `RegexValidator`, e.g.:

```
from django.core.validators import RegexValidator
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

phone = CharField(
    _("phone number"),
    max_length=15,
    blank=True,
    help_text=_("Prefix '+' followed by 1-14 digits, e.g. '+436641234'"),
    validators=[
        RegexValidator(
            r"^\+\d{1,14}$",
            _("Phone number must be entered in the format: '+123456789'. Prefix '+' with 1 to 14 digits allowed."),
        )
    ],
)
```
