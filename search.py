#! /usr/bin/python3

# To do:
#  chain endlessly - first argument to cross_match should be the cumulative results so far,
#    and the groups are taken from the last item in each tuple?
#  test the last example, using '*'

import re

def load_dict(dictfile="dic.txt"):
  global words
  with open(dictfile) as f:
    words = f.read()

# Search
# The main activity is building a list of WordSets.

def matches(regex):
  """ Return an iterator that matches the given string as a regex over all the words,
      using the substitutions we're making here.
      The iterator returns re.Matches.
  """
  regex = re.sub('~', '(.)', regex)
  regex = re.sub('(=+)', lambda x: '(' + len(x[0]) * '.' + ')', regex)
  return re.finditer("^" + regex + "$", words, re.IGNORECASE | re.MULTILINE)

class WordSet(list):
  """ A list of words that match the given constraints.
      Contains as many elements as we have matched constraints so far.
      Each element is a re.Match.
  """
  def __str__(self):
    """Format nicely for display, as a list of matching words."""
    # return [match[0] for match in self]
    return "a WordSet"

def match_word_sets(regex):
  """ Like matches(), but return an iterator that returns WordSets,
      rather than single re.Matches.
  """
  return map(lambda m: WordSet([m]), matches(regex))

def cross_match(wordsets, regex):
  """ Given an iterable of WordSets from preceding searches,
      generates WordSets, adding matches
      for the given new regex, evaluated with each WordSet's last match's groups
      substituted for single-digit integers.
  """
  for wordset in wordsets:
    # Substitute all groups from the last match into regex.
    lastmatch = wordset[-1]
    for i in range(1, lastmatch.lastindex + 1):
      regex = re.sub(str(i), '(' + lastmatch[i] + ')', regex)

    # Now match the resulting regex over the words, add matches to a new WordSet, and list them.
    for match in matches(regex):
       yield wordset + match

def main():
  # Setup
  import argparse
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

  load_dict(args.dictfile)

  # Do the intersection: run each subsequent search with the substitutions from the previous searches.
  all_matches = match_word_sets(args.regexes[0])
  print("First matches:", list(all_matches))
  for r in args.regexes[1:]:
    all_matches = cross_match(all_matches, r)

  # Report the matches.
  print("Matches:", list(all_matches))

if __name__ == "__main__": main()
