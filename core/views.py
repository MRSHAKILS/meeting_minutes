import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User,auth
from core.models import MeetingMinutes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MeetingMinutes
from .serializers import MeetingMinutesSerializer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

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

        # New fields
        hosts = request.POST.get('hosts')
        co_hosts = request.POST.get('co_hosts')
        guests = request.POST.get('guests')
        written_by = request.POST.get('written_by')
        total_attendees = request.POST.get('total_attendees')
        category = request.POST.get('category')

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
                    end_time=end_time,
                    hosts=hosts,
                    co_hosts=co_hosts,
                    guests=guests,
                    written_by=written_by,
                    total_attendees=total_attendees if total_attendees else None,
                    category=category,
                )
                messages.success(request, "Meeting minutes saved successfully.")
                return redirect('core:homepage')
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


@login_required
def edit_minutes(request, pk):
    meeting = get_object_or_404(MeetingMinutes, pk=pk)

    if request.method == 'POST':
        meeting.date = request.POST.get('date')
        meeting.location = request.POST.get('location')
        meeting.agenda = request.POST.get('agenda')
        meeting.discussion = request.POST.get('discussion')
        meeting.start_time = request.POST.get('start_time')
        meeting.end_time = request.POST.get('end_time')

        
        meeting.hosts = request.POST.get('hosts')
        meeting.co_hosts = request.POST.get('co_hosts')
        meeting.guests = request.POST.get('guests')
        meeting.written_by = request.POST.get('written_by')
        attendees = request.POST.get('total_attendees')
        meeting.total_attendees = int(attendees) if attendees else None
        meeting.category = request.POST.get('category')

        meeting.save()
        return redirect('core:homepage')

    return render(request, 'edit_minutes.html', {'meeting': meeting})

@login_required
def minutes_detail(request, pk):
    meeting = get_object_or_404(MeetingMinutes, pk=pk)
    return render(request, 'minutes_detail.html', {'meeting': meeting})


@api_view(['PATCH'])
def autosave_meeting_minutes(request, pk):
    try:
        meeting = MeetingMinutes.objects.get(pk=pk)
    except MeetingMinutes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MeetingMinutesSerializer(meeting, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    # Add this line to show exactly why it's failing
    print(serializer.errors)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download_meeting_pdf(request, pk):
    # Try to fetch the meeting by primary key
    try:
        meeting = MeetingMinutes.objects.get(pk=pk)
    except MeetingMinutes.DoesNotExist:
        return HttpResponse("Meeting not found.", status=404)

    # Set up HTTP response headers for PDF download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="meeting_{pk}.pdf"'

    # Create a canvas object for drawing the PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4  # Page size

    # Start position from the top of the page
    y = height - 100
    line_height = 30  # Space between lines
    
    logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'logo.jpg')  
    if os.path.exists(logo_path):
        p.drawImage(
    ImageReader(logo_path),
    x=500, y=height - 100,  # Position
    width=80, height=80,   # Size
    preserveAspectRatio=True,
    mask='auto'            # Remove background if needed
)
        
    print("LOGO PATH:", logo_path)
    print("Exists:", os.path.exists(logo_path))    

   
    p.saveState()
    p.setFont("Helvetica", 40)
    p.setFillColorRGB(0.7, 0.9, 1.0, alpha=0.5)
    p.drawCentredString(width / 2, height / 2, "IEEE NSU Student Branch")
    p.restoreState()

    # Helper function to draw each field in the PDF
    def draw_line(label, value):
        nonlocal y
        p.setFont("Helvetica", 16)
        p.drawString(50, y, f"{label}: {value}")
        y -= line_height

    # Write meeting fields to PDF
    draw_line("Date", meeting.date.strftime("%Y-%m-%d"))
    draw_line("Time", f"{meeting.start_time.strftime('%H:%M')} - {meeting.end_time.strftime('%H:%M')}")
    draw_line("Location", meeting.location)
    draw_line("Agenda", meeting.agenda)
    draw_line("Hosts", meeting.hosts)
    draw_line("Co-hosts", meeting.co_hosts)
    draw_line("Guests", meeting.guests)
    draw_line("Written by", meeting.written_by)
    draw_line("Total Attendees", meeting.total_attendees)
    draw_line("Category", meeting.category)

    # Add the "Discussion" section
    p.drawString(50, y, "Discussion:")
    y -= line_height

    # Begin text block for discussion content (multi-line)
    text_object = p.beginText(50, y)
    text_object.setFont("Helvetica", 12)

    # Write each line of discussion to the PDF
    for line in meeting.discussion.splitlines():
        text_object.textLine(line)

    p.drawText(text_object)

    # Finalize and close the PDF document
    p.showPage()
    p.save()

    # Return the response as a downloadable PDF
    return response