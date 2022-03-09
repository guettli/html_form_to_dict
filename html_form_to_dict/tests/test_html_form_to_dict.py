# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import pytest
from html_form_to_dict import html_form_to_dict


def test_html_form_to_dict__empty():
    html = '''
    <form>
    <input type="text" name="my-input">
    <textarea name="my-textarea">\n</textarea>
    </form>'''
    assert html_form_to_dict(html) == {'my-input': '', 'my-textarea': ''}


def test_html_form_to_dict__with_value():
    html = '''
    <form>
     <input type="text" name="my-input" value="my-input-value">
     <textarea name="my-textarea">\nmy-textarea-value</textarea>
     <input type="checkbox" name="my-checkbox" value="my-checkbox-value" checked>
    </form>'''
    assert html_form_to_dict(html) == {'my-input': 'my-input-value',
                                       'my-textarea': 'my-textarea-value',
                                       'my-checkbox': 'my-checkbox-value',
                                       }


def test_html_form_to_dict__checkboxes_checked():
    html = '''
    <form>
     <input type="checkbox" name="my-checkbox" value="v1" checked>
     <input type="checkbox" name="my-checkbox" value="v2" checked>
    </form>'''
    assert html_form_to_dict(html) == {
        'my-checkbox': ['v1', 'v2'],
    }


def test_html_form_to_dict__checkboxes_unchecked():
    html = '''
    <form>
     <input type="checkbox" name="my-checkbox" value="v1">
     <input type="checkbox" name="my-checkbox" value="v2">
    </form>'''
    assert html_form_to_dict(html) == {'my-checkbox': []}


def test_html_form_to_dict__unknown_key():
    html = '''
    <form>
     <input type="checkbox" name="name" value="value">
    </form>'''
    data = html_form_to_dict(html)
    with pytest.raises(KeyError):
        data['typo']


def test_html_form_to_dict__select_single():
    html = '''
    <form>
     <select name="cars" id="cars">
      <option value="volvo">Volvo</option>
      <option value="saab" selected>Saab</option>
      <option value="mercedes">Mercedes</option>
     </select>
    <form>
     '''
    assert html_form_to_dict(html) == {'cars': 'saab'}


def test_html_form_to_dict__select_multiple():
    html = '''
    <form>
     <select name="cars" id="cars" multiple>
      <option value="volvo" selected>Volvo</option>
      <option value="saab">Saab</option>
      <option value="mercedes" selected>Mercedes</option>
     </select>
    <form>
     '''
    assert html_form_to_dict(html) == {'cars': ['volvo', 'mercedes']}


def test_form_by_index_name_or_id():
    html = '''
    <form name="one" id="id1">
     <input type="text" name="my_input" value="some value">
    </form>
    <form name="two" id="id2">
     <input type="text" name="my_input" value="some other value">
    </form>
    '''

    # by name
    assert html_form_to_dict(html, name="one") == {'my_input': 'some value'}
    assert html_form_to_dict(html, name="two") == {'my_input': 'some other value'}
    with pytest.raises(ValueError) as excinfo:
        html_form_to_dict(html, name='unknown')
    assert str(excinfo.value) == '''No form with name="unknown" found. Found forms with these names: ['one', 'two']'''

    # by id
    assert html_form_to_dict(html, id="id1") == {'my_input': 'some value'}
    assert html_form_to_dict(html, id="id2") == {'my_input': 'some other value'}
    with pytest.raises(ValueError) as excinfo:
        html_form_to_dict(html, id='unknown')
    assert str(excinfo.value) == '''No form with id="unknown" found. Found forms with these ids: ['id1', 'id2']'''

    # by index
    assert html_form_to_dict(html, 1) == {'my_input': 'some other value'}
    with pytest.raises(IndexError):
        html_form_to_dict(html, 2)


class DummyClient:
    def __init__(self):
        self.calls = []

    def get(self, url, data):
        self.calls.append(('get', url, data))

    def post(self, url, data):
        self.calls.append(('post', url, data))


def test_form_data__submit():
    html = '''
    <form action="my-url">
     <input type="text" name="my_input" value="some value">
    </form>'''
    data = html_form_to_dict(html)
    client = DummyClient()
    data.submit(client)
    assert client.calls == [('get', 'my-url', {'my_input': 'some value'})]

    html = '''
    <form action="my-url" method=POST>
     <input type="text" name="my_input" value="some value">
    </form>'''
    data = html_form_to_dict(html)
    client = DummyClient()
    data.submit(client)
    assert client.calls == [('post', 'my-url', {'my_input': 'some value'})]

    html = '''
    <form hx-get="my-url">
     <input type="text" name="my_input" value="some value">
    </form>'''
    data = html_form_to_dict(html)
    client = DummyClient()
    data.submit(client)
    assert client.calls == [('get', 'my-url', {'my_input': 'some value'})]

    html = '''
    <form hx-post="my-url">
     <input type="text" name="my_input" value="some value">
    </form>'''
    data = html_form_to_dict(html)
    client = DummyClient()
    data.submit(client)
    assert client.calls == [('post', 'my-url', {'my_input': 'some value'})]
