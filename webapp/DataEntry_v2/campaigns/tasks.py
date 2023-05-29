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
from celery.decorators import task
from celery.utils.log import get_task_logger

from .functions import loadList, barcodeProjectImages, ocrProjectImages, populateDatabase, loadData, exportData, loadImgs, adjustImageSize

logger = get_task_logger(__name__)

@task(name="loadListTask")
def loadListTask(fname, id):
    """loads csv list"""
    logger.info("loading list %s" % fname)
    n=loadList(fname, id)
    logger.info("%d records written." % n)
    return n

@task(name="loadDataTask")
def loadDataTask(fname, idcampaign, blocknum):
    """loads csv data"""
    logger.info("loading data %s" % fname)
    n=loadData(fname, idcampaign, blocknum)
    logger.info("%d records written." % n)
    return n


@task(name="loadImgsTask")
def loadImgsTask(fname, extractfolder, destfolder, blockid, fields):
    """ load imgs """
    logger.info("loading images from %s" % fname)
    n=loadImgs(fname, extractfolder, destfolder, blockid, fields)
    logger.info("%d images/records loaded" % n)
    return n
    
@task(name="exportDataTask")
def exportDataTask(fname, idcampaign, blocknum):
    """exports csv campaign data"""
    logger.info("loading data %s" % fname)
    n=exportData(fname, idcampaign, blocknum)
    logger.info("%d records written." % n)
    return n


@task(name="populateDatabaseTask")
def populateDatabaseTask(idcampaign, blocknum, totregs=None, imgfile=None):
    """database clear and fill with blanks"""
    logger.info("populating database of project %d" % int(idcampaign))
    n=populateDatabase(idcampaign, blocknum, totregs=totregs, imgfile=imgfile)
    logger.info("%d records written." % n)
    return n

@task(name="barcodeProjectImagesTask")
def barcodeProjectImagesTask(idcampaign):
    """barcode reader task"""
    logger.info("OCR Images from campaign %d" % (int(idcampaign)))
    n=barcodeProjectImages(idcampaign)
    logger.info("%d records written." % n)
    return n


@task(name="ocrProjectImagesTask")
def ocrProjectImagesTask(idcampaign, lang):
    """ocr images task"""
    logger.info("OCR Images from campaign %d lang %s" % (int(idcampaign), lang))
    n=ocrProjectImages(idcampaign, lang)
    logger.info("%d records written." % n)
    return n

