import urllib2
import robotparser
import re
import random
import urlparse
import time
from datetime import datetime
import Queue
#import mongo_cache
import socket

DEFAULT_TIMEOUT = 60


class Downloader(object):
    
    def __init__(self,delay=-1,user_agent='wswwp',proxies=None,
                  num_retries=4,timeout=DEFAULT_TIMEOUT,cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies=proxies
        self.num_retries=num_retries
        self.cache=cache
        
    def __call__(self,url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not avilable in cache
                pass
            else:
                if self.num_retries>0 and \
                   500 <=result['code']<600:
                    #server error so ignore result from cache
                    #and re-download
                    result =None
        
        if result is None:
            # result was not loaded from cache
            # so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent':self.user_agent}
            result = self.download(url,headers,proxy,self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']
    def download(self,url,headers,proxy,num_retries,data=None):
        print 'Downloading:',url
        #headers={'User-agent':user_agent}

        request=urllib2.Request(url,data,headers or {})
        socket.setdefaulttimeout(9.0)

        opener = urllib2.build_opener()
        if proxy:
            proxy_pagrams={urlparse.urlparse(url).scheme:proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_pagrams))

        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except urllib2.URLError as e:
            print 'Download error',str(e)
            html=None
            if hasattr(e,'code'):
                code = e.code
                if num_retries>0 and 500<=e.code<600:
                    return self.download(url,headers,proxy,num_retries-1,data)
                #elif num_retries>0:
                    #return download(url,headers,proxy,0,data)
            else :
                code = None
        return {'html':html,'code':code}



def link_crawler(seed_url,link_regex=None,crawl_queue=Queue.deque(),seen=[],scrape_callback=None,cache=None,delay=-1,max_depth=-1,max_urls=-1,user_agent='Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',proxies=None,num_retries=0):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    if not len(crawl_queue) and seed_url not in seen:
        crawl_queue.append(seed_url)
    # the URL's that have been seen and at what depth
    #seen = {seed_url:0}

    # track how many URL's have been downloaded
    num_urls=0

    rp = get_robots(seed_url)
    D = Downloader(delay=delay,user_agent=user_agent,proxies=proxies,num_retries=num_retries,cache=cache)
    #throttle = Throttle(delay)

      
    while len(crawl_queue):
        url = crawl_queue.pop()
        #check url passes robots.txt restrictions

        if rp.can_fetch(user_agent,url):
            #throttle.wait(url)
            '''
            if url == scrape_callback.seed_url:
                with open('zipped_data.zip','rb') as fp:
                    html = fp.read()
                #print html
            else:
            '''
            try:
                html= D(url)
                if not html:
                    print "Html get error:%s"%url
                    continue
            except socket.timeout:
                print "url:%s timeout -pass "%url
                continue
            except:
                continue


            links = []
            if scrape_callback:
                #print scrape_callback(url,html),"?"
                links.extend(scrape_callback(url,html)or[])
            #depth=seen[url]

            '''
            if depth !=max_depth:
                #can still crawl further
                '''
            if link_regex:
                #filter for links matching our regular expression
                links.extend(link for link in get_links(html) if re.match(link_regex,link))
                    

                """
                
                for link in get_links(html):
                    if re.match(link_regex,link):
                        #from absolute link
                        link=urlparse.urljoin(seed_url,link)
                        #check if have already seen this link
                        
                """

            for link in links:
                link = normalize(seed_url,link)
                # check whether already crawled this link
                if link not in seen:
                        seen.append(link)
                        #seen[link] =depth +1
                        if  same_domain(seed_url,link):
                                #success! add this new link to queue
                                 crawl_queue.append(link)
            #check whether have reached downloaded maximum
            num_urls +=1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:',url

def normalize(seed_url,link):
    """Normalize this URL by removing hash and adding domain
    """
    link,_=urlparse.urldefrag(link)  # remove hash to avoid duplicate
    return urlparse.urljoin(seed_url,link)

def same_domain(url1,url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc

def get_links(html):
    """Return a list of links  from html
    """
    # a Regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #list of all links from the webpage
    return webpage_regex.findall(html)
def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


class Throttle(object):
    """Add a delay between downloads to the same domain
    """
    def __init__(self,delay):
        #amount of delay between downloads for each domain
        self.delay = delay
        #timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self,url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                #domain has been accessed recently
                #so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = datetime.now()




if __name__=="__main__":
    #url="http://httpstat.us/500"
    #download(url)
    #download("http://www.baidu.com")
    start =int (time.time())
    seed_url='http://example.webscraping.com'
    link_regex='/(index|view)'
    #cache=mongo_cache.MongoCache()
    link_crawler(seed_url,link_regex,cache={})
    end = int (time.time())
    print"It takes %s minutes %s seconds"%((end-start)/60,(end-start)%60)
'''
rp =robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
url='http://example.webscraping.com'
user_agent='GoodCrawler'
rp.can_fetch(user_agent,url)


'''
   
                
