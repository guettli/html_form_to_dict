from collections import UserDict

import lxml.html
from lxml.html import CheckboxValues, MultipleSelectOptions


class FormData(UserDict):
    def __init__(self, *args, **kwargs):
        self.frozen = False
        super().__init__(*args, **kwargs)
        self.frozen = True

    def __setitem__(self, key, value):
        if self.frozen and key not in self:
            raise ValueError('Key %s is not in the dict. Available: %s' % (
                key, self.keys()
            ))
        if value is None:
            value = ''
        if isinstance(value, str):
            value = value.lstrip('\n')
        if isinstance(value, CheckboxValues):
            value = [el.value for el in value.group if el.value is not None]
        if isinstance(value, MultipleSelectOptions):
            value = list(value)
        super().__setitem__(key, value)


def html_form_to_dict(html, index=0, name=None, id=None) -> FormData:
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
                return FormData(form.fields)
            found_names.append(form.get('name'))
        raise ValueError(f'No form with name="{name}" found. Found forms with these names: {found_names}')
    if id is not None:
        found_ids = []
        for form in tree.iterfind('.//form'):
            if form.get('id') == id:
                return FormData(form.fields)
            found_ids.append(form.get('id'))
        raise ValueError(f'No form with id="{id}" found. Found forms with these ids: {found_ids}')
    return FormData(tree.forms[index].fields)
