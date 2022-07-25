import argparse
from bs4 import BeautifulSoup
import urllib.request
import re
from itertools import product
from requests import get

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
                self.center = self.letters[0].upper()
            elif p.startswith("Two letter list"):
                self.stems = re.findall("([a-z]{2})-", self.paras[i + 1])

    def get_corncob(self):
        res = get('http://www.mieliestronk.com/corncob_caps.txt')
        self.corncob = res.text

    def corncob_words(self):
        letters = ''.join(self.letters).upper()
        candidates = re.findall(f'\n([{letters}]{{4,}})\r', self.corncob)
        candidates = [w for w in candidates if self.center in w]
        self.words = candidates

def main():
    puzzle = Puzzle(args.y, args.m, args.d)#, args.p)
    puzzle.make_url()
    try:
        puzzle.get_puzzle()
    except:
        print(
            "####\nCheck date: may be entered incorrectly, or no hints page exists for that date\n####"
        )
        return -1
    puzzle.parse_paras()
    puzzle.get_corncob()
    puzzle.corncob_words()
    print(puzzle.words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("y", type=str)
    parser.add_argument("m", type=str)
    parser.add_argument("d", type=str)
    args = parser.parse_args()
    main()