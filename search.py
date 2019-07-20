#! /usr/bin/python3

from collections import UserList
import re

# The dictionary of words.
# Initialize to a trivial dictionary for use in testing.
words = """eggs
spam
swim
"""

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

      >>> matches("s==m")  #doctest: +ELLIPSIS
      <callable_iterator object at ...>
      >>> list(matches("s==m"))
      [<re.Match object; span=(5, 9), match='spam'>, <re.Match object; span=(10, 14), match='swim'>]
  """
  regex = re.sub('~', '(.)', regex)
  regex = re.sub('(=+)', lambda x: '(' + len(x[0]) * '.' + ')', regex)
  return re.finditer("^" + regex + "$", words, re.IGNORECASE | re.MULTILINE)

class WordSet(UserList):
  """ A list of words that match the given constraints.
      Each element is a re.Match.
      Contains as many elements as we have matched constraints so far.

      (This class mainly exists to make it easy to print, but it also
      makes documentation clearer to have this list defined as a concept!)

      >>> WordSet(matches("s==m"))
      spam, swim
  """
  def __repr__(self):
    """Format nicely for display, as a list of matching words."""
    return ', '.join([match[0] for match in self])

  def __str__(self):
    return repr(self)

def match_word_sets(regex):
  """ Like matches(), but return an iterator that returns WordSets,
      rather than single re.Matches.

      >>> list(match_word_sets("s==m"))
      [spam, swim]
  """
  return map(lambda m: WordSet([m]), matches(regex))

def cross_match(wordsets, regex):
  """ Given an iterable of WordSets from preceding searches,
      generates new WordSets, adding matches for the given new regex, 
      evaluated with each WordSet's last match's groups substituted for single-digit integers.
  """
  for wordset in wordsets:
    # Substitute all groups from the last match into regex.
    lastmatch = wordset[-1]
    rs = regex  # the regex with group substitutions
    for i in range(1, lastmatch.lastindex + 1):
      rs = re.sub(str(i), '(' + lastmatch[i] + ')', rs)
    # print("cross_match: rs =", rs)

    # Now match the resulting regex over the words, add matches to a new WordSet, and list them.
    for match in matches(rs):
      # print("cross_match: adding", match, "to", wordset)
      yield wordset + [match]

def search_regexes(regexes):
    """ Returns an iterable of WordSets that match all the regexes in the given list. 

        >>> list(search_regexes(["=gg=", "2p=="]))
        [eggs, spam]
    """
    all_matches = match_word_sets(regexes[0])
    for r in regexes[1:]:
      all_matches = cross_match(all_matches, r)
    return all_matches

def main():
  # Setup
  import argparse
  import readline

  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description='Search for words that match various constraints.',
                                   epilog="""
If no regular expressions are listed, you can enter them interactively at the prompt.

Regular expressions follow the standard Python regex rules, with these
rules to make it easier to type word searches:

  Use parentheses to mark groups as usual.

  Groups will be available to the following regex using a bare digit, 1-9.

  Bare digit references will each become groups for the following regex,
  renumbered in the order they appear.

  Each tilde is converted into a group of any single character: ~ becomes (.)

  Sequences of equals are converted into a group of dots: === becomes (...)

  Example: A=LE 1AK=~ c=wa3=  gives ABLE, BAKER, COWARD
""")
  parser.add_argument('regexes', metavar='R', nargs='*',
                      help="""A regular expression to use for searching.  Case-insensitive.
                        Use digit n to interpolate the n-th group from the previous regex.""")
  parser.add_argument('--dict', dest='dictfile', default='dic.txt',
                      help='File with words, one per line (default: dic.txt)')
  parser.add_argument('--test', action='store_true', help='Run unit tests (only).')

  args = parser.parse_args()

  load_dict(args.dictfile)

  def print_results(results):
    hadSome = False
    for wordset in results:
      print(wordset)
      hadSome = True
    if not hadSome:
      print("No matches.")
    print("")

  if len(args.regexes):
    # Report the matches from command-line arguments.
    print_results(search_regexes(args.regexes))
  else:
    # Prompt for input.
    print("Interactive mode.  Type ? for help, blank line to end.")
    while True:
      line = input("Regular expressions: ").strip()
      if line == '':
        exit(0)
      if line == '?':
        print(parser.epilog)
      else:
        regexes = line.split(' ')
        print_results(search_regexes(regexes))

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == '--test':
        test()
    else:
        main()
