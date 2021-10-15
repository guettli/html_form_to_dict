
![Python package](https://github.com/guettli/html_form_to_dict/workflows/Python%20package/badge.svg)

# HTML Form to Dict

This is a tiny library which provides a method called `html_form_to_dict()`.

This method takes a string containing HTML and returns a dictionary of the value of the first form.

You can use it in tests like this:

```
def test_foo(client):
    url = reverse('foo')
    response = client.get(url)
    data = html_form_to_dict(response.content) # <====================
    assert data == {'city': 'Chemnitz', 'name': 'Mr. X'}
    data['name']='Mrs. Y'
    response = client.post(url, data)
    assert resonse.status == 302, response.context['form'].errors
```

Above code uses pytest-django. See [client fixture](https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client)

The dictionary returned by `html_form_to_dict()` does not allow adding new
keys, which are not in the dictionary yet. This way you get an error if your
test sets the value for an input which (due to refactoring) does not exist any more.

# Install

```shell
pip install html_form_to_dict
```

# Development

You need to upload your ssh-pub-key to github first:

```shell
pip install -e git+ssh://git@github.com/guettli/html_form_to_dict#egg=html_form_to_dict
edit-the-code
pytest
create Pull-Request
```

# Alternatives

* [Mechanize](https://mechanize.readthedocs.io/en/latest/) This library is like a browser without JS support.
* You could use BeautifulSoup like explained in this [Stackoverflow Answer](https://stackoverflow.com/a/65571001/633961)
* Use [Playwright](https://playwright.dev/) for browser based end-to-end tests.
