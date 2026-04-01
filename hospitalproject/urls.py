from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from patients.models import Patient
from staff.models import Staff
from appointments.models import Appointment
from billing.models import Billing
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from .auth_views import login_view, logout_view
import json

@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_staff = Staff.objects.count()
    total_appointments = Appointment.objects.count()
    total_billing = Billing.objects.filter(status='unpaid').count()

    appt_status = list(Appointment.objects.values('status')
                      .annotate(count=Count('status')))

    monthly_appts = list(Appointment.objects
                        .annotate(month=TruncMonth('appointment_date'))
                        .values('month')
                        .annotate(count=Count('id'))
                        .order_by('month')[:6])

    paid_amount = Billing.objects.filter(status='paid').aggregate(
                  total=Sum('amount'))['total'] or 0
    unpaid_amount = Billing.objects.filter(status='unpaid').aggregate(
                    total=Sum('amount'))['total'] or 0

    staff_roles = list(Staff.objects.values('role')
                       .annotate(count=Count('role')))

    recent_appointments = Appointment.objects.select_related(
                          'patient', 'doctor').order_by('-created_at')[:5]

    recent_patients = Patient.objects.order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'total_patients': total_patients,
        'total_staff': total_staff,
        'total_appointments': total_appointments,
        'total_billing': total_billing,
        'appt_status': json.dumps(appt_status),
        'monthly_appts': json.dumps([
            {'month': str(x['month'].strftime('%b %Y') if x['month'] else ''),
             'count': x['count']}
            for x in monthly_appts
        ]),
        'paid_amount': paid_amount,
        'unpaid_amount': unpaid_amount,
        'staff_roles': json.dumps(staff_roles),
        'recent_appointments': recent_appointments,
        'recent_patients': recent_patients,
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('patients/', include('patients.urls')),
    path('staff/', include('staff.urls')),
    path('appointments/', include('appointments.urls')),
    path('billing/', include('billing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)