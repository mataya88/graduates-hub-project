from django.shortcuts import render
from .models import Skill
# Create your views here.

def get_skill_set(request):
    # this is a sample view
    skills = Skill.objects.all()
    return render(request, 'hub/our_skills.html', {'skills': skills})

def get_profile(request):
    return render()

def handle_sponsorship():
    result = [{'name': 'ahmad', 'phone': '35353', '':''}]
