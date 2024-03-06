from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import pandas as pd
import random
import numpy as np

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
        self.declared_states = []
        self.declared_actions = []
        self.states_with_no_action_trans = []
        self.states_with_actions = set()
        self.defined_state_actions = {}
        self.transactions = None
        self.transactions_prob = False
        self.first_state = None
        self.warnings = []
        self.errors = []

    def createTransactions(self):
        columns_names = ['Origin', 'Action'] + self.declared_states
        self.transactions = pd.DataFrame(columns=columns_names)

    def update_transactions_prob(self):
        df = self.transactions.copy()
        df.fillna(0, inplace = True) 
        df.iloc[:, 2:] = df.iloc[:, 2:].div(df.iloc[:, 2:].sum(axis=1), axis='rows') # Transform weights in probabilities
        self.transactions_prob = df
        self.transactions_prob = self.transactions_prob[["Origin", "Action"]+self.declared_states]
        
    def enterDefstates(self, ctx):
        states = [str(x) for x in ctx.ID()]
        self.declared_states.extend([s for s in states if s not in self.declared_states])
        print("Initialy declared states: %s" % states)
        if self.first_state is None:
            self.first_state = states[0]

    def enterDefactions(self, ctx):
        actions = [str(x) for x in ctx.ID()]
        self.declared_actions.extend(a for a in actions if a not in self.declared_actions)
        print("Initialy declared actions: %s" % actions)
        

    def enterTransact(self, ctx):
        if self.transactions is None:
            self.createTransactions()

        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        
        if (dep, act) in self.defined_state_actions:
            self.warnings.append(f"State {dep} with action {act} has already been defined, using te first one.")
            return

        self.defined_state_actions[(dep, act)] = True
        if dep in self.states_with_no_action_trans:
            self.errors.append(f"State {dep} cannot have the action {act} since a no-action distribution has already been assigned, using the no-action only.")
            return 
                    
        if dep not in self.declared_states:
            self.warnings.append(f"Undeclared state {dep} in transition with action {act}, declared automaticaly")
            self.declared_states.append(dep)
        if dep not in self.transactions.columns:
            self.transactions[dep] = np.nan
        
        if act not in self.declared_actions:
            self.warnings.append(f"Undeclared action in transition: {dep} with action {act}, declared automaticaly")
            self.declared_actions.append(act)

        for target in ids:
            if target not in self.declared_states:
                self.warnings.append(f"Undeclared state {target} targeted in transition: {dep} with action {act}, declared automaticaly")
                self.declared_states.append(target)
            if target not in self.transactions.columns:
                self.transactions[target] = np.nan

        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))
        self.states_with_actions.add(dep)
        
        new_trans_data = {id:weight for id, weight in zip(ids, weights)}
        new_trans_data.update({'Origin' : dep, 'Action' : act})
        
        new_record = pd.DataFrame([new_trans_data])
        self.transactions = pd.concat([self.transactions, new_record], ignore_index=True)
        
        desired_columns_order = ['Origin', 'Action'] + [col for col in self.transactions.columns if col not in ['Origin', 'Action']]
        self.transactions = self.transactions[desired_columns_order]

       
    def enterTransnoact(self, ctx):
        if self.transactions is None:
            self.createTransactions()
            
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)

        if dep not in self.declared_states:
            self.warnings.append(f"Undeclared state in transition: {dep}, declared automaticaly")
            self.declared_states.append(dep)
        
        if dep not in self.transactions.columns:
            self.transactions[dep] = np.nan
        
        if dep in self.states_with_no_action_trans:
            self.errors.append(f"State {dep} cannot have multiple no-action distributions, using only the first one.")
            return
        
        if dep in self.states_with_actions:
            self.errors.append(f"State {dep} cannot have a no-action distribution since an action distribution has already been assigned, using action only.")
            return 
        
        for target in ids:
            if target not in self.declared_states:
                self.warnings.append(f"Undeclared state {target} targeted in transition from {dep} with NA, declared automaticaly")
                self.declared_states.append(target)
            if target not in self.transactions.columns:
                self.transactions[target] = np.nan
        
        self.states_with_no_action_trans.append(dep)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))

        new_trans_data = {id:weight for id, weight in zip(ids, weights)}
        new_trans_data.update({'Origin' : dep, 'Action' : "NA"})
        
        new_record = pd.DataFrame([new_trans_data])
        self.transactions = pd.concat([self.transactions, new_record], ignore_index=True)       


def run(path = "mdp_examples//lancer_de_pieces.mdp", return_printer = False, print_transactions = False, print_states = False):
    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream(path))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    
    MISSING_ID = "<missing ID>"
    if printer.first_state == MISSING_ID:
        print("No states declared, chosing a random state as first state")
        printer.declared_states.remove(MISSING_ID)
        printer.first_state = random.choice(printer.declared_states)
    
    printer.update_transactions_prob() 

    if print_transactions:
        print("\n","------- transactions df -------")
        print(printer.transactions.head(10))
        print("\n","------- transactions_prob df -------")
        print(printer.transactions_prob.head(10), "\n",)
    
    if printer.warnings: # If there are warnings in the list
        print("\n", '---------- WARNINGS WHEN PARSING -----------')
        for i, warning in enumerate(printer.warnings):
            print(f"( {i} ) - {warning}")

    if printer.errors: # If there are errors in the list
        print("\n", '---------- ERRORS WHEN PARSING -----------')
        for i, error in enumerate(printer.errors):
            print(f"( {i} ) - {error}")
        print("\n", '---------- Continuing the code with suggested corrections -----------', "\n")

    if print_states:
        print('---------- States attributes -----------')
        print(f"First state: {printer.first_state}")
        print(f"Declared states: {printer.declared_states}")

    if return_printer:
        return printer

def main():
    run(print_transactions = True, return_printer=True, print_states = True)


if __name__ == '__main__':
    main()
