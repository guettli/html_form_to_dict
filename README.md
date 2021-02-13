# HTML Form to Dict

This is a tiny library which provides a method called `html_form_to_dict()`.

This method takes a string containing HTML and returns a dictionary of the value of the first form.

You can use it in tests like this:

```Python
response = user_client.get(url)
data = html_form_to_dict(response.content)
assert data == {'city': 'Chemnitz', 'name': 'Mr. X'}
data['name']='Mrs. Y'
response = user_client.post(url, data)
```    

The dictionary returned by `html_form_to_dict()` does not allow adding new
keys, which are not in the dictionary yet. This way you get an error if your
test sets the value for an input which (due to refactoring) does not exist any more.


# Development

```

# If you have your ssh key uploaded to github:
pip install -e git+ssh://git@github.com/guettli/html_form_to_dict#egg=html_form_to_dict
```
