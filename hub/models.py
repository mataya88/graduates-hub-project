from django.db import models

# Create your models here.


class Semester(models.Model):
    TERMS_CHOICES = [('FA', 'Fall'), ('SP', 'Spring'), ('SU', 'Summer')]
    start_date = models.DateField()
    end_date = models.DateField()
    year = models.PositiveIntegerField()
    term = models.CharField(max_length=2, choices=TERMS_CHOICES)


class User(models.Model):
    GENDERS = [('M', 'Male'), ('F', 'Female')]

    name = models.CharField(max_length=40)
    phone = models.PositiveIntegerField()
    bio = models.TextField(max_length=500)
    photo = models.ImageField(null=True)
    website = models.URLField(null=True)
    email = models.EmailField()


class Notification(models.Model):
    STATUSES = [('R', 'Received'), ('S', 'Seen'), ('D', 'Dismissed')]
    title = models.CharField(max_length=30)
    description = models.TextField()
    links = models.TextField()
    status = models.CharField(max_length=1, choices=STATUSES)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notification')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_notification')


class Team(models.Model):
    name = models.CharField(max_length=30)
    project = models.OneToOneField(
        'Post', on_delete=models.SET_NULL, null=True)


class Student(User):

    PERSONALITIES = [('INTP', 'INTP'), ('INTJ', 'INTJ'), ('INFP', 'INFP'),
                     ('INFJ', 'INFJ'), ('ISTP', 'ISTP'), ('ISTJ', 'ISTJ'),
                     ('ISFP', 'ISFP'), ('ISFJ', 'ISFJ'), ('ENTP', 'ENTP'),
                     ('ENTJ', 'ENTJ'), ('ENFP', 'ENFP'), ('ENFJ', 'ENFJ'),
                     ('ESTP', 'ESTP'), ('ESTJ', 'ESTJ'), ('ESFP', 'ESFP'),
                     ('ESFJ', 'ESFJ')]

    gender = models.CharField(max_length=1, choices=User.GENDERS)
    year = models.PositiveIntegerField()
    personality = models.CharField(max_length=4, choices=PERSONALITIES)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    design_semester = models.ForeignKey(
        Semester, null=True, on_delete=models.SET_NULL)
    skills = models.ManyToManyField(
        'Skill')
    occupancies = models.ManyToManyField('Occupancy')


class Graduate(User):
    gender = models.CharField(max_length=1, choices=User.GENDERS)
    skills = models.ManyToManyField(
        'Skill')


class Company(User):
    industry = models.CharField(max_length=30)
    status = models.CharField(max_length=15)


class Skill(models.Model):
    FIELDS = [('Embedded Systesm', 'Embedded Systems'),
              ('App Development', 'App Development'),
              ('Programming Language', 'Programming Language'),
              ('Graphic Design', 'Graphics Design'),
              ('Machine Learning', 'Machine Learning'),
              ('Databases', 'Databases'),
              ('Web Backend', 'Web Backend'),
              ('Web Frontend', 'Web Frontend')]

    field = models.CharField(max_length=40)
    name = models.CharField(max_length=40)


class Occupancy(models.Model):
    WEEK_DAYS = [('Sun', 'Sunday'), ('Mon', 'Monday'),
                 ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
                 ('Thu', 'Thursday')]
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=3, choices=WEEK_DAYS)


class Post(models.Model):
    VISIBILITY_OPTIONS = [('Pub', 'Public'), ('Pri', 'Private')]
    POST_TYPES = [('Pos', 'Post'), ('Pro', 'Project'), ('Job', 'Job')]
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=3, choices=VISIBILITY_OPTIONS)
    links = models.TextField()
    post_type = models.CharField(max_length=3)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Image(models.Model):
    photo = models.ImageField()
    alt_text = models.CharField(max_length=200)
    line = models.PositiveIntegerField()


class Meeting(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False)
    creator = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
