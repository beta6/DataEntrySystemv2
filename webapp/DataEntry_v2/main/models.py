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

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from DataEntry_v2.settings import LANGUAGES

class DataEntryUser(models.Model):
    ROLES = (
        ('GV', _('Worker')),
        ('MN', _('Data Entry Monitor')),
        ('PG', _('Developer')),
    )

    user = models.OneToOneField(User)
    rol = models.CharField(max_length=2, choices=ROLES)
    language = models.CharField(default='en-us', choices=LANGUAGES, max_length=5)

    def is_entry(self):
        if self.rol == "GV":
            return True
        else:
            return False

    def is_monitor(self):
        if self.rol == "MN":
            return True
        else:
            return False

    def is_programmer(self):
        if self.rol == "PG":
            return True
        else:
            return False

    def is_prod(self):
        if self.rol in ["GV", "MN"]:
            return True
        else:
            return False

    def __unicode__(self):
        return "%s %s (%s) %d" % (self.user.first_name, self.user.last_name, self.rol, self.user.is_active)


class Customers(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    contact = models.CharField(max_length=65)
    address = models.CharField(max_length=220)
    telephone = models.CharField(max_length=19)
    email = models.EmailField(max_length=45)

    def __unicode__(self):
        return self.name
