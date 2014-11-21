#This file was originally generated by PyScripter's unitest wizard

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

import unittest
from Lexer import *
from Context import *
from ExpressionContext import *

class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLexerAndSymbolGetIdentifierAndLiteral(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        lexer = Lexer('xyz 1234', context)
        token = lexer.peep()
        self.assertEqual(token.id, '(identifier)')
        self.assertEqual(token.data[0], 'xyz')
        token = lexer.advance()
        self.assertEqual(token.id, '(literal)')
        self.assertEqual(token.data[0], 1234)

    def testGetInfixAddOperatorTokens(self):
        manager = ContextManager()
        context = Context(manager)
        expression = ExpressionContext(manager)
        manager.setCurrentContexts([context, expression])
        expression.addInfixOperator('+', 70)
        expression.addInfixOperator('-', 70)
        lexer = Lexer('+ -', context)
        token = lexer.peep()
        self.assertEqual(token.id, '+')
        self.assertEqual(token.arity, Context.BINARY)
        token = lexer.advance()
        self.assertEqual(token.id, '-')
        self.assertEqual(token.arity, Context.BINARY)

    def testLookAHeadWillShowTheNextToken(self):
        manager = ContextManager()
        context = Context(manager)
        expression = ExpressionContext(manager)
        manager.setCurrentContexts([context, expression])
        expression.addInfixOperator('+', 70)
        expression.addInfixOperator('-', 70)
        lexer = Lexer('3 + 5 - 6', context)
        token = lexer.peep()
        self.assertEqual(token.id, '(literal)')
        self.assertEqual(token.data[0], 3)
        token = lexer.advance()
        self.assertEqual(token.id, '+')

    def testLookAHeadWillShowTheNextTokenAfterAdvance(self):
        manager = ContextManager()
        context = Context(manager)
        expression = ExpressionContext(manager)
        manager.setCurrentContexts([context, expression])
        expression.addInfixOperator('+', 70)
        expression.addInfixOperator('-', 70)
        lexer = Lexer('13 + 5 - 6', context)
        token = lexer.peep()
        self.assertEqual(token.id, '(literal)')
        self.assertEqual(token.data[0], 13)
        token = lexer.advance()
        self.assertEqual(token.id, '+')


    def testAdvanceWillReturnAnEmptyTokenWhenItReachedTheEndOfTheStatement(self):
        manager = ContextManager()
        context = Context(manager)
        expression = ExpressionContext(manager)
        manager.setCurrentContexts([context, expression])
        expression.addInfixOperator('+', 70)
        lexer = Lexer('13 + 5', context)
        token = lexer.peep()
        self.assertEqual(token.id, '(literal)')
        self.assertEqual(token.data[0], 13)
        token = lexer.advance()
        self.assertEqual(token.id, '+')
        token = lexer.advance()
        self.assertEqual(token.id, '(literal)')
        self.assertEqual(token.data[0], 5)
        token = lexer.advance()
        self.assertEqual(token.id, '(systemToken)')
        self.assertEqual(token.data[0], '(end)')

if __name__ == '__main__':
    unittest.main()