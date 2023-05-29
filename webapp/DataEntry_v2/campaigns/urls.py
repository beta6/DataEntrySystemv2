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
    url(r'^helper/new$', v.newhelper, name="newhelper"),
    url(r'^lists$', v.lists, name="lists"),
    url(r'^lists/(?P<pageno>\d+)$', v.lists, name="lists"),
    url(r'^lists/new$', v.listsnew, name="listsnew"),
    url(r'^lists/remove/(?P<idlist>\d+)$', v.listsremove, name="listsremove"),
    url(r'^lists/view/(?P<idlist>\d+)/(?P<pageno>\d+)$', v.listsview, name="listsview"),
    url(r'^lists/view/(?P<idlist>\d+)$', v.listsview, name="listsview"),
    url(r'^helper/edit/(?P<idcampaign>\d+)$', v.edithelper, name="edithelper"),
    url(r'^helper/remove/(?P<idcampaign>\d+)$', v.removehelper, name="removehelper"),
    url(r'^campaign/(?P<idcampaign>\d+)$', v.campaign, name="campaign"),
    url(r'^field/rm/(?P<idcampaign>\d+)/(?P<idfield>\d+)$', v.fieldrm, name="fieldrm"),
    url(r'^field/props/(?P<idcampaign>\d+)/(?P<idfield>\d+)$', v.fieldprops, name="fieldprops"),
    url(r'^field/props/rm/(?P<idcampaign>\d+)/(?P<idfield>\d+)/(?P<idprop>\w+)$', v.fieldpropsrm, name="fieldpropsrm"),
    url(r'^field/props/edit/(?P<idcampaign>\d+)/(?P<idfield>\d+)/(?P<idprop>\w+)$', v.fieldpropsedit, name="fieldpropsedit"),
    url(r'^field/(?P<idcampaign>\d+)/(?P<idfield>\d+)$', v.field, name="field"),
    url(r'^field/imgselect/(?P<idcampaign>\d+)$', v.imgselect, name="imgselect"),
    url(r'^field/imgselect/(?P<idcampaign>\d+)/(?P<idfield>\d+)$', v.imgselect, name="imgselect"),
    url(r'^fields/(?P<idcampaign>\d+)$', v.fields, name="fields"),
    url(r'^imgfile/(?P<idcampaign>\d+)$', v.imgfile, name="imgfile"),
    url(r'^imgfile/(?P<idcampaign>\d+)/(?P<block_number>\d+)$', v.imgfile, name="imgfile"),
    url(r'^startocr/(?P<idcampaign>\d+)/(?P<lang>\w+)$', v.startocr, name="startocr"),
    url(r'^startpopulate/(?P<idcampaign>\d+)/(?P<blocknum>\d+)$', v.startpopulate, name="startpopulate"),
    url(r'^startpopulate/(?P<idcampaign>\d+)/(?P<blocknum>\d+)/(?P<totreg>\d+)$', v.startpopulate, name="startpopulate"),
    url(r'^removeblock/(?P<idcampaign>\d+)/(?P<blocknum>\d+)$', v.removeblock, name="removeblock"),
    url(r'^loaddata/(?P<idcampaign>\d+)$', v.loaddata, name="loaddata"),
    url(r'^loaddata/(?P<idcampaign>\d+)/(?P<blocknum>\d+)$', v.loaddata, name="loaddata"),
    url(r'^exportdata/(?P<idcampaign>\d+)/(?P<blocknum>\d+)$', v.exportdata, name="exportdata"),
    url(r'^tasks$', v.tasks, name="tasks"),
    url(r'^$', v.campaigns, name="campaigns")
]

