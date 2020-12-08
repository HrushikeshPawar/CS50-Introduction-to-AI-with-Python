import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    #Probaility of Page
    prob = dict()

    #Adding randomly chosen probabilities
    pages = corpus.keys()
    N = len(pages)
    for pg in pages:
        prob[pg] = (1-damping_factor)*(1/N)

    #Linked pages to given pages
    linked_pages = list(corpus[page])
    M = len(linked_pages)
    if(M != 0):
        for pg in linked_pages:
            prob[pg] = prob[pg] + damping_factor*(1/M)


    return prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Sample Space
    samples = []

    # Get all pages and randomly choose one
    pages = list(corpus.keys())
    page = random.choice(pages)
    samples.append(page)

    #Next page with  probability
    next_page_prob = transition_model(corpus, page, damping_factor)

    #Loop for all SAMPLES
    for i in range(n-1):
        keys = []
        values = []
        for key, value in next_page_prob.items():
            keys.append(key)
            values.append(value)

        samples.append(random.choices(keys, weights=values, k=1)[0])

        next_page_prob = transition_model(corpus, samples[-1], damping_factor)

    #Now check all SAMPLES
    pagerank = dict()
    for page in pages:
        pagerank[page] = samples.count(page)/len(samples)

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #All pages and create rank dict
    pages = list(corpus.keys())
    N = len(pages)
    pagerank = dict()
    for page in pages:
        pagerank[page] = 1/N
    while(True):
        new_pagerank = dict()
        for page in pages:
            new_pagerank[page] = (1-damping_factor)/N

            linking_pages = []
            summ = 0
            for pg, links in corpus.items():
                if(len(links) == 0):
                    links = pages
                if page in links:
                    summ += pagerank[pg]/len(links)
            new_pagerank[page] += damping_factor*summ

        #Check with previous ranks
        cnt = 0
        #print(abs(new_pagerank['logic.html'] - pagerank['logic.html']))
        for page in pages:
            #print(abs(new_pagerank[page] - pagerank[page]))
            if(abs(new_pagerank[page] - pagerank[page]) < 0.001):
                cnt += 1
            pagerank[page] = new_pagerank[page]
        if(cnt == len(pages)):
            break

    return pagerank




if __name__ == "__main__":
    main()
