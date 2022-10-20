# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import lxml.html
import six
from lxml.html import CheckboxValues, MultipleSelectOptions, InputElement


class FormData(dict):
    def __init__(self, form_element):
        self.frozen = False
        for key, element in form_element.inputs.items():
            skip, value = self.get_value_from_element(element)
            if skip:
                continue
            self.__setitem__(key, value)
        self.frozen = True
        self.form = form_element

    def get_value_from_element(self, element):
        if isinstance(element, InputElement):
            if element.attrib.get('type') == 'submit':
                return True, None
        value_obj = element.value
        if value_obj is None:
            return False, ''
        if isinstance(value_obj, str):
            value_obj = value_obj.lstrip('\n')
        if isinstance(value_obj, CheckboxValues):
            value_obj = [el.value for el in value_obj.group if el.value is not None]
        if isinstance(value_obj, MultipleSelectOptions):
            value_obj = list(value_obj)
        return False, value_obj

    def __setitem__(self, key, value):
        if self.frozen and key not in self:
            raise ValueError('Key %s is not in the dict. Available: %s' % (
                key, self.keys()
            ))
        dict.__setitem__(self, key, value)

    def update(self, other_dict):
        for key, value in other_dict.items():
            self[key] = value

    def submit(self, client):
        for method in ['get', 'post', 'delete']:
            url = self.form.get('hx-' + method)
            if url:
                break
        if not url:
            url = self.form.get('action')
            if not url:
                raise ValueError('Could not find an URL to send data to. Tried hx-get, hx-post, hx-delete and action')
            method = self.form.get('method')
            if not method:
                method = 'get'
            else:
                method = method.lower()
        return getattr(client, method)(url, self)


def html_form_to_dict(html, index=0, name=None, id=None):
    # type: () -> FormData
    """
    return data of a form in `html`.

    index: Return the data of the n'th form in the html. By default the first one.

    name: Return the data of the form with the given name.
    """
    tree = lxml.html.fromstring(html)
    if name is not None:
        found_names = []
        for form in tree.iterfind('.//form'):
            if form.get('name') == name:
                return FormData(form)
            found_names.append(form.get('name'))
        raise ValueError('No form with name="{name}" found. Found forms with these names: {found_names}'.format(
            name=name, found_names=found_names))
    if id is not None:
        found_ids = []
        for form in tree.iterfind('.//form'):
            if form.get('id') == id:
                return FormData(form)
            found_ids.append(form.get('id'))
        raise ValueError('No form with id="{id}" found. Found forms with these ids: {found_ids}'.format(
            id=id, found_ids=found_ids))
    return FormData(tree.forms[index])
