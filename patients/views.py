from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, MedicalRecord

@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all().order_by('-created_at')
    if query:
        patients = patients.filter(full_name__icontains=query) | \
                   patients.filter(email__icontains=query) | \
                   patients.filter(phone__icontains=query)
    return render(request, 'patients/list.html', {
        'patients': patients,
        'query': query,
    })

@login_required
def patient_add(request):
    if request.method == 'POST':
        Patient.objects.create(
            full_name=request.POST['full_name'],
            date_of_birth=request.POST['date_of_birth'] or None,
            gender=request.POST['gender'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST['address'],
        )
        messages.success(request, 'Patient added successfully!')
        return redirect('patient_list')
    return render(request, 'patients/add.html')

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.full_name = request.POST['full_name']
        patient.date_of_birth = request.POST['date_of_birth'] or None
        patient.gender = request.POST['gender']
        patient.phone = request.POST['phone']
        patient.email = request.POST['email']
        patient.address = request.POST['address']
        patient.save()
        messages.success(request, 'Patient updated successfully!')
        return redirect('patient_list')
    return render(request, 'patients/edit.html', {'patient': patient})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    messages.success(request, 'Patient deleted successfully!')
    return redirect('patient_list')

@login_required
def patient_records(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    records = MedicalRecord.objects.filter(
              patient=patient).order_by('-uploaded_at')
    return render(request, 'patients/records.html', {
        'patient': patient,
        'records': records,
    })

@login_required
def record_upload(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        if file:
            MedicalRecord.objects.create(
                patient=patient,
                title=title,
                description=description,
                file=file,
            )
            messages.success(request, 'Medical record uploaded successfully!')
        else:
            messages.error(request, 'Please select a file to upload.')
        return redirect('patient_records', pk=pk)
    return render(request, 'patients/upload_record.html', {
        'patient': patient
    })

@login_required
def record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    patient_pk = record.patient.pk
    record.file.delete()
    record.delete()
    messages.success(request, 'Record deleted successfully!')
    return redirect('patient_records', pk=patient_pk)