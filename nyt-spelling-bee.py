import argparse
from bs4 import BeautifulSoup
import urllib.request
import re
from nltk.corpus import wordnet
from itertools import product

# wordnet.synsets('word')


def make_url():
    url = f"https://www.nytimes.com/{args.y}/{args.m}/{args.d}/crosswords/spelling-bee-forum.html"
    return url


def parse_page(url):
    html = urllib.request.urlopen(url)
    htmlParse = BeautifulSoup(html, "html.parser")
    paras = [para.get_text() for para in htmlParse.find_all("p")]
    return paras


def parse_paras(paras):
    for i, p in enumerate(paras):
        if p.startswith("Center letter"):
            letters = paras[i + 1].split()
        if p.startswith("WORDS"):
            word_lens = paras[i + 1].split(chr(931))[0].strip().split()
            max_len = int(word_lens[-1])
        elif p.startswith("Two letter list"):
            stems = re.findall("([A-Z]{2})-", paras[i + 1])
    return letters, max_len, stems


def word_strings(letters, max_len, stems):
    center = letters[0]
    candidates = set()
    for stem in stems:
        for tail_len in range(2, max_len - 1):
            # tails is going to be a problem if there are any long words
            for tail in product(letters, repeat=tail_len):
                word = stem + "".join(tail)
                # tails = set(
                #     map(lambda x: "".join(x), set(product(letters, repeat=tail_len)))
                # )
                # for tail in tails:
                # word = stem + tail
                if (center in word) and wordnet.synsets(word):
                    candidates.add(word)
    return candidates


def main():
    url = make_url()
    try:
        paras = parse_page(url)
    except:
        print(
            "####\nCheck date: may be entered incorrectly, or no hints page exists for that date\n####"
        )
        return -1
    letters, max_len, stems = parse_paras(paras)
    candidates = word_strings(letters, max_len, stems)
    print(candidates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("y", type=str)
    parser.add_argument("m", type=str)
    parser.add_argument("d", type=str)
    args = parser.parse_args()
    main()
