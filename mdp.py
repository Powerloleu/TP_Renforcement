from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import pandas as pd

'''
We modified the gramPrintListener class, adding the attributes:
- declared_states -> All states declared in the begining.
- declared_actions -> All actions declared in the begining.
- states_with_no_action_trans -> States without action 
- defined_state_actions -> All couples state actions defined
- transactions -> Dataframe representind a 3D matrix with weights to each state from a couple 
                  state action (or no action).NA values means that the actions doesnt lead 
                  to this state.
- transactions_prob -> Same dataframe as before converting weights to probabilities, sum being 1. 
                       NAs are set to zero, since it's what they mean .

We divided the main into "run" and "main". So that we can specify when running:
- The path where the file .mdp is
- If we should return the printer instance or not (Then being able to collect the data instead of just reading it)

We added verification functions to raise an error if the .mdp:
- Duplicates in definition the same couple (state, action)
- Defines a state with both an action and no action 
'''
        
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

def run(path = "correct_ex.mdp", return_printer = False, print_transactions = False):
    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream(path))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    printer.update_transactions_prob() 
    if print_transactions:
        print("------- transactions df -------")
        print(printer.transactions.head(10))
        print("------- transactions_prob df -------")
        print(printer.transactions_prob.head(10))
    if return_printer:
        return printer

def main():
    run(print_transactions = True)


if __name__ == '__main__':
    main()
