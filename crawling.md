# Crawler / Spider
Salas' ([leVirve](https://github.com/leVirve)@Github)

## Prerequisites
* Familiar with basic Python syntax
* Knowledge about HTTP

## Implementations
 Crawler can be separated into two parts, crawling and parsing.
 
 * **Crawl**:  Fetch raw data through URI
	 * Make HTTP *request*
	 * Receive the *response*, and pass to `Parse`
 * **Parse**:
	 * Parse out structured data from response (HTML or somethings)
	 * Get interested information from structured data.
	 *  (Optional) Maybe store or serve the information for other applications.

We use Python in implementation,

* `Crawl`:
	*  Python has its built-in library for HTTP requests.
	*  However, `requests` is a recommended solution by [Python official](https://docs.python.org/3/library/urllib.request.html#module-urllib.request).

	> Python Document: The [Requests package](https://requests.readthedocs.org/) is recommended for a higher-level http client interface.

* `Parse`:
	* Python has its own `HTMLParser` serves as the basis for parsing text files formatted in HTML or XHTML.
	* Somehow, we may choose other libraries for the jobs. Such as, 
		* `lxml` for better HTML text processing
		* `Beautifulsoup` serves better interface for parsing tree operations
		* `Selenium` acts as a real browser for complicated interactions.

## Crawl
```
pip install requests
```
Using python and `requests` to fetch raw response. See `requests` [quickstart](http://docs.python-requests.org/en/master/user/quickstart/) for more operations.

Sample of `requests` power ([doc](http://docs.python-requests.org/en/master/))
```bash
>>> # Use keyword parameters for advanced usage
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> # access data in `dict` way
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> # get the encoding of response text
>>> r.encoding
'utf-8'
>>> # raw text string
>>> r.text
'{"type":"User"...'
>>> # make response to json type
>>> r.json()
{'private_gists': 419, 'total_private_repos': 77, ...}
```

Python code for crawling.
```python
import requests

url = 'https://api.github.com/events'
response = requests.get(url)
```
That's it. You get a response from server.

## Parse
We've got HTTP response in previous section. Now we are going to parse it.

* If  response is well-formatted data: `json`
	*  `response.json()` will turn json data into a python `dict()` format.
	* Access it directly to get target information .
* Not

```python
""" 
	response object
	- content: binary content
	- text: text string
	- json: json object
"""
data = response.json()

text = response.text
process(text)
```

# Anti-crawling
# Speed up Crawler
## Async
## Parallel
# Scale up Crawler
## Distributed
