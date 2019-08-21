import re

NAME_RE = re.compile(r"(\d*_)([\w\s]+)(\.py)")

def format_name(string):
    """ Formats the name of a FoxDot tutorial file for user-friendly display """
    match = NAME_RE.match(string)
    if match:
        output = " ".join(match.group(2).split("_")).title()
    else:
        output = "Un-named Tutorial"
    return output


a = "01"
b1 = "Basic Tutorial Name"


b2 = format_name(a)

print(b1, b2, b1 == b2)