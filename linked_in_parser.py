import cookielib
import os
import urllib
import urllib2
import re
import string
from bs4 import BeautifulSoup
from scrapy import Selector
from linkedIn.linkedIn.items import linkedInItem
import getpass

cookie_filename = "parser.cookies.txt"
class LinkedInParser(object):

    def __init__(self, login, password,url):
        """ Start up... """
        self.login = login
        self.password = password

        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]


        # Login
        self.loginPage()

        title = self.loadNewPage(url)
        print title

        self.cj.save()


    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join(response.readlines())
        except:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            return self.loadPage(url, data)
    def parseResponse(self, response):
        f = open("html.txt","w+")
        f.write(response)
        f.close()
        sys.exit()
        return None
        #item['location'] = striplist(hxs.xpath('//dd/span/text()').extract())

        #item['industry'] = striplist(hxs.xpath('//dd[@class="industry"]/text()').extract())

        #return item


    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        html = self.loadPage("https://www.linkedin.com/uas/login")
        #locs = [m.start() for m in re.finditer('csrf', html)]
        #print [html[l:l+20] for l in locs]
        soup = BeautifulSoup(html)
        csrf = soup.find(id="loginCsrfParam-login")['value']

        login_data = urllib.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        })

        html = self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        return

    def loadNewPage(self,url):
        html = self.loadPage(url)
        soup = BeautifulSoup(html)
        f = open("html.txt","w+")
        f.write(html)
        f.close()
        return soup.find("title")

if __name__ == '__main__':

    LINKED_IN_PASSWORD = getpass.getpass()
    LINKED_IN_USERNAME = 'benjaminschreck93@gmail.com'
    url = 'https://www.linkedin.com/in/elaineo'
    parser = LinkedInParser(LINKED_IN_USERNAME, LINKED_IN_PASSWORD,url)
