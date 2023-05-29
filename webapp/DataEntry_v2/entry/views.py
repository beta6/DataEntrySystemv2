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


from django.shortcuts import render, get_object_or_404
from main.views import getMenuOptions, isdeveloper, ismonitor, isworker, loginurl
from django.contrib.auth.decorators import permission_required, login_required,user_passes_test, available_attrs
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from campaigns.models import Campaigns, Fields, fieldsPerformsProperties, ListOptions, List
from .models import Register, Data, Edit, Blocks
from main.models import DataEntryUser
from django.contrib.auth.models import User
from functools import wraps
from types import FunctionType
import django, datetime
from django.db.models import Max, Count, Q, DateTimeField
from django.db.models.functions import Trunc
import json, os
from django.core.paginator import Paginator
from collections import OrderedDict
import itertools
from django.utils.translation import gettext as _

def class_or_function_view_decorator(class_method_to_wrap='dispatch'):
    '''
    A decorator that enables other decorators to decorate both function-
    and class-based views.  Can also be used on class-based views' methods.

    Usage:
        @class_or_function_view_decorator()
        def sayhello(f):
           """
           A decorator that says hello before the function is called.
           When used on a class, it will wrap the class's `dispatch` method.

           Usage:
                @sayhello
                def saybye():
                    print 'bye!'

                @sayhello
                def MyClass(object):
                    def dispatch(self):
                        print 'bye!'
           """
           @functools.wraps(f)
           def wrapped(*args, **kwargs):
                print 'hello!'
                return f(*args, **kwargs)
            return wrapped

        @class_or_function_view_decorator('__init__')
        def saybye(f):
            """
            When this decorator is used on a class, it will wrap the class's `__init__` method,
            unlike the previous example which wrapped `dispatch`.
            """
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                x = f(*args, **kwargs)
                print 'bye!'
                return x
            return wrapped

    This decorator is used to decorate a view decorator to enable it to be used on
    function-based views or on class-based views.  If the resulting decorator is used on class-based views, you can
    choose which method of the class it will decorate, defaulting to 'dispatch' if not provided.
    If used on function-based views, the resulting decorator works as normal.

    '''
    def outside_wrapper(f):
        @wraps(f)
        def wrapped(to_be_wrapped):
            if type(to_be_wrapped) is FunctionType:
                return f(to_be_wrapped)
            else:
                setattr(to_be_wrapped, class_method_to_wrap, f(getattr(to_be_wrapped, class_method_to_wrap)))
                return to_be_wrapped
        return wrapped
    return outside_wrapper


@class_or_function_view_decorator()
def request_passes_test(test_func, login_url=loginurl):
    """
    Decorator for views that checks that the session passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the request object and returns True if the test passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            else:
                if login_url:
                    return HttpResponseRedirect(login_url)
                else:
                    return HttpResponse("403 forbidden")
        return _wrapped_view
    return decorator


def allowed(request):

    if "screen" in request.session.keys():
        if request.user.id in request.session["screen"]["users"]:
            return True
        else:
            return False
    else:
        return False

def getScreenDef(idcampaign, op, userid, blockid):
    screen={ "project":idcampaign, "operation":op, "fields":[], "currentrecord":None }
    project=get_object_or_404(Campaigns, id=int(idcampaign))
    block=Blocks.objects.filter(campaign=project).filter(number=blockid).first()
    screen["imagepath"]=os.path.join(project.imagePath, "%04d" % blockid)
    screen["block"]=blockid
    screen["projectname"] = project.name
    screen["users"]= [ user.user.id for user in project.idworker.all() ]
    screen["user"]=int(userid)
    screen["totrecs"]=int(Register.objects.filter(block=block).aggregate(Count("id"))["id__count"])
    if screen["imagepath"].strip()=="":
        wimage=False
    else:
        wimage=True
    screen["wimage"]=wimage
    fields=Fields.objects.filter(campaign=project)
    fmin=fmax=None
    for field in fields:
        if fmin is None or fmin>field.id:
            fmin=field.id
        if fmax is None or fmax<field.id:
            fmax=field.id
        properties=[ [ prop.property.identifier, prop.value1, prop.value2 ] for prop in fieldsPerformsProperties.objects.filter(field=field)]
        screen["fields"].append({"id":field.id, "name":field.name, "type":field.type, "length":field.length, "num":field.fieldNum,"screen":field.screenNumber, "imgPos":field.imgPos, "properties":properties})

    screen["fmin"]=fmin
    screen["fmax"]=fmax

    return screen


def blockOwnedByUser(project, iduser, op, block):
    user = ""
    edits=Edit.objects.filter(register__block__campaign=project).filter(register__block=block).filter(op=op)
    if len(edits)>0:
        edit=edits[0]
        user=edit.user.username
    else:
        user = _("unassigned")
    return user, (len(edits)==0)


@login_required(login_url=loginurl)
def start(request, idcampaign=None, idblock=None, op="G"):
    options,lang = getMenuOptions(request,request.user)
    ismonitor=request.user.dataentryuser.is_monitor()
    if idcampaign is None:
        dblocks={}
        dblocksusr={}
        projects = Campaigns.objects.filter(idworker__user__id=request.user.id)
        for proj in projects:
            urls=[]
            urlsowned=[]
            blocks = Blocks.objects.filter(campaign=proj)
            for block in blocks:
                blockOwned,blockEmpty=blockOwnedByUser(proj, request.user.id, op, block)
                urls.append(["/entry/start/%d/%d/%s" % (proj.id, block.number, op), block.number, blockOwned ])
                if blockOwned in [_("unassigned"), request.user.username]:
                    urlsowned.append(["/entry/start/%d/%d/%s" % (proj.id, block.number, op), block.number, blockOwned ])
            dblocks[proj.id]=urls
            dblocksusr[proj.id]=urlsowned
            
        return render(request, "main/projects.html", { "options":options, "projects":projects, "op":op, "dblocks":dblocks, "showblocks":True, "ismonitor":ismonitor, "dblocksusr":dblocksusr  })
    else:
        idcampaign=int(idcampaign)
        request.session["screen"]=getScreenDef(idcampaign, op, request.user.id, int(idblock))
        request.session["options"]=options
        request.session.modified = True
        if op=="G":
            return HttpResponseRedirect("/entry/entry?r=1")
        elif op=="V":
            return HttpResponseRedirect("/entry/verify?r=1")
        else:
            return Http404()

@login_required(login_url=loginurl)
def stop(request):
    del request.session["screen"]
    del request.session["options"]
    request.session.modified = True
    return HttpResponseRedirect("/main/controlpanel")

def getChartData(edits, mask, curop, step):

    a=[]
    data={}
    adata=[[ step,  _("Data Entry"), _("Data Verify") ]]
    for op in ["G","V"]:
        grouped = itertools.groupby(edits.filter(op=op), lambda record: record.timestamp.strftime(mask))
        for day, countsgrouped in grouped:
            l=data.get(day, [day, 0, 0])
            l[1 if op=="G" else 2]+=len(list(countsgrouped))
            data[day]=l
   
    for d in data.values():
        a.append(d)

    a=sorted(a, key=lambda x: x[0])
    adata+=a
    
    return adata


@login_required(login_url=loginurl)
def stats(request, idproject=None, iduser=None, period=None, op=None):
    options,lang = getMenuOptions(request,request.user)
    if idproject is not None:
        project=Campaigns.objects.get(id=int(idproject))
        if period == "H":
            step = 'hour'
            mask= "%Y-%m-%d, %H"
        elif period == "D":
            step = 'day'
            mask="%Y-%m-%d"
        elif period == "M":
            step = 'month'
            mask="%Y-%m"
        elif period == "Y":
            step = 'year'
            mask= "%Y"
        else:
            step = "day"
            mask = "%Y-%m-%d"
        if iduser is not None:
            if request.user.dataentryuser.is_monitor():
                if iduser is None or iduser=="A" or int(iduser)==0:
                    edits=Edit.objects.filter(register__block__campaign=project)
                else:
                    edits=Edit.objects.filter(register__block__campaign=project).filter(user__id=int(iduser))
            else:
                if iduser is not None and (iduser=="A" or int(iduser)==request.user.id):
                    if iduser == "A":
                        iduser=request.user.id
                    edits=Edit.objects.filter(register__block__campaign=project).filter(user__id=int(iduser))
                else:
                    return HttpResponse(json.dumps(False))

            if op is not None and op in ["G","V"]:
                edits=edits.filter(op=op)
            response=getChartData(edits, mask, op, step)
            return HttpResponse(json.dumps(response))
    else:
        if request.user.dataentryuser.is_monitor():
            users=User.objects.all()
            projects=Campaigns.objects.all()
        else:
            users=User.objects.filter(id=request.user.id)
            projects = Campaigns.objects.filter(idworker__user=request.user)
        periods=zip(["H", "D", "M", "Y"], [_("Hour"), _("Day"), _("Month"), _("Year")])
        ops=zip(["G", "V", "A"],[_("Data Entry"), _("Data Verify"), _("All")])
    return render(request, "entry/stats.html", {"options":options, "users":users, "sprojects":projects, "periods":periods, "ops":ops})

def getFieldsProps(fields):

    """

    B1   ByPass by Value: Salto segun valor en lista (SI)
    B2   ByPass by Value: Salto segun valor en lista (NO)
    + B3   ByPass : Salto incondicional
    + B4   ByPass Blank: Salto si el campo esta en blanco
    B5   ByPass Screen: Salto a otra pagina
    + A1   Alpha Adjust: Ajuste alfanumerico.
    + C1   identifier Select: Codigo tecleado selecciona texto en otro campo
    + C2   identifier Select: Texto selecciona codigo
    + C3   identifier Select: Autoseleccion segun desplegable.
    C4   identifier Select: Modo lista. Si el valor no existe en la lista, se crea en ella.
    + O1   OCR: Numero o Texto.
    + O2   OCR: Codigo de Barras.
    + I1   Image: Area de Imagen en pantalla para grabacion.
    + M1   Alphanumeric Mask: Mascara Alfanumerica.
    + M2   Numeric Mask: Mascara Numerica.
    + M3   Alphanumeric Mask: Transformacion de formateo del texto.
    + V1   To Be verified: Campo a verificar n veces.

    """
    line=1
    lengthForDiv=5
    curLength=0
    vfields=OrderedDict()
    for field in fields:
        ftype=field["type"]
        name=field["name"]
        flen=field["length"]
        fid=field["id"]
        nn="uk-width-1-%d" % (1 if (lengthForDiv/flen) < 1 else int(lengthForDiv/flen)) 
        if curLength % lengthForDiv == 0:
            line+=1
        curLength+=1
        if  ftype == "bool":
            vfields[name] = django.forms.BooleanField(required=False)
            vfields[name].widget.attrs['class'] = "uk-checkbox uk-width-1-1"
            vfields[name].widget.attrs["data-uk-tooltip title"] = name
            vfields[name].widget.attrs['placeholder'] = name
            vfields[name].widget.attrs['sline'] = str(line)
            vfields[name].widget.attrs['divuik'] = nn
        elif field["type"] == "dec":
            vfields[name] = django.forms.DecimalField(max_digits=flen, decimal_places=flen, required=False)
            vfields[name].widget.attrs["class"] = "uk-input uk-width-1-1"
            vfields[name].widget.attrs["data-uk-tooltip title"] = name
            vfields[name].widget.attrs["placeholder"] = name
            vfields[name].widget.attrs['sline'] = str(line)
            vfields[name].widget.attrs['divuik'] = nn
        elif field["type"] == "str":
            vfields[name] = django.forms.CharField(max_length=flen, required=False )
            vfields[name].widget.attrs["class"] = "uk-input uk-width-1-1"
            vfields[name].widget.attrs["data-uk-tooltip title"] = name
            vfields[name].widget.attrs["placeholder"] = name
            vfields[name].widget.attrs['sline'] = str(line)
            vfields[name].widget.attrs['divuik'] = nn
        elif field["type"] == "int":
            vfields[name] = django.forms.IntegerField(required=False )
            vfields[name].widget.attrs["class"] = "uk-input uk-width-1-1"
            vfields[name].widget.attrs["data-uk-tooltip title"] = name
            vfields[name].widget.attrs["placeholder"] = name
            vfields[name].widget.attrs['sline'] = str(line)
            vfields[name].widget.attrs['divuik'] = nn
        for id, value1, value2 in field["properties"]:
            n=int(id[1])
            id=id.upper()
            if id[0]=="C":
                qlist = ListOptions.objects.filter(list__id=int(value1))
                choices = [(value.id, value.__unicode__()) for value in qlist[:100]]
                if n==5:
                    vfields[name].widget.attrs["des-list"]=int(value1)
                    vfields[name].widget.attrs["des-ajax"]="2"
                    continue
                if qlist.aggregate(Count("id"))["id__count"]>100:
                    vfields[name]=django.forms.CharField(widget=django.forms.Select, max_length=15)
                    vfields[name].widget.attrs["des-ajax"]="1"
                else:
                    vfields[name]=django.forms.ChoiceField(widget=django.forms.Select, choices=choices)
                vfields[name].widget.attrs["class"] = "uk-select uk-width-1-1"
                line+=1
                curLength=lengthForDiv
                vfields[name].widget.attrs['sline'] = str(line)
                line+=1
                vfields[name].widget.attrs['divuik'] = "uk-width-1-1"
                vfields[name].widget.attrs["placeholder"] = name
                vfields[name].widget.attrs["des-list"]=int(value1)
                if n==1:
                    vfields[name].widget.attrs["des-%s" % id]=value2
                elif n>2:
                    vfields[name].widget.attrs["des-%s" % id]=""
            elif id[0] == "B":
                if n<3:
                    vfields[name].widget.attrs["des-%s-list" % id]=value1
                    vfields[name].widget.attrs["des-%s-field" % id] = value2
                else:
                    vfields[name].widget.attrs["des-%s-field" % id] = value1
            elif id[0] == "I" and n==1:
                vfields[name].widget.attrs["des-%s" % id] = "1"
            elif id[0] == "I" and n==2:
                vfields[name].widget.attrs["des-img"] = ""
            elif id[0] in ["M", "V"]:
                vfields[name].widget.attrs["des-%s" % id] = value1
            elif id[0] == "R" and n==1:
                vfields[name].required=True
            elif id[0] == "O" and n==3:
                vfields[name].widget.attrs["des-or"] = value1
            elif id[0] == "F" and n==1:
                vfields[name].widget.attrs["des-%s" % id] = "%d" % flen
            elif id[0]=="L" and n==1:
                vfields[name].widget.attrs["des-min"] = "%d" % int(value1)
            elif id[0]=="L" and n==2:
                vfields[name].widget.attrs["des-max"] = "%d" % int(value1)
                
        vfields[name].widget.attrs["des-field"] = fid
    return vfields


def get_form_class(vfields):

    form_fields = {}
    for name, field in vfields.items():
        form_fields[str(name)] = field

    # ok now form_fields has all the fields for our form
    return type(str("DynamicForm"), (django.forms.Form,), form_fields)

class DynamicForm(django.forms.Form):

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        # This should be done before any references to self.fields
        super(DynamicForm, self).__init__(*args, **kwargs)

        self.vflds = vflds =  extra

        for name, field in vflds.items():
            self.fields[str(name)] = field



def createNewEdit(screen, request, edits):

    block=Blocks.objects.filter(campaign__id=screen["project"]).filter(number=screen["block"])
    register = Register.objects.filter(block=block).filter(~Q(regnum__in=[ edit.register.regnum for edit in edits ]))
    if len(register)==0:
        return False
    edit = Edit.objects.create(register=register[0], user=request.user, op=screen["operation"])
    edit.save()
    return [edit, register[0]]

def getLastEdit(request):
    screen = request.session["screen"]
    currentrec, campaignid, op, totrecs, userid, blockid=screen["currentrecord"], screen["project"],screen["operation"], screen["totrecs"], screen["user"], screen["block"]
    block=Blocks.objects.filter(campaign__id=screen["project"]).filter(number=screen["block"])
    edits = Edit.objects.filter(op=op).filter(register__block=block)
    lastn=len(edits)
    if currentrec is None:
        currentrec=lastn-1 if lastn>0 else 0
        screen["currentrecord"]=currentrec
        request.session["screen"]=screen
        request.session.modified = True
    return lastn, edits, currentrec


def move(request, n):
    screen = request.session["screen"]
    count=screen["currentrecord"] is not None
    resp = getLastEdit(request)
    if resp:
        lastn, edits, current=resp
    else:
        return False
    current+=(n if count else 0)
    if current<lastn and lastn>0:
        if current<0:
            current=0
        edit=edits[current]
        register=edit.register
    elif lastn<screen["totrecs"]:
        resp=createNewEdit(screen, request, edits)
        if resp:
            edit, register=resp
            current=register.regnum
        else:
            return False
    else:
        return False
    screen["currentrecord"]=current
    request.session["screen"]=screen
    request.session.modified = True
    return edit, register, current


def forward(request):
    return move(request, 1)


def backward(request):
    return move(request, -1)


@request_passes_test(allowed)
def entry(request):
    options = request.session["options"]
    screen=request.session["screen"]
    imgPos=[]
    if screen["wimage"]:
        for fld in screen["fields"]:
            imgPos.append(list(map(lambda x: int(x) if len(x)>0 else 0, fld["imgPos"].strip().split(","))))
    vfields = getFieldsProps(screen["fields"])
    initial={}
    if request.method=="GET":
        mvn=int(request.GET.get("r", 1))
        form = get_form_class(vfields)
        if screen["currentrecord"]==0 and mvn<0:
            return HttpResponseRedirect("/entry/entry?r=0")
        if mvn>0:
            if mvn==1:
                resp=forward(request)
            else:
                resp=move(request, mvn)

            if resp:
                edit, register, current=resp
            else:
                image=""
                current=screen["currentrecord"]
                edit=None
                rndr=render(request, "entry/entry.html", {"options":options, "projid":screen["project"],"project":screen["projectname"], "nblock":screen["block"],"image":image, "imgPos":imgPos, "current":current,"edit":edit,"wimage":screen["wimage"], "form":form, "finished":True, "operation":screen["operation"], "lastRecord":screen["totrecs"], "fmin":screen["fmin"] , "fmax":screen["fmax"]  })
                return rndr
        elif mvn<0:
            if mvn==-1:
                resp = backward(request)
            else:
                resp=move(request, mvn)

            if resp:
                edit, register, current=resp
            else:
                image=""
                edit=None
                current=screen["currentrecord"]
                return render(request, "entry/entry.html", {"options": options, "projid": screen["project"], "project": screen["projectname"],"nblock":screen["block"],"image":image, "imgPos":imgPos, "current":current,"edit":edit,"wimage": screen["wimage"], "form": form, "finished": True, "operation": screen["operation"], "lastRecord":screen["totrecs"], "fmin":screen["fmin"] , "fmax":screen["fmax"]  })
        else:
            resp = move(request, 0)
            if resp:
                edit, register, current=resp
            else:
                image=""
                edit=None
                current=screen["currentrecord"]
                return render(request, "entry/entry.html",  {"options": options, "projid": screen["project"], "project": screen["projectname"],"nblock":screen["block"],"image":image, "imgPos":imgPos, "current":current,"edit":edit,"wimage": screen["wimage"], "form": form, "finished": True, "operation": screen["operation"], "lastRecord":screen["totrecs"], "fmin":screen["fmin"] , "fmax":screen["fmax"]  })

        datas=Data.objects.filter(includes=register)
        image=register.image
        recValue={}
        for data in datas:
            recValue[data.field.name]=data.contents
        for key in vfields.keys():
            initial[key] = recValue[key]
            if "des-ajax" in vfields[key].widget.attrs.keys():
                try:
                    vfields[key].widget.attrs["des-default"]=ListOptions.objects.get(id=int(recValue[key])).__unicode__()
                except:
                    vfields[key].widget.attrs["des-default"] =""
                vfields[key].widget.attrs["des-reg"]=recValue[key]
            else:
                vfields[key].widget.attrs["des-default"]=recValue[key]
        form=(form)(initial=initial)
    elif request.method=="POST":
        edit, register, current = move(request, 0)
        image=register.image
        form=(get_form_class(vfields))(request.POST)
        if form.is_valid():
            block=Blocks.objects.filter(campaign__id=screen["project"]).filter(number=screen["block"])
            datas = Data.objects.filter(includes__regnum=register.regnum).filter(includes__block=block)
            n=0
            for data in datas:
                isList=False
                for prop in screen["fields" ][n]["properties"]:
                    if prop[0][0]=="C":
                        if prop[0][1]!="5":
                            isList=True
                            break
                        else:
                            break

                if data.field.type=="str" and type(form.cleaned_data[data.field.name]) in [type(""), type(u"")]:
                    data.contents = form.cleaned_data[data.field.name].encode("utf8")
                elif data.field.type=="bool":
                    data.contents = bool(form.cleaned_data[data.field.name])
                elif data.field.type == "dec":
                    data.contents = float(form.cleaned_data[data.field.name])
                elif data.field.type == "int":
                    data.contents = int(form.cleaned_data[data.field.name])
                elif data.field.type=="str" and isList:
                    data.contents = str(form.cleaned_data[data.field.name.strip()].id)
                data.save()
                n+=1
            edit.register=register
            edit.timestamp=datetime.datetime.now()
            edit.save()
            return HttpResponseRedirect("/entry/entry?r=1")
    return render(request, "entry/entry.html", {"options":options, "projid":screen["project"],"project":screen["projectname"],"nblock":screen["block"],"image": image, "imgPos": imgPos, "current": current,"edit":edit,"wimage":screen["wimage"], "form":form, "finished":False, "operation":screen["operation"], "lastRecord":screen["totrecs"], "fmin":screen["fmin"] , "fmax":screen["fmax"]   })


@request_passes_test(allowed)
def verify(request):
    return entry(request)


@request_passes_test(allowed)
def vlist(request, idlist):
    search=request.GET.get("search", "")
    page=request.GET.get("page", 1)
    qlist = ListOptions.objects.filter(Q(list__id=int(idlist)) & (Q(value__contains=search) | Q(code__contains=search)))
    paginator=Paginator(qlist, 20)
    qlist=paginator.page(int(page))
    data={"results": [{"id":l.id, "text":l.__unicode__()} for l in qlist],
      "pagination": {
        "more": paginator.num_pages>int(page)
      }
    }
    return HttpResponse(json.dumps(data))


@request_passes_test(allowed)
def lists(request, idlist):
    search = request.GET.get("search", "")
    create = request.GET.get("create", "n")
    qexists = ListOptions.objects.filter(Q(list__id=int(idlist)) & (Q(value__contains=search) | Q(code__contains=search))).exists()
    if create=="y" and not qexists:
        dlist=List.objects.get(id=int(idlist))
        data=search.split(" ", 1)
        option=ListOptions.objects.create(list=dlist, code=data[0], value=data[1])
        option.save()
        qexists=True
    return HttpResponse(json.dumps(qexists))

