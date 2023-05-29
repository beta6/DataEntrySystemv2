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
    url(r'^$', v.start, name="start"),
    url(r'^login$', v.ulogin, name="login"),
    url(r'^logout$', v.ulogout, name="logout"),
    url(r'^register$', v.register, name="register"),
    url(r'^language$', v.clanguage, name="language"),
    url(r'^password$', v.password, name="password"),
    url(r'^docs$', v.docs, name="docs"),
    url(r'^controlpanel$', v.controlpanel, name="controlpanel"),
    url(r'^users$', v.users, name="users"),
    url(r'^user$', v.user, name="user"),
    url(r'^customers$', v.customers, name="customers"),
    url(r'^customer$', v.customer, name="customer"),
    url(r'^project$', v.project, name="project"),
    url(r'^project/(?P<campaignid>\d+)$', v.project, name="project"),
    url(r'^about$', v.about, name="about")
]
