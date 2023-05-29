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
from django.conf.urls import include, url
import views as v

urlpatterns=[
    url(r'^start/(?P<op>(G|V))$', v.start, name="start"),
    url(r'^start/(?P<idcampaign>\d+)/(?P<idblock>\d+)/(?P<op>(G|V))$', v.start, name="start"),
    url(r'^entry$', v.entry, name="entry"),
    url(r'^verify$', v.verify, name="verify"),
    url(r'^stats$', v.stats, name="stats"),
    url(r'^stats/(?P<idproject>\d+)/(?P<iduser>(\d+|A))/(?P<period>\w+)/(?P<op>(G|V|A))$', v.stats, name="stats"),
    url(r'^stop$', v.stop, name="stop"),
    url(r'^list/(?P<idlist>\d+)$', v.vlist, name="vlist"),
    url(r'^lists/(?P<idlist>\d+)$', v.lists, name="lists")
]
