import sys
import regex
import argparse
from enum import Enum

class FilterMode(Enum):
    clean = "clean"
    smudge = "smudge"

    def __str__(self) -> str:
        return self.value

# string indicating that a line break was added while cleaning, 
# and needs to be removed when smudging
NL_REPLACE = "%%\n"

def smudge():
    for line in sys.stdin:
        # Smudge remote when pulling to local
        workingLine = ""
        for line in sys.stdin:
            # print(line)
            # print(replace)
            # print(replace in line)
            # print(f"line: {line}")
            # print(f"{NL_REPLACE in line}")
            # print(f"{line.replace(NL_REPLACE, '')}")
            if NL_REPLACE in line:
                workingLine += line.replace(NL_REPLACE, "")
            else:
                print(f"{workingLine + line}", end="")
                workingLine = ""
        
        # print if it didn't on the last run
        if workingLine != "":
            print(f"b: {workingLine}")

# clean local before commit to remote
def clean():
    readingFromDocBody = False
    # readingFromDocBody = True
    for line in sys.stdin:
        # only parse within the document body
        punctuationRegex = "((?:(?<!et|al|[A-Z])[\.]|(?:[\?|\!|;])) |---)(?!\n)"
        
        # captures punctuation marks, but ignores those in comments
        commentRegex = f"(?(?=%)(?:.*)\n|{punctuationRegex})"

        # if "\\begin{document}" in line:
        #     readingFromDocBody = True
        # elif "\\end{document}" in line:
        #     readingFromDocBody = False        

        # if readingFromDocBody:
        splitList = regex.split(commentRegex, line)
        # print(splitList)
        resultListItr = iter(splitList)

        curItem = next(resultListItr, None)
        nextItem = next(resultListItr, None)
        while nextItem is not None:
            # next item is punctuation, so combine them
            # print(f"cur item:{curItem}")
            # print(f"next item:{nextItem}")
            # print(f"regex match: {regex.match(punctuationRegex, nextItem)}")
            if curItem.endswith('\n'):
                print(f"{curItem}")
            elif regex.match(punctuationRegex, nextItem) is not None:
                print(f"{curItem + nextItem}", end=NL_REPLACE)
                nextItem = next(resultListItr, None)
            else:
                print(f"{curItem}")
            
            curItem, nextItem = nextItem, next(resultListItr, None)
        print(f"{curItem}", end="")
        # else:
        #     print(f"{line}", end="")


if __name__ == '__main__':
    #  init argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=FilterMode, choices=list(FilterMode), help="smudge: runs the smudge filter, for when pulling from a remote repository\nclean: runs the clean filter, for when pushing to a remote repository")
    
    # get args
    args = parser.parse_args()

    if args.mode is FilterMode.smudge:
        smudge()
    elif args.mode is FilterMode.clean:
        clean()
    else:
        parser.print_usage()
        parser.print_help()