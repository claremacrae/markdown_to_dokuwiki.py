markdown_to_dokuwiki.py
=======================

Python script to convert a Markdown file to Dokuwiki

This is based on my SuperUser answer to my question [How to convert Markdown files to Dokuwiki, on a PC](http://superuser.com/questions/402097/how-to-convert-markdown-files-to-dokuwiki-on-a-pc).

Since that answer, I've added some new features, and published my testsuite.

Pandoc needed!
================

Note that [pandoc](https://github.com/jgm/pandoc) must be in the your path, for this to work.

I have tested it with the following versions of Pandoc:

* 1.9.1.2
* 1.9.3
* 1.10.1
* 1.11.1

Running the TestSuite
=====================

To test the code, run:

    python markdown_to_dokuwiki_testsuite.py

This simply converts the sample file ''markdown_to_dokuwiki_test_input.md'' to Dokuwiki format, 
and tests that the output matches the contents of ''markdown_to_dokuwiki_test_expected.txt''

Successful output looks something like this:

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.114s
    
    OK
