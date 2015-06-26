__author__ = 'Jing'
import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

import unittest
from LexerStateMachine import *
from Context import *
from ContextManager import *

class TestLexer(unittest.TestCase):

    def setUp(self):
        pass



    def testAdvance(self):
        manager = ContextManager()
        context = Context(manager)
        lexer = LexerStateMachine(""" hi krizz
                          987 456 """, context)
        self.assertEqual(lexer.peep().data[0], 'hi')
        self.assertEqual(lexer.advance().data[0], 'krizz')
        self.assertEqual(lexer.advance().data[0], 987)
        self.assertEqual(lexer.advance().data[0], 456)

    def test_peep_should_raise_error_when_the_returned_symbol_is_not_equal_to_the_expected_symbol(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        lexer = LexerStateMachine('(', context)
        self.assertRaises(SyntaxError, lexer.peep, '*')

    def test_peep_should_not_raise_error_when_the_returned_symbol_is_equal_to_the_expected_symbol(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        lexer = LexerStateMachine('(', context)
        lexer.peep()
        #self.assertRaises(None, lexer.peep, '(')

    def test_peep_should_not_raise_error_when_the_expected_symbol_is_none(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        lexer = LexerStateMachine('(', context)
        lexer.peep()

    def test_advance_should_raise_error_when_the_returned_token_is_not_equal_to_the_expected_token(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('( )', context)
        self.assertRaises(SyntaxError, lexer.advance, '*')

    def test_advance_should_not_raise_error_when_the_returned_token_is_equal_to_the_expected_token(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('( )', context)
        lexer.advance()
        #self.assertRaises(None, lexer.advance, ')')

    def test_advance_should_not_raise_error_when_expected_symbol_is_none(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('( )', context)
        lexer.advance()

    def test_the_lexer_will_contain_the_first_token_in_the_class(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('12', context)
        testToken = lexer.currentToken
        self.assertEqual(testToken.data[0], 12)
        self.assertEqual(testToken.id, '(literal)')

    def test_peep_will_return_the_currentToken_inside_the_lexer(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('151915354', context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 151915354)
        self.assertEqual(testToken.id, '(literal)')
        testToken1 = lexer.peep()
        self.assertEqual(testToken1.data[0], 151915354)
        self.assertEqual(testToken1.id, '(literal)')

    def test_the_lexer_will_make_a_token_for_the_number_with_e_and_E(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('12E10', context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0],120000000000)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_get_the_second_word_in_the_string(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12E10', context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 'Price')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],120000000000)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_get_the_number_with_eE_power_to_positive(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12E+10', context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 'Price')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertEqual(testToken.data[0],120000000000)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_get_the_number_with_eE_power_to_negative(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12E-10', context)
        testToken = lexer.peep()
        self.assertEqual(testToken.data[0], 'Price')
        self.assertEqual(testToken.id, '(identifier)')
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1.2e-09)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_throw_exception_for_two_notation_is_included_in_the_e_floating_point(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12E--10', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Unexpected symbol \"-\" been found after -", e.msg)

    def test_advance_will_throw_exception_for_plus_plus_appear_inside_the_floating_point_e(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12E++10', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Unexpected symbol \"+\" been found after +", e.msg)


    def test_advance_will_throw_exception_for_unknown_symbol_inside_the_floating_point_e(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12E*10', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Expecting a positive or negative number after E/e.", e.msg)


    def test_advance_will_throw_exception_if_no_number_is_added_after_the_e_or_E(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        lexer = LexerStateMachine('Dummy 12E', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Expecting a positive or negative number after E/e.", e.msg)

    def test_advance_will_throw_exception_if_alphabet_added_after_the_E(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        lexer = LexerStateMachine('Dummy 12EA', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Expecting a positive or negative number after E/e.", e.msg)

    def test_advance_will_accept_E_and_e_as_floating_point(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Dummy 12e-10', context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1.2e-09)
        self.assertEqual(testToken.id, '(floating)')

    def test_advance_will_throw_the_same_error_if_e_is_replace_E_in_the_floating_point(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Price 12e--10', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Unexpected symbol \"-\" been found after -", e.msg)

        lexer = LexerStateMachine('Price 12e++10', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Unexpected symbol \"+\" been found after +", e.msg)

        lexer = LexerStateMachine('Price 12e*10', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Expecting a positive or negative number after E/e.", e.msg)

        lexer = LexerStateMachine('Dummy 12e', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Expecting a positive or negative number after E/e.", e.msg)

        lexer = LexerStateMachine('Dummy 12eA', context)
        try:
            lexer.advance()
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Expecting a positive or negative number after E/e.", e.msg)

    def test_advance_will_return_the_actual_value_if_the_floating_point_with_bigger_number_on_both_sides(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('Dummy 13123e151', context)
        testToken = lexer.advance()
        self.assertAlmostEqual(testToken.data[0], 1.3123e+155)
        self.assertEqual(testToken.id, '(floating)')
