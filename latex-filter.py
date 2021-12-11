import sys
import regex


def smudge():
    for line in sys.stdin:
        # Smudge remote when pulling to local

        pass

# clean local before commit to remote
def clean():
    readingFromDocBody = False
    for line in sys.stdin:
        # only parse within the document body
        punctuationRegex = "((?<!et|al|[A-Z])([\?|\!|\.|;]) )|---|%.*"
        
        # captures punctuation marks, but ignores those in comments
        commentRegex = "(?(?=%)(?:.*)\n|((?:(?<!et|al|[A-Z])(?:[\?|\!|\.|;]) )|---))"
        if readingFromDocBody:
            resultListItr = iter(regex.split(commentRegex), line)

            nextItem = next(resultListItr)
            while nextItem is not None:
                curItem, nextItem = nextItem, next(resultListItr)

                # next item is punctuation, so combine them
                if regex.match(punctuationRegex, nextItem) is not None:
                    print(curItem + nextItem + "%break%")
                    next(resultListItr)
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