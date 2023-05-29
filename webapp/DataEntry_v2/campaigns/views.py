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

import os, re, shutil, imghdr
import json
from PIL import Image
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import permission_required, login_required,user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from main.views import getMenuOptions, isdeveloper, loginurl
from .models import Campaigns, Fields, Properties, fieldsPerformsProperties, List, ListOptions
from .forms import CampaignForm, LoadFileForm, LoadFileFormBatch, FieldForm, PropertiesForm, ImageSelectionForm, ListNameForm
from main.forms import MultiLanguageTesseractForm
from entry.models import Register, Blocks, Edit, Data
from DataEntry_v2.settings import MEDIA_ROOT, BASE_DIR, TESSERACT_LANGS
from django.db.models import Max, Count
from django.core.paginator import Paginator
from .tasks import loadListTask, barcodeProjectImagesTask, ocrProjectImagesTask, populateDatabaseTask, loadDataTask, exportDataTask, loadImgsTask
import django
import csv, imghdr
from collections import OrderedDict
from .functions import extract, createPathIfNotExists, adjustImageSize, getBlock, getEncoding
from django.utils.translation import gettext as _
import pickle

fieldstitles = [_(u"Field Name"), _(u"Field Type"), _(u"Length"), _(u"Field Nº"),_(u"Screen Nº")]
props = {"B1":["list", "field"],"B2":["list", "field"],"B3":["field"], "B4":["field"], "B5":["screen"], "A1":["mask"], "C1":["list", "field"], "C2":["list"], "C3":["list"], "C4":["list"], "C5":["list"], "O1":[], "O2":[], "I1":[],"M1":["mask"], "M2":["mask"], "M3":["mask"], "V1":["int"], "R1":[], "F1":[], "L1":["int"], "L2":["int"], "O3":["field"], "I2":[]}


def getTask(request):
    if "task" not in request.session.keys():
        request.session["task"]=pickle.dumps([])
        request.session["tasks"]=[]
        request.session.modified = True
    return pickle.loads(request.session["task"])

def putTask(request, task):
    request.session["task"]=pickle.dumps(task)
    request.session.modified = True
    return

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def newhelper(request):
    options,lang = getMenuOptions(request,request.user)
    campaignform=CampaignForm()
    imgfileform=LoadFileForm()
    loaddataform = LoadFileForm()
    fieldform=FieldForm()
    fields=Fields.objects.filter(campaign__id=-1)
    campaignid=0
    return render(request, "campaigns/helper.html", {"options":options, "campaignform":campaignform, "imgfileform":imgfileform, "campaignid":campaignid, "fieldstitles":fieldstitles, "fieldform":fieldform, "fields":fields, "loaddataform":loaddataform, "blocknumber":1 })


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def edithelper(request, idcampaign):
    options,lang = getMenuOptions(request,request.user)
    campaign=get_object_or_404(Campaigns, id__exact=int(idcampaign))
    campaignform=CampaignForm(initial={"name":campaign.name, "customer":campaign.idcustomer, "isImage":"on" if campaign.imagePath != "" else "" })
    fields=Fields.objects.filter(campaign__id=int(idcampaign))
    imgfileform = LoadFileForm()
    fieldform = FieldForm()
    return render(request, "campaigns/helper.html", {"options": options, "campaignform": campaignform, "imgfileform":imgfileform, "campaignid": int(idcampaign), "fieldstitles":fieldstitles, "fieldform":fieldform, "fields":fields, "blocknumber":1 })


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def removehelper(request, idcampaign):
    campaign=get_object_or_404(Campaigns, id__exact=int(idcampaign))
    campaign.delete()
    return HttpResponseRedirect("/campaigns")

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def lists(request, pageno=1):
    options,lang = getMenuOptions(request,request.user)
    alists=ListOptions.objects.values('list__name', 'list__pk').order_by('list__name').annotate(Count('code'))
    paginator=Paginator(alists, 25)
    page=paginator.page(pageno)
    return render(request, "campaigns/lists.html", {"options":options, "lists":page, "pages":page, "title":_("List Name"), "count":_("Count")})



@user_passes_test(isdeveloper, loginurl)
def listsnew(request):

    task = getTask(request)
    options,lang = getMenuOptions(request,request.user)
    form=ListNameForm()
    helptext=_("Enter csv file with separator ':' and two fields: code and value")
    redirecttotasks=False
    if request.method == "POST":
        form=ListNameForm(request.POST, request.FILES)
        if form.is_valid():
            listName=form.cleaned_data["name"]
            file = request.FILES['file']
            if not file:
                return HttpResponse(_("error saving file..."))
            fname=os.path.join('/tmp', "nlist.txt")
            with open(fname, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if not getEncoding(fname):
                helptext=_("file must be utf-8 encoding")
            else:
                olist=List.objects.create(name=listName)
                olist.save()

                task.append(loadListTask.delay(fname, olist.id))
                putTask(request, task)
                data = {"href": "",  "text": _("List load ") + file.name}
                request.session["tasks"].append({"task": task[-1].status, "data": data, "name": _("Import Data")})
                redirecttotasks=True
    return render(request, "campaigns/newlist.html", {"options":options, "listform":form, "helptext":helptext,"redirect2tasks":redirecttotasks})

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def listsremove(request, idlist):
    alist = get_object_or_404(List, id__exact=int(idlist))
    alist.delete()
    return HttpResponseRedirect("/campaigns/lists")

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def listsview(request, idlist, pageno=1):
    options,lang = getMenuOptions(request,request.user)
    alist = get_object_or_404(List, id__exact=int(idlist))
    optlist=ListOptions.objects.filter(list=alist)
    paginator=Paginator(optlist, 25)
    page=paginator.page(pageno)
    return render(request, "campaigns/listview.html", {"options":options, "lists":page, "idlist":idlist, "code":_("Code"), "value":_("Value")})


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def campaign(request, idcampaign):

    if request.method=="POST":
        id=int(idcampaign)
        form=CampaignForm(request.POST)
        if form.is_valid():
            imagePath=""
            if id==0:
                campaign = Campaigns.objects.create(name=form.cleaned_data["name"], idcustomer=form.cleaned_data["customer"], imagePath=imagePath)
                campaign.save()
                block = getBlock(campaign.id, 1)
                if form.cleaned_data['isImage']:
                    imagePath = os.path.join(MEDIA_ROOT, "images/entry/%04d/" % campaign.id)
                    if not os.path.exists(imagePath+"/%04d/" % 1):
                        os.makedirs(imagePath+"/%04d/" % 1)
                    campaign.imagePath=imagePath
            else:
                try:
                    campaign = Campaigns.objects.get(id__exact=id)
                except:
                    return HttpResponse(Http404())
                else:
                    campaign.name=form.cleaned_data["name"]
                    campaign.idcustomer=form.cleaned_data["customer"]
                    if form.cleaned_data['isImage']:
                        imagePath = os.path.join(MEDIA_ROOT, "images/entry/%04d/" % id)
                        if not os.path.exists(imagePath+"/%04d/" % 1):
                            os.makedirs(imagePath+"/%04d/" % 1)
                        campaign.imagePath=imagePath
            campaign.save()
            response= HttpResponse("ok %d" % campaign.id)
            response.set_cookie('cid', campaign.id)
        else:
            response= HttpResponse("'invalid form'")
        return response
    else:
        return HttpResponse("'not implemented'")

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def campaigns(request):
    if "tasks" not in request.session.keys():
        request.session["tasks"]=[]
        request.session.modified = True
    options,lang = getMenuOptions(request,request.user)
    campaigns = Campaigns.objects.all()
    loaddataform=LoadFileFormBatch()
    imgfileform=LoadFileForm()
    tesseractForm=MultiLanguageTesseractForm()
    fields = [_("Name"), _("Customer"), _("Image Project")]
    return render(request, "campaigns/campaigns.html", {"options":options, "campaigns":campaigns, "fields":fields, "loaddataform":loaddataform, "imgfileform":imgfileform, "tesseractForm":tesseractForm, "languages":TESSERACT_LANGS})

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def removeblock(request, idcampaign, blocknum):
    Edit.objects.filter(register__block__number=int(blocknum)).delete()
    Register.objects.filter(block__number=int(blocknum)).delete()
    Blocks.objects.filter(campaign__id=int(idcampaign)).filter(number=int(blocknum)).delete()
    return HttpResponse('Ok');

    
def createPathIfNotExists(destfolder):
    curdir=os.getcwd()
    if os.path.isdir(destfolder):
        os.chdir(destfolder)
    else:
        os.makedirs(destfolder)
        os.chdir(curdir)
    shutil.rmtree(destfolder)
    os.makedirs(destfolder)
    os.chdir(curdir)

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def imgfile(request, idcampaign, block_number=None):

    campaign = get_object_or_404(Campaigns, id=int(idcampaign))
    if request.method=="POST":
        frm=LoadFileForm(request.POST, request.FILES)
        if frm.is_valid():
            destfolder = os.path.join(MEDIA_ROOT, "images", "entry", "%04d" % int(idcampaign))
            if not os.path.exists(destfolder):
                os.mkdir(destfolder)

            file = request.FILES['file']                
                
            if not file:
               return HttpResponse("error saving file...")
            else:
               fname=os.path.join('/tmp', file.name)
               with open(fname, 'wb+') as destination:
                   for chunk in file.chunks():
                       destination.write(chunk)    
              
               ftype=imghdr.what(fname)
               imgfile={"jpeg":"jpg", "gif":"gif", "png":"png", "bmp":"bmp", "tiff":"tif"}
               if ftype not in imgfile.keys() or re.search("[^\w\.\-\_]+", file.name):
                   return HttpResponse("image not supported")
               ext=imgfile[ftype]
               fdest="%08d.%%s" % (0)
               fnpdest=os.path.join("/tmp", fdest % ext)
               shutil.copy(fname, fnpdest)
               adjustImageSize(fname, os.path.join(MEDIA_ROOT, "images", "entry", "%04d" % int(idcampaign), fdest % "jpg"))

            return HttpResponse("ok")
        else:
            return HttpResponse("form not valid")
    return HttpResponse("method unknown")


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def field(request, idcampaign, idfield):

    campaign = get_object_or_404(Campaigns, id=int(idcampaign))
    idf=int(idfield)
    if idf!=0:
        field=get_object_or_404(Fields, fieldNum=idf, campaign=campaign)
    if request.method=="POST":
        fieldform=FieldForm(request.POST)
        if fieldform.is_valid():
            #ftype=fieldform.cleaned_data["ftype"]
            #screenno=int(fieldform.cleaned_data["screenno"])
            name=fieldform.cleaned_data["name"]
            length=int(fieldform.cleaned_data["flength"])
            ftype="str"
            screenno=1
            fieldno = idf
            if fieldno!=0:
                field.name=name
                field.type=ftype
                field.length=length
                field.screenNumber=screenno
                field.fieldNum=fieldno
            else:
                fields=Fields.objects.filter(campaign=campaign)
                fieldno=fields.aggregate(Max("fieldNum"))['fieldNum__max']
                fieldno=1 if fieldno is None else fieldno+1
                field=Fields.objects.create(name=name, type=ftype, length=length, screenNumber=screenno, campaign=campaign, fieldNum=fieldno)
            field.save()
            isok=True
            msg=""
        else:
            isok=False
            msg=_("Invalid data. Correct it and retry.")
    elif request.method=="GET":
        if idf==0:
            fieldform = FieldForm()
            msg=""
        else:
            fieldform=FieldForm(initial={"name":field.name, "ftype":field.type, "flength":field.length, "screenno":field.screenNumber, "fieldNum":field.fieldNum})
        isok=False
        msg=""
    else:
        return HttpResponse("method not implemented")

    data = render(request, "campaigns/field.html",  { "fieldform": fieldform, "cid":idcampaign, "fid":idf, "msg":msg })
    return HttpResponse(json.dumps({"data":data.content, "isok":isok}))

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def fields(request, idcampaign):
    fields=Fields.objects.filter(campaign__id=int(idcampaign))
    return render(request, "campaigns/fields.html", {"fields":fields, "campaignid":idcampaign})


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def fieldrm(request, idcampaign, idfield):
    idf=int(idfield)
    campaign=get_object_or_404(Campaigns, id=int(idcampaign))
    field = get_object_or_404(Fields, fieldNum=idf, campaign=campaign)
    if field is not None:
        field.delete()
        return HttpResponse("ok")
    else:
        return HttpResponse("fail")


def get_form_class(vfields):

    form_fields = OrderedDict()
    for name, field in vfields.items():
        form_fields['field_%s'  % (name)] = field

    # ok now form_fields has all the fields for our form
    return type(str("DynamicForm"), (django.forms.Form,), form_fields)

def getFieldProps(id, idcampaign):

    vfields=OrderedDict()
    for control in props[id]:
        if control=="list":
            vfields[control+id]=django.forms.ModelChoiceField(queryset=List.objects.all(), label=_(u"List"), \
                                      empty_label=_(u"Select List"), widget=django.forms.Select, required=True)
            vfields[control+id].widget.attrs['class'] = "uk-select"
            vfields[control+id].widget.attrs['placeholder'] = _(u"List")
        elif control=="field":
            fields = Fields.objects.filter(campaign__id=int(idcampaign))
            vfields[control+id]=django.forms.ModelChoiceField(queryset=fields, label=_(u"Field"), \
                                      empty_label=_(u"Select Field"), widget=django.forms.Select, required=True)
            vfields[control+id].widget.attrs['class'] = "uk-select"
            vfields[control+id].widget.attrs['placeholder'] = _(u"Field")
        elif control=="screen":
            maxscreen = fields.aggregate(Max("screenNumber"))['screenNumber__max']
            vfields[control+id]=django.forms.IntegerField(min_value=1, max_value=maxscreen)
            vfields[control+id].widget.attrs["class"] = "uk-input"
            vfields[control+id].widget.attrs["placeholder"] = _(u"Screen")
        elif control == "mask":
            vfields[control+id]=django.forms.CharField(max_length=45)
            vfields[control+id].widget.attrs["class"] = "uk-input"
            vfields[control+id].widget.attrs["placeholder"] = _(u"Field Name")
        elif control == "int":
            vfields[control+id]=django.forms.IntegerField()
            vfields[control+id].widget.attrs["class"] = "uk-input"
            vfields[control+id].widget.attrs["placeholder"] = _(u"Integer")

    return vfields



@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def fieldprops(request, idcampaign, idfield):
    properties=PropertiesForm()
    properties.fields['property'].queryset=Properties.objects.language(request.session["language"]).all()
    campaign=get_object_or_404(Campaigns, id=int(idcampaign))
    fieldsprops=fieldsPerformsProperties.objects.filter(field__fieldNum=int(idfield)).filter(field__campaign=campaign)
    field = Fields.objects.filter(fieldNum=int(idfield)).filter(campaign=campaign).first()
    fieldname=field.name
    initial={}
    formsProps=OrderedDict()
    for fp in fieldsprops:
        fid=fp.property.identifier
        vfields=getFieldProps(fid, idcampaign)
        keys=vfields.keys()
        f=None
        if len(keys)>0:
            value = fp.value1
            if keys[0]=="list"+fid and value!="":
                f=List.objects.filter(id=int(value))
            elif keys[0]=="field"+fid and value!="":
                f=Fields.objects.filter(campaign__id=int(idcampaign)).filter(id=int(value))
            if f is not None and f.exists():
                value=f.first().id
            initial["field_%s" % (keys[0])] = value
        f=None
        if len(keys)>1:
            value = fp.value2
            if keys[1]=="list"+fid and value!="":
                f=List.objects.filter(id=int(value))
            elif keys[1]=="field"+fid and value!="":
                f=Fields.objects.filter(campaign__id=int(idcampaign)).filter(id=int(value))
            if f is not None and f.exists():
                value=f.first().id
            initial["field_%s" % (keys[1])] = value
        formsProps[fid]=(get_form_class(vfields))(initial=initial)
    if request.method=="POST":
        properties=PropertiesForm(request.POST)
        properties.fields['property'].queryset=Properties.objects.language(request.session["language"]).all()
        if properties.is_valid():
            _property=properties.cleaned_data['property']
            if fieldsPerformsProperties.objects.filter(field=field).filter(property=_property).count()==0:
                fpp=fieldsPerformsProperties.objects.create(field=field, property=_property, value1="", value2="")
                fpp.save()
    return render(request, "campaigns/properties.html", {"properties": properties, "campaignid": idcampaign, "fieldid":idfield, "fieldsprops":fieldsprops, "fieldname":fieldname, "formsProps":formsProps})


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def fieldpropsrm(request, idcampaign, idfield, idprop):
    fprop=fieldsPerformsProperties.objects.filter(field__campaign__id=int(idcampaign)).filter(field__fieldNum=int(idfield)).filter(property__identifier=idprop)
    if fprop.exists():
        fprop.first().delete()
    return HttpResponse("ok")

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def fieldpropsedit(request, idcampaign, idfield, idprop):
    campaign = get_object_or_404(Campaigns, id=int(idcampaign))
    fieldsprops=fieldsPerformsProperties.objects.filter(field__fieldNum=int(idfield)).filter(field__campaign=campaign).filter(property__identifier=idprop).first()
    vfields = getFieldProps(idprop, idcampaign)
    formsProps = get_form_class(vfields)
    if request.method=="POST":
        form=formsProps(request.POST)
        if form.is_valid():
            keys=vfields.keys()
            if len(keys) > 0:
                if keys[0] in ["int"+idprop, "screen"+idprop]:
                    fieldsprops.value1 = form.cleaned_data['field_%s' % keys[0]]
                elif keys[0] in ["list"+idprop, "field"+idprop]:
                    fieldsprops.value1 = form.cleaned_data['field_%s' % keys[0]].id
                else:
                    fieldsprops.value1 = form.cleaned_data['field_%s' % keys[0]]
            if len(keys) > 1:
                if keys[1] in ["int"+idprop, "screen"+idprop]:
                    
                    fieldsprops.value2 = form.cleaned_data['field_%s' % keys[1]]
                elif keys[1] in ["list"+idprop, "field"+idprop]:
                    fieldsprops.value2 = form.cleaned_data['field_%s' % keys[1]].id
                else:
                    fieldsprops.value2 = form.cleaned_data['field_%s' % keys[1]]
            fieldsprops.save()
        else:
            return HttpResponse(_("invalid form"))
    return HttpResponse("ok")

@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def imgselect(request, idcampaign, idfield=None):

    if idfield is not None:
        vfield = Fields.objects.filter(campaign__id=int(idcampaign), id=int(idfield))[0]
        initial = {"field": vfield.id}
        if vfield.imgPos.strip()=="":
            values=[0]*4
        else:
            values = map(int, vfield.imgPos.split(","))
        for var, value in zip(['x1', 'y1', 'x2', 'y2'], values):
            initial[var] = value
        imageSForm = ImageSelectionForm(initial=initial)
    else:
        imageSForm = ImageSelectionForm()
        vfield = None
    imageSForm.fields['field'].queryset=Fields.objects.filter(campaign__id=int(idcampaign))

    if request.method=="POST":
        imageSForm=ImageSelectionForm(request.POST)
        imageSForm.fields['field'].queryset = Fields.objects.filter(campaign__id=int(idcampaign))

        if imageSForm.is_valid():
            if idfield is None:
                field = imageSForm.cleaned_data['field']
                vfield = Fields.objects.filter(campaign__id=int(idcampaign), name=field)[0]
            else:
                vfield = Fields.objects.filter(campaign__id=int(idcampaign), id=int(idfield))[0]
                field=vfield.name

            avar=[]
            for var in ['x1', 'y1', 'x2', 'y2']:
                avar.append(str(imageSForm.cleaned_data['%s' % var]).strip())
            vfield.imgPos=",".join(avar)
            vfield.save()
        else:
            if idfield is not None:
                vfield = Fields.objects.filter(campaign__id=int(idcampaign), id=int(idfield))[0]
                initial = {"field": vfield.id}
                values = map(int, vfield.imgPos.split(","))
                for var, value in zip(['x1', 'y1', 'x2', 'y2'], values):
                    initial[var] = value
                imageSForm = ImageSelectionForm(initial=initial)
            else:
                imageSForm = ImageSelectionForm()
                vfield = None
            imageSForm.fields['field'].queryset = Fields.objects.filter(campaign__id=int(idcampaign))

    return render(request, "campaigns/imgselect.html", { "imageSelectionForm":imageSForm, "campaignid": int(idcampaign), "vfield":vfield })


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def startocr(request, idcampaign, lang):

    task = getTask(request)    
    task.append(barcodeProjectImagesTask.delay(idcampaign))
    putTask(request, task)
    data={ "href":"", "text":_("BarCode read from campaign ") + str(int(idcampaign)) }
    request.session["tasks"].append({ "task":task[-1].status, "data":data, "name":"BarCode" })
    request.session.modified = True
   
    task = getTask(request)  
    task.append(ocrProjectImagesTask.delay(idcampaign, lang))
    putTask(request, task)
    data={ "href":"", "text":_("OCR read from campaign ") + str(int(idcampaign)) }
    request.session["tasks"].append({ "task":task[-1].status, "data":data, "name":"OCR" })
    request.session.modified = True
   
    return HttpResponse("ok")


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def startpopulate(request, idcampaign, blocknum, totreg=None, imgfile=None):
    
    form=LoadFileForm()
    if request.method == "POST":
        form=LoadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filen = request.FILES['file']
            if not filen:
                return HttpResponse(_("error saving file..."))
            fname=os.path.join('/tmp', filen.name)
            with open(fname, 'wb+') as destination:
                for chunk in filen.chunks():
                    destination.write(chunk)
            task = getTask(request)  
            task.append(populateDatabaseTask.delay(idcampaign, blocknum, totreg, imgfile=fname))
            putTask(request, task)
            data={ "href":"", "text":_("Campaign ") + str(int(idcampaign))  + _(", filling in") }
            request.session["tasks"].append({ "task":task[-1].status, "data":data, "name":_("Clear&Fill Data") })
            request.session.modified = True
    elif request.method == "GET":
            task = getTask(request)  
            task.append(populateDatabaseTask.delay(idcampaign, blocknum, totreg, imgfile=None))
            putTask(request, task)
            data={ "href":"", "text":_("Campaign ") + str(int(idcampaign))  + _(", filling in") }
            request.session["tasks"].append({ "task":task[-1].status, "data":data, "name":_("Clear&Fill Data") })
            request.session.modified = True

    return HttpResponse("ok")


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def loaddata(request, idcampaign, blocknum=0):

    task = getTask(request)      
    form=LoadFileForm()
    if request.method == "POST":
        form=LoadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file:
                return HttpResponse("error saving file...")
            fname=os.path.join('/tmp', file.name)
            with open(fname, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            if not getEncoding(fname):
                return HttpResponse("fail encoding")
            task.append(loadDataTask.delay(fname, int(idcampaign), blocknum))
            putTask(request, task)
            data = {"href": "", "text": _("Load Data from campaign ") + str(int(idcampaign))}
            request.session["tasks"].append({"task":task[-1].status, "data": data, "name": _("Load Data")})
            request.session.modified = True
            return HttpResponse("ok")
    return HttpResponse("fail")


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def exportdata(request, idcampaign, blocknum):
    
    fname=os.path.join("exports", str(idcampaign)+"_"+str(blocknum)+".csv")
    fpath=os.path.join(MEDIA_ROOT, fname)
    task = getTask(request)  
    task.append(exportDataTask.delay(fpath, idcampaign, blocknum))
    putTask(request, task)
    data={ "href":"/media/%s" % fname, "text":_("Download campaign ").decode("utf-8") + ("%d >> B %d " % (int(idcampaign) ,int(blocknum))) }
    request.session["tasks"].append({ "task":task[-1].status, "data":data, "name":_("Export Data").decode("utf-8") })
    request.session.modified = True
    return HttpResponse("ok")


@csrf_exempt
@user_passes_test(isdeveloper, loginurl)
def tasks(request):

    options,lang = getMenuOptions(request,request.user)
    task = getTask(request)
    if "tasks" in request.session.keys():
        atasks=request.session["tasks"]
        la, lt=len(atasks), len(task)
        mi = la if la<lt else lt
        for i in range(mi):
            if i < len(atasks):
                atasks[i]["task"]=task[i].status
        request.session["tasks"]=atasks
    else:
        del task[:]
        atasks=[]
        request.session["tasks"]=[]
    
    putTask(request, task)            
    request.session.modified = True
    status=_("Status")
    name = _("Name")
    data = _("Data")
    return render(request, "campaigns/tasks.html", {"tasks":atasks, "status":status, "name":name, "data":data, "options":options })


