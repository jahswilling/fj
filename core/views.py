from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
import datetime;
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
import openpyxl
from pathlib import Path
from io import TextIOWrapper
from tablib import Dataset
import csv
import requests
import json
import qrcode
import io
import base64
from django.db import models
import time

User = get_user_model()


def send_msg(msg,subject):
    message = msg
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["donssagency@gmail.com"]
    send_mail( subject, message, email_from, recipient_list,fail_silently=True )


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = f'Name: {name}\nMessage: {request.POST.get("message")}\nContact Email: {email}'
        send_msg(message,subject)
        messages.success(request,'message sent successfully')

    return render(request, "landing_page/index.html")

def terms(request):

    return render(request, "landing_page/terms.html")



@login_required(login_url='accounts:login')
def dashboard(request):
    users = User.objects.filter(is_staff=False,is_active=True).order_by("-id")[:6]
    users1 = User.objects.filter(is_staff=False)
    users2 = User.objects.filter(is_staff=True)
    activities = Activities.objects.all().order_by("-id")[:6]
    context = {"users":users,"activities":activities,"users1":users1,"users2":users2}

    return render(request, "dashboard.html",context)

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def user_list(request):
    users = Guest.objects.all()

    context = {'users':users}
    # get_image()

    return render(request, "user_list.html",context)

@user_passes_test(lambda user: user.is_staff)
def add_guest(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        joining = request.POST.get('joining', 'No').strip() or 'No'
        black_list_val = request.POST.get('black_list')
        black_list = True if black_list_val in ['True', 'on', '1', 'yes', 'Yes'] else False
        if full_name:
            guest = Guest(full_name=full_name, email=email or None, joining=joining if joining in ['Yes','No'] else 'No', black_list=black_list)
            guest.checked_in = False
            try:
                guest.save()
                messages.info(request, f"Added {guest.full_name} to Guest List")
                return redirect('core:user_list')
            except Exception as e:
                messages.error(request, f"Failed to add guest: {str(e)}")
        else:
            messages.error(request, 'Invalid details: full_name is required')
        # fall through to render form again
        form = GuestForm(request.POST or None)
    else:
        form = GuestForm()
    return render(request, 'register.html', {"form": form})


@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def admin_list(request):
    users = User.objects.filter(is_staff=True,is_active=True).order_by("-id")

    context = {'users':users}
    return render(request, "admin_list.html",context)

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def history(request):
    historys = Activities.objects.all().order_by("-id")

    context = {'historys':historys}
    return render(request, "history.html",context)

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def profile(request, pk):
    import qrcode
    import io
    import base64
    from django.http import HttpResponse
    
    user = get_object_or_404(Guest, pk=pk)

    # Check if QR code already exists, if not generate and save it
    if not user.qr_code:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=2,
        )
        qr.add_data(user.access_code)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 string for embedding in HTML
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Save to database
        user.qr_code = img_str
        user.save()
    
    # Use saved QR code or generate one if it doesn't exist
    qr_code = user.qr_code if user.qr_code else ""
    
    context = {
        "user": user,
        "qr_code": f"data:image/png;base64,{qr_code}" if qr_code else ""
    }
    return render(request, "profile.html", context)


@login_required(login_url='accounts:login')
def delet_user(request, pk):

    user = get_object_or_404(Guest, pk=pk)
    user.is_deleted = True
    user.save()

    return redirect('core:user_list')

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def delet_user2(request, pk):

    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.is_deleted = True
    user.save()

    return redirect('core:admin_list')


def get_image():
    
    
    users = Guest.objects.all()
    count = 0
    for user in users:
        url = "https://api.happi.dev/v1/qrcode?apikey=a60214qCfPuHRpeRhtnOqrvh9xIob8nSdHUwlWnh57GV8DVPstfqgTDp&data=https://fj2025.pythonanywhere.com/profile/" + str(user.id)

        payload={}
        headers = {
        'Authorization': 'Token 7eeb7b15dedd3d8fc46daaf3b49779009f645c5a'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)

        user.image = response["qrcode"]
        user.save()
        count = count + 1 
        print(count)

  
  
@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def send_invite_email(request, pk):
    from django.http import HttpResponse
    import base64, io
    guest = get_object_or_404(Guest, pk=pk)
    # Eligibility checks
    if not guest.email:
        messages.error(request, f'No email address found for {guest.full_name}')
        return redirect('core:user_list')
    if 'noemail.fj25' in guest.email:
        messages.error(request, f"Cannot send invite: Guest {guest.full_name} does not have a valid email.")
        return redirect('core:user_list')
    if guest.black_list:
        messages.error(request, f"Cannot send invite: Guest {guest.full_name} is blacklisted.")
        return redirect('core:user_list')
    if guest.invite_sent:
        messages.info(request, f"Already sent invite to {guest.full_name}.")
        return redirect('core:user_list')
    # Generate QR code if not exists
    if not guest.qr_code:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=2,
        )
        qr.add_data(guest.access_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        guest.qr_code = img_str
        guest.save()
    qr_image_data = base64.b64decode(guest.qr_code)
    context = {'guest': guest}
    from django.conf import settings
    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives
    from email.mime.image import MIMEImage
    html_message = render_to_string('email/invite_card.html', context)
    subject = "You're Invited to FJ2025 - Access Card"
    msg = EmailMultiAlternatives(
        subject,
        'Please view this email in an HTML-enabled email client.',
        settings.EMAIL_HOST_USER,
        [guest.email]
    )
    img = MIMEImage(qr_image_data)
    img.add_header('Content-ID', '<qr_code.png>')
    img.add_header('Content-Disposition', 'inline')
    msg.attach(img)
    msg.attach_alternative(html_message, 'text/html')
    try:
        msg.send()
        guest.invite_sent = True
        guest.save()
        messages.success(request, f'Invitation email sent successfully to {guest.email}')
    except Exception as e:
        messages.error(request, f'Failed to send email: {str(e)}')
    return redirect('core:user_list')


@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['myfile']
        csv_file = TextIOWrapper(uploaded_file, encoding='utf-8')
        imported_data = csv.reader(csv_file, delimiter=',')
        content = []
        for row in imported_data:  # for every row in the file
            if len(row) > 1:
                content.append(row)
            
        imported_data = content
        del content[0:2]
        for d in imported_data:

            if d[0] != None:
                full_name = d[0]

            if d[1] != None:
                location = d[1]
            if d[2] != None:
                seat_no = d[2]
            if d[3] != None:
                formula = d[3]
            if d[5] != None:
                access_code = d[5]
            if d[6] != None:
                status = d[6]
                if status == 'S':
                    status = 'Single'
                elif status == 'M':
                    status = 'Married'
                else:
                    status = "Undefined"
            if d[7] != None:
                plus_one = d[7]
                if plus_one == 'Y':
                    plus_one = 'Yes'
                else:
                    plus_one = 'No'
            if d[8] != None:
                invited_by = d[8]
            
            off_list = ['126','142','143','154','161','162','166','167','174','175','178','179','180','241','242','250','251','272']
            if formula in off_list:
                pass
            else:
                guest = Guest(full_name=full_name,location=location,status=status,seat_no=seat_no,formula=formula,access_code=access_code,plus_one=plus_one,invited_by=invited_by)
                # guest.save()

    return render(request, "history.html")

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def toggle_blacklist(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    guest.black_list = not guest.black_list
    guest.save()
    return redirect('core:user_list')

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def checkin(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    guest.checked_in = True
    guest.save()
    return redirect('core:user_list')

import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage

@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def batch_upload_guests(request):
    if request.method == 'POST' and request.FILES.get('csvfile'):
        csvfile = request.FILES['csvfile']
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        header = next(reader)
        header_map = {h.strip().lower(): i for i, h in enumerate(header)}
        get_col = lambda key: header_map.get(key, None)
        joining_col = get_col('are you joining us?')
        fullname_col = get_col('your full name')
        email_col = get_col('email address')
        blacklist_col = get_col('black list')
        number_col = get_col('number')
        created = 0
        current_max = Guest.objects.aggregate(models.Max('number')).get('number__max') or 0
        number_next = current_max + 1
        for row in reader:
            try:
                joining = (row[joining_col].strip().capitalize() if joining_col is not None else 'No')
                full_name = row[fullname_col].strip() if fullname_col is not None else ''
                email = row[email_col].strip() if email_col is not None else ''
                black_list = False
                if blacklist_col is not None:
                    bl_val = row[blacklist_col].strip().lower()
                    black_list = bl_val in ['yes', 'true', '1', 'y']
                number = None
                if number_col is not None:
                    nval = row[number_col].strip()
                    if nval.isdigit():
                        number = int(nval)
                if not number:
                    number = number_next
                    number_next += 1
                access_code = f"fj25{number:03d}"
                if not full_name:
                    messages.warning(request, f"Row skipped (no name): {row}")
                    continue
                # Enforce unique name (case-insensitive, trimmed)
                if Guest.objects.filter(full_name__iexact=full_name).exists():
                    messages.warning(request, f"Row skipped (duplicate name): {full_name}")
                    continue
                if not email:
                    email = f"guest{number}@noemail.fj25"
                guest = Guest.objects.create(
                    email=email,
                    full_name=full_name,
                    joining=joining if joining in ['Yes','No'] else 'No',
                    black_list=black_list,
                    number=number,
                    access_code=access_code
                )
                created += 1
            except Exception as e:
                messages.warning(request, f"Row skipped: {row} [error: {str(e)}]")
        messages.success(request, f"Batch upload complete. {created} new guests added (duplicate full names were skipped).")
        return redirect('core:user_list')
    return render(request, 'batch_upload_guests.html')


@login_required(login_url='accounts:login')
@user_passes_test(lambda user: user.is_staff)
def send_invite_to_all_guests(request):
    from django.conf import settings
    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives
    from email.mime.image import MIMEImage
    import base64, io
    guests = Guest.objects.filter(black_list=False).exclude(email__icontains='noemail.fj25')
    success, errors, skipped = 0, 0, 0
    for guest in guests:
        try:
            # Skip if we've already sent to this guest
            if guest.invite_sent:
                skipped += 1
                continue
            # QR code logic (copied from send_invite_email):
            if not guest.qr_code:
                import qrcode
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=6, border=2)
                qr.add_data(guest.access_code)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                guest.qr_code = img_str
                guest.save()
            context = { 'guest': guest }
            html_message = render_to_string('email/invite_card.html', context)
            subject = 'You\'re Invited to FJ2025 - Access Card'
            msg = EmailMultiAlternatives(
                subject,
                'Please view this email in an HTML-enabled email client.',
                settings.EMAIL_HOST_USER,
                [guest.email]
            )
            qr_image_data = base64.b64decode(guest.qr_code)
            img = MIMEImage(qr_image_data)
            img.add_header('Content-ID', '<qr_code.png>')
            img.add_header('Content-Disposition', 'inline')
            msg.attach(img)
            msg.attach_alternative(html_message, 'text/html')
            msg.send()
            guest.invite_sent = True
            guest.save(update_fields=["invite_sent"]) 
            success += 1
            time.sleep(3)
        except Exception:
            errors += 1
            continue
    messages.success(request, f"Invites sent: {success}. Skipped (already sent): {skipped}. Errors: {errors}.")
    return redirect('core:user_list')
