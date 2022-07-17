import argparse
from bs4 import BeautifulSoup
import urllib.request
import re
from nltk.corpus import wordnet
from itertools import product
from joblib import Parallel, delayed
from multiprocessing import Pool
from requests import get

# wordnet.synsets('word')


class Puzzle:
    def __init__(self, year, month, day, processes=1):
        self.year = year
        self.month = month
        self.day = day
        self.processes = processes
        self.words = None

    def make_url(self):
        url = f"https://www.nytimes.com/{self.year}/{self.month}/{self.day}/crosswords/spelling-bee-forum.html"
        self.url = url

    def get_puzzle(self):
        req = urllib.request.Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req)
        htmlParse = BeautifulSoup(html, "html.parser")
        self.paras = [para.get_text().strip() for para in htmlParse.find_all("p")]
        self.table = htmlParse.find('table')

    def parse_paras(self):
        for i, p in enumerate(self.paras):
            if p.startswith("Center letter"):
                self.letters = self.paras[i + 1].split()
                self.center = self.letters[0]
#            if p.startswith("WORDS"):
#                word_lens = self.paras[i + 1].split(chr(931))[0].strip().split()
#                self.max_len = int(word_lens[-1])
            elif p.startswith("Two letter list"):
                self.stems = re.findall("([a-z]{2})-", self.paras[i + 1])

    def len_table(self):
        rows = self.table.find_all('tr')
        table = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            table.append([ele for ele in cols if ele])
        self.table = table
        self.max_len = int(table[0][-2])


    def get_words(self):
        candidates = set()
        ###
        processes_pool = Pool(self.processes)
        candidates = processes_pool.map(self.search_stem, self.stems)
        ###
        # for stem in self.stems:
        #     candidates.update(self.search_stem(stem))
        self.words = candidates

    def search_stem(self, stem):
        candidates = set()
        for tail_len in range(2, self.max_len - 1):
            for tail in product(self.letters, repeat=tail_len):
                word = stem + "".join(tail)
                if (self.center in word) and wordnet.synsets(word):
                    candidates.add(word)
        return candidates

    def get_corncob(self):
        res = get('http://www.mieliestronk.com/corncob_caps.txt')
        self.corncob = res.text

    def corncob_words(self):
        letters = ''.join(self.letters).upper()
        candidates = re.findall(f'\n([{letters}]{{4,}})\r', self.corncob)
        candidates = [w for w in candidates if self.center in w]
        self.words = candidates

def main():
    puzzle = Puzzle(args.y, args.m, args.d, args.p)
    puzzle.make_url()
    try:
        puzzle.get_puzzle()
    except:
        print(
            "####\nCheck date: may be entered incorrectly, or no hints page exists for that date\n####"
        )
        return -1
    puzzle.parse_paras()
    # puzzle.len_table()
    # puzzle.get_words()
    puzzle.get_corncob()
    puzzle.corncob_words()
    print(puzzle.words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("y", type=str)
    parser.add_argument("m", type=str)
    parser.add_argument("d", type=str)
    parser.add_argument("p", type=int, default=1)
    args = parser.parse_args()
    main()
