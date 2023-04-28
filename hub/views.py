from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.http import JsonResponse


# Create your views here.

def get_skill_set(request):
    # this is a sample view
    skills = Skill.objects.all()
    return render(request, 'hub/our_skills.html', {'skills': skills})

def get_schedule_meeting_page(request):
    
    team_members = [
        {"name": "Abdelrahman Hesham", "picture": "/profile_pics/robot.png"},
        {"name": "Muataz Attaia", "picture": "/profile_pics/profile2.png"},
        {"name": "AbdulAziz Aldhafeeri", "picture": "/profile_pics/profile2.png"},
        {"name": "John Doe", "picture": "/profile_pics/profile2.png"}
    ]

    team = Team.objects.get(name="Bugs-Slayerz")
    team_members = Student.objects.filter(team=team)
   
    meetingsObj = Meeting.objects.filter(team=team)

    meetings = []
    for meeting in meetingsObj:
        meetings.append({"title": meeting.title, "description": meeting.description, "date": meeting.date,
        "start_time": meeting.start_time.strftime('%I:%M %p'), "end_time": meeting.end_time.strftime('%I:%M %p'), 
        "members_available": meeting.members_available})

    context = {"team_members": team_members, "meetings": meetings}
 
    return render(request, 'hub/schedule_meeting.html', context)

def get_occupancies(request):
    day_of_week = int(request.GET.get('dayOfWeek'))
    days = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
    team = Team.objects.get(name="Bugs-Slayerz")
    members = Student.objects.filter(team=team)
    data = []
 
    for member in members:
        occ = []
        if day_of_week in (0, 1, 2, 3, 4):
        
            occupancies = member.occupancies.filter(day=days[day_of_week])
            for oc in occupancies:
                occ.append({'start': oc.start_time, 'end': oc.end_time})
                
        data.append(occ)

    #while len(data) < 4:
     #   data.append([])

    print(data)
    return JsonResponse(data, safe=False)


def get_calendar(request):

    return render(request, 'hub/calendar.html')



def get_events(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    """
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])
    data = DataModel.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date)).values_list('field1', 'field2', 'field3', 'field4')
    return JsonResponse(list(data), safe=False)
    """
    # Dummy Data
    data = [ { 
            0: 'Meeting: 9:00',
            1: 'Meeting: 11:00',
            2: 'Meeting: 18:00',

        },
        {   0: 'Meeting: 9:00',
            1: 'Meeting: 11:00',
            2: 'Meeting: 18:00',
            3: 'Meeting: 20:00',
        },
        {   0: 'Meeting: 9:00',
            1: 'Meeting: 11:00',
            2: 'Meeting: 18:00',
        },]
    """
    queryset = YourModel.objects.all()
    for obj in queryset:
        data.append({
            'field_1': obj.field_1,
            'field_2': obj.field_2,
            'field_3': obj.field_3,
            'field_4': obj.field_4,
        })"""
    return JsonResponse(data, safe=False)



def submit_courses(request):
    # If this is a POST request, the user has submitted the form
    if request.method == 'POST':
        # Retrieve the data from the form
        data_slots = request.POST.getlist('slots')
        slot_list = data_slots[0].split(',')
        print(slot_list)

        # Do something with the data here

        # Return a response to the user
        return redirect('calendar')

    # If this is a GET request, render the form HTML template
    return render(request, 'hub/weekly_courses.html')




def get_project(request):
    return render(request, 'hub/Proj_desc.html')

def get_search(request):
    return render(request, 'hub/search_page.html')

def get_profile(request):
    return render()

def handle_sponsorship():
    result = [{'name': 'ahmad', 'phone': '35353', '':''}]
