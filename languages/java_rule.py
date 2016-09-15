# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
from dragonfly import Dictation
from dragonfly import Function
from dragonfly import Key, Text, MappingRule

from languages import specs


def defineMethod(_node):
    # "define [(public | protected | private)] [static] [final] [void] method"
    modifiers_string = ""
    if len(_node.words()) > 2:
        modifiers = _node.words()[1: -1]
        modifiers_string = ""
        for modifier in modifiers:
            modifiers_string = modifiers_string + modifier + " "

    modifiers_string = modifiers_string.strip()
    Text(modifiers_string + " ()").execute()
    Key("lbrace, enter, up, end, left:3").execute()
    

class JavaRule(MappingRule):

    mapping = {
        specs.SymbolSpecs.IF:                       Text("if(){") + Key("enter,up,left"),
        specs.SymbolSpecs.ELSE:                     Text("else {") + Key("enter"),
        specs.SymbolSpecs.DEFINE_METHOD:            Function(defineMethod),
        specs.SymbolSpecs.SWITCH:                   Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"),
        specs.SymbolSpecs.CASE:                     Text("case :")+Key("left"),
        specs.SymbolSpecs.BREAK:                    Text("break;"),
        specs.SymbolSpecs.DEFAULT:                  Text("default: "),
        specs.SymbolSpecs.DO_LOOP:                  Text("do {}")+Key("left, enter:2"),
        specs.SymbolSpecs.WHILE_LOOP:               Text("while ()")+Key("left"),
        specs.SymbolSpecs.FOR_LOOP:                 Text("for (int i=0; i< ; i++){") + Key("enter,up"),
        specs.SymbolSpecs.FOR_EACH_LOOP:            Text("for( : ){") + Key("enter,up"),

        specs.SymbolSpecs.TO_INTEGER:               Text("Integer.parseInt()")+ Key("left"),
        specs.SymbolSpecs.TO_STRING:                Text(".toString()"),
        
        specs.SymbolSpecs.AND:                      Text(" && "),
        specs.SymbolSpecs.OR:                       Text(" || "),
        specs.SymbolSpecs.NOT:                      Text("!"),
        
        specs.SymbolSpecs.SYSOUT:                   Text("System.out.println()")+Key("left"),
        specs.SymbolSpecs.IMPORT:                   Text( "import " ),
        specs.SymbolSpecs.FUNCTION:                 Text("(){}")+Key("left"),
        specs.SymbolSpecs.CLASS:                    Text("class  {}")+Key("left:3"),
        
        specs.SymbolSpecs.COMMENT:                  Text( "// " ),
        specs.SymbolSpecs.LONG_COMMENT:             Text("/**/")+Key("left,left"),
        specs.SymbolSpecs.NULL:                     Text("null"),
        specs.SymbolSpecs.RETURN:                   Text("return "),
        specs.SymbolSpecs.TRUE:                     Text("true"),
        specs.SymbolSpecs.FALSE:                    Text("false"),

        # "it are in": Text("Arrays.asList(TOKEN).contains(TOKEN)"),
        "deco override": Text("@Override"),
        "generic list": Text("List<>") + Key("left"),
        "generic map": Text("Map<>") + Key("left"),
        "convert (array | hooray) to list": Text("Arrays.asList("),
        "(array | hooray) list": Text("ArrayList"),
        "hash map": Text("HashMap"),

        "public": Text("public "),
        "private": Text("private "),
        "static": Text("static "),
        "final": Text("final "),
        "void": Text("void "),

        # "cast to integer": Text("(int)()")+ Key("left"),
        "new new": Text("new "),
        "big integer": Text("Integer "),
        "string": Text("String "),
        "boolean": Text("boolean "),
        # "substring": Text("substring"),

        # "sue iffae": Text("if ()")+ Key("left"),
        # "sue shells": Text("else")+ Key("enter"),
        "shell if": Text("else if ()")+ Key("left"),

        "ternary": Text("()?:") + Key("left:3"),
        "this": Text("this"),
        "continue": Text("continue"),
        "throw exception": Text("throw new Exception()")+ Key("left"),
        "is instance of": Text(" instanceof "),        
    }
    extras = [
        Dictation("modifiers"),
    ]
    defaults = {
        "modifiers": None,
    }

