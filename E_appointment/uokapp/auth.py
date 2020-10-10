from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from uokapp.models import student, staffs, appointment, othersuggestion


"""============================================== LOGIN & LOGOUT ==============================================================="""
#login
def login(request):
    if request.method == "GET":
        return render(request, "auth/login.html")

    elif request.method == "POST":
        username = request.POST['username']

        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and student.is_student or student.is_intern:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "home"
                    return redirect(next)
            elif user.is_active and staffs.is_HOD:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "suggestion_list"
                    return redirect(next)
            elif user.is_active and staffs.is_dean:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "suggestion_list"
                    return redirect(next)
            elif user.is_active and staffs.is_lecturer:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "suggestion_list"
                    return redirect(next)
            elif user.is_active and staffs.is_registror:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "suggestion_list"
                    return redirect(next)
            elif user.is_active and staffs.is_CFO:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "suggestion_list"
                    return redirect(next)
            elif user.is_active and user.is_staff:
                auth.login(request, user)
                next=""
                if "next" in request.GET:
                    next = request.GET["next"]
                if next == None or next == "" :
                    next = "admin"
                    return redirect(next)
            else:
                return render(request, 'auth/login.html',{'warning':'your account is disabled'})
        else:
            return render(request, 'auth/login.html',{'warning':'invalid username and/or password'})
            # what it will return after login_required is done.
    return render(request, 'auth/auth/appointment.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

"""================================================== COUNT ============================================================================"""
@login_required(login_url='/login/')
def count_unreaded(request, self):
    count = appointment.objects.filter(lecture = self.request.user.staffs).count()
    return render(request, 'index.html',{'count_appointment': count})

