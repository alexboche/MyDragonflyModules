from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key, Text, Mimic, Dictation, Function, CompoundRule)
from supporting import utils


def printNumberWithExtension(extension, w, x=None, y=None, z=None):
    number = utils.buildNumber(w, x, y, z)
    Text(number + extension).execute()
    
def printNumber(w, x=None, y=None, z=None):
    printNumberWithExtension("", w, x, y, z)

def printNumberGoToTab(w, x=None, y=None, z=None):
    printNumberWithExtension(":t", w, x, y, z)

def printNumberToTab(w, x=None, y=None, z=None):
    printNumberWithExtension(":b", w, x, y, z)

def printNumberFocus(w, x=None, y=None, z=None):
    printNumberWithExtension(":f", w, x, y, z)

def printNumberClick(w, x=None, y=None, z=None):
    printNumberWithExtension(":c", w, x, y, z)

def printNumberGoToWindow(w, x=None, y=None, z=None):
    printNumberWithExtension(":w", w, x, y, z)

go_command = "(go | goat | goke | launch | lunch)"

class GlobalChromeMappings(MappingRule):
    mapping = {
        "new (thing | tab)": Key("c-t"),
        "new window": Key("c-n"),
        "reopen tab": Key("cs-t"),
        "(next | nex) tab [<n>]": Key("c-pgdown:%(n)d"),
        "(previous | preev) tab [<n>]": Key("c-pgup:%(n)d"),
        "show tab <tab>": Key("c-%(tab)d"),
        "(first | firs) tab": Key("c-1"),
        "(last | lass | las ) tab": Key("c-9"),
        "go back": Key("a-left"),
        "go forward": Key("a-right"),
        "address [bar]": Key("a-d"),
        "refresh page": Key("f5"),
        "find <text>": Key("c-g/25") + Text("%(text)s"),
        "find next": Key("enter"),
        "find (prev | previous)": Key("s-enter"),
        "bookmark page": Key("c-d"),
        "(full-screen | full screen)": Key("f11"),
        "open <w> [<x>] [<y>] [<z>]": Key("cs-space/50") + Function(printNumber) + Key("enter"),  # click by voice
        "open focus <w> [<x>] [<y>] [<z>]": Key("cs-space/50") + Function(printNumberFocus) + Key("enter"),  # click by voice
        "open click <w> [<x>] [<y>] [<z>]": Key("cs-space/50") + Function(printNumberClick) + Key("enter"),  # click by voice
        go_command + " <w> [<x>] [<y>] [<z>]": Key("cs-space/50") + Function(printNumberToTab) + Key("enter"),  # click by voice
        go_command + " tab <w> [<x>] [<y>] [<z>]": Key("cs-space/50") + Function(printNumberGoToTab) + Key("enter"),  # click by voice
        go_command + " window <w> [<x>] [<y>] [<z>]": Key("cs-space/50") + Function(printNumberGoToWindow) + Key("enter"),  # click by voice
        "hide hints": Key("cs-space/50") + Text(":-") + Key("enter"),  # click by voice
        "show hints": Key("cs-space/50") + Text(":+") + Key("enter"),  # click by voice
        "open": Key("f"),                         # vimium
        "tabs": Key("s-f"),                       # vimium
        # "(go | goat | goke | launch | lunch) <number>": Text("%(number)d"),        # vimium
        # "(duplicate | dupe) tab": Key("y/25,t"),  # vimium
    }
    extras=[
        Integer("n", 1, 50),
        Integer("w", 0, 10),
        Integer("x", 0, 10),
        Integer("y", 0, 10),
        Integer("z", 0, 10),
        Integer("tab", 1, 8),
        Integer("number", 1, 9999),
        Dictation("text"),
    ]
    defaults = {
        "n": 1,
    }

class GmailMappings(MappingRule):
    mapping = {
        "Gmail find <text>": Key("slash/25") + Text("%(text)s"),
        "compose": Key("c"),
        "next mail [<n>]": Key("j:%(n)d"),
        "(previous | preev) mail [<n>]": Key("k:%(n)d"),
        "[go to] inbox": Key("g,i"),
        "[go to] sent mail": Key("g,t"),
        "[go to] drafts": Key("g,d"),
        "(delete | trash)": Key("hash"),
        "line trash": Key("x/5,hash"),
        "send [and] archive": Mimic("click", "send", "and", "archive"),
        "send (it | mail)": Key("c-enter"),
        "reply": Key("r"),
        "reply [to] all": Key("a"),
        "forward": Key("f"),
        "select": Key("x"),
        "move": Key("v"),
        "[to] receipts": Key("x,v/20") + Text("aa_receipts") + Key("enter"),
        "move to <text>": Key("x,v/20") + Text("%(text)s") + Key("enter"),
        "send archive": Mimic("click", "send", "and", "archive"),
    }

    extras = [
        Dictation("text"),
        Integer("n", 1, 50),
    ]

    defaults = {
        "n": 1,
    }

class OpenGmailLineRule(CompoundRule):
    """ Mimics the Dragon builtin command ("click <subject>") to open a Gmail line item.
    Always "chooses 2" to bypass that step.
    """
    spec = "take <text>"
    extras = [
        Dictation("text"),
    ]

    def _process_recognition(self, node, extras):
        dictation = str(extras["text"]).split()  # this is the target email subject
        dictation.insert(0, "click")  # this adds the "click" command for Dragon

        Mimic(*dictation).execute()  # expand the list to var args

        #Pause("10").execute()  # doesn"t seem to need this...

        Mimic("choose", "2").execute()


# the following is too brittle because the open command
# doesn"t reliably produce the same numbers for each execution.
# but, it was an interesting idea...
# class NavigateCalendarWeeks(CompoundRule):
#     """ Mimics the Dragon builtin command ("click <subject>") to open a Gmail line item.
#     Always "chooses 2" to bypass that step.
#     """
#     spec = "(next | preev) week"
#     # extras = [
#     #     Dictation("text"),
#     # ]
# 
#     def _process_recognition(self, node, extras):
#         print node.words()
#         words = node.words()
#         if len(words) >= 2:
#             if words[0] == "next":
#                 print "next"
#                 Mimic("open").execute()
#                 Pause("20").execute()
#                 Key("3,9").execute()
#             elif (words[0] == "preev") | (words[0] == "previous"):
#                 print "preev"
#                 Mimic("open").execute()
#                 Pause("20").execute()
#                 Key("8,8").execute()
#             else:
#                 print "Commmand had incorrect word: " + words[0]
#         else:
#             print "Wrong number of words in command: " + words
# 


#gmail_context = AppContext(executable="chrome", title="Gmail")

context = AppContext(executable="chrome")
chrome_grammar = Grammar("Google Chrome", context=context)
chrome_grammar.add_rule(GlobalChromeMappings())
chrome_grammar.add_rule(GmailMappings())
chrome_grammar.add_rule(OpenGmailLineRule())
# chrome_grammar.add_rule(NavigateCalendarWeeks())
chrome_grammar.load()

def unload():
    global chrome_grammar
    if chrome_grammar:
        print "unloading " + __name__ + "..."
        chrome_grammar.unload()
    chrome_grammar = None
