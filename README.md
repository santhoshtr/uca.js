uca.js
======

Unicode Collation Algorithm- Javascript implementation

Introduction
------------

This is a minimal Unicode collation algorithm implementation in javascript. For a detailed specification of UCA see http://www.unicode.org/reports/tr10

The default collation table provided by Unicode, often refered as allkeys.txt is available from http://www.unicode.org/Public/UCA/latest/allkeys.txt. It is a plan text file with 1.5+ MB size and get updated regularly in every new release of Unicode.

To use this definition file in html pages, there are some issues. First of all the whole the definition file is very big in size. Secondly it is plain text file with a defined syntax. To reduce the complexity we first feed this file to a python script to convert it to a json file. While doing this we do some optimization on the table structure of definitions so that the later javascript lookup is efficient. We form a Trie in python and dump it as javascript.

To reduce the size of the json file created, we will not dump the whole DUCET to json, instead we will give a unicode range - it can be the unicode range of the language we are dealing with. To make things more easier, the python script will dump the definition for the whole unicode range given and for the common latin code points.

uca.js, the main javascript file reads this json file and creates sortkey for each string passed. The sortkey can be used for weight comparison of strings.

For a demonstration, see the demo.html file included in the source.
