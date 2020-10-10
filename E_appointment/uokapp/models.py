from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
situation=[
    ('Working','working'),
    ('Available','Available'),
    ('Off','off'),
    ('Appointment','appointment'),
    ('Break','break'),
    ('Meeting','meeting'),
]
faculty = [
    ('IT & Architecture','IT & Architecture'),
    ('Law Administration','Law Administration'),
    ('Finance','Finance')
]
department=[
    ('BIT','Information Technology'),
    ('BBIT','Business & Information Technology'),
    ('BCS','Computer Sciences'),
]
campus = [
    ('Kigali','Kigali'),
    ('Musanze','Musanze'),
    ('Nyanza','Nyanza'),
]
session=[
    ('Day','day'),
    ('Evening','evening'),
    ('Weekend','weekend'),
]
statuses=[
    ('accepted','accepted'),
    ('rejected','rejected'),
    ('canceled','canceled'),

]

class staffs(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    ViceChancellor = models.BooleanField(default = False)
    DVCA = models.BooleanField(default = False)
    dean = models.BooleanField(default = False)
    HOD = models.BooleanField(default = False)
    lecturer = models.BooleanField(default = False)
    registror = models.BooleanField(default = False)
    CFO = models.BooleanField(default = False)
    faculty = models.CharField(max_length =19 ,  choices = faculty, blank=True )
    campus = models.CharField(max_length=7, choices=campus)
    profile = models.ImageField(upload_to='profile_pics/', blank=True, default = None)

    @property
    def is_dean(self):
        return self.dean
    @property
    def is_HOD(self):
        return self.HOD
    @property
    def is_CFO(self):
        return self.CFO
    @property
    def is_lecturer(self):
        return self.lecturer
    @property
    def is_registror(self):
        return self.registror

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('userdetail', kwargs={'pk':self.pk})

class student(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    student = models.BooleanField(default = True)
    interns = models.BooleanField(default=False)
    depart = models.CharField(max_length =5 ,  choices = department )
    session = models.CharField(max_length = 7, choices = session)
    campus = models.CharField(max_length=7, choices=campus)
    profile = models.ImageField(upload_to='profile_pics/', blank=True, default="media/profile_pics/westbl_dFbRfcB.jpg")

    def __str__(self):
        return self.user.username
    @property
    def is_student(self):
        return self.student
    @property
    def is_intern(self):
        return self.interns

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk':self.pk})


class appointment(models.Model):
    student = models.ForeignKey(student, default=None, on_delete=models.CASCADE)
    lecture = models.ForeignKey(staffs, on_delete=models.CASCADE)
    suggestion_date = models.DateField(default=None,blank=True)
    suggestion_hour = models.TimeField(default=None,null=True, blank=True)
    end_time = models.TimeField(default=None,null=True, blank=True)
    student_reason = models.TextField(max_length=1000, blank=True)
    status = models.CharField(max_length=9, default=None, choices=statuses, null=True, blank=True)
    suggested_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    @property
    def is_seen(self):
        return self.seen
        
    def approved_app(self):
        self.status = 'accepted'
        self.save()
    def denied_app(self):
        self.status = 'rejected'
        self.save()
    def canceled_app(self):
        self.status = 'canceled'
        self.save()

    def get_absolute_url(self):
        return reverse('suggestion_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.student.user.username

class othersuggestion(models.Model):
    appointment = models.ForeignKey(appointment, related_name='othersuggestion', default=None, on_delete=models.CASCADE)
    staffsuggestion = models.ForeignKey(staffs, default=None,null=True, on_delete=models.CASCADE)
    studentsuggestion = models.ForeignKey(student, default=None,null=True, on_delete=models.CASCADE)
    suggestion_date = models.DateField(default=None,blank=True)
    suggestion_hour = models.TimeField(default=None,null=True, blank=True)
    end_time = models.TimeField(default=None,null=True, blank=True)
    reason = models.TextField(max_length=1000)
    status = models.CharField(max_length=9, default=None, null=True, choices=statuses, blank=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    @property
    def is_seen(self):
        return self.seen

    def approved_sug(self):
        self.status = 'accepted'
        self.save()
    def denied_sug(self):
        self.status = 'rejected'
        self.save()
    def canceled_sug(self):
        self.status = 'canceled'
        self.save()

    def get_absolute_url(self):
        return reverse('othersuggestion_detail', kwargs={'pk':self.pk})

    def __str__(self):
        if self.staffsuggestion is not None:
            return self.staffsuggestion.user.username
        else:
            return self.studentsuggestion.user.username
