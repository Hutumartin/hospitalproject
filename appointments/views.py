from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from patients.models import Patient
from staff.models import Staff

def send_appointment_email(appointment, action):
    try:
        patient_email = appointment.patient.email
        patient_name = appointment.patient.full_name
        doctor_name = str(appointment.doctor.full_name) if appointment.doctor else 'N/A'
        date = appointment.appointment_date.strftime('%d %B %Y at %H:%M')

        print(f"Sending email to: {patient_email}")
        print(f"Patient: {patient_name}")
        print(f"Doctor: {doctor_name}")
        print(f"Action: {action}")

        if not patient_email:
            print("No email address for patient — skipping")
            return

        if action == 'created':
            subject = 'Appointment Confirmation — Hospital Management System'
            message = f"""Dear {patient_name},

Your appointment has been successfully scheduled.

Appointment Details:
Doctor      : {doctor_name}
Date & Time : {date}
Status      : {appointment.status.upper()}
Notes       : {appointment.notes or 'N/A'}

Please arrive 15 minutes before your appointment time.

Thank you,
Hospital Management System
            """

        elif action == 'updated':
            subject = 'Appointment Updated — Hospital Management System'
            message = f"""Dear {patient_name},

Your appointment has been updated.

Updated Details:
Doctor      : {doctor_name}
Date & Time : {date}
Status      : {appointment.status.upper()}
Notes       : {appointment.notes or 'N/A'}

Thank you,
Hospital Management System
            """

        elif action == 'cancelled':
            subject = 'Appointment Cancelled — Hospital Management System'
            message = f"""Dear {patient_name},

Your appointment scheduled for {date} has been cancelled.

If you have any questions please contact us.

Thank you,
Hospital Management System
            """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [patient_email],
            fail_silently=False,
        )
        print(f"✅ Email sent successfully to {patient_email}")

    except Exception as e:
        print(f"❌ Email error: {str(e)}")


@login_required
def appointment_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.all().order_by('-created_at')
    if query:
        appointments = appointments.filter(
            patient__full_name__icontains=query) | \
            appointments.filter(doctor__full_name__icontains=query)
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'appointments/list.html', {
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter,
    })


@login_required
def appointment_add(request):
    if request.method == 'POST':
        appointment = Appointment.objects.create(
            patient_id=request.POST['patient_id'],
            doctor_id=request.POST['doctor_id'] or None,
            appointment_date=request.POST['appointment_date'],
            status=request.POST['status'],
            notes=request.POST['notes'],
        )
        print(f"Appointment created: {appointment.pk}")
        send_appointment_email(appointment, 'created')
        messages.success(request, 'Appointment added and confirmation email sent!')
        return redirect('appointment_list')
    patients = Patient.objects.all()
    doctors = Staff.objects.filter(role='doctor')
    return render(request, 'appointments/add.html', {
        'patients': patients,
        'doctors': doctors,
    })


@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.patient_id = request.POST['patient_id']
        appointment.doctor_id = request.POST['doctor_id'] or None
        appointment.appointment_date = request.POST['appointment_date']
        appointment.status = request.POST['status']
        appointment.notes = request.POST['notes']
        appointment.save()
        print(f"Appointment updated: {appointment.pk}")
        send_appointment_email(appointment, 'updated')
        messages.success(request, 'Appointment updated and email sent!')
        return redirect('appointment_list')
    patients = Patient.objects.all()
    doctors = Staff.objects.filter(role='doctor')
    return render(request, 'appointments/edit.html', {
        'appointment': appointment,
        'patients': patients,
        'doctors': doctors,
    })


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    print(f"Appointment deleted: {appointment.pk}")
    send_appointment_email(appointment, 'cancelled')
    appointment.delete()
    messages.success(request, 'Appointment cancelled and email sent!')
    return redirect('appointment_list')