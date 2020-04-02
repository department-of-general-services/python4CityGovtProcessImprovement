Beautiful Soup Notes
=============================================================
## Kinds of objects
- ```BeautifulSoup```: The top-level object that represents the parsed document as a whole. Usually this is called/instantiated once and the rest of the time you're working with...
- ```Tag```: Tags are the workhorses of any Beautiful Soup project since virtually every webpage is nothing BUT tags. So searching tags and extracting data from them is a pretty much the entirety of most Beautiful Soup projects.
- ```NavigableString```: These haven't been terribly useful to me, since they represent regular strings and are functionally almost identical.
- Other: BS4 also defines a ```Comment``` class that is a special type of ```NavigableString```, as well as some other classes for more niche tag/data types

		
## Parsing the document
BS4 doesn't actually parse the document itself. It uses external parsers to do so and provides an flexible, intuitive interface to interact with the parsed document. By default, only the python standard ```html.parser``` is available, but others (particularly the ```lxml``` parser) are easily installed using pip. I use the ```lxml``` parser throughout my examples because I don't see any particular need to change it and I used it when following some BS4 tutorials. Whenever you call the ```BeautifulSoup()``` function, you will also need to specify which parser you want to use.
	
## Navigating the tree
While you can use the ```.find_all()``` and ```.select()``` methods to quickly go to exactly what you want, sometimes you might want to iterate through part of a document in a more readily-interpreted way. This is where the functions/generators/attributes of:
- ```.contents```
- ```.children```
- ```.descendants```
- ```.string(s)```
- ```.parent(s)```
- ```.next_sibling(s)```
- ```.previous_sibling(s)```
- ```.next_element(s)```
- ```.previous_elements(s)```

come in. Check the documentation because different accessors behave differently. For example, the ```.contents``` and ```.children``` attributes only consider a tag's direct children, not any grandchildren or more. For that, you would need to use the ```.descendants``` attribute to get ALL the tags that are children (in some fashion) of the tag you're calling. I haven't had much need for this, but could be useful.

## Getting data out of the tree
Retrieving data is very simple. Just call the ```.get(attr)``` method on a ```Tag``` object where ```attr``` is a string representing the name of the attribute you wish to retrieve.

## Searching the tree
This is the bread and butter of BS4. Learning to quickly search through an html (or xml) document means you can grab the data you're interested in more quickly and get the project over with. To this end, BS4 supports two main ways of searching: using ```.find()``` or ```.find_all()```, or using ```.select()```. The ```.find()``` and ```.find_all()``` methods allow you to specify a tag name (e.g.: a, body, table, div, etc) and tag attributes in two main ways. 

The first is passing in a dictionary containing the filter criteria (e.g.: ```attrs={"name": "email", "id": "username"}```). This allows you to specify an attribute called "name", because by default, the "name" parameter refers to the tag name, not the attribute "name".

The second way is to pass the parameters in as named arguments that are not part of the named argument list. For example, calling:

```tag.find_all("a", rel="prev")```

will return a list of all anchor tags (```a```) with a ```rel``` attribute that has a value of ```prev```. 
The ```.find_all()``` method is very powerful and can do more than just matching a regular string. It supports a variety of filter types that make it much easier to find data that may not be formatted the same way every time. ```.find_all()``` supports five kinds of filters.
- a string
- a list
- ```True```
- a regular expression (here there be dragons)
- a function

The string we've been over and is the simplest filter. A list is the next step up in that it matches any tag with a name in the list. So the list:

```['a', 'b']```

will match any ```a``` tags or any ```b``` tags and will return both kinds (if found) in the results. At a similar level of complexity is using ```True```. This simply tests for the existence of an attribute, and if the tag has such an attribute, it will be returned in the results. For example, calling:

```tag.find_all("a", "title=True")```

will return all anchor tags that have a "title" attribute, regardless of what the value of the "title" attribute is. This is useful if you need to pull some meta-data from the tag, but don't know what it is ahead of time.

The next step up in complexity is a regular expression (regex). If you pass in a regex object, BS4 will run the ```.match()``` method against the tag names. This allows a much more flexible search at the cost of having to learn something about regex. Now you have two problems. 

The last way is to pass in a function. This is the most complex but the most powerful way of filtering. To do this, the function you create must follow two rules:
1) The function takes a single argument that is assumed to be a tag object.
2) The function returns either True or False, nothing else.

The function can be as complex or simple as you wish. The example given in the documentation is a good example of this. It defines the function:
```
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
```

so when the function is passed to ```.find_all()``` (like so...)

```soup.find_all(has_class_but_no_id)```

it will return any tag that has a ```class``` attribute but explicitly does NOT have an ```id``` attribute. Remember that the logic in the function can be ANY valid python code, so long as it follows the two rules listed above. So if you wanted to select tags based on some combination of what their parent tags are, how many and what kind of children the tag has, and the values of certain attributes of any of those tags, you can do that.