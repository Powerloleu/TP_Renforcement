from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import pandas as pd
import sys
import io

        
class gramPrintListener(gramListener):

    def __init__(self):
        self.declared_states = set()
        self.declared_actions = set()
        self.states_with_no_action_trans = set()
        self.defined_state_actions = {}
        self.transactions = None
        self.transactions_prob = False
        
    def createTransactions(self):
        columns_names = ['Origin', 'Action'] + list(self.declared_states)
        self.transactions = pd.DataFrame(columns=columns_names)

    def update_transactions_prob(self):
        df = self.transactions.copy()
        df.fillna(0, inplace = True) 
        df.iloc[:, 2:] = df.iloc[:, 2:].div(df.iloc[:, 2:].sum(axis=1), axis='rows') # Transform weights in probabilities
        print(df.head(10))
        self.transactions_prob = df

        
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
            raise ValueError(f"Error: State {dep} with action {act} has already been defined.")
            
        self.defined_state_actions[(dep, act)] = True
        if dep in self.states_with_no_action_trans:
            raise ValueError(f"Error: State {dep} cannot have an action since a no-action distribution has already been assigned.")
            
        if dep not in self.declared_states or act not in self.declared_actions:
            raise ValueError(f"Error: Undeclared state or action in transition: {dep} with action {act}")
            
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))
        
        new_trans_data = {id:weight for id, weight in zip(ids, weights)}
        new_trans_data.update({'Origin' : dep, 'Action' : act})
        new_record = pd.DataFrame([new_trans_data])
        self.transactions = pd.concat([self.transactions, new_record], ignore_index=True)

    def enterTransnoact(self, ctx):
        if self.transactions is None:
            self.createTransactions()
            
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        if dep not in self.declared_states:
            raise ValueError(f"Error: Undeclared state in transition: {dep}")

        if dep in self.states_with_no_action_trans:
            raise ValueError(f"Error: State {dep} cannot have multiple no-action distributions.")
            
        self.states_with_no_action_trans.add(dep)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))

        new_trans_data = {id:weight for id, weight in zip(ids, weights)}
        new_trans_data.update({'Origin' : dep, 'Action' : "NA"})
        new_record = pd.DataFrame([new_trans_data])
        self.transactions = pd.concat([self.transactions, new_record], ignore_index=True)       

def run(path = "correct_ex.mdp", return_printer = False):
    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream(path))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.update_transactions_prob()
    
    if return_printer:
        return printer

def main():
    run()


if __name__ == '__main__':
    main()
