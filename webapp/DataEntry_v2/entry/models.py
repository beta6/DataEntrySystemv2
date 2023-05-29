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
from main.models import User
from campaigns.models import Campaigns, Fields
from django.utils import timezone

class Blocks(models.Model):
    campaign=models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    number=models.IntegerField() 
    
    class Meta:
        ordering=["campaign", "number"]

class Register(models.Model):
    block=models.ForeignKey(Blocks, on_delete=models.CASCADE)
    image=models.CharField(max_length=25, default="", blank=True)
    regnum=models.IntegerField()

    class Meta:
        ordering=["regnum"]

    def __unicode__(self):
        return "%s %d" % (self.image, self.regnum)


class Data(models.Model):
    id=models.AutoField(primary_key=True)
    includes = models.ForeignKey(Register, on_delete=models.CASCADE)
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    contents=models.CharField(max_length=255, null=True)

    class Meta:
        ordering=["includes", "field"]
    
    def __unicode__(self):
        return "%s" % (self.contents)

class Edit(models.Model):
    t=("G", "V")
    opt=zip(t, t)

    register=models.ForeignKey(Register, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    op=models.CharField(choices=opt, max_length=1)
    timestamp=models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=["register"]
    
    def __unicode__(self):
        return "%d %d %s" % (self.register.regnum, self.user.id, self.timestamp)
