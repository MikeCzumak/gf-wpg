# gf-wpg
A wordlist-based pattern generator to use with gf (by tomnomnom)

## Overview

I use tomnomnom's [gf](https://github.com/tomnomnom/gf) quite a lot and there are some patterns for which I rely on a number of wordlists. For example, when grepping for keywords in URLs I have separate lists for SSRF and SQLi. I regularly update those wordlists (and often customize them depending on the testing target) so I don't want to manually have to create or update separate gf pattern files. 

This *really basic* python does that work for me, reading in a wordlist and creating a corresponding gf pattern file in a matte of seconds.  

## Usage

```
usage: gf-gen.py [-h] -t {query_param,body_param,path,ext} -w WORDLIST -n NAME [-a] [-f FLAGS]

Generate .json pattern file for gf

optional arguments:
  -h, --help            show this help message and exit


  -t {query_param,body_param,path,ext}, --type {query_param,body_param,path,ext}

	Type of regex to generate.
	 query_param: Find query parameter names in the URL
	 body_param: Find query parameter names in the html body
	 path: Find keywords in a URL path
	 ext: Filter on extensions (e.g. .jpeg)


  -w WORDLIST, --wordlist WORDLIST
                        Path to the wordlist to use for regex generation


  -n NAME, --name NAME  Name of the pattern (used to name the json file


  -a, --audit           Generate 'looser' audit regex to find additional matches (higher false positives). Default = False.


  -f FLAGS, --flags FLAGS

	Omit dashes (E is included by default)
	 H: Print filename
	 n: Print line #
	 o: Only match
	 v: Invert
	 i: Ignore case
	 r: Recursive
	 a: Binary as text


	(see Grep man for more flag options)
```

This is a really basic script but there are a few options to be aware of.

*type*

I've included four different options for the pattern `type` (`-t`). The two "param" options (`query_param` and `body_param`) are what I use to grep for wordlist values in the respective parameter names. So, if you have a wordlist that includes a value of `user_id`, the `query_param` regex will grep for `?user_id=` and `&user_id=` (to be used if you're parsing URLs) while the `body_param` regex will grep for `name="user_id"` (to be used if you're parsing html). The `path` option will grep for `/path/` (also for URLs). I use `ext` option to grep for lists of file extensions (.jpg, .php, etc.), primarily when filtering in/out specific URLs. 

*wordlist*

The wordlist argument is self-explanatory -- just a path to a simple, line-delimited list of words.

*name*

The `name` argument provides the name of the file. It will automatically be written to the .gf folder (obviously you must have gf installed, see dependencies). The script leverages `os.path.expanduser('~/.gf')` to find the write directory but I've only tested on Mac to-date. 

*audit*

By default, the `audit` argument is set to False and explicitly passing it at run time sets it to True. What this does is select a 'looser' regex for each of the types described above to allow for broader matching. For example, in the default mode, the regex for `query_param` looks like this: `[?&]{1}%s[=]` which only allows for strict matching of the words in the provided wordlist. So a word `user_id` will only match on `?user_id=` or `&user_id=`. When sorting through a large number of URLs I often prefer this preciseness to eliminate false positive matches, which is why I regularly curate my wordlists. However, this strict match would miss a parameter value of `admin_user_id` so you then risk false negatives (i.e. missing something interesting). 

The 'looser' regex for `query_param` which is enabled with the `-a` option looks like this `[?&]{1}[0-9a-zA-Z_-]*%s[0-9a-zA-Z_-]*[=]{1}`. It still follows the general format of `?word=` or `&word=` but allows for characters to occur on either side of the provided word. 


## Dependencies
You should just need gf and python. I included the link to gf above. I will caution that I've only tested on Mac OS to-date so I can't guarantee behavior / portability on other OSs at the moment.

## License 

LICENSE/WARRANTY: This code is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
