from django.db import models

class Staff(models.Model):
    ROLE_CHOICES = [('doctor', 'Doctor'), ('nurse', 'Nurse'), ('admin', 'Admin')]

    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    specialization = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"