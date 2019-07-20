#! /usr/bin/python3
import argparse
import re

# To do:
#  chain endlessly - first argument to cross_match should be the cumulative results so far,
#    and the groups are taken from the last item in each tuple?
#  test the last example, using '*'

# Setup
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='Search for words that match various constraints.',
                                 epilog="""
Regular expressions follow the standard Python regex rules, with these
rules to make it easier to type word searches:

  Use parentheses to mark groups as usual.

  Groups will be available to the following regex using a bare digit, 1-9.

  Bare digit references will each become groups for the following regex,
  renumbered in the order they appear.

  Each tilde is converted into a group of any single character: ~ becomes (.)

  Sequences of equals are converted into a group of dots: === becomes (...)
""")
parser.add_argument('regexes', metavar='R', nargs='+',
                    help="""A regular expression to use for searching.  Case-insensitive.
                      Use digit n to interpolate the n-th group from the previous regex.""")
parser.add_argument('--dict', dest='dictfile', default='dic.txt',
                    help='File with words, one per line (default: dic.txt)')

args = parser.parse_args()

with open(args.dictfile) as f:
  words = f.read()

# Search

def matches(regex):
  """ Return an iterator that matches the given string as a regex over all the words. """
  regex = re.sub('~', '(.)', regex)
  regex = re.sub('(=+)', lambda x: '(' + len(x[0]) * '.' + ')', regex)
  return re.finditer("^" + regex + "$", words, re.IGNORECASE | re.MULTILINE)

def cross_match(a, b):
  """ Return a list of pairs of RegEx matches for regex a and regex b,
      where regex b is evaluated with each of a's matches' groups substituted for single-digit integers.
  """
  result = []
  for amatch in matches(a):
    # Make bs into regex b, with all groups from this match substituted.
    bs = b
    for gn in range(1, amatch.lastindex + 1):
      bs = re.sub(str(gn), '(' + amatch[gn] + ')', bs)
    # Now match the resulting regex over the words, and form the tuples.
    for bmatch in matches(bs):
      result.append((amatch, bmatch))
  return result

# Do the intersection: run each subsequent search with the substitutions from the previous searches.
# Stub: just do the first one or two.
if len(args.regexes) == 1:
  all_matches = matches(args.regexes[0])
else:
  all_matches = cross_match(args.regexes[0], args.regexes[1])

# Flatten the matches for reporting - replace each regex match with its string
all_matches = [[match[0] for match in match_set] for match_set in all_matches]

# Report the matches.
print("matches:", all_matches)
