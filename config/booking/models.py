from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Bemor'),
        ('doctor', 'Shifokor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient', verbose_name="Roli")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram Chat ID")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.CharField(max_length=100, verbose_name="Mutaxassisligi")
    experience_years = models.PositiveIntegerField(default=1, verbose_name="Tajribasi (yil)")
    price_per_visit = models.PositiveIntegerField(verbose_name="Qabul narxi (so'm)")
    bio = models.TextField(blank=True, null=True, verbose_name="Shifokor haqida")
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True, verbose_name="Rasm")

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        return f"Dr. {full_name} - {self.speciality}"



class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlandi'),
        ('cancelled', 'Bekor qilindi'),
        ('completed', 'Yakunlandi'),
    )
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments', verbose_name="Shifokor")
    patient_name = models.CharField(max_length=100, verbose_name="Bemor ismi")
    patient_phone = models.CharField(max_length=20, verbose_name="Bemor telefoni")
    date_time = models.DateTimeField(verbose_name="Qabul vaqti")
    symptoms = models.TextField(blank=True, null=True, verbose_name="Shikoyatlar / Alomatlar")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} -> {self.doctor.username} ({self.date_time.strftime('%Y-%m-%d %H:%M')})"