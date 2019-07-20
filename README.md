# words
Tools for searching word lists.

Currently includes:

* `search.py` - search a dictionary of words for sets of words that have traits in common
* `dic.txt` - a fairly permissive list of words from some tutorial on the Web
* `words.txt` - a more cromulent list of words, a bit smaller

## search.py

This program helps solve word puzzles, like crosswords or Scrabble.  It was
initially motivated by the Split Decisions puzzles in the New York Times
Magazine.

The typical use case is when you want to not only find all the words that meet
a particular set of criteria, but you also want to find another word (or more)
that share common letters with the first word *and* meet some  additional
criteria.

(You can also use it just to search a dictionary of words for a single regular
expression, though `grep` is probably already on your system for that.)

Run `search.py -h` to see command line usage.

Example usage:

  `search.py "(...)RI(..)" 1AN2`

shows all pairs of 7-letter words that have the same three-letter prefix and
two-letter suffix, with "RI" between them in the first word and "AN" between
them in the second word.

  `search.py ===ri== 1an2`

does the same.

  `search.py ===ri~~ 1an23 3w==`

does the same, and also requires the last letter of both the first and second
words to be the first letter of the third, which then has a 'd' and two more
letters.

  `search.py ==ri~~ 2ef* 1ie`

shows six-letter words with 'ri' in the middle, where the second-to-last
letter starts the next word, which then has 'ef' and anything else of any
length, and the third word starts with the same letter as the second, followed
by 'ie'. 
