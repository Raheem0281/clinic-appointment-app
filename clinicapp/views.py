from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Patient, Doctor, Appointment
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'clinicapp/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        age = request.POST['age']

        user = User.objects.create_user(username=username, password=password, email=email)
        Patient.objects.create(user=user, phone=phone, age=age)

        return redirect('login')
    return render(request, 'clinicapp/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('doctor_list')
        else:
            return render(request, 'clinicapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'clinicapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinicapp/doctor_list.html', {'doctors': doctors})


@login_required
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=date, appointment_time=time)
        return render(request, 'clinicapp/booking_success.html', {'doctor': doctor, 'date': date, 'time': time})

    return render(request, 'clinicapp/book_appointment.html', {'doctor': doctor})


def doctor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        specialization = request.POST['specialization']
        available_time = request.POST['available_time']

        if User.objects.filter(username=username).exists():
            return render(request, 'clinicapp/doctor_register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        Doctor.objects.create(user=user, name=username, specialization=specialization, available_time=available_time)

        return redirect('doctor_login')
    return render(request, 'clinicapp/doctor_register.html')


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("Authenticated User:", user)
        if user is not None:
            print("Has Doctor:", hasattr(user, 'doctor'))
        if user is not None and hasattr(user, 'doctor'):
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            return render(request, 'clinicapp/doctor_login.html', {'error': 'Invalid credentials or not a doctor'})
    return render(request, 'clinicapp/doctor_login.html')


@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'clinicapp/doctor_dashboard.html', {'doctor': doctor, 'appointments': appointments})
