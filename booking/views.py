import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import LoginFrom, RegistrationForm
from .models import Bookings


def index2(request):
    return render(request, 'booking/index.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error('password', 'Incorrect username or password')
    else:
        form = LoginFrom()
    return render(request, 'booking/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save user to database and login automatically
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def api_bookings(request, device_id):
    try:
        # provide the list of events for the calendar to call
        booking_set = DeviceBookingCalendar.objects.filter(device_instance_id=device_id).all()
        bookings = []
        for booking in booking_set:
            username = User.objects.filter(id=booking.user_id).first().username
            booking_data = {
                'start': booking.datetime_start,
                'end': booking.datetime_end,
                'title': "booked by " + username + "\ndescription:" + booking.description,
            }
            bookings.append(booking_data)
        return JsonResponse(bookings, safe=False)
    except Exception as e:
        print("Error in api_bookings:", str(e))
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def add_booking(request):
    # get booking info and add to database
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            DeviceBookingCalendar.objects.create(datetime_start=data.get('datetime_start'),
                                    datetime_end=data.get('datetime_end'),
                                    description=data.get('description'),
                                    user=request.user,
                                    duration=data.get('duration'),
                                    timestamp=data.get('timestamp'),
                                    device_instance=DeviceInstance.objects.filter(deviceinstance_id=data.get('device_instance_id')).first(),
                                    )
            return JsonResponse({'message': 'Booking successful!'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'invalid request'})


@login_required
def delete_booking(request, booking_id):
    # get booking id and delete booking from database
    if request.method == 'DELETE':
        try:
            Bookings.objects.filter(booking_id=booking_id).delete()
            return JsonResponse({'message': 'Booking deleted!'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'invalid request'})


from django.shortcuts import render, get_object_or_404
from .models import DeviceInstance, DeviceBookingCalendar

def index(request):
    devices = DeviceInstance.objects.all()
    return render(request, 'booking/index.html', {'devices': devices})

@login_required
def device_calendar(request, device_id):
    device = get_object_or_404(DeviceInstance, pk=device_id)
    calendar_events = DeviceBookingCalendar.objects.filter(device_instance=device)
    return render(request, 'booking/device_calendar.html', {'device': device, 'calendar_events': calendar_events})