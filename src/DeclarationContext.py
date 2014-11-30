__author__ = 'JingWen'

import os,sys
lib_path = os.path.abspath('\..\src')
sys.path.append(lib_path)

from Context import *
from ContextManager import *

class DeclarationContext(Context):
    def addIntDeclaration(self, id, bindingPower):
        thisContext = self
        def nud(self):
            nameToken = thisContext.contextManager.parser.lexer.advance()
            self.data.append(nameToken)
            expressionToken = thisContext.contextManager.parser.parse(0)
            if expressionToken.id != nameToken.id:
                self.data.append(expressionToken)
            return self
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass