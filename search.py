import argparse
import re

# Setup
parser = argparse.ArgumentParser(description='Search for words that match various constraints.',
                                 epilog='Example: "(...)RI(..)" "$1AN$2" shows all pairs of 7-letter words that have '
                                 	+ 'the same prefix and suffix and those two pairs of fourth and fifth letters.')
parser.add_argument('regexes', metavar='R', nargs='+',
                    help='A regular expression to use for searching.  Case-insensitive.'
                    	+ 'Use $n to interpolate the n-th group from a previous regex.')
parser.add_argument('--dict', dest='dictfile', default='dic.txt',
                    help='File with words, one per line (default: dic.txt)')

args = parser.parse_args()

with open(args.dictfile) as f:
	words = f.read()

# Search
# To do: successive iterations matching each regex in turn, and saving tuples of matching words.
s = re.compile("^" + args.regexes[0] + "$", re.IGNORECASE | re.MULTILINE)
matches = [m.group() for m in s.finditer(words)]

# Report the matches.
print("matches:", 	matches)
