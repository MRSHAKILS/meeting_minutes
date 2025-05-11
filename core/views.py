from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User,auth
from core.models import MeetingMinutes

@login_required
def homepage(request):

    all_meeting_minutes= MeetingMinutes.objects.all()

    context={
        'all_meeting_minutes':all_meeting_minutes,
    }

    return render(request, 'homepage.html',context=context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:homepage')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            
            return redirect('core:login')

    return render(request, 'signup.html')

@login_required
def minutes(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        location = request.POST.get('location')
        agenda = request.POST.get('agenda')
        discussion = request.POST.get('discussion')

        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not date or not location or not agenda:
            messages.error(request, "Date, Location, and Agenda are required.")
        else:
            try:
                MeetingMinutes.objects.create(
                    date=date,
                    location=location,
                    agenda=agenda,
                    discussion=discussion,
                    start_time=start_time,
                    end_time=end_time
                )
                messages.success(request, "Meeting minutes saved successfully.")
                return redirect('core:homepage')  # Redirect to prevent resubmission
            except Exception as e:
                messages.error(request, f"Error saving data: {str(e)}")
    return render(request, 'minutes.html')

def logout(request):
    auth.logout(request)
    return redirect('core:login')

def delete_minutes(request, pk):
    meeting = get_object_or_404(MeetingMinutes, pk=pk)
    meeting.delete()
    return redirect('core:homepage') 

