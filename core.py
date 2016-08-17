import re
import argparse
import sys
import requests

from bs4 import BeautifulSoup

SEARCH_URL = 'http://www.shopping.com/products?KW={keyword}'
PAGE_URL = 'http://www.shopping.com/products~PG-{page_num}?KW={keyword}'


def pretty_print_items(items):
    if len(items) == 0:
        print "No results at given page"
        return

    for item in items:
        print '-' * 50
        print '  Item    : {}'.format(item.get('title', '').encode('utf-8').strip())
        print '  Price   : {}'.format(item.get('price', '').encode('utf-8').strip())
        print '  Merchant: {}'.format(
            item.get('merchant', '').encode('utf-8').strip()
        )
    print '-' * 50

class ShoppingCrawler(object):
    def fetch_page_items(self, keyword, page):
        '''
        Page items are products for sale. These are <div>'s of class 'gridBox'
        '''
        page = requests.get(PAGE_URL.format(page_num=page, keyword=keyword))

        if page.status_code != 200:
            raise ValueError("Please check keyword/page number supplied")

        soup = BeautifulSoup(page.text, 'html.parser')
        return soup.select('.gridBox')

    def get_item_count(self, keyword):
        '''
        To get the result count, we do:

           Item count  = Items per page * (No.of pages - 1) + Items in last page

        :type keyword: string
        :rtype: int
        '''
        search_results = requests.get(SEARCH_URL.format(keyword=keyword))

        if search_results.status_code != 200:
            raise ValueError("Please check keyword supplied")

        soup = BeautifulSoup(search_results.text, 'html.parser')

        # 'Next' link has name attribute 'PLN'. Others have 'PL1', 'PL2' etc.
        page_links = filter(
            lambda e: e.attrs.get('name') and e.attrs.get('name') != 'PLN',
            soup.select('.paginationNew a')
        )

        # We consider the last page label to be the no of pages
        page_nums = [
            self._get_page_num_from_link(each.attrs.get('href', ''))
            for each in page_links
        ]
        no_of_pages = max(page_nums) if len(page_nums) > 0 else 0

        per_page_count = len(self.fetch_page_items(keyword, 1))
        last_page_count = len(self.fetch_page_items(keyword, no_of_pages))

        return per_page_count * (no_of_pages-1) + last_page_count

    def get_items_in_page(self, keyword, page):
        '''
        Elements with class 'gridItemBtm' are search results.

        :rtype: list
        '''
        items = []

        for page_item in self.fetch_page_items(keyword, page):
            contents = page_item.select_one('.gridItemBtm')
            if contents:
                product = contents.select_one('.productName')
                if product:
                    title = product.attrs.get('title') or\
                            product.select_one('span').attrs.get('title')
                
                product_price = contents.select_one('.productPrice')
                if product_price:
                    price = product_price.string or\
                            product_price.select_one('a').string

                merchant = contents.select_one('.newMerchantName')
                if merchant:
                    merchant_name = merchant.string or\
                                    merchant.select_one('a').string
                if title and price and merchant_name:
                    items.append({
                        'title': title, 'price': price, 'merchant': merchant_name
                    })
        
        return items

    def _get_page_num_from_link(self, link):
        res = re.search(r'PG-(?P<page_no>\d+)', link)
        try:
            return int(res.group('page_no')) if res else 0
        except ValueError:
            return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape shopping.com')
    parser.add_argument('keyword', help='Search keyword')
    parser.add_argument('page', default=None, nargs='?',
                        help='Search results page number')
    args = parser.parse_args()

    try:
        crawler = ShoppingCrawler()
        print "Total of {} results".format(crawler.get_item_count(args.keyword))

        if args.page:
            pretty_print_items(
                crawler.get_items_in_page(args.keyword, args.page)
            )
    except ValueError:
        parser.print_help()

