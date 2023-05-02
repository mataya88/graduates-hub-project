from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =  [path("allSkills/", views.get_skill_set),
                path("newmeeting/", views.get_schedule_meeting_page, name='new-meeting'),
                path('fetch-occupancies/', views.get_occupancies, name='fetch-occ'),
                path("my-calendar/", views.get_calendar, name='calendar'),
                path('fetch-data/', views.get_events, name='fetch_data'),
                path("editCourses/", views.submit_courses, name='edit-courses'),
                path("proj-desc/", views.get_project, name='project-page'),
                path("search/", views.get_search, name='search-page'),
                path("student-home/", views.get_student_home, name='student-home'),
                path("recommended-partners/", views.get_recommended_partners, name='recommended'),
                path("student-profile/<int:id>/", views.get_student_profile, name='student-profile'),
                path("advisor-home/", views.get_advisor_home, name='advisor-home'),
                path("company-home/", views.get_company_home, name='company-home'),
                path("team-request/", views.post_team_request, name='team-request'),
                path("accept-team-request/", views.accept_team_request, name='accept-team-request'),
                path("dismiss-notification/", views.dismiss_notification, name='dismiss-notification')
                ]  #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
