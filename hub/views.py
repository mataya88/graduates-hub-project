from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.http import JsonResponse
from datetime import datetime, time
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count


# Create your views here.

def get_skill_set(request):
    # this is a sample view
    skills = Skill.objects.all()
    return render(request, 'hub/our_skills.html', {'skills': skills})

# Return the page schedule meetings with the team data and meetings data needed
# Creates a meeting with the data the user specified in the page

@login_required
def get_schedule_meeting_page(request):

    team = request.user.profile.team
    team_members = Student.objects.filter(team=team)
    
    # If this is a POST request, the user has submitted the form
    if request.method == 'POST':
        # Retrieve the data from the form
        data_attributes = request.POST.get('meeting_data').split(',')

        meeting_name = data_attributes[0]
        meeting_desc = data_attributes[1]
        year = "2023"
        month = data_attributes[2]
        day = data_attributes[3]
        start_time = datetime.strptime(data_attributes[4], '%H:%M').time()
        end_time = datetime.strptime(data_attributes[5], '%H:%M').time()
        members_available_str = data_attributes[6:]

        date_string = f"{year}-{month}-{day}"
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()

        members_available_obj = []
        for i, student in enumerate(team_members):
            if members_available_str[i] == 'yes':
                members_available_obj.append(student)

        

        meeting = Meeting(title=meeting_name, description=meeting_desc, start_time=start_time, end_time=end_time,
                date=date_obj, team=team)

        meeting.save()

        meeting.members_available.add(*members_available_obj)


        # Return a response to the user
        return redirect('calendar')

    
    meetingsObj = Meeting.objects.filter(team=team)

    meetings = []
    for meeting in meetingsObj:
        meetings.append({"title": meeting.title, "description": meeting.description, "date": meeting.date,
        "start_time": meeting.start_time.strftime('%I:%M %p'), "end_time": meeting.end_time.strftime('%I:%M %p'), 
        "members_available": meeting.members_available})

    context = {"team_members": team_members, "meetings": meetings}
 
    return render(request, 'hub/schedule_meeting.html', context)

# A function to return occupancies of the team: Used in schedule meeting page to show occupied and unoccupied members for a meeting slot
@login_required
def get_occupancies(request):
    day_of_week = int(request.GET.get('dayOfWeek'))
    days = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
    team = request.user.profile.team
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


# Returns the url of the calendar page
@login_required
def get_calendar(request):

    return render(request, 'hub/calendar.html')


# Used by the calendar page to get events(meetings) in each day of a specific month and year for a student
@login_required
def get_events(request):
    # Fetch the team
    team = request.user.profile.team

    # Fetch the requested month and year
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))

    print(year)
    print(month)

    # Get the meetings data for every day in that month and year
    
    data = []
    
    for day in range(1, 31):
        day_meetings = Meeting.objects.filter(team= team, date__year=year, date__month=month+1, date__day=day)
        day_data = {}
        i = 0
        for meeting in day_meetings:
            start = meeting.start_time.strftime('%I:%M %p')
            title = meeting.title
            day_data[i] = f"{start}: {title}"
            i += 1

        data.append(day_data)
    
 
    return JsonResponse(data, safe=False)


# Return the edit courses page
# Also, updates the database with the occupancies that the user selected in the page
@login_required
def submit_courses(request):
    student = request.user.profile
    
 
    # If this is a POST request, the user has submitted the form
    if request.method == 'POST':
        # Retrieve the data from the form input (name="slots")
        selected_slots = json.loads(request.POST.get('slots'))
        print(selected_slots)

        # Get references to Occupancy items
        occupancies_obj = []
        for slot in selected_slots:
            day = slot["day"]
            start = datetime.strptime(slot["start"], '%H:%M').time()
            end = datetime.strptime(slot["end"], '%H:%M').time()
            occupancy = Occupancy.objects.get(day=day, start_time=start, end_time=end)
            occupancies_obj.append(occupancy)
        
        print(occupancies_obj)

        student.occupancies.set(occupancies_obj)


        # Return a response to the user
        return redirect('calendar')

    # If this is a GET request, render the form HTML template
    return render(request, 'hub/weekly_courses.html')



# Returns project description page

def get_project(request):
    return render(request, 'hub/Proj_desc.html')

# Returns search page

def get_search(request):
    return render(request, 'hub/search_page.html')




def handle_sponsorship():
    result = [{'name': 'ahmad', 'phone': '35353', '':''}]

# Returns Student Home page
def get_student_home(request):
    Posts = Post.objects.all()
    Meetings = Meeting.objects.all()
    context = {'Posts': Posts, 'Meetings': Meetings}
    return render(request, 'hub/Student_Home.html', context)

# Returns Recommended Partners (Students) page
def get_recommended_partners(request):

    user_personality = 'ESTP'
    
    compatibility_matrix = {
        'INTJ': ['ENFP', 'INFP', 'ENTJ', 'INTJ', 'INFJ', 'ISTJ'],
        'INTP': ['ENFJ', 'INFJ', 'ENTP', 'INTP', 'INFP', 'ISTP'],
        'INFJ': ['ENFP', 'INFP', 'ENTJ', 'INTJ', 'INFJ', 'ENFJ'],
        'INFP': ['ENFJ', 'INFJ', 'ENTP', 'INTP', 'INFP', 'ENFP'],
        'ISTJ': ['ENFJ', 'INFJ', 'ESFJ', 'ISFJ', 'ISTJ', 'ESTJ'],
        'ISFJ': ['ENFJ', 'INFJ', 'ESFJ', 'ISFJ', 'ISTJ', 'ESTJ'],
        'ISTP': ['ENFP', 'INFP', 'ENTP', 'INTP', 'ISFP', 'ISTP'],
        'ISFP': ['ENFJ', 'INFJ', 'ESFP', 'ISFP', 'ISTP', 'ESTP'],
        'ENTJ': ['ENFP', 'INFP', 'ENTJ', 'INTJ', 'INFJ', 'ENFJ'],
        'ENTP': ['ENFJ', 'INFJ', 'ENTP', 'INTP', 'INFP', 'ENFP'],
        'ENFJ': ['ENFP', 'INFP', 'ENTJ', 'INTJ', 'INFJ', 'ENTP'],
        'ENFP': ['ENFJ', 'INFJ', 'ENTP', 'INTP', 'INFP', 'ENFP'],
        'ESTJ': ['ESFJ', 'ISFJ', 'ISTJ', 'ESTJ', 'ENTJ', 'INTJ'],
        'ESFJ': ['ESFJ', 'ISFJ', 'ISTJ', 'ESTJ', 'ENFJ', 'INFJ'],
        'ESTP': ['ESFP', 'ISFP', 'ISTP', 'ESTP', 'ENTP', 'INTP'],
        'ESFP': ['ESFJ', 'ISFJ', 'ESFP', 'ISFP', 'ISTP', 'ESTP']
    }

    # get list of compatible personalities
    compatible_list = compatibility_matrix.get(user_personality)
    
    # filter Users and Students by compatible personalities
    Students = Student.objects.filter(personality__in= compatible_list )
    
    return render(request, 'hub/recommended_partners.html', {'Students': Students})

def get_student_profile(request):
    
    Students = Student.objects.all()
    return render(request, 'hub/student_profile.html',{'Students': Students})

# Returns Advisor Home page
def get_advisor_home(request):
    Posts = Post.objects.all()
    return render(request, 'hub/advisor_home.html',{'Posts':Posts})

# Returns Company Home page
def get_company_home(request):
    Posts = Post.objects.all()
    return render(request, 'hub/company_home.html',{'Posts':Posts})


