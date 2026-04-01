from django.db import models
from patients.models import Patient
from appointments.models import Appointment

class Billing(models.Model):
    STATUS_CHOICES = [('unpaid', 'Unpaid'), ('paid', 'Paid')]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - ${self.amount} ({self.status})"