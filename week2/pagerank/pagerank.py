import os
import random
import re
import sys
import numpy as np;

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
    
    output = {i: (1 - damping_factor) / len(corpus) for i in corpus}
    
    # if page has no outgoing links
    if len(corpus[page]) == 0:
        return {i: 1 / len(corpus) for i in corpus}
    
    linked_pages = corpus[page]
    for linked_page in linked_pages:
        output[linked_page] += damping_factor / len(linked_pages)
    
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    initial_sample = random.choice(list(corpus.keys()))
    sample_value = {page:0 for page in corpus.keys()}
    sample_value[initial_sample] += 1
    
    for _ in range(n-1):
        previous_distribution = transition_model(corpus, initial_sample, damping_factor)
        
        initial_sample = random.choices(list(previous_distribution.keys()), weights=previous_distribution.values(), k=1)[0]
        
        sample_value[initial_sample] += 1

    return {page:distribution/n for page, distribution in sample_value.items()}
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    """
    [d/numLinks(i), d/numLinks(j), d/numLinks(k), ...]
    [d/numLinks(i), d/numLinks(j), d/numLinks(k), ...]
    [d/numLinks(i), d/numLinks(j), d/numLinks(k), ...]* U0 = U1 - [1-d/n, 1-d/n, 1-d/n...]
    [                   ...                          ]
    [d/numLinks(i), d/numLinks(j), d/numLinks(k), ...]
    
    some entries in column might be zero, because some page might not connect to other pages
    this transition model is markov matrix because the sum of each column is 1
    """
    pages = list(corpus.keys())
    n = len(pages)
    ranks = np.full(n, 1/n)
    threshold = 0.001
    
    numLinks = {page:len(corpus[page]) for page in corpus}
    
    # constructing the matrix
    matrix = np.zeros((n,n))
    for i, page in enumerate(pages):
        # A page that has no links at all should be interpreted as having 
        # one link for every page in the corpus (including itself).
        if numLinks[page]:
            for link in corpus[page]:
                j = pages.index(link)
                matrix[j, i] = 1 / len(corpus[page])
        else:
            matrix[:, i] = 1/n

    # iterate until the difference is less than threshold
    while True:
        new_ranks = (1 - damping_factor) / n + damping_factor * matrix @ ranks
        if np.all(np.abs(new_ranks - ranks) < threshold):
            break
        ranks = new_ranks
    
    normalized_ranks = new_ranks / np.sum(new_ranks)
    return {page:rank for page, rank in zip(pages, normalized_ranks)}


if __name__ == "__main__":
    main()
