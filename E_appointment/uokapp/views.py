from django.shortcuts import render, redirect, get_object_or_404
import datetime
import smtplib
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from uokapp.models import appointment,student, staffs,othersuggestion
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView, TodayArchiveView
from uokapp.models import appointment as Appointment
from uokapp.forms import appointmentform, othersuggestionform,userform, studentform, staffform
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    # counte = counter()
    return render(request, 'index.html',{})

# def counter():
#     statuses = appointment.objects.filter(status='rejected').count()
#     print(statuses)
#     return statuses

def counter(request):
    staff = staffs.objects.filter(user=request.user.id)
    students = student.objects.filter(user=request.user.id)
    user = User.objects.filter(id = request.user.id).first()
    if students:  
        appoints = appointment.objects.filter(student__user=request.user).all()
        statuses=0
        for appoint in appoints:
            a_sec_counter = othersuggestion.objects.filter(appointment=appoint, staffsuggestion__user=appoint.lecture.user, seen=False).count()
            statuses += a_sec_counter

    elif staff:
        sta_counter = appointment.objects.filter(lecture__user=request.user, seen=False).count()
        sta_sec_counter = othersuggestion.objects.filter(staffsuggestion__user=request.user, seen=False).count()
        statuses = int(sta_counter)+int(sta_sec_counter)
    elif user:
        if user.is_staff:
            sta_counter = appointment.objects.filter(seen=False).count()
            sta_sec_counter = othersuggestion.objects.filter(seen=False).count()
            statuses = int(sta_counter)+int(sta_sec_counter)
    else:
        statuses=0
    
    context = {
            "counter":statuses
        }
    return context

"""==================================================== STUDENT SUGGESTION ========================================================="""


def registerstudent(request):
    registered = False

    if request.method == "POST":
        user_form = userform(data=request.POST)
        student_form = studentform(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()
            registered = True

            return redirect('login')

        else:
            return render(request, 'auth/auth/studentregistry.html', {'warnigng':'something went wrong'})
    else:
        user_form = userform()
        student_form = studentform()
    return render(request, 'auth/auth/studentregistry.html',{'userform':user_form, 'studentform':student_form, 'registered':registered})


@login_required(login_url='/login/')
def studentsuggestions(request, pk):
    staff = get_object_or_404(staffs, pk=pk)
    if request.method == "POST":
        suggestion = appointmentform(data=request.POST)
        if suggestion.is_valid():
            suggestions=suggestion.save(commit=False)
            suggestions.student = request.user.student
            suggestions.lecture = staff
            todaydate = datetime.date.today()
            if suggestions.suggestion_date >= todaydate :
                if suggestions.suggestion_hour <= suggestions.end_time:
                    suggestions.save()
                    return redirect('suggestion_list')
                else:
                    suggestion = appointmentform()
                    return render(request, 'auth/mine/forms.html', {'warning':'the starting time must be lower than the end time', 'appointmentform': suggestion})
            else:
                suggestion = appointmentform()
                return render(request, 'auth/mine/forms.html', {'warning':'Use the date from today and up', 'appointmentform': suggestion})
        else:
            return render(request, 'auth/mine/forms.html', {'warning':'something went wrong', 'appointmentform': suggestion})
    else:
        suggestion = appointmentform()
    return render(request, 'auth/mine/forms.html',{'appointmentform':suggestion })

class studentdetail(LoginRequiredMixin, DetailView):
    context_object_name = 'userinfo'
    model = student
    template_name = "auth/auth/userdetail.html"

class studentsuggestionlist(LoginRequiredMixin, ListView):
    context_object_name = 'stusuggest'
    model = appointment
    template_name = 'auth/mine/list.html'
    def get_queryset(self):
        return appointment.objects.filter(student=self.request.user.student).order_by('-suggested_date')

class studentsuggestionliststaff(LoginRequiredMixin, ListView):
    context_object_name = 'stasuggest'
    model = appointment
    template_name = 'auth/mine/list.html'
    def get_queryset(self):
        return appointment.objects.filter(lecture=self.request.user.staffs).order_by('-suggested_date')

class studentsuggestionlistadmin(LoginRequiredMixin, ListView):
    context_object_name = 'asuggest'
    model = appointment
    template_name = 'auth/mine/list.html'
 
class studentsuggestiondetail(LoginRequiredMixin, DetailView):
    context_object_name = 'stusuggest'
    model = appointment
    template_name = 'auth/mine/detail.html'
    def get_context_data(self, *args,**kwargs):
        pk = self.kwargs.get('pk') # this is the primary key from your URL
        user = self.request.user
        appoint = appointment.objects.filter(id=pk).first()
        staff = staffs.objects.filter(user=user)
        students = student.objects.filter(user=user)
        # your other code
        if staff:
            others   = othersuggestion.objects.filter(appointment=appoint, studentsuggestion=appoint.student).all()
            for other in others:
                other.seen = True
                other.save()
            appoint.seen = True
            appoint.save()

        elif students:
            others   = othersuggestion.objects.filter(appointment=appoint, staffsuggestion=appoint.lecture).all()
            for other in others:
                other.seen = True
                other.save()
        context = super(studentsuggestiondetail, self).get_context_data(**kwargs)
        return context

class studentsuggestionupdate(LoginRequiredMixin, UpdateView):
    model = appointment
    template_name = 'auth/mine/forms.html'
    fields = ('lecture','suggestion_date','suggestion_hour','end_time','student_reason')

class studentsuggestiondelete(LoginRequiredMixin, DeleteView):
    context_object_name = 'stusuggest'
    model = appointment
    template_name = 'auth/mine/delete.html'
    success_url = reverse_lazy('suggestion_list')

#REACTIONS
@login_required(login_url='/login/')
def approving_other_suggestion(request, pk):
    suggestion = get_object_or_404(othersuggestion, pk=pk)
    suggestion.approved_sug()
    staffs = suggestion.staffsuggestion
    suggestions =suggestion.suggestion_date
    subject = 'thank you for using our system'
    message = "The appointment is set on " + str(suggestions)
    from_email = settings.EMAIL_HOST_USER
    if request.user.student:
        to_list = [staffs.user.email, settings.EMAIL_HOST_USER, request.user.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)
    elif request.user.staffs:
        to_list = [suggestion.student.user.email, settings.EMAIL_HOST_USER, request.user.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)
    return redirect('suggestion_detail', pk=suggestion.appointment.pk)

@login_required(login_url='/login/')
def denying_other_suggestion(request, pk):
    suggestion = get_object_or_404(othersuggestion, pk=pk)
    suggestion.denied_sug()
    return redirect('suggestion_detail', pk=suggestion.appointment.pk)

@login_required(login_url='/login/')
def canceling_other_suggestion(request, pk):
    suggestion = get_object_or_404(othersuggestion, pk=pk)
    suggestion.canceled_sug()
    return redirect('suggestion_detail', pk=suggestion.appointment.pk)


"""=============================================== STAFF ================================================================================="""
# Staff registration.
@login_required(login_url='/login/')
def registerstaff(request):
    registered = False

    if request.method == "POST":
        user_form = userform(data=request.POST)
        staff_form = staffform(request.POST, request.FILES)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            staffs = staff_form.save(commit=False)
            staffs.user = user
            staffs.save()
            registered = True
        else:
            return render(request, 'auth/auth/staffregistry.html', {'warnigng':'something went wrong'})
    else:
        user_form = userform()
        staff_form = staffform()
    return render(request, 'auth/auth/staffregistry.html',{'userform':user_form, 'staffform':staff_form, 'registered':registered})

class staffdetail(LoginRequiredMixin, DetailView):
    template_name = "auth/auth/userdetail.html"
    context_object_name = 'userinfo'
    model = staffs

class searched_stafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Searched'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self,*args, **kwargs):
        request = self.request
        searching = request.GET.get('queri')
        for x in searching.split(' '):    
            searching_word = x
        if searching_word is not None:
            result_user = ( Q(user__username__icontains=searching_word)|
                            Q(user__last_name__icontains=searching_word)|
                            Q(user__first_name__icontains=searching_word)|
                            Q(user__email=searching_word))
            result_other = (Q(campus__icontains =x)|
                            Q(faculty__icontains=x))
            searchs = staffs.objects.filter(result_user and result_other)
            searchs_or = staffs.objects.filter(result_user or result_other)
            if searchs:
                searched = searchs
            else:
                searched = searchs_or
            if searching_word.lower() == "cfo":
                searched = staffs.objects.filter(CFO=True)
            elif searching_word.lower() == "vicechancellor":
                searched = staffs.objects.filter(ViceChancellor=True)
            elif searching_word.lower() == "dvca":
                searched = staffs.objects.filter(DVCA=True)
            elif searching_word.lower() == "hod":
                searched = staffs.objects.filter(HOD=True)
            elif searching_word.lower() == "dean":
                searched = staffs.objects.filter(dean=True)
            elif searching_word.lower() == "lecture":
                searched = staffs.objects.filter(lecture=True)
            elif searching_word.lower() == "registror":
                searched = staffs.objects.filter(registror=True)
        return searched.distinct()

class itstafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Istaffs'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self):
        return staffs.objects.filter(faculty="IT & Architecture")

class lawstafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Lstaffs'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self):
        return staffs.objects.filter(faculty="Law Administration")

class Financestafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Fstaffs'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self):
        return staffs.objects.filter(faculty="Finance")

class Musanzestafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Mstaffs'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self):
        return staffs.objects.filter(campus="Musanze")

class Kigalistafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Kstaffs'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self):
        return staffs.objects.filter(campus="Kigali")

class Nyanzastafflist(LoginRequiredMixin, ListView):
    context_object_name = 'Nstaffs'
    model = staffs
    template_name = "auth/mine/stafflist.html"
    def get_queryset(self):
        return staffs.objects.filter(campus="Nyanza")

"""class staffsuggestionlist(SelectRelatedMixin, ListView):
    context_object_name = 'stasuggest'
    model = othersuggestion
    select_related = ('user',)
    template_name = 'auth/mine/list.html'

    def get_queryset(self):
        try:
            self.staff_suggestion = User.objects.prefetch_related('stasuggestion').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExit:
            raise Http404
        else:
            return self.staff_suggestion.stasuggestion.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_suggestion']=self.Staff_suggestion
        return context

class staffsuggestiondetail(DetailView):
    context_object_name = 'stasuggest'
    model = othersuggestion
    template_name = 'auth/mine/detail.html'

@login_required
def add_staffsuggestion(request, pk):
    studentsuggestion = get_object_or_404(appointment, pk=pk)
    if request.method =="POST":
        form = staffsuggestionform(data=request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.studentsuggestion = studentsuggestion
            suggestion.author = request.user
            suggestion.save()
            return redirect('suggestion_detail', pk=studentsuggestion.pk)
    else:
        form = staffsuggestionform()
    return render(request, 'auth/mine/detail.html', {'staffsuggestionform': form})
    """
@login_required(login_url='/login/')
def add_suggestion(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = othersuggestionform(data=request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.appointment = appointment
            suggestion.studentsuggestion = request.user.student
            suggestion.save()
            return redirect('suggestion_detail', pk=appointment.pk)
    else:
        form = othersuggestionform()
    return render(request, 'auth/mine/othersuggestion.html', {'othersuggestionform':form})


@login_required(login_url='/login/')
def add_other_suggestion(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = othersuggestionform(data=request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.appointment = appointment
            suggestion.staffsuggestion = request.user.staffs
            suggestion.save()
            return redirect('suggestion_detail', pk=appointment.pk)
    else:
        form = othersuggestionform()
    return render(request, 'auth/mine/othersuggestion.html', {'othersuggestionform':form})

class staffsuggestionupdate(LoginRequiredMixin, UpdateView):
    model = othersuggestion
    template_name = 'auth/mine/forms.html'
    fields = ('suggestion_date','suggestion_hour','end_time','reason')

class staffsuggestiondelete(LoginRequiredMixin, DeleteView):
    model = othersuggestion
    template_name = 'auth/mine/delete.html'
    success_url = reverse_lazy('suggestion_list_staff')

#REACTIONS
@login_required(login_url='/login/')
def approving_suggestion(request, pk):
    suggestion = get_object_or_404(Appointment, pk=pk)
    suggestion.approved_app()
    
    student = suggestion.student
    suggestion =suggestion.suggestion_date
    
    subject = 'thank you for using our system'
    message = "The appointment is set on " + str(suggestion)
    from_email = settings.EMAIL_HOST_USER
    to_list = [student.user.email, settings.EMAIL_HOST_USER, request.user.email]
    send_mail(subject, message, from_email, to_list, fail_silently = True)
    return redirect('suggestion_detail', pk=pk)

@login_required(login_url='/login/')
def denying_suggestion(request, pk):
    suggestion = get_object_or_404(Appointment, pk=pk)
    suggestion.denied_app()
    return redirect('suggestion_detail', pk=pk)

@login_required(login_url='/login/')
def canceling_suggestion(request, pk):
    suggestion = get_object_or_404(Appointment, pk=pk)
    suggestion.canceled_app()
    return redirect('suggestion_detail', pk=pk)

@login_required(login_url='/login/')
def studentcounting(self):
    appoint = appointment.objects.all.filter(student=self.request.user.student and status is None).count()
    othersuggest = othersuggestion.objects.all.filter(lecture=self.request.user.lecture and status is None).count()
    counter = int(appoint)+int(othersuggest)
    return counter

def allstaff(request):
    allstaff = staffs.objects.all()
    context={
        'research':allstaff
    }
    return render(request, "auth/mine/stafflist.html",context)