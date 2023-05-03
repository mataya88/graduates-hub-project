from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.http import JsonResponse
from datetime import datetime, time
import json
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.db.models import Count
from itertools import chain

=======
from django.db.models import Count, Q
>>>>>>> c4f2c71e6f97c9ceb440fa0422b140e2bd10f773


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
        return redirect('student-home')

    meetingsObj = Meeting.objects.filter(team=team).prefetch_related('members_available')

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
    days = {0: 'Sun', 1: 'Mon', 2: 'Tue',
            3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
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

    # while len(data) < 4:
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
        day_meetings = Meeting.objects.filter(
            team=team, date__year=year, date__month=month+1, date__day=day)
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
            occupancy = Occupancy.objects.get(
                day=day, start_time=start, end_time=end)
            occupancies_obj.append(occupancy)

        print(occupancies_obj)

        student.occupancies.set(occupancies_obj)

        # Return a response to the user
        return redirect('student-home')

    # If this is a GET request, render the form HTML template
    return render(request, 'hub/weekly_courses.html')


# Returns project description page

def get_project(request):
    return render(request, 'hub/Proj_desc.html')

# Returns search page


def get_search(request):
    if request.method == "POST":
  
        searched = request.POST['searched']
        result_list = []
        if searched:
            user_results = User.objects.filter(name__contains=searched)
            posts_results = Post.objects.filter(title__contains=searched, visibility='Pub')

    
            results = list(chain(user_results, posts_results))

            print(results)
            for result in results:
                if hasattr(result, 'student'):
                    student = Student.objects.get(pk=result.pk)
                    results[results.index(result)] = student
                    print(student)
                if hasattr(result, 'graduate'):
                    graduate = Graduate.objects.get(pk=result.pk)
                    results[results.index(result)] = graduate
                    print(graduate)
                if hasattr(result, 'company'):
                    company = Company.objects.get(pk=result.pk)
                    results[results.index(result)] = company
                    print(company)
            

            print(results)
            result_list = [{'type': type(obj).__name__, 'object': obj} for obj in results]
            print(result_list)

            

        return render(request, 'hub/search_page.html', {'searched': searched, 'results': result_list})

    return render(request, 'hub/search_page.html')


# Returns Student Home page


@login_required
def get_student_home(request):
    if request.user.profile.team:
        team_members = request.user.profile.team.student_set.all().exclude(
            id=request.user.profile.id)
    else:
        team_members = []

    notifications = Notification.objects.filter(
        receiver=request.user.profile, status="S").prefetch_related('sender')
    posts = Post.objects.filter(visibility="Pub").select_related(
        'creator').order_by('-time')
    meetings = Meeting.objects.all().order_by('-date')
    context = {'Posts': posts, 'Meetings': meetings,
               'members': team_members, 'notifications': notifications}
    return render(request, 'hub/Student_Home.html', context)

# Returns Recommended Partners (Students) page


@login_required
def get_recommended_partners(request):

    student = request.user.profile
    student_skills_fields = [
        skill.field for skill in list(student.skills.all())]

    # fields where the student does not have skills in
    missed_skill_fields = [skill.field for skill in list(
        Skill.objects.exclude(field__in=student_skills_fields))]

    # students that have more skills in other fields will have more prioriy
    recommended_students = (Student.objects
                            .exclude(name=student.name)
                            .exclude(Q(team=student.team) & ~ Q(team__isnull=True))
                            .filter(
                                personality__in=student.COMPATIBILITY_MATRIX[student.personality])
                            .filter(skills__field__in=missed_skill_fields)
                            .annotate(priority=Count('skills'))
                            .select_related('design_semester')
                            .order_by('-priority'))
    print(recommended_students)

    # filter Users and Students by compatible personalities

    return render(request, 'hub/recommended_partners.html', {'Students': recommended_students})


def get_student_profile(request, id):
    if request.user.profile.id == id:
        return redirect('my-profile')
    student = Student.objects.get(id=id)
    student_skills = student.skills.all()
    if student.team:
        student_team = student.team.student_set.all().exclude(name=student.name)
    else:
        student_team = []
    student_year = student.ORDINALS[student.year]
    context = {'student': student, 'skills': student_skills,
               'study_year': student_year, 'team': student_team}

    return render(request, 'hub/student_profile.html', context)

# Returns Advisor Home page


def get_advisor_home(request):
    Posts = Post.objects.all()
    return render(request, 'hub/advisor_home.html', {'Posts': Posts})

# Returns Company Home page


def get_company_home(request):
    Posts = Post.objects.all()
    return render(request, 'hub/company_home.html', {'Posts': Posts})


@login_required
def post_team_request(request):
    if request.method == 'POST':

        requested_student = Student.objects.get(
            id=request.POST['requested_student_id'])
        user_profile = request.user.profile

        if requested_student.team and not user_profile.team:
            request_notification = Notification(
                title="Team Join Request", description=f"{user_profile.name} wants to join your team.", sender=user_profile, receiver=requested_student, status="S", links=" ")
        elif not requested_student.team and user_profile.team:
            pronoun = 'his'
            if user_profile.gender == "F":
                pronoun = 'her'

            request_notification = Notification(
                title="Team Join Invite", description=f"{user_profile.name} wants you to join {pronoun} team.", sender=user_profile, receiver=requested_student, status="S", links=" ")

        elif not requested_student.team and not user_profile.team:
            request_notification = Notification(
                title="Team Request", description=f"{user_profile.name} wants to create a team with you.", sender=user_profile, receiver=requested_student, status="S", links=" ")
        else:
            failed = "There was a problem in sending the request."
            return HttpResponse(failed, status=400)

        request_notification.save()

        success = "Team request sent successfully"
        return HttpResponse(success)


@login_required
def accept_team_request(request):
    if request.method == "POST":
        request_sender = Student.objects.get(id=request.POST['request_sender'])
        request_receiver = request.user.profile
        notification = Notification.objects.get(
            id=request.POST['notification'])
        if request_sender.team and not request_receiver.team:
            request_sender.team.student_set.add(request_receiver)
            notification.status = "R"
            notification.save()
        elif not request_sender.team and request_receiver.team:
            request_receiver.team.student_set.add(request_sender)
            notification.status = "R"
            notification.save()
        elif not request_sender.team and not request_receiver.team:
            new_team = Team(name="Design Team")
            new_team.save()
            new_team.student_set.add(request_receiver)
            new_team.student_set.add(request_sender)
            notification.status = "R"
            notification.save()
        else:
            error = "Request could not be accepted"
            return HttpResponse(error, status=400)

        success = "Request accepted successfully"
        return HttpResponse(success)


@login_required
def dismiss_notification(request):
    if request.method == "POST":
        notification = Notification.objects.get(
            id=request.POST['notification'])
        notification.status = "D"
        notification.save()
        return HttpResponse()
