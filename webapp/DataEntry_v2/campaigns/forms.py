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

from main.forms import _
from django import forms
from .models import Customers, t, Properties, Fields


class CampaignForm(forms.Form):

    name = forms.CharField(
        max_length=45,
        required=True,
    )
    customer = forms.ModelChoiceField(queryset=Customers.objects.all(), widget=forms.Select, required=True)

    isImage = forms.BooleanField(widget=forms.CheckboxInput, label=_(u"Image Project "), required=False)

    name.widget.attrs["class"] = "uk-input"
    name.widget.attrs["placeholder"] = _(u"Campaign Name")
    customer.widget.attrs["class"]="uk-select"
    customer.widget.attrs["placeholder"] = _(u"Customer")
    isImage.widget.attrs["class"] = "uk-checkbox"
    isImage.widget.attrs["placeholder"] =  _(u"Image Project")


class LoadFileForm(forms.Form):
    file=forms.FileField(widget=forms.FileInput)

    file.widget.attrs["class"] = "uk-button"
    file.widget.attrs["placeholder"] = _(u"Load File")


class LoadFileFormBatch(forms.Form):
    file=forms.FileField(widget=forms.FileInput)
    
    file.widget.attrs["class"] = "uk-button"
    file.widget.attrs["placeholder"] = _(u"Load File")
    
    batch=forms.IntegerField()

    batch.widget.attrs["class"] = "uk-input"
    batch.widget.attrs["placeholder"] = _(u"Block Number")


class FieldForm(forms.Form):

    name=forms.CharField(max_length=45)
    name.widget.attrs["class"] = "uk-input"
    name.widget.attrs["placeholder"] = _(u"Field Name")
    
    flength=forms.IntegerField(min_value=1, max_value=125)
    flength.widget.attrs["class"] = "uk-input"
    flength.widget.attrs["placeholder"] = _(u"Length")
    
    ftype=forms.CharField(widget=forms.HiddenInput, initial="str")
    screenno=forms.IntegerField(widget=forms.HiddenInput, initial=1)
    
    """
    ftype=forms.TypedChoiceField(
        choices=zip(t,t),
        widget=forms.Select,
        initial='3',
        required=True,
    )
    ftype.widget.attrs['class'] = "uk-select"
    ftype.widget.attrs['placeholder'] = _(u"Field Type")
    """

    """
    screenno=forms.IntegerField(defaultmin_value=1, max_value=99)
    screenno.widget.attrs["class"] = "uk-input"
    screenno.widget.attrs["placeholder"] = _(u"Screen Nº")
    """



class PropertiesForm(forms.Form):

    property=forms.ModelChoiceField(queryset=Properties.objects.all(), label=_(u"Properties"),
                                      empty_label=_(u"Select Property"), widget=forms.Select, required=True)
    property.widget.attrs['class'] = "uk-select uk-width-2-3"
    property.widget.attrs['placeholder'] = _(u"Property")


class ImageSelectionForm(forms.Form):
    field=forms.ModelChoiceField(queryset=Fields.objects.none(), label=_(u"Fields"),
                                      empty_label=_(u"Select Field"), widget=forms.Select, required=True)
    x1 = forms.IntegerField()
    y1 = forms.IntegerField()
    x2 = forms.IntegerField()
    y2 = forms.IntegerField()

    field.widget.attrs['class'] = "uk-select uk-width-2-3"
    field.widget.attrs['placeholder'] = _(u"Field")
    field.widget.attrs['onclick'] = "javascript:startImgSelect();"
    x1.widget.attrs["class"] = "uk-input uk-width-1-4"
    x2.widget.attrs["class"] = "uk-input uk-width-1-4"
    y1.widget.attrs["class"] = "uk-input uk-width-1-4"
    y2.widget.attrs["class"] = "uk-input uk-width-1-4"

class ListNameForm(forms.Form):

    name=forms.CharField(max_length=50)
    file=forms.FileField(widget=forms.FileInput)

    file.widget.attrs["class"] = "uk-button"
    file.widget.attrs["placeholder"] = _(u"Load File")

    name.widget.attrs["class"] = "uk-input"
    name.widget.attrs["placeholder"] = _(u"List Name")
