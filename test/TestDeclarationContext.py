__author__ = 'JingWen'

import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Parser import *
from Context import *
from ContextManager import *
from DeclarationContext import *
from DefaultContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestDeclarationContextStartingWithShort(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]

        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_addShort_nud_given_short_x(self):
        lexer = LexerStateMachine('short x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addShort_nud_given_short_int_x(self):
        lexer = LexerStateMachine('short int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addShort_nud_given_short_unsigned_x(self):
        lexer = LexerStateMachine('short unsigned x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addShort_nud_given_short_int_signed_x(self):
        lexer = LexerStateMachine('short signed int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addShort_nud_given_short_unsigned_int_x(self):
        lexer = LexerStateMachine('short unsigned int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addShort_nud_given_short_x_with_assignment(self):
        lexer = LexerStateMachine('short x = 5 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.assertEqual('(def)', token[0].id)
            self.assertEqual('(decl)', token[0].data[0].id)
            self.assertEqual('int', token[0].data[0].data[0].id)
            self.assertEqual('signed', token[0].data[0].data[0].sign)
            self.assertEqual('short', token[0].data[0].data[0].modifier)
            self.assertEqual('(identifier)', token[0].data[0].data[1].id)
            self.assertEqual('x', token[0].data[0].data[1].data[0])
            self.assertEqual(5, token[0].data[1].data[0])
        except SyntaxError as e:
            self.fail('should not raise Exception')

    def test_addShort_nud_given_short_without_identifier(self):
        lexer = LexerStateMachine('short ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError ("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][7]:Expecting (identifier) before ;"+'\n'+
                             'short ;'+'\n'+
                             '      ^', e.msg)

    def test_addShort_nud_given_short_without_identifier_and_semicolon(self):
        lexer = LexerStateMachine('short', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError ("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting (identifier) before EOF"+'\n'+
                             'short'+'\n'+
                             '     ^', e.msg)

    def test_addShort_nud_given_short_without_semicolon(self):
        lexer = LexerStateMachine('short x ', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError("Exception test failed!")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting ; before EOF"+'\n'+
                             'short x '+'\n'+
                             '        ^', e.msg)

    def test_addShort_nud_given_short_x_int(self):
        lexer = LexerStateMachine('short x int ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError("Exception test failed!")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting ; before int"+'\n'
                             "short x int ;"+'\n'
                             '        ^', e.msg)

    def test_addShort_nud_given_short_long_x(self):
        lexer = LexerStateMachine('short long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError ("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][7]:Cannot have both 'short' and 'long' in declaration statement"+'\n'
                             "short long x ;"+'\n'
                             '      ^', e.msg)

    def test_addShort_nud_given_short_short_x(self):
        lexer = LexerStateMachine('short short x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError ("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][7]:Duplication of 'short' in declaration statement"+'\n'
                             "short short x ;"+'\n'
                             '      ^', e.msg)

class TestDeclarationContextStartingWithLong(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]

        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_addLong_nud_given_long_x(self):
        lexer = LexerStateMachine('long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_long_x(self):
        lexer = LexerStateMachine('long long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_long_int_x(self):
        lexer = LexerStateMachine('long long int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_long_int_unsigned_x(self):
        lexer = LexerStateMachine('long long int unsigned x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_long_signed_x(self):
        lexer = LexerStateMachine('long long signed x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_long_unsigned_int_x(self):
        lexer = LexerStateMachine('long long unsigned int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_unsigned_x(self):
        lexer = LexerStateMachine('long unsigned x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_signed_long_x(self):
        lexer = LexerStateMachine('long signed long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_unsigned_long_x(self):
        lexer = LexerStateMachine('long unsigned long int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_signed_int_x(self):
        lexer = LexerStateMachine('long signed int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_unsigned_int_long_x(self):
        lexer = LexerStateMachine('long unsigned int long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_int_x(self):
        lexer = LexerStateMachine('long int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_int_long_x(self):
        lexer = LexerStateMachine('long int long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_int_long_signed_x(self):
        lexer = LexerStateMachine('long int long signed x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_int_unsigned_x(self):
        lexer = LexerStateMachine('long int unsigned x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addLong_nud_given_long_int_signed_long_x(self):
        lexer = LexerStateMachine('long int signed long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

class TestDeclarationContextStartingWithSignedOrUnsigned(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]

        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_addSignedAndUnsigned_nud_given_signed_x(self):
        lexer = LexerStateMachine('signed x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual(None, token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_x(self):
        lexer = LexerStateMachine('unsigned int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual(None, token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_short_x(self):
        lexer = LexerStateMachine('signed int short x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_long_x(self):
        lexer = LexerStateMachine('unsigned int long x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_long_long_x(self):
        lexer = LexerStateMachine('signed int long long x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_x(self):
        lexer = LexerStateMachine('unsigned long x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_int_x(self):
        lexer = LexerStateMachine('signed long int x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_int_long_x(self):
        lexer = LexerStateMachine('unsigned long int long x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_signed_short_x(self):
        lexer = LexerStateMachine('signed short x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_short_int_x(self):
        lexer = LexerStateMachine('unsigned short int x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_long_x(self):
        lexer = LexerStateMachine('signed long long x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_long_int_x(self):
        lexer = LexerStateMachine('unsigned long long int x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

class TestDeclarationContextStartingWithInt(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]

        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_addInt_nud_given_int_x(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual(None, token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_short_x(self):
        lexer = LexerStateMachine('int short x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_long_long_signed_x(self):
        lexer = LexerStateMachine('int long long signed x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_long_x(self):
        lexer = LexerStateMachine('int long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_long_unsigned_x(self):
        lexer = LexerStateMachine('int long unsigned x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_long_signed_long_x(self):
        lexer = LexerStateMachine('int long signed long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_signed_x(self):
        lexer = LexerStateMachine('int signed x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual(None, token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_unsigned_short_x(self):
        lexer = LexerStateMachine('int unsigned short x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_unsigned_long_x(self):
        lexer = LexerStateMachine('int unsigned long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('unsigned', token[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_addInt_nud_given_int_signed_long_long_x(self):
        lexer = LexerStateMachine('int signed long long x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual('long long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

class TestDeclarationContextWithAssignmentAndComa(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]

        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_int_x_without_semicolon(self):
        lexer = LexerStateMachine('int x', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_int_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_int_y_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int x, int y ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_coma_but_left_empty_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int x, ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_x(self):
        lexer = LexerStateMachine('int x x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Error[1][7]:Expecting ; before (identifier)"+'\n'
                             "int x x ;"+'\n'
                             '      ^', e.msg)

    def test_int_x(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].sign)
        self.assertEqual(None, token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])

    def test_int_x_equal_to_2(self):
        lexer = LexerStateMachine('int x = 2 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)

        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].data[0].sign)
        self.assertEqual(None, token[0].data[0].data[0].modifier)
        self.assertEqual('x', token[0].data[0].data[1].data[0])
        self.assertEqual(2, token[0].data[1].data[0])

    def test_short_x_equal_to_2(self):
        lexer = LexerStateMachine('short x = 2 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)

        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].data[0].sign)
        self.assertEqual('short', token[0].data[0].data[0].modifier)
        self.assertEqual('x', token[0].data[0].data[1].data[0])
        self.assertEqual(2, token[0].data[1].data[0])

    def test_long_x_equal_to_2(self):
        lexer = LexerStateMachine('long x = 2 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)

        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual('signed', token[0].data[0].data[0].sign)
        self.assertEqual('long', token[0].data[0].data[0].modifier)
        self.assertEqual('x', token[0].data[0].data[1].data[0])
        self.assertEqual(2, token[0].data[1].data[0])


    def test_int_x_y_and_z(self):
        lexer = LexerStateMachine('int x , y , z ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[1].data[0])
        self.assertEqual('(decl)', token[1].id)
        self.assertEqual('int', token[1].data[0].id)
        self.assertEqual('y', token[1].data[1].data[0])
        self.assertEqual('(decl)', token[2].id)
        self.assertEqual('int', token[2].data[0].id)
        self.assertEqual('z', token[2].data[1].data[0])

    def test_short_x_y_and_z(self):
        lexer = LexerStateMachine('short x , y , z ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)

        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('short', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])
        self.assertEqual('(decl)', token[1].id)
        self.assertEqual('int', token[1].data[0].id)
        self.assertEqual('short', token[1].data[0].modifier)
        self.assertEqual('y', token[1].data[1].data[0])
        self.assertEqual('(decl)', token[2].id)
        self.assertEqual('int', token[2].data[0].id)
        self.assertEqual('short', token[2].data[0].modifier)
        self.assertEqual('z', token[2].data[1].data[0])

    def test_long_x_y_and_z(self):
        lexer = LexerStateMachine('long x , y , z ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('long', token[0].data[0].modifier)
        self.assertEqual('x', token[0].data[1].data[0])
        self.assertEqual('(decl)', token[1].id)
        self.assertEqual('int', token[1].data[0].id)
        self.assertEqual('long', token[1].data[0].modifier)
        self.assertEqual('y', token[1].data[1].data[0])
        self.assertEqual('(decl)', token[2].id)
        self.assertEqual('int', token[2].data[0].id)
        self.assertEqual('long', token[2].data[0].modifier)
        self.assertEqual('z', token[2].data[1].data[0])

    def test_signed_x_y_and_z(self):
        lexer = LexerStateMachine('signed x = - 1 , y = - 2 , z = - 3 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual(None, token[0].data[0].data[0].modifier)
        self.assertEqual('signed', token[0].data[0].data[0].sign)
        self.assertEqual('x', token[0].data[0].data[1].data[0])
        self.assertEqual('-', token[0].data[1].id)
        self.assertEqual(1, token[0].data[1].data[0].data[0])
        self.assertEqual('(def)', token[1].id)
        self.assertEqual('(decl)', token[1].data[0].id)
        self.assertEqual('int', token[1].data[0].data[0].id)
        self.assertEqual(None, token[1].data[0].data[0].modifier)
        self.assertEqual('signed', token[1].data[0].data[0].sign)
        self.assertEqual('y', token[1].data[0].data[1].data[0])
        self.assertEqual('-', token[1].data[1].id)
        self.assertEqual(2, token[1].data[1].data[0].data[0])
        self.assertEqual('(def)', token[2].id)
        self.assertEqual('(decl)', token[2].data[0].id)
        self.assertEqual('int', token[2].data[0].data[0].id)
        self.assertEqual(None, token[2].data[0].data[0].modifier)
        self.assertEqual('signed', token[2].data[0].data[0].sign)
        self.assertEqual('z', token[2].data[0].data[1].data[0])
        self.assertEqual('-', token[2].data[1].id)
        self.assertEqual(3, token[2].data[1].data[0].data[0])

    def test_int_x_y_and_z_with_some_initialization(self):
        lexer = LexerStateMachine('int x = 3 , y , z = 2 + 3 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[1].data[0])
        self.assertEqual(3, token[0].data[1].data[0])
        self.assertEqual('(decl)', token[1].id)
        self.assertEqual('int', token[1].data[0].id)
        self.assertEqual('y', token[1].data[1].data[0])
        self.assertEqual('(def)', token[2].id)
        self.assertEqual('(decl)', token[2].data[0].id)
        self.assertEqual('int', token[2].data[0].data[0].id)
        self.assertEqual('z', token[2].data[0].data[1].data[0])
        self.assertEqual('+', token[2].data[1].id)
        self.assertEqual(2, token[2].data[1].data[0].data[0])
        self.assertEqual(3, token[2].data[1].data[1].data[0])

    def test_int_x_y_z_with_initialization(self):  ################################################# should fail?
        lexer = LexerStateMachine('int x = 3 , y = 2 + 3 , z = y + 3 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[1].data[0])
        self.assertEqual(3, token[0].data[1].data[0])
        self.assertEqual('(def)', token[1].id)
        self.assertEqual('(decl)', token[1].data[0].id)
        self.assertEqual('int', token[1].data[0].data[0].id)
        self.assertEqual('y', token[1].data[0].data[1].data[0])
        self.assertEqual('+', token[1].data[1].id)
        self.assertEqual(2, token[1].data[1].data[0].data[0])
        self.assertEqual(3, token[1].data[1].data[1].data[0])
        self.assertEqual('(def)', token[2].id)
        self.assertEqual('(decl)', token[2].data[0].id)
        self.assertEqual('int', token[2].data[0].data[0].id)
        self.assertEqual('z', token[2].data[0].data[1].data[0])
        self.assertEqual('+', token[2].data[1].id)
        self.assertEqual('y', token[2].data[1].data[0].data[0])
        self.assertEqual(3, token[2].data[1].data[1].data[0])

    def test_expression_with_separate_initialization(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                      int y = 15 ; }', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('(def)', token[0].data[0].id)
        self.assertEqual('(decl)', token[0].data[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[1].data[0])
        self.assertEqual(3, token[0].data[0].data[1].data[0])
        self.assertEqual('(def)', token[0].data[1].id)
        self.assertEqual('(decl)', token[0].data[1].data[0].id)
        self.assertEqual('int', token[0].data[1].data[0].data[0].id)
        self.assertEqual('y', token[0].data[1].data[0].data[1].data[0])
        self.assertEqual(15, token[0].data[1].data[1].data[0])

    def test_nested_bracers(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                         { int y = 5 ; }\
                         { int z = 15 ; } }', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('(def)', token[0].data[0].id)
        self.assertEqual('(decl)', token[0].data[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[1].data[0])
        self.assertEqual(3, token[0].data[0].data[1].data[0])
        self.assertEqual('{', token[0].data[1].id)
        self.assertEqual('(def)', token[0].data[1].data[0].id)
        self.assertEqual('(decl)', token[0].data[1].data[0].data[0].id)
        self.assertEqual('int', token[0].data[1].data[0].data[0].data[0].id)
        self.assertEqual('y', token[0].data[1].data[0].data[0].data[1].data[0])
        self.assertEqual(5, token[0].data[1].data[0].data[1].data[0])
        self.assertEqual('{', token[0].data[2].id)
        self.assertEqual('(def)', token[0].data[2].data[0].id)
        self.assertEqual('(decl)', token[0].data[2].data[0].data[0].id)
        self.assertEqual('int', token[0].data[2].data[0].data[0].data[0].id)
        self.assertEqual('z', token[0].data[2].data[0].data[0].data[1].data[0])
        self.assertEqual(15, token[0].data[2].data[0].data[1].data[0])

    def test_declaration_expression_declaration(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                                     x = 5 + 10 ;\
                                     int z = 15 ; }', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('(def)', token[0].data[0].id)
        self.assertEqual('(decl)', token[0].data[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[1].data[0])
        self.assertEqual(3, token[0].data[0].data[1].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual('+', token[0].data[1].data[1].id)
        self.assertEqual(5, token[0].data[1].data[1].data[0].data[0])
        self.assertEqual(10, token[0].data[1].data[1].data[1].data[0])
        self.assertEqual('(def)', token[0].data[2].id)
        self.assertEqual('(decl)', token[0].data[2].data[0].id)
        self.assertEqual('int', token[0].data[2].data[0].data[0].id)
        self.assertEqual('z', token[0].data[2].data[0].data[1].data[0])
        self.assertEqual(15, token[0].data[2].data[1].data[0])

    def test_int_int_will_raiseException(self):
        lexer = LexerStateMachine('int int x = 3 ;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Error[1][5]:Duplication of 'int' in declaration statement"+'\n'+
                             'int int x = 3 ;'+'\n'+
                             '    ^', e.msg)

    def test_bracket_int_x(self):
        lexer = LexerStateMachine('(int x);', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][2]:Do not expect int here"+ '\n' +
                               '(int x);'+ '\n' +
                               ' ^',e.msg)

    def test_positive_sign_ptr_should_fail(self):
        lexer = LexerStateMachine('int +ptr;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:

            token = parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][5]:Expecting (identifier) before +"+ '\n' +
                             'int +ptr;' + '\n' +
                             '    ^', e.msg)

    def test_ptr_post_decrement_should_fail(self):
        lexer = LexerStateMachine('int ptr--;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Expecting ; before --" + '\n' +
                             'int ptr--;' + '\n' +
                             '       ^', e.msg)

class TestPointerAndArrayDeclaration(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]

        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_pointer_to_int(self):
        lexer = LexerStateMachine('int *ptr;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('*', token[0].data[0].data[0].id)
        self.assertEqual('ptr', token[0].data[1].data[0])

    def test_bracket_pointer_to_int(self):
        lexer = LexerStateMachine('int (*ptr);', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('(', token[0].data[0].data[0].id)
        self.assertEqual('*', token[0].data[0].data[0].data[0].id)
        self.assertEqual('ptr', token[0].data[1].data[0])

    def test_array_of_pointers_to_int(self):
        lexer = LexerStateMachine('int *ptr[10];', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)
        self.assertEqual('(decl)', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('*', token[0].data[0].data[0].id)
        self.assertEqual('[', token[0].data[0].data[0].data[0].id)
        self.assertEqual(10, token[0].data[0].data[0].data[0].data[0].data[0])
        self.assertEqual('ptr', token[0].data[1].data[0])

    def test_int_pointer_equal_3(self):  # check if the left token of '=', (identifier) will contain the *, [] or not
        lexer = LexerStateMachine('int *ptr = 3;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        token = parser.parseStatement(0)
        self.assertEqual('(def)', token[0].id)
        self.assertEqual('(decl)', token[0].data[0].id)
        self.assertEqual('int', token[0].data[0].data[0].id)
        self.assertEqual('*', token[0].data[0].data[0].data[0].id)
        self.assertEqual('ptr', token[0].data[0].data[1].data[0])
        self.assertEqual(3, token[0].data[1].data[0])

    def test_int_ptr_int_should_fail(self):
        lexer = LexerStateMachine('int *int x;;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting (identifier) before int"+ '\n' +
                               'int *int x;;'+ '\n' +
                               '     ^',e.msg)

    def test_int_ptr_short_should_fail(self):
        lexer = LexerStateMachine('int *short x;;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting (identifier) before short"+ '\n' +
                               'int *short x;;'+ '\n' +
                               '     ^',e.msg)

    def test_ptr_pointer_array_10_should_fail(self):
        lexer = LexerStateMachine('int ptr*[10];', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][8]:Expecting ; before *"+ '\n' +
                               'int ptr*[10];'+ '\n' +
                               '       ^',e.msg)

    def test_array_10_ptr_should_fail(self):
        lexer = LexerStateMachine('int [10]ptr;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][5]:Expecting (identifier) before ["+ '\n' +
                               'int [10]ptr;'+ '\n' +
                               '    ^',e.msg)

    def test_pointer_ptr_array_10_pointer_x_array_10_should_fail(self):
        lexer = LexerStateMachine('int *ptr[10]*x[10];', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][13]:Expecting ; before *"+ '\n' +
                               'int *ptr[10]*x[10];'+ '\n' +
                               '            ^',e.msg)

    def test_ptr_array_int_ptr(self):
        lexer = LexerStateMachine('int ptr[int ptr];', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting expression before int" + '\n' +
                             'int ptr[int ptr];' + '\n' +
                             '        ^', e.msg)

    def test_pointer_positive_sign_ptr_should_fail(self):
        lexer = LexerStateMachine('int *+ptr;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Do not expect + here" + '\n' +
                               'int *+ptr;'+ '\n' +
                               '     ^',e.msg)

    def test_pointer_ptr_postdec_should_fail(self):
        lexer = LexerStateMachine('int *ptr--;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expecting ; before --" + '\n' +
                               'int *ptr--;' + '\n' +
                               '        ^', e.msg)

    def test_pointer_array_10_should_fail(self):
        lexer = LexerStateMachine('int *[10];', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting (identifier) before [" + '\n' +
                               'int *[10];' + '\n' +
                               '     ^', e.msg)

    def test_pointer_10_should_fail(self):
        lexer = LexerStateMachine('int *10;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting (identifier) before (literal)" + '\n' +
                               'int *10;' + '\n' +
                               '     ^', e.msg)

    def test_pointer_to_10_array_10_fail(self):
        lexer = LexerStateMachine('int (*10)[10];', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        try:
            parser.parseStatement(0)
            self.fail()
        except SyntaxError as e:
            self.assertEqual("Error[1][7]:Expecting (identifier) before (literal)" + '\n' +
                               'int (*10)[10];'+ '\n' +
                               '      ^', e.msg)

if __name__ == '__main__':
    unittest.main()
