from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Staff

@login_required
def staff_list(request):
    query = request.GET.get('q', '')
    staff = Staff.objects.all().order_by('-created_at')
    if query:
        staff = staff.filter(full_name__icontains=query) | \
                staff.filter(email__icontains=query) | \
                staff.filter(specialization__icontains=query)
    return render(request, 'staff/list.html', {
        'staff': staff,
        'query': query,
    })

@login_required
def staff_add(request):
    if request.method == 'POST':
        Staff.objects.create(
            full_name=request.POST['full_name'],
            role=request.POST['role'],
            specialization=request.POST['specialization'],
            phone=request.POST['phone'],
            email=request.POST['email'],
        )
        messages.success(request, 'Staff member added successfully!')
        return redirect('staff_list')
    return render(request, 'staff/add.html')

@login_required
def staff_edit(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.full_name = request.POST['full_name']
        staff.role = request.POST['role']
        staff.specialization = request.POST['specialization']
        staff.phone = request.POST['phone']
        staff.email = request.POST['email']
        staff.save()
        messages.success(request, 'Staff member updated successfully!')
        return redirect('staff_list')
    return render(request, 'staff/edit.html', {'staff': staff})

@login_required
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    staff.delete()
    messages.success(request, 'Staff member deleted!')
    return redirect('staff_list')