"""E_appointment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from uokapp import views,auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Main
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth.login, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),

    # Student
    url(r'^student/detail/(?P<pk>[\d]+)/$', views.studentdetail.as_view(), name='student_detail'),
    url(r'^student/registration/$', views.registerstudent, name="student_registration"),
    url(r'^student/suggestion/(?P<pk>[\d]+)/$', views.studentsuggestions, name='student_suggestion'),
    url(r'^student/suggestion/list/$', views.studentsuggestionlist.as_view(), name="suggestion_list"),
    url(r'^student/suggestion/list/admin/$', views.studentsuggestionlistadmin.as_view(), name="suggestion_list_admin"),
    url(r'^student/suggestion/list/staff/$', views.studentsuggestionliststaff.as_view(), name="suggestion_list_staff"),
    url(r'^student/suggestion/(?P<pk>[\d]+)/detail/$', views.studentsuggestiondetail.as_view(), name='suggestion_detail'),
    url(r'^student/suggestion/(?P<pk>[\d]+)/update/$', views.studentsuggestionupdate.as_view(), name='suggestion_update'),
    url(r'^student/suggestion/(?P<pk>[\d]+)/delete/$', views.studentsuggestiondelete.as_view(), name='suggestion_delete'),
 
    # Staff
    url(r'^staff/(?P<pk>[\d]+)/detail/$', views.staffdetail.as_view(), name='staff_detail'),
    url(r'^staff/registration/$', views.registerstaff, name='staff_registration'),
    url(r'^student/other/suggestion/(?P<pk>[\d]+)/add/$', views.add_suggestion, name='others_suggestion'),
    url(r'^other/suggestion/(?P<pk>[\d]+)/add/$', views.add_other_suggestion, name='add_others_suggestion'),
    url(r'^all/staff/list/$', views.allstaff, name="all_staff"),
    url(r'^searched/staffs/list/$', views.searched_stafflist.as_view(), name="searched_staff"),
    url(r'^IT/staff/list/$', views.itstafflist.as_view(), name="it_staff"),
    url(r'^LAW/staff/list/$', views.lawstafflist.as_view(), name="law_staff"),
    url(r'^FINANCE/staff/list/$', views.Financestafflist.as_view(), name="finance_staff"),
    url(r'^kigali/staff/list/$', views.Kigalistafflist.as_view(), name="kigali_staff"),
    url(r'^musanze/staff/list/$', views.Musanzestafflist.as_view(), name="musanze_staff"),
    url(r'^nyanza/staff/list/$', views.Nyanzastafflist.as_view(), name="nyanza_staff"),
    url(r'^staff/suggestion/(?P<pk>[\d]+)/delete/$', views.staffsuggestiondelete.as_view(), name='othersuggestion_delete'),

    #Reaction
    url(r'^approving/student/(?P<pk>[\d]+)/suggestion/$', views.approving_suggestion, name='approving_suggestion'),
    url(r'^denying/student/(?P<pk>[\d]+)/suggestion/$', views.denying_suggestion, name='denying_suggestion'),
    url(r'^canceling/student/(?P<pk>[\d]+)/suggestion/$', views.canceling_suggestion, name='canceling_suggestion'),
    url(r'^approving/other/(?P<pk>[\d]+)/suggestion/$', views.approving_other_suggestion, name='approving_other_suggestion'),
    url(r'^canceling/other/(?P<pk>[\d]+)/suggestion/$', views.canceling_other_suggestion, name='canceling_other_suggestion'),
    url(r'^denying/other/(?P<pk>[\d]+)/suggestion/$', views.denying_other_suggestion, name='denying_other_suggestion'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
