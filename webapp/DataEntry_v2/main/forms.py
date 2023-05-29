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

from django import forms
from django.contrib.auth.models import User
from main.models import DataEntryUser
from DataEntry_v2.settings import LANGUAGES, TESSERACT_LANGS
from django.utils.translation import gettext as _

class LoginForm(forms.Form):
    nick = forms.CharField(
        max_length=50,
        required=True,
    )
    passwd = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)

    nick.widget.attrs["class"] = "uk-input"
    nick.widget.attrs["placeholder"] = _(u"User")

    passwd.widget.attrs["class"] = "uk-input"
    passwd.widget.attrs["placeholder"] = _(u"Password")


class AddmeForm(forms.Form):
    first_name = forms.CharField(
        max_length=45,
        required=True,
    )
    first_name.widget.attrs['class'] = "uk-input"
    first_name.widget.attrs['placeholder'] = _(u"Name")

    last_name = forms.CharField(
        max_length=65,
        required=True,
    )
    last_name.widget.attrs['class'] = "uk-input"
    last_name.widget.attrs['placeholder'] = _(u"Surname")

    username = forms.CharField(
        max_length=50,
        required=True,
    )
    username.widget.attrs['class'] = "uk-input"
    username.widget.attrs['placeholder'] = _(u"User")

    password = forms.CharField(widget=forms.PasswordInput, max_length=30)
    password.widget.attrs['class'] = "uk-input"
    password.widget.attrs['placeholder'] = _(u"Password")

    rol = forms.TypedChoiceField(
        choices=(("PG", _(u"Developer")), ("MN", _(u"Monitor")), ("GV", _(u"Worker")),),
        widget=forms.Select,
        required=True,
    )

    rol.widget.attrs['class'] = "uk-select"
    rol.widget.attrs['placeholder'] = _(u"Position")
    
    language = forms.TypedChoiceField(
        choices=LANGUAGES,
        widget=forms.Select,
        required=True,
    )

    language.widget.attrs['class'] = "uk-select"
    language.widget.attrs['placeholder'] = _(u"Language")


class NewPasswordForm(forms.Form):
    current = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)
    new = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)
    repeat = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)

    current.widget.attrs['placeholder'] = _(u"Current Password")
    current.widget.attrs['class'] = "uk-input"
    new.widget.attrs['placeholder'] = _(u"New Password")
    new.widget.attrs['class'] = "uk-input"
    repeat.widget.attrs["placeholder"] = _(u"New Password (again)")
    repeat.widget.attrs['class'] = "uk-input"


class MultiLanguageForm(forms.Form):
    language = forms.TypedChoiceField(
        choices=LANGUAGES,
        widget=forms.Select,
        initial='1',
        required=True,
    )
    language.widget.attrs['class'] = "uk-select"
    language.widget.attrs['placeholder'] = _(u"Language")

class MultiLanguageTesseractForm(forms.Form):
    language = forms.TypedChoiceField(
        choices=TESSERACT_LANGS,
        widget=forms.Select,
        initial='1',
        required=True,
    )
    language.widget.attrs['class'] = "uk-select"
    language.widget.attrs['placeholder'] = u"Tesseract "+_(u"Language")



class UserCampaignChoiceForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=DataEntryUser.objects.all(),
                                           widget=forms.SelectMultiple, required=True)
    users.widget.attrs['class'] = "uk-select"
    users.widget.attrs['style'] = _(u"Users")


class UserUpdateForm(forms.Form):

    id = forms.IntegerField(widget=forms.HiddenInput)
    first_name = forms.CharField(
        max_length=45,
        required=True,
    )
    first_name.widget.attrs['class'] = "uk-input"
    first_name.widget.attrs['placeholder'] = _(u"Name")

    last_name = forms.CharField(
        max_length=65,
        required=True,
    )
    last_name.widget.attrs['class'] = "uk-input"
    last_name.widget.attrs['placeholder'] = _(u"Surname")

    rol = forms.TypedChoiceField(
        choices=(("PG", _(u"Developer")), ("MN", _(u"Monitor")), ("GV", _(u"Worker")),),
        widget=forms.Select,
        required=True,
    )

    rol.widget.attrs['class'] = "uk-select"
    rol.widget.attrs['placeholder'] = _(u"Position")

    is_active = forms.BooleanField(widget=forms.CheckboxInput, label=_(u"Active"), required=False)

    is_active.widget.attrs['class'] = "uk-checkbox"
    is_active.widget.attrs['id'] = "ckactive"


class CustomerUpdateForm(forms.Form):

    id = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField(
        max_length=45,
        required=True,
    )
    name.widget.attrs['class'] = "uk-input"
    name.widget.attrs['placeholder'] = _(u"Name")

    contact = forms.CharField(
        max_length=65
    )
    contact.widget.attrs['class'] = "uk-input"
    contact.widget.attrs['placeholder'] = _(u"Contact")

    address = forms.CharField(max_length=220)

    address.widget.attrs['class'] = "uk-input"
    address.widget.attrs['placeholder'] = _(u"Address")

    telephone = forms.CharField(
        max_length=19
    )
    telephone.widget.attrs['class'] = "uk-input"
    telephone.widget.attrs['placeholder'] = _(u"Telephone")

    email=forms.EmailField()
    email.widget.attrs['class'] = "uk-input"
    email.widget.attrs['placeholder'] = _(u"e-mail")
