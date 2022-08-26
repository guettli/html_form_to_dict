
![Python package](https://github.com/guettli/html_form_to_dict/workflows/Python%20package/badge.svg)

# HTML Form to Dict

This is a tiny library which provides a method called `html_form_to_dict()`.

This method takes a string containing HTML and returns a dictionary of the values of the first form.

The data returned by `html_form_to_dict()` is a `FormDict` which has the method `submit()`. This way
you can submit the data like a real browser would.

This mean you can do simple end-to-end testing of form handling without a real browser (like selenium/puppeteer/playwright).

The `submit()` method supports the "action" and "method" attributes of forms and additionaly the [htmx](//htmx.org) attributes [hx-get](https://htmx.org/attributes/hx-get/), [hx-post](https://htmx.org/attributes/hx-post/).

Example:

```
def test_foo(client):
    ...
    
    # client is a DjangoClient. But you could use
    # python-requests or a different URL-lib, too
    response = client.get(url)
    
    # This method parses the HTML in response.content to a dictionary.
    # This dictionary is like request.POST or request.GET.
    # It is a flat mapping from the input elements of the form
    # to their value.
    data = html_form_to_dict(response.content)
    
    # Now you can test the default values of the form.
    assert data == {'city': 'Chemnitz', 'name': 'Mr. X'}
    
    # You can edit the data. This is like a human (or Playwright/Selenium)
    # altering the HTML input fields
    data['name'] = 'Mrs. Y'
    
    # This submits the data to the server.
    # This methods uses the "action" attribute of the form.
    # The hx-get, hx-post attributes of htmx are supported, too
    response = data.submit(client)
    
    # If you use the Post/Redirect/Get pattern:
    assert response.status == 302, response.context['form'].errors
```

Above code uses pytest-django. See [client fixture](https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client)

The `FormDict` returned by `html_form_to_dict()` does not allow adding new
keys, which are not in the dictionary yet. This way you get an error if your
test sets the value for an input which (maybe due to refactoring) does not exist.

Above example uses Django, but the library is a pure Python library which does not depend on any
particular web-framework.

This library was build for testing, but you can use it for all tasks where you
want to parse and submit html forms.

This library does not evaluate JavaScript. If you need JS support, please use Playwright (or a similar tool).

# Install

```shell
pip install html_form_to_dict
```

# Development

You need to upload your ssh-pub-key to github first:

```shell
pip install -e git+ssh://git@github.com/guettli/html_form_to_dict#egg=html_form_to_dict
edit-the-code
pip install pytest
pytest
create Pull-Request
```

# Alternatives

* [Mechanize](https://mechanize.readthedocs.io/en/latest/) This library is like a browser without JS support.
* You could use BeautifulSoup like explained in this [Stackoverflow Answer](https://stackoverflow.com/a/65571001/633961)
* Use [Playwright](https://playwright.dev/) for browser based end-to-end tests.

# Deploy

via deploy-library.py

for py2 tgz package: `python -m twine upload dist/html_form_to_dict-*.tar.gz`

