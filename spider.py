from bs4 import BeautifulSoup as bs
from collections import deque
import requests, re, sys
import numpy as np

START_PAGE = 'https://tanaybiradar.com'
MAX_STACK_DEPTH = 4
MAT_SIZE = 500
freq_mat = np.zeros((MAT_SIZE, MAT_SIZE))
link_ids = {} # key = link, value = index in freq matrix

def find_links(html): # returns unique links
    soup = bs(html, 'html.parser')
    links = set()

    for link in soup.find_all('a', attrs={'href': re.compile('^https://')}):
        href = link.get('href')
        if not href in link_ids:
            link_ids[href] = len(link_ids)

        links.add(href)

    return links

def crawl(source):
    global freq_mat
    if not source in link_ids: # assign a new id
        link_ids[source] = len(link_ids)

    html = requests.get(source).text
    links = find_links(html) # pages source links to
    edge_ids = [link_ids[link] for link in links] # ids of pages source connects to

    print(link_ids[source], source)
    print(edge_ids, len(edge_ids)) 

    if len(link_ids) > MAT_SIZE: # resize matrix (should only happen once)
        new_mat = np.zeros((len(link_ids), len(link_ids)))
        new_mat[:MAT_SIZE, :MAT_SIZE] = freq_mat
        freq_mat = new_mat

    for ident in edge_ids:
        freq_mat[link_ids[source], ident] += 1

    return links

def main():
    crawled = set()

    q = deque()
    q.append(START_PAGE)

    while len(link_ids) < MAT_SIZE: # modified bfs on link tree
        page = q.popleft() # dequeue
        links = crawl(page)
        crawled.add(page)

        for link in links:
            if link not in crawled:
                crawled.add(link)
                q.append(link)

    np.savetxt('freq_mat.out', freq_mat)

if __name__ == '__main__':
    main()
