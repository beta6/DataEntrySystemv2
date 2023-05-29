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
import csv
from django.db.models import Max
from pyzbar.pyzbar import decode
from PIL import Image
from .models import ListOptions, List, fieldsPerformsProperties, Fields, Campaigns, t, msk
from entry.models import Register, Data, Blocks, Edit
import pytesseract
from csvmodule import UnicodeReader, UnicodeWriter
from DataEntry_v2.settings import MEDIA_ROOT, STATIC_ROOT
import os, re, shutil, imghdr
from glob import glob
from django.utils.translation import gettext as _
import magic

def getEncoding(fname):
    
    encoding = magic.from_file(fname)
    encoding2 = magic.from_file(fname, mime=True)
    if (encoding2=="text/plain" or encoding2=="text/csv"):
        return True
    else:
        return False

def adjustImageSize(filename, newfile):
    img=Image.open(filename)
    width=float(1200)
    origheight=float(img.size[1])
    origwidth=float(img.size[0])
    height=(origheight/origwidth)*width
    size=(int(width), int(height))
    img=img.convert("L") 
    img=img.resize(size, Image.BILINEAR) 
    if os.path.isfile(newfile): os.unlink(newfile)
    img.save(newfile)
    return


def loadImgs(fname, extractfolder, destfolder, blockid, idfields):
    
    isok, error = extract(fname, extractfolder)
    if isok:
        curdir = os.getcwd()
        os.chdir(extractfolder)
        block=Blocks.objects.filter(id=blockid).first()
        fields=Fields.objects.filter(id__in=idfields).order_by("fieldNum")
        regs=Register.objects.filter(block=block).order_by("regnum")
        for reg in regs:
            datas=Data.objects.filter(includes=reg)
            edits=Edit.objects.filter(register=reg)
            edits.delete()
            datas.delete()
        regs.delete()
        n=0
        for dp, dn, fn in os.walk(extractfolder):
            for nfile in [os.path.join(dp, f) for f in fn]:
                if not os.path.isfile(nfile):
                    continue
                filetype = imghdr.what(nfile)
                if filetype in ["jpeg", "gif", "png", "bmp", "tiff"]:
                    destfile="%08d.jpg" % n
                    adjustImageSize(nfile, os.path.join(destfolder, destfile))
                    register = Register.objects.create(block=block, image=destfile, regnum=n)
                    register.save()
                    for field in fields:
                        data = Data.objects.create(includes=register, field=field)
                        data.save()
                    n+=1
        os.chdir(curdir)
        
    return n


def loadList(fname, id):

    olist=List.objects.get(id=id)
    csv_reader = UnicodeReader(fname, delimiter=str(u':').encode('utf-8'))
    line_count = 0
    for row in csv_reader:
        listoption = ListOptions.objects.create(list=olist, code=row[0], value=row[1])
        listoption.save()
        line_count += 1

    return line_count

def createPathIfNotExists(destfolder):
    curdir=os.getcwd()
    try:
        os.chdir(destfolder)
    except:
        os.makedirs(destfolder)
    finally:
        os.chdir(curdir)
        shutil.rmtree(destfolder)
        os.makedirs(destfolder)

    os.chdir(curdir)

def extract(filename, destfolder):
    compressions={"\.zip$":"unzip -uo %s", "\.tar$":"tar xvf %s", "\.tgz$":"tar zxvf %s", "\.tar\.gz$":"tar zxvf %s","\.tar\.bz2$":"tar jxvf %s","\.rar$":"unrar e -o+ %s","\.7z$":"7z x -aoa %s"}

    if re.search("[^\d\w\.\_\-]+", filename.split("/")[-1]):
        return (False, _("Incorrect Filename. Allowed Chars: '0-9a-z._-A-Z'"))

    curdir=os.getcwd()
    createPathIfNotExists(destfolder)
    os.chdir(destfolder)
    
    for ext, cmd in compressions.items():
        if re.search(ext, filename.split("/")[-1], re.IGNORECASE):
            if os.system(cmd % filename)!=0:
                os.chdir(curdir)
                return (False, _("Error: processing compressed file: %s") % filename)
            else:
                os.chdir(curdir)
                return (True, "")
    return (False, _("Error: file type not supported."))


def cropImage(image, imgPos):
    pos = map(int, imgPos.split(","))
    img = Image.open(image).crop(pos)
    img.save("/tmp/%s.jpg" % imgPos)
    return img


def readBarCode(image, lang="", imgPos=""):
    img = cropImage(image, imgPos)
    barcode=decode(img)
    if len(barcode)>0:
        return barcode[0].data.strip()
    else:
        return ""

def getBlock(idcampaign, blocknum):
    if blocknum is None:
        blocknum=Blocks.objects.filter(campaign__id=int(idcampaign)).aggregate(Max('number'))['number__max']+1
    block=Blocks.objects.filter(campaign__id=int(idcampaign)).filter(number=int(blocknum))
    if len(block)==0:
        campaign=Campaigns.objects.get(id=int(idcampaign))
        block=Blocks.objects.create(campaign=campaign, number=int(blocknum))
        block.save()
    else:
        block=block.first()
    return block

def OCRImage(image, lang, imgPos):
    img=cropImage(image, imgPos)
    text=pytesseract.image_to_string(img, lang=lang).strip()
    return text

def getCSVCount(fname):
    lines=open(fname, "r+").readlines()
    numRegs=len(lines)
    return numRegs

def loadData(fname, idcampaign, blocknum):
    totregs=getCSVCount(fname)
    if blocknum==0:
        blocknums=Blocks.objects.filter(campaign__id=int(idcampaign)).order_by('number')
        if blocknums.exists():
            blocknum=blocknums.last().number+1
        else:
            blocknum=1
    populateDatabase(idcampaign, blocknum, totregs=totregs)
    return loadDataFields(fname, blocknum, idcampaign)


def loadDataFields(fname, blocknum, idcampaign):
    campaign=Campaigns.objects.get(id=int(idcampaign))
    fields = Fields.objects.filter(campaign=campaign).order_by("fieldNum")
    registers = Register.objects.filter(block__campaign=campaign).filter(block__number=int(blocknum))

    numRegs=0
    csv_reader = UnicodeReader(fname, delimiter=str(u':').encode('utf-8'))
    line_count = 0
    for register in registers:
        row=csv_reader.next()
        # populate with csv data
        fldn=0
        for field in fields:
            data=Data.objects.get(includes=register, field=field)
            if field.type=="str":
                dt=row[fldn] if len(row[fldn])<=field.length else row[fldn][:field.length]
            elif field.type=="bool":
                dt=bool(row[fldn])
            elif field.type=="int":
                dt=int(row[fldn])
            elif field.type=="dec":
                dt=float(row[fldn])
            else:
                dt=row[fldn]
            data.contents=dt
            data.save()
            fldn+=1
        numRegs += 1

    return numRegs

def putMask(dtype, dvalue, dlen):
    
    if dtype=="str":
        tp=u"%% %ds" % dlen
        dvalue=dvalue
    if dtype=="int":
        tp=u"%%0%dd" % dlen
        dvalue=int(dvalue)
    if dtype=="dec":
        tp=u"%%0%d.03f" % 4 if dlen<4 else dlen-3
        dvalue=float(dvalue)
        
    return tp % dvalue


def exportData(fname, idcampaign, nblock):
    fields = Fields.objects.filter(campaign__id=int(idcampaign))
    if int(nblock)==0:
        registers = Register.objects.filter(block__campaign__id=int(idcampaign)).order_by("block__number", "regnum")
    else:
        registers = Register.objects.filter(block__number=nblock).filter(block__campaign__id=int(idcampaign)).order_by("block__number", "regnum")

    numRegs=0
    if os.path.isfile(fname):
        os.unlink(fname)
    csv_writer = UnicodeWriter(fname, delimiter=str(u':').encode('utf-8'))
    for register in registers:
        row=[]
        # populate with csv data
        fldn=0
        for field in fields:
            cprops=[ prop.property.identifier for prop in fieldsPerformsProperties.objects.filter(field=field, property__identifier__startswith="C")]
            data=Data.objects.get(includes=register, field=field)
            if len(cprops)>0:
                ldata = ListOptions.objects.filter(id=data.contents.strip())[0]
                if cprops[0] in ["C1", "C2"]:
                    row.append(ldata.code)
                elif cprops[0] in ["C3", "C4"]:
                    row.append(ldata.value)
                else:
                    row.append(data.contents)
            else:
                row.append(data.contents)
            row[-1]=putMask(field.type, row[-1], field.length)
            fldn+=1
        csv_writer.writerow(row)
        numRegs += 1

    return numRegs

    



def populateDatabase(idcampaign, blocknum, totregs=None, imgfile=None):
    campaign=Campaigns.objects.get(id=int(idcampaign))
    fields = Fields.objects.filter(campaign=campaign)
    block=getBlock(idcampaign ,blocknum)
    registers = Register.objects.filter(block=block)
    
    fpaths=[]
    if imgfile is not None:
        extpath=os.path.join(MEDIA_ROOT, "images", "extract", "%04d" % int(idcampaign), "%04d" % int(blocknum))
        destpath=os.path.join(MEDIA_ROOT, "images", "entry", "%04d" % int(idcampaign), "%04d" % int(blocknum))
        createPathIfNotExists(extpath)
        createPathIfNotExists(destpath)
        ok=extract(imgfile, extpath)
        if ok[0]:
            n=0
            for dp, dn, fn in os.walk(extpath):
                for nfile in [os.path.join(dp, f) for f in fn]:
                    if not os.path.isfile(nfile):
                        continue
                    filetype = imghdr.what(nfile)
                    if filetype in ["jpeg", "gif", "png", "bmp", "tiff"]:
                        destfile="%08d.jpg" % n
                        dfl=os.path.join(destpath, destfile)
                        adjustImageSize(nfile, dfl)
                        fpaths.append(dfl)
                        n+=1

    numRegs = 0
    if campaign.imagePath.strip() == "" and totregs is not None:
        for register in registers:
            datas=Data.objects.filter(includes=register)
            edits=Edit.objects.filter(register=register)
            edits.delete()
            datas.delete()
        registers.delete()
        for numRegs in xrange(int(totregs)):
            register=Register.objects.create(regnum=numRegs, block=block)
            register.save()
            for field in fields:
                data = Data.objects.create(includes=register, field=field)
                data.save()

            numRegs += 1
    elif len(fpaths)==0:
        for register in registers:
            for data in datas:
                data.delete()
            for field in fields:
                data = Data.objects.create(includes=register, field=field)
                data.save()
            Edit.objects.filter(register=register).delete()
            numRegs += 1
    else:
        if len(registers):
            for register in registers:
                datas=Data.objects.filter(includes=register)
                datas.delete()
                Edit.objects.filter(register=register).delete()
            registers.delete()
        numRegs=0
        for fpath in fpaths:
            imgname=fpath.split("/")[-1]
            register=Register.objects.create(regnum=numRegs, image=imgname, block=block)
            register.save()
            for field in fields:
                data = Data.objects.create(includes=register, field=field)
                data.save()
            numRegs+=1
    
    return numRegs


def scanProjectImages(idcampaign, blocknum, propertyid="O1", func=OCRImage, lang="eng"):

    # OCR || BARCODE records
    
    block=getBlock(idcampaign ,blocknum)
    ocrfields=fieldsPerformsProperties.objects.filter(field__campaign__id=int(idcampaign), property__identifier=propertyid)
    ocrnum=0
    if len(ocrfields)>0:
        imagePath=ocrfields[0].field.campaign.imagePath+"/%04d/" % block.number
        registers=Register.objects.filter(block=block)
        for register in registers:
            for ocrfield in ocrfields:
                data=Data.objects.get(includes=register, field=ocrfield.field)
                text=func(os.path.join(imagePath, register.image), lang, ocrfield.field.imgPos)
                data.contents=text[:255] if len(text)>254 else text
                data.save()
                ocrnum+=1

    return ocrnum


def ocrProjectImages(idcampaign, lang):
    ocrnum=0
    for block in Blocks.objects.filter(campaign__id=int(idcampaign)).order_by("number"):
        ocrnum+=scanProjectImages(idcampaign, block.number, "O1", OCRImage, lang)
    return ocrnum


def barcodeProjectImages(idcampaign):
    ocrnum=0
    for block in Blocks.objects.filter(campaign__id=int(idcampaign)).order_by("number"):
        ocrnum+=scanProjectImages(idcampaign, block.number, "O2", readBarCode)
    return ocrnum

