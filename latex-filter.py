import sys
import regex


NL_REPLACE = "%%"

def smudge():
    for line in sys.stdin:
        # Smudge remote when pulling to local
        workingLine = ""
        for line in sys.stdin:
            # print(line)
            # print(replace)
            # print(replace in line)
            if NL_REPLACE in line:
                workingLine += line.replace(NL_REPLACE, "")
            else:
                print(workingLine+line)
                workingLine = ""
        
        # print if it didn't on the last run
        if workingLine != "":
            print(workingLine)

# clean local before commit to remote
def clean():
    # readingFromDocBody = False
    readingFromDocBody = True
    for line in sys.stdin:
        # print(f"line: {line}")
        # only parse within the document body
        punctuationRegex = "((?:(?<!et|al|[A-Z])[\.]|(?:[\?|\!|;])) |---)"
        
        # captures punctuation marks, but ignores those in comments
        commentRegex = "(?(?=%)(?:.*)\n|((?:(?<!et|al|[A-Z])[\.]|(?:[\?|\!|;])) |---))"
        if readingFromDocBody:
            splitList = regex.split(commentRegex, line)
            # print(splitList)
            resultListItr = iter(splitList)

            nextItem = next(resultListItr)
            # print(nextItem is not None)
            while nextItem is not None:
                curItem, nextItem = nextItem, next(resultListItr)
                # print(f"nextitem: [{nextItem}]")

                # next item is punctuation, so combine them
                if regex.match(punctuationRegex, nextItem) is not None:
                    print(curItem + nextItem + NL_REPLACE)
                    nextItem = next(resultListItr)
                else:
                    print(curItem)

        else:
            readingFromDocBody = "\\begin{document}" in line or "\\end{document}" in line
            print(line)


if __name__ == '__main__':
    try:
        if sys.argv[1] == '--smudge':
            smudge()
        elif sys.argv[1] == '--clean':
            clean()
        else:
            pass
    except Exception:
        pass