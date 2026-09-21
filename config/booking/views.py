from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, Appointment

def index(request):
    doctors = DoctorProfile.objects.select_related('user').all()
    doctor_data = [
        {
            'id': doctor.id,
            'name': doctor.user.get_full_name() or doctor.user.username,
            'spec': doctor.speciality,
            'exp': doctor.experience_years,
            'price': doctor.price_per_visit,
            'photo': doctor.photo.url if doctor.photo else '',
        }
        for doctor in doctors
    ]
    context = {
        'doctors': doctors,
        'doctor_data': doctor_data,
    }
    return render(request, 'index.html', context)



@login_required
def doctor_dashboard(request):

    if request.user.role != 'doctor':
        return redirect('index')

    appointments = Appointment.objects.filter(doctor=request.user).order_by('-date_time')

    context = {
        'appointments': appointments,
        'pending_count': appointments.filter(status='pending').count(),
        'confirmed_count': appointments.filter(status='confirmed').count(),
    }
    return render(request, 'doctor_dashboard.html', context)



@login_required
def update_appointment_status(request, pk, status):
    if request.user.role == 'doctor':
        appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user)
        if status in ['confirmed', 'cancelled', 'completed']:
            appointment.status = status
            appointment.save()
    return redirect('doctor_dashboard')