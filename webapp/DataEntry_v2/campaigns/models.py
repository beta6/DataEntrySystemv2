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

from django.db import models
from main.models import Customers, DataEntryUser
import select2
from parler.models import TranslatableModel, TranslatedFields

t=("int", "dec", "str", "bool")
msk=("d", "f", "s", "d")

class Campaigns(models.Model):
    id=models.AutoField(primary_key=True)
    idcustomer=models.ForeignKey(Customers)
    idworker=models.ManyToManyField(DataEntryUser)
    name=models.CharField(max_length=45)
    imagePath=models.CharField(max_length=125)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering=["name"]


class Fields(models.Model):

    TYPES=zip(t, t)

    campaign=models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    name=models.CharField(max_length=45)
    type=models.CharField(default="str", max_length=6)
    length=models.SmallIntegerField()
    fieldNum=models.SmallIntegerField()
    screenNumber=models.SmallIntegerField(default=1)
    imgPos=models.CommaSeparatedIntegerField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering=["fieldNum"]


class Properties(TranslatableModel):
    identifier=models.CharField(max_length=2)
    translations=TranslatedFields(
    description=models.CharField(max_length=255)
    )

    def __unicode__(self):
        return "%s %s" % (self.identifier, self.description)



class fieldsPerformsProperties(models.Model):
    field=models.ForeignKey(Fields, on_delete=models.CASCADE)
    property=models.ForeignKey(Properties)
    value1=models.CharField(max_length=50)
    value2=models.CharField(max_length=50)


class List(models.Model):
    name=models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % self.name

class ListOptions(models.Model):
    list=models.ForeignKey(List, on_delete=models.CASCADE)
    code=models.CharField(max_length=35)
    value=models.CharField(max_length=255)

    def __unicode__(self):
        return "%s %s" % (self.code, self.value)

