from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail, get_connection
from django.conf import settings
from pathlib import Path
from datetime import datetime
from threading import Thread

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import os
from .forms import ContactForm
from .utils_excel import append_submission_xlsx
from .utils_contact import normalize_phone_and_country, country_name_from_alpha2



def home(request):
    return render(request, 'index.html')

def factory(request):
    return render(request, 'factory.html')

def healthcare(request):
    return render(request, 'healthcare.html')
def facility(request):
    return render(request, 'facility.html')
def city(request):
    return render(request, 'city.html')
def transport(request):
    return render(request, 'transport.html')
def contact(request):
    return render(request, 'contact.html')
def iot(request):
    return render(request, 'iot.html')
def eam(request):
    return render(request, 'eam.html')
def apm(request):
    return render(request, 'apm.html')
def mobility(request):
    return render(request, 'mobility.html')
def plans(request):
    return render(request, 'plans.html')

def about(request):
    return render(request, 'about.html')
def workorder(request):
    return render(request, "workorder.html")
def compliance(request):
    return render(request, "compliance.html")
def scada(request):
    return render(request, "scada.html")
def gis(request):
    return render(request, "gis.html")
def erpsync(request):
    return render(request, "erpsync.html")


def _send_contact_email_async(subject, body):
    """Send email in background; print any error to console."""
    try:
        conn = get_connection(timeout=getattr(settings, "EMAIL_TIMEOUT", 15))
        send_mail(
            subject=subject,
            message=body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None)
                        or getattr(settings, "EMAIL_HOST_USER", None),
            recipient_list=getattr(settings, "CONTACT_RECIPIENTS", None)
                        or [getattr(settings, "CONTACT_INBOX", None)
                        or getattr(settings, "EMAIL_HOST_USER", None)],
            fail_silently=False,
            connection=conn,
            auth_user=getattr(settings, "EMAIL_HOST_USER", None),
            auth_password=getattr(settings, "EMAIL_HOST_PASSWORD", None),
        )
    except Exception as e:
        print("EMAIL ERROR:", repr(e))

def contact_section(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data

        # Normalize phone + resolve country
        e164_phone, resolved_alpha2, resolved_country_name = normalize_phone_and_country(
            cd.get("phone", ""), cd.get("country", "")
        )

        # Append to Excel
        xlsx_path = Path(getattr(settings, "CONTACT_SUBMISSIONS_XLSX",
                          Path(settings.BASE_DIR) / "contact_submissions.xlsx"))
        append_submission_xlsx(
            xlsx_path,
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                cd["first_name"],
                cd.get("last_name", ""),
                cd.get("company", ""),
                cd["email"],
                resolved_alpha2,
                resolved_country_name,
                e164_phone or cd.get("phone", ""),
                cd.get("message", ""),
            ],
        )

        # Email body
        body = "\n".join([
            "New contact submission for Carl  Software:",
            f"Name: {cd['first_name']} {cd.get('last_name','')}".strip(),
            f"Company: {cd.get('company','')}",
            f"Email: {cd['email']}",
            f"Country: {resolved_country_name or country_name_from_alpha2(resolved_alpha2) or cd.get('country','')}",
            f"Phone: {e164_phone or cd.get('phone','')}",
            "",
            "Message:",
            cd.get("message", "")
        ])

        # Fire-and-forget email
        Thread(target=_send_contact_email_async,
               args=("New website contact submission for Carl Software", body),
               daemon=True).start()

        # Redirect to Thanks page
        return redirect(reverse("cmmsApp:contact_thanks"))

    return render(request, "contact_section.html", {"form": form, "sent": request.GET.get("sent")})

def contact_thanks(request):
    return render(request, "contact_thanks.html", {})

