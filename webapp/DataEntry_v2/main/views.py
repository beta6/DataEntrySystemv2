# -*- coding: utf-8 -*-

"""
Data Entry System v2
Copyright (C) 2019-2023  Javier Garcia Gonzalez javiergargon@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import permission_required, login_required,user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from .forms import LoginForm, AddmeForm, NewPasswordForm, UserUpdateForm, CustomerUpdateForm, MultiLanguageForm
from .models import DataEntryUser, Customers
from campaigns.models import Campaigns
from entry.models import Blocks
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.utils import translation
from django.utils.translation import gettext as _

loginurl="/main/login"

def ismonitor(user):
    try:
        return user.dataentryuser.is_monitor()
    except:
        return False


def isworker(user):
    try:
        return user.dataentryuser.is_entry()
    except:
        return False


def isdeveloper(user):
    try:
        return user.dataentryuser.is_programmer()
    except:
        return False

def getMenu(item):
	MENU={
	     (u"Developer"):[
		 ["/campaigns", "database", _("Campaigns")],
		 ["/main/customers", "database", _("Customers")],
		 ["/campaigns/lists", "album", _("Lists")],
		 ["/campaigns/tasks", "list", _("Tasks")],
		 ["/entry/start/G", "server", _("Data Entry")],
		 ["/entry/start/V", "server", _("Data Verify")],
		 ["/entry/stats", "world", _("Statistics")],
		 ["/main/docs", "question", _("Docs")],
		 ["/main/about", "info", _("About")],
		 ["/main/password", "lock", _("Change Password")],
		 ["/main/language", "world", _("Language")],
		 ["/main/logout", "sign-out", _("Logout")]
	    ],
	     (u"Monitor"):[
		 ["/main/users", "users", _("Users")],
		 ["/main/project", "users", _("Project Users")],
		 ["/entry/start/G", "server", _("Data Entry")],
		 ["/entry/start/V", "server", _("Data Verify")],
		 ["/entry/stats", "world", _("Statistics")],
		 ["/main/docs", "question", _("Docs")],
		 ["/main/about", "info", _("About")],
		 ["/main/password", "lock", _("Change Password")],
		 ["/main/language", "world", _("Language")],
		 ["/main/logout", "sign-out", _("Logout")]
	     ],
	     (u"Worker"):[
		 ["/entry/start/G", "server", _("Data Entry")],
		 ["/entry/start/V", "server", _("Data Verify")],
		 ["/entry/stats", "world", _("Statistics")],
		 ["/main/docs", "question", _("Docs")],
		 ["/main/about", "info", _("About")],
		 ["/main/password", "lock", _("Change Password")],
		 ["/main/language", "world", _("Language")],
		 ["/main/logout", "sign-out", _("Logout")]
	     ],
	     (u"guest"):[
		["/main/login", "sign-in", _("Login")],
		["/main/register", "user", _("Register")],
		["/main/docs", "question", _("Docs")],
		["/main/about", "info", _("About")]
	    ]
	}
	return MENU[item]


def getMenuOptions(request,u):

    if u is not None:
        deuser = DataEntryUser.objects.get(user__id=u.id)
        lang=deuser.language
    elif "language" in request.session.keys():
        lang=request.session["language"]
    else:
        lang="en"

    if u is None:
        usr=(u"guest")
    else:	
        if deuser.is_entry():
            usr=(u"Worker")
        elif deuser.is_monitor():
            usr=(u"Monitor")
        elif deuser.is_programmer():
            usr=(u"Developer")
    
    translation.activate(lang)
    request.session.setdefault('language', lang)
    request.session["language"]=lang
    return getMenu(usr), lang

def begin(request):
    return redirect("/main/")


def start(request):
    if request.user.is_authenticated():
        return redirect("/main/controlpanel")
    options,lang = getMenuOptions(request,None)
    response = render(request, "main/start.html")
    return response

@csrf_protect
def ulogin(request):
    msg = ''
    form = LoginForm()
    active = False
    next = ""
    options,lang=getMenuOptions(request,None)
    basetemplate="main/base.html"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nick = form.cleaned_data['nick']
            passwd = form.cleaned_data['passwd']

            u = authenticate(request, username=nick, password=passwd)
            if u is not None:
                login(request, u)
                active = True
                basetemplate = "main/baselogged.html"
                msg = _("Welcome, %s") % nick
                next = request.GET.get('next', "")
                options, language=getMenuOptions(request,u)
                translation.activate(language)
                request.session["language"]=language
                if next != "":
                    return HttpResponseRedirect(next)
            else:
                msg = _(u"Username or password not valid or account disabled.")

    return render(request, "main/login.html", {'form': form, 'msg': msg, 'loggedin': active, "basetemplate":basetemplate, "options": options })

@login_required(login_url=loginurl)
def ulogout(request):
    if request.user.is_authenticated():
        action = request.user.username.encode("utf8") + _(u", Session Finished") 
        logout(request)
        options,lang = getMenuOptions(request,None)
    return render(request, "main/logout.html", {'action': action, "options":options})

@csrf_protect
def register(request):
    form=AddmeForm()
    msg=''
    saved=False
    options,lang= getMenuOptions(request,None)
    if request.method == 'POST':
        form = AddmeForm(request.POST)
        if form.is_valid():
            try:
                u=User.objects.get(username=form.cleaned_data['username'])
                msg=_("%s username already exists, try another one") % form.cleaned_data['username']
                saved=False
            except:
                name=form.cleaned_data['first_name']
                surname=form.cleaned_data['last_name']
                user=form.cleaned_data['username']
                passwd=form.cleaned_data['password']
                frol=form.cleaned_data['rol']
                language=form.cleaned_data['language']
                uuser=User.objects.create_user(username=user, password=passwd)
                uuser.first_name=name
                uuser.last_name=surname
                uuser.is_active=False
                uuser.save()
                deuser=DataEntryUser(user=uuser, rol=frol, language=language)
                deuser.save()
                msg=_("%s. Notification sent.") % user
                saved=True
        else:
            msg=_("Incorrect data. Review and retry.")
    return render(request, "main/register.html", {'form':form, 'msg':msg, 'saved':saved, "options":options})


@login_required(login_url=loginurl)
def clanguage(request):
    saved = False
    message = unicode(u"")
    options,lang = getMenuOptions(request,request.user)
    form=MultiLanguageForm(initial={'language':lang})
    if request.method == 'POST':
        frm = MultiLanguageForm(request.POST)
        if frm.is_valid():
            current = frm.cleaned_data['language']
            deuser = DataEntryUser.objects.get(user__id=request.user.id)
            deuser.language=current
            deuser.save()
            translation.activate(current)
            request.session["language"]=current
            message = _(u"Language updated to ")
            message = message.decode("utf-8") + current
            saved=True
        else:
            message = _(u"Incorrect Data")
    else:
        message = _(u"Select desired language, please")
    return render(request, "main/language.html", {'form':form, 'msg':message, 'saved':saved, 'options':options})    


@login_required(login_url=loginurl)
def password(request):
    ok = False
    message = ""
    options,lang = getMenuOptions(request,request.user)
    frm = NewPasswordForm()
    if request.method == 'POST':
        frm = NewPasswordForm(request.POST)
        if frm.is_valid():
            current = frm.cleaned_data['current']
            new = frm.cleaned_data['new']
            repeat = frm.cleaned_data['repeat']
            user = authenticate(username=request.user.username, password=current)
            if user is not None:
                if new == repeat:
                    u = User.objects.get(username__exact=request.user.username)
                    u.set_password(repeat)
                    u.save()
                    login(request, u)
                    message = _("Password updated")
                    ok = True
                else:
                    message = _("Passwords do not match")
            else:
                message = _("Incorrect Password")
        else:
            message = _("Incorrect Data")

    return render(request, "main/password.html", {'ok': ok, 'message': message, 'form': frm, "options":options})


def docs(request):
    if request.user.is_authenticated():
        options,lang=getMenuOptions(request,request.user)
        basetemplate = "main/baselogged.html"
    else:
        options,lang=getMenuOptions(request,None)
        basetemplate="main/base.html"
    response = render(request, "main/docs.html", {"options": options, "basetemplate":basetemplate})
    return response


@login_required(login_url=loginurl)
def controlpanel(request):
    options,lang = getMenuOptions(request,request.user)
    response = render(request, "main/controlpanel.html", {"user":request.user.username, "options":options})
    return response


def getUsers(request):
    options,lang = getMenuOptions(request,request.user)
    users = DataEntryUser.objects.all()
    fields = [_("Username"), _("Position"), _("First Name"), _("Last Name"), _("Active"), _("Registered Date"),
              _("Last Login")]
    return options, users, fields


@csrf_exempt
@user_passes_test(ismonitor, loginurl)
def users(request):
    frm = UserUpdateForm()
    options, users, fields = getUsers(request)
    return render(request, "main/users.html", {"form":frm, "users":users, "fields":fields, "options":options})


@csrf_exempt
@user_passes_test(ismonitor, loginurl)
def user(request):
    frm = UserUpdateForm()
    if request.method=="POST":
        frm=UserUpdateForm(request.POST)
        if frm.is_valid():
            with transaction.atomic():
                id=frm.cleaned_data["id"]
                user = User.objects.get(id__exact=int(id))
                user.first_name = frm.cleaned_data["first_name"]
                user.last_name = frm.cleaned_data["last_name"]
                user.is_active = frm.cleaned_data["is_active"]
                user.save()
                deuser=DataEntryUser.objects.get(user__id=int(id))
                deuser.rol=frm.cleaned_data["rol"]
                deuser.save()
                result='ok'
        else:
            result="invalid data"
    else:
        result = 'fail'
    return HttpResponseRedirect("/main/users")


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def customers(request):
    frm=CustomerUpdateForm()
    options,lang = getMenuOptions(request,request.user)
    customers=Customers.objects.all()
    fields=[_("Name"),_("Contact"),_("Address"),_("Telephone"),_("e-mail")]
    return render(request, "main/customers.html", {"form":frm, "customers":customers, "fields":fields, "options":options})


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def customer(request):
    frm = CustomerUpdateForm()
    if request.method=="POST":
        frm=CustomerUpdateForm(request.POST)
        if frm.is_valid():
            with transaction.atomic():
                id=frm.cleaned_data["id"]
                if int(id)==0:
                    customer = Customers.objects.create(name=frm.cleaned_data["name"])
                else:
                    customer = Customers.objects.get(id__exact=int(id))
                    customer.name = frm.cleaned_data["name"]
                customer.contact = frm.cleaned_data["contact"]
                customer.address = frm.cleaned_data["address"]
                customer.telephone = frm.cleaned_data["telephone"]
                customer.email = frm.cleaned_data["email"]
                customer.save()
                result='ok'
            return HttpResponseRedirect("/main/customers")
        else:
            result = Http404()
    else:
        result = Http404()
    return HttpResponse(result)


def about(request):
    if request.user.is_authenticated():
        options,lang=getMenuOptions(request,request.user)
        basetemplate = "main/baselogged.html"
    else:
        options,lang=getMenuOptions(request,None)
        basetemplate="main/base.html"
    response = render(request, "main/about.html", {"options": options, "basetemplate":basetemplate})
    return response

@csrf_exempt
@user_passes_test(ismonitor, loginurl)
def project(request, campaignid=None):
    options,lang = getMenuOptions(request,request.user)
    if campaignid is not None:
        saved = False
        project=get_object_or_404(Campaigns, id=int(campaignid))
        if request.method=="POST":
            ids = map(int, request.POST.getlist("checks[]"))
            print ids
            users=DataEntryUser.objects.filter(user__id__in=ids)
            project.idworker.clear()
            project.idworker.add(*users)
            project.save()
            saved=True
        elif request.method=="GET":
            pass
        selectedUsers=project.idworker.all()
        users=DataEntryUser.objects.filter(~Q(id__in=[ user.id for user in selectedUsers ]))
        return render(request, "main/projectusers.html", {"options": options, "selected":selectedUsers, "users":users, "proj":project, "projid":campaignid, "saved":saved })
    else:
        projects = Campaigns.objects.all()
        dblocks={}
        urls="/main/project/"
        return render(request, "main/projects.html", {"options": options, "projects":projects , "op":"G", "dblocks":dblocks,"urls":urls,"showblocks":False })


