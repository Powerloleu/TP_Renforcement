from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import io

        
class gramPrintListener(gramListener):

    def __init__(self):
        self.declared_states = set()
        self.declared_actions = set()
        self.states_with_no_action_trans = set()
        self.defined_state_actions = {}
        
    def enterDefstates(self, ctx):
        states = [str(x) for x in ctx.ID()]
        self.declared_states.update(states)
        print("States: %s" % states)

    def enterDefactions(self, ctx):
        actions = [str(x) for x in ctx.ID()]
        self.declared_actions.update(actions)
        print("Actions: %s" % actions)
        

    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        if (dep, act) in self.defined_state_actions:
            print(f"Error: State {dep} with action {act} has already been defined.")
            return
        self.defined_state_actions[(dep, act)] = True
        if dep in self.states_with_no_action_trans:
            print(f"Error: State {dep} cannot have an action since a no-action distribution has already been assigned.")
            return
        if dep not in self.declared_states or act not in self.declared_actions:
            print(f"Error: Undeclared state or action in transition: {dep} with action {act}")
            return
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))


    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        if dep not in self.declared_states:
            print(f"Error: Undeclared state in transition: {dep}")
            return
        if dep in self.states_with_no_action_trans:
            print(f"Error: State {dep} cannot have multiple no-action distributions.")
            return
        self.states_with_no_action_trans.add(dep)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))
                

def main():
    lexer = gramLexer(StdinStream())
    #lexer = gramLexer(FileStream("ex.mdp"))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main()
