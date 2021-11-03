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
            value=''
        if isinstance(value, str):
            value = value.lstrip('\n')
        if isinstance(value, CheckboxValues):
            value = [el.value for el in value.group if el.value is not None]
        if isinstance(value, MultipleSelectOptions):
            value = list(value)
        super().__setitem__(key, value)

def html_form_to_dict(html):
    tree = lxml.html.fromstring(html)
    return FormData(tree.forms[0].fields)
