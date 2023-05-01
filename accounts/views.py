# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# # Create your views here.

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('student-profile')
#             # Redirect to a success page.

#         else:
#             # Return an 'invalid login' error message.
#             messages.success(request, ("Wrong login credentials"))
#             return redirect('login-page')

#     else:
#         return render(request, 'authenticate/login.html', {})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'authenticate/register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    user_skills = profile.skills.all()
    user_team = profile.team.student_set.all().exclude(name=profile.name)
    student_year = profile.ORDINALS[profile.year]
    context = {'skills': user_skills,
               'study_year': student_year, 'team': user_team}
    return render(request, 'authenticate/student_profile.html', context)
