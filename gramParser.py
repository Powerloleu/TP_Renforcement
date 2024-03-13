# Generated from gram.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,108,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,1,0,3,0,19,8,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,5,1,
        29,8,1,10,1,12,1,32,9,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        5,2,44,8,2,10,2,12,2,47,9,2,1,2,1,2,1,3,1,3,1,3,1,3,5,3,55,8,3,10,
        3,12,3,58,9,3,1,3,1,3,1,4,1,4,5,4,64,8,4,10,4,12,4,67,9,4,1,5,1,
        5,3,5,71,8,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,5,6,
        85,8,6,10,6,12,6,88,9,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,
        1,7,5,7,101,8,7,10,7,12,7,104,9,7,1,7,1,7,1,7,0,0,8,0,2,4,6,8,10,
        12,14,0,0,107,0,16,1,0,0,0,2,24,1,0,0,0,4,35,1,0,0,0,6,50,1,0,0,
        0,8,61,1,0,0,0,10,70,1,0,0,0,12,72,1,0,0,0,14,91,1,0,0,0,16,18,3,
        2,1,0,17,19,3,4,2,0,18,17,1,0,0,0,18,19,1,0,0,0,19,20,1,0,0,0,20,
        21,3,6,3,0,21,22,3,8,4,0,22,23,5,0,0,1,23,1,1,0,0,0,24,25,5,1,0,
        0,25,30,5,13,0,0,26,27,5,8,0,0,27,29,5,13,0,0,28,26,1,0,0,0,29,32,
        1,0,0,0,30,28,1,0,0,0,30,31,1,0,0,0,31,33,1,0,0,0,32,30,1,0,0,0,
        33,34,5,7,0,0,34,3,1,0,0,0,35,36,5,3,0,0,36,37,5,13,0,0,37,38,5,
        5,0,0,38,45,5,12,0,0,39,40,5,8,0,0,40,41,5,13,0,0,41,42,5,5,0,0,
        42,44,5,12,0,0,43,39,1,0,0,0,44,47,1,0,0,0,45,43,1,0,0,0,45,46,1,
        0,0,0,46,48,1,0,0,0,47,45,1,0,0,0,48,49,5,7,0,0,49,5,1,0,0,0,50,
        51,5,2,0,0,51,56,5,13,0,0,52,53,5,8,0,0,53,55,5,13,0,0,54,52,1,0,
        0,0,55,58,1,0,0,0,56,54,1,0,0,0,56,57,1,0,0,0,57,59,1,0,0,0,58,56,
        1,0,0,0,59,60,5,7,0,0,60,7,1,0,0,0,61,65,3,10,5,0,62,64,3,10,5,0,
        63,62,1,0,0,0,64,67,1,0,0,0,65,63,1,0,0,0,65,66,1,0,0,0,66,9,1,0,
        0,0,67,65,1,0,0,0,68,71,3,12,6,0,69,71,3,14,7,0,70,68,1,0,0,0,70,
        69,1,0,0,0,71,11,1,0,0,0,72,73,5,13,0,0,73,74,5,10,0,0,74,75,5,13,
        0,0,75,76,5,11,0,0,76,77,5,6,0,0,77,78,5,12,0,0,78,79,5,5,0,0,79,
        86,5,13,0,0,80,81,5,9,0,0,81,82,5,12,0,0,82,83,5,5,0,0,83,85,5,13,
        0,0,84,80,1,0,0,0,85,88,1,0,0,0,86,84,1,0,0,0,86,87,1,0,0,0,87,89,
        1,0,0,0,88,86,1,0,0,0,89,90,5,7,0,0,90,13,1,0,0,0,91,92,5,13,0,0,
        92,93,5,6,0,0,93,94,5,12,0,0,94,95,5,5,0,0,95,102,5,13,0,0,96,97,
        5,9,0,0,97,98,5,12,0,0,98,99,5,5,0,0,99,101,5,13,0,0,100,96,1,0,
        0,0,101,104,1,0,0,0,102,100,1,0,0,0,102,103,1,0,0,0,103,105,1,0,
        0,0,104,102,1,0,0,0,105,106,5,7,0,0,106,15,1,0,0,0,8,18,30,45,56,
        65,70,86,102
    ]

class gramParser ( Parser ):

    grammarFileName = "gram.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'States'", "'Actions'", "'Rewards'", 
                     "'transition'", "':'", "'->'", "';'", "','", "'+'", 
                     "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "STATES", "ACTIONS", "REWARDS", "TRANSITION", 
                      "DPOINT", "FLECHE", "SEMI", "VIRG", "PLUS", "LCROCH", 
                      "RCROCH", "INT", "ID", "WS" ]

    RULE_program = 0
    RULE_defstates = 1
    RULE_defrewards = 2
    RULE_defactions = 3
    RULE_transitions = 4
    RULE_trans = 5
    RULE_transact = 6
    RULE_transnoact = 7

    ruleNames =  [ "program", "defstates", "defrewards", "defactions", "transitions", 
                   "trans", "transact", "transnoact" ]

    EOF = Token.EOF
    STATES=1
    ACTIONS=2
    REWARDS=3
    TRANSITION=4
    DPOINT=5
    FLECHE=6
    SEMI=7
    VIRG=8
    PLUS=9
    LCROCH=10
    RCROCH=11
    INT=12
    ID=13
    WS=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def defstates(self):
            return self.getTypedRuleContext(gramParser.DefstatesContext,0)


        def defactions(self):
            return self.getTypedRuleContext(gramParser.DefactionsContext,0)


        def transitions(self):
            return self.getTypedRuleContext(gramParser.TransitionsContext,0)


        def EOF(self):
            return self.getToken(gramParser.EOF, 0)

        def defrewards(self):
            return self.getTypedRuleContext(gramParser.DefrewardsContext,0)


        def getRuleIndex(self):
            return gramParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = gramParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.defstates()
            self.state = 18
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 17
                self.defrewards()


            self.state = 20
            self.defactions()
            self.state = 21
            self.transitions()
            self.state = 22
            self.match(gramParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefstatesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATES(self):
            return self.getToken(gramParser.STATES, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.ID)
            else:
                return self.getToken(gramParser.ID, i)

        def SEMI(self):
            return self.getToken(gramParser.SEMI, 0)

        def VIRG(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.VIRG)
            else:
                return self.getToken(gramParser.VIRG, i)

        def getRuleIndex(self):
            return gramParser.RULE_defstates

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefstates" ):
                listener.enterDefstates(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefstates" ):
                listener.exitDefstates(self)




    def defstates(self):

        localctx = gramParser.DefstatesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_defstates)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(gramParser.STATES)
            self.state = 25
            self.match(gramParser.ID)
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==8:
                self.state = 26
                self.match(gramParser.VIRG)
                self.state = 27
                self.match(gramParser.ID)
                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 33
            self.match(gramParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefrewardsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REWARDS(self):
            return self.getToken(gramParser.REWARDS, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.ID)
            else:
                return self.getToken(gramParser.ID, i)

        def DPOINT(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.DPOINT)
            else:
                return self.getToken(gramParser.DPOINT, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.INT)
            else:
                return self.getToken(gramParser.INT, i)

        def SEMI(self):
            return self.getToken(gramParser.SEMI, 0)

        def VIRG(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.VIRG)
            else:
                return self.getToken(gramParser.VIRG, i)

        def getRuleIndex(self):
            return gramParser.RULE_defrewards

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefrewards" ):
                listener.enterDefrewards(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefrewards" ):
                listener.exitDefrewards(self)




    def defrewards(self):

        localctx = gramParser.DefrewardsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_defrewards)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(gramParser.REWARDS)
            self.state = 36
            self.match(gramParser.ID)
            self.state = 37
            self.match(gramParser.DPOINT)
            self.state = 38
            self.match(gramParser.INT)
            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==8:
                self.state = 39
                self.match(gramParser.VIRG)
                self.state = 40
                self.match(gramParser.ID)
                self.state = 41
                self.match(gramParser.DPOINT)
                self.state = 42
                self.match(gramParser.INT)
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 48
            self.match(gramParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefactionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ACTIONS(self):
            return self.getToken(gramParser.ACTIONS, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.ID)
            else:
                return self.getToken(gramParser.ID, i)

        def SEMI(self):
            return self.getToken(gramParser.SEMI, 0)

        def VIRG(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.VIRG)
            else:
                return self.getToken(gramParser.VIRG, i)

        def getRuleIndex(self):
            return gramParser.RULE_defactions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefactions" ):
                listener.enterDefactions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefactions" ):
                listener.exitDefactions(self)




    def defactions(self):

        localctx = gramParser.DefactionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_defactions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(gramParser.ACTIONS)
            self.state = 51
            self.match(gramParser.ID)
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==8:
                self.state = 52
                self.match(gramParser.VIRG)
                self.state = 53
                self.match(gramParser.ID)
                self.state = 58
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 59
            self.match(gramParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransitionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def trans(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramParser.TransContext)
            else:
                return self.getTypedRuleContext(gramParser.TransContext,i)


        def getRuleIndex(self):
            return gramParser.RULE_transitions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransitions" ):
                listener.enterTransitions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransitions" ):
                listener.exitTransitions(self)




    def transitions(self):

        localctx = gramParser.TransitionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_transitions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.trans()
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 62
                self.trans()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def transact(self):
            return self.getTypedRuleContext(gramParser.TransactContext,0)


        def transnoact(self):
            return self.getTypedRuleContext(gramParser.TransnoactContext,0)


        def getRuleIndex(self):
            return gramParser.RULE_trans

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrans" ):
                listener.enterTrans(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrans" ):
                listener.exitTrans(self)




    def trans(self):

        localctx = gramParser.TransContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_trans)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.transact()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.transnoact()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransactContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.ID)
            else:
                return self.getToken(gramParser.ID, i)

        def LCROCH(self):
            return self.getToken(gramParser.LCROCH, 0)

        def RCROCH(self):
            return self.getToken(gramParser.RCROCH, 0)

        def FLECHE(self):
            return self.getToken(gramParser.FLECHE, 0)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.INT)
            else:
                return self.getToken(gramParser.INT, i)

        def DPOINT(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.DPOINT)
            else:
                return self.getToken(gramParser.DPOINT, i)

        def SEMI(self):
            return self.getToken(gramParser.SEMI, 0)

        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.PLUS)
            else:
                return self.getToken(gramParser.PLUS, i)

        def getRuleIndex(self):
            return gramParser.RULE_transact

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransact" ):
                listener.enterTransact(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransact" ):
                listener.exitTransact(self)




    def transact(self):

        localctx = gramParser.TransactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_transact)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(gramParser.ID)
            self.state = 73
            self.match(gramParser.LCROCH)
            self.state = 74
            self.match(gramParser.ID)
            self.state = 75
            self.match(gramParser.RCROCH)
            self.state = 76
            self.match(gramParser.FLECHE)
            self.state = 77
            self.match(gramParser.INT)
            self.state = 78
            self.match(gramParser.DPOINT)
            self.state = 79
            self.match(gramParser.ID)
            self.state = 86
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9:
                self.state = 80
                self.match(gramParser.PLUS)
                self.state = 81
                self.match(gramParser.INT)
                self.state = 82
                self.match(gramParser.DPOINT)
                self.state = 83
                self.match(gramParser.ID)
                self.state = 88
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 89
            self.match(gramParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransnoactContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.ID)
            else:
                return self.getToken(gramParser.ID, i)

        def FLECHE(self):
            return self.getToken(gramParser.FLECHE, 0)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.INT)
            else:
                return self.getToken(gramParser.INT, i)

        def DPOINT(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.DPOINT)
            else:
                return self.getToken(gramParser.DPOINT, i)

        def SEMI(self):
            return self.getToken(gramParser.SEMI, 0)

        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(gramParser.PLUS)
            else:
                return self.getToken(gramParser.PLUS, i)

        def getRuleIndex(self):
            return gramParser.RULE_transnoact

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransnoact" ):
                listener.enterTransnoact(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransnoact" ):
                listener.exitTransnoact(self)




    def transnoact(self):

        localctx = gramParser.TransnoactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_transnoact)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(gramParser.ID)
            self.state = 92
            self.match(gramParser.FLECHE)
            self.state = 93
            self.match(gramParser.INT)
            self.state = 94
            self.match(gramParser.DPOINT)
            self.state = 95
            self.match(gramParser.ID)
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9:
                self.state = 96
                self.match(gramParser.PLUS)
                self.state = 97
                self.match(gramParser.INT)
                self.state = 98
                self.match(gramParser.DPOINT)
                self.state = 99
                self.match(gramParser.ID)
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            self.match(gramParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





