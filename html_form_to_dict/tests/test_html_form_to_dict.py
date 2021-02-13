from html_form_to_dict import html_form_to_dict


def test_get_form_data_empty():
    html = '''
    <form>
    <input type="text" name="my-input">
    <textarea name="my-textarea">\n</textarea>
    </form>'''
    assert html_form_to_dict(html) == {'my-input': '', 'my-textarea': ''}


def test_get_form_data_with_value():
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

def test_get_form_data_checkboxes():
    html = '''
    <form>
     <input type="checkbox" name="my-checkbox" value="v1" checked>
     <input type="checkbox" name="my-checkbox" value="v2" checked>
    </form>'''
    assert html_form_to_dict(html) == {
                                   'my-checkbox': ['v1', 'v2'],
                                   }

