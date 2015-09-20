# URLS

# https://hackmit.devpost.com/submissions
#import sys
#from HTMLParser import HTMLParser

#class MyHTMLParser(HTMLParser):
    #def __init__(self):
        #HTMLParser.__init__(self)
        #self.starttags = []
        #self.endtags = []
        #self.data = []
        #self.attrs = []
        #self.recordData = False
        #self.participant_names = []
    #def handle_starttag(self, tag, attrs):
        #if tag == 'li' and any(['participant' == attrElement[1][:11] for attrElement in attrs]):
            #self.recordData = True
            #curAttrs = {}
            #for attrElement in attrs:
                #curAttrs[attrElement[0]] = attrElement[1]
            #self.attrs.append(curAttrs)
    #def handle_endtag(self, tag):
        #if tag == 'li' and self.recordData:
            #self.recordData == False
    #def handle_data(self, data):
        #if self.recordData and data.replace(' ','') and data != '\n':
            #curAttrs = self.attrs[-1]
            #if curAttrs['class'] == 'participant-name':
                #self.participant_names.append(data)
            #self.recordData = False
#parser = MyHTMLParser()
#participants_pages = [
    #'hackmit.devpost.com/participants?page=1',
    #'hackmit.devpost.com/participants?page=2',
    #'hackmit.devpost.com/participants?page=3',
    #'hackmit.devpost.com/participants?page=36',
    #'hackmit.devpost.com/participants?page=4',
    #'hackmit.devpost.com/participants?page=5',
        #]
#for page in participants_pages:
    #with open(page, 'rb') as participants_html:
        #keepGoing = True
        #while keepGoing:
            #line = participants_html.readline()
            #if line:
                #parser.feed(line)
            #else:
                #keepGoing = False
##print parser.starttags
##print parser.endtags
#for i,d in enumerate(parser.participant_names):
    #print d

import json
import requests
from bs4 import BeautifulSoup
from dateutil.parser import *
import datetime
import sys
import util

class DevPostScraper(object):
    def __init__(self):
        self.search_request = {
                }
    def scrape(self):
        names = self.scrape_names()
        #for name in list(names):
            #print name
    def scrape_names(self):
        names = set()
        for page in xrange(1,37):
            r = requests.get(
                url='http://hackmit.devpost.com/participants?page='+str(page),
                headers={
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )

            s = BeautifulSoup(r.text)

            for r in s.findAll('li'):
                if 'class' in r.attrs and 'participant-name' in r['class']:
                    noSpaceName = r.text.replace(' ','').replace('\n','')
                    if noSpaceName:
                        name = r.text.replace('\n','')
                        names.add(name)
                        print name
        return names
    def scrape_hackathons(self):
        names = set()
        for page in xrange(1,3000):
            r = requests.get(
                url='http://devpost.com/hackathons?page='+str(page),
                headers={
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )

            s = BeautifulSoup(r.text)
            for r in s.findAll('article'):
                if 'class' in r.attrs and 'challenge-listing' in r['class']:
                    href = r.a.get('href').split('.devpost')[0]
                    print href
                for sub in r.findAll('span'):
                    if 'class' in sub.attrs and 'value' in sub['class'] and 'date-range' in sub['class']:
                        datestring =u"{}".format(sub.text).encode('utf8')
                        formattedDatestring = []
                        forbidden = False
                        for c in datestring:
                            if ord(c) < 128 and not forbidden:
                                formattedDatestring.append(c)
                            elif ord(c) < 128:
                                if c == ',':
                                    forbidden = False
                            else:
                                forbidden = True

                        formattedDatestring = ''.join(formattedDatestring)
                        d = parse(formattedDatestring)
                        print d
                        #recent = datetime.datetime.now() - datetime.timedelta(hours=72)
                        #if d < recent:
                            #print href
                            #print recent


    def scrape_projects(self, pages= 1221,pf = 'projects.p'):

        util.checkPickleFileExistsAndCreate(pf)
        names = set()
        projects = []
        for page in xrange(1,pages+1):
            print "working on page:", page
            r = requests.get(
                url='http://devpost.com/software/search?page='+str(page),
                headers={
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )

            projects_dict= json.loads(r.text)
            for p in projects_dict['software']:
                hackathon, members, details = self.scrape_project(p['url'])
                p['hackathon'] = hackathon
                p['members'] = members
                p['details'] = details
                del p['photo']
                del p['slug']
                del p['url']
                projects.append(p)
            util.saveObjectsToPickleFile({'projects':projects},pf)
        return projects

    def scrape_project(self, url):
        r = requests.get(
            url=url,
            headers={
                'X-Requested-With': 'XMLHttpRequest'
            }
        )
        s = BeautifulSoup(r.text)
        hackathon = ''
        submissions = s.find(id='submissions')
        if submissions:
            for sub in submissions.findAll('div'):
                if 'class' in sub.attrs and 'software-list-content' in sub['class']:
                    hackathon = sub.a['href']
        members = []
        team = s.find(id='app-team')
        if team:
            for sub in team.findAll('li'):
                if 'class' in sub.attrs and 'software-team-member' in sub['class']:
                    for link in sub.findAll('a'):
                        if 'class' in link.attrs and 'user-profile-link' in link['class']:
                            if link.string:
                                url = link['href']
                                name = link.string
                                members.append({'url':url, 'name':name})
        parsedDetails = ''
        details = s.find(id='app-details-left')
        if details:
            for d in details.findAll('div'):
                if 'id' not in d.attrs or (d['id'] != 'built-with'):
                    parsedDetails += d.get_text()

        return hackathon, members, parsedDetails


scraper = DevPostScraper()
pf = 'projects.p'
projects = scraper.scrape_projects(pages = 1221, pf = pf)
#print scraper.scrape_project('http://devpost.com/software/kannek-ujkf5e')

