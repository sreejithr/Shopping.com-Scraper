# Shopping.com Scraper
A robust text scraper to scrape search result contents from Shopping.com. Uses BeautifulSoup in Python.

## Installation

```
git clone https://github.com/sreejithr/Shopping.com-Scraper
cd Shopping.com-Scraper
pip install -r requirements.txt
```

## Usage
```
python core.py <keyword>
python core.py <keyword> <page number>
```

## Problem statement

Implement a robust text scraper that will connect to a page on www.shopping.com, and return a result for a given keyword. Two queries can be performed using this program. The first query is getting the total number of results for a given keyword. The second query is to find all results for a given keywords on a specified page. Handle all the exceptions gracefully any feel free to use your favorite library.


### Following are the URLs
    `http://www.shopping.com/products?KW=<keword>`
    `http://www.shopping.com/products~PG-<number>?KW=<keyword>"`

### Queries: 
    Query 1: (requires a single argument)
    `your_program <keyword>`
    
    Query 2: (requires two arguments)
    `your_program <keyword> <page number>`
