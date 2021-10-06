import json
import ntpath
import os
import argparse

# gf-wpg.py - Author: Mike Czumak | @MikeCzumak

# format help output (bypass argparse deletion of newlines)
class BlankLinesHelpFormatter (argparse.HelpFormatter):
    def _split_lines(self, text, width):
        lines = super()._split_lines(text, width) + ['\n']
        lines = [l.replace('[n]', '\n\t') for l in lines]
        return lines

# Construct the pattern (either strict or audit) from the wordlist  
def buildPattern(regex_type, wordlist, audit, flags_in):

    # strict regexes that don't allow for any variation outside of the designated wordlist
    strict_regexes = {
                'query_param':r'''[?&]{1}%s[=]''',
                'path':r'''[/]{1}%s[/?#;]{1}''',
                'body_param':r'''[\s]{1}name="%s"''',
                'ext':r'''[.]%s$|[.]%s[?;#]'''
    }

    # 'looser' regexes intended to be used for identifying parameters that
    # might be missed with a stricter match. Good for auditing wordlists
    audit_regexes = {
                'query_param':r'''[?&]{1}[0-9a-zA-Z_-]*%s[0-9a-zA-Z_-]*[=]{1}''',
                'path':r'''[/]{1}[0-9a-zA-Z_-]*%s[0-9a-zA-Z_-]*[/]{1}''',
                'body_param':r'''[\s]{1}name="[0-9a-zA-Z_-]*%s[0-9a-zA-Z_-]*"''',
                'ext':r'''[.]%s[^\s]*'''
    }
    
    # the pattern construct (withuser-provided flags)
    pattern = {
        'flags': '-E' + flags_in.strip(),
        'patterns': []
    }

    # choose the correct regex bsed on regex_type and audit value 
    if audit:
        regex = audit_regexes[regex_type]
    else:
        regex = strict_regexes[regex_type]

    # append the patterns to the pattern list and return
    for word in wordlist:
        pattern['patterns'].append(regex % word.strip())
    
    return pattern

# write the pattern file to the .gf folder
def writePattern(pattern, filename):
    
    # find the path and generate the filename
    path = os.path.expanduser('~/.gf')
    pattern_file = ('%s/%s.json' % (path, filename))
    
    # write the pattern to file
    with open(pattern_file, 'w') as outfile:
        outfile.write(json.dumps(pattern, indent=4))


# main
def main():
    # the args
    parser = argparse.ArgumentParser(description='Generate .json pattern file for gf', formatter_class=BlankLinesHelpFormatter)
    parser.add_argument("-t", "--type", required=True, 
                            choices=[ 
                                        "query_param", 
                                        "body_param",
                                        "path",
                                        "ext"  
                                    ], 
                        help="[n]Type of regex to generate.[n]\
                             query_param: Find query parameter names in the URL[n]\
                             body_param: Find query parameter names in the html body[n]\
                             path: Find keywords in a URL path[n]\
                             ext: Filter on extensions (e.g. .jpeg)")
    parser.add_argument("-w", "--wordlist", type=str, default=None, required=True, 
                        help="Path to the wordlist to use for regex generation")
    parser.add_argument("-n", "--name", type=str, default=None, required=True, 
                        help="Name of the pattern (used to name the json file")
    parser.add_argument("-a", "--audit", default=False, action="store_true",
                        help="Generate 'looser' audit regex to find additional matches (higher false positives). Default = False.")
    parser.add_argument("-f", "--flags", type=str, required=False, default='Hnro',
                        help="[n]Omit dashes (E is included by default)[n]\
                             H: Print filename[n]\
                             n: Print line #[n]\
                             o: Only match[n]\
                             v: Invert[n]\
                             i: Ignore case[n]\
                             r: Recursive[n]\
                             a: Binary as text[n]\
                            [n][n](see Grep man for more flag options)")

    args = parser.parse_args()

    # open the wordlist
    with open(args.wordlist) as wordfile:
        wordlist = [word.rstrip() for word in wordfile]

    #build and write the pattern
    pattern = buildPattern(args.type, wordlist, args.audit, args.flags)
    writePattern(pattern, args.name.strip())


if __name__ == '__main__':
    main()
