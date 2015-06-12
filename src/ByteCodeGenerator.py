__author__ = 'JingWen'

from Mapping import *
from Context import *
from ContextManager import *
from RegisterAllocator import *


class ByteCodeGenerator:
    byteCodeList = []
    byteRequired = {'char': 1, 'short': 1, 'int': 4, 'long': 4, 'float': 4, 'double': 8}
    variablesInThisAST = {}

    def __init__(self, context, contextManager):
        self.context = context
        self.contextManager = contextManager
        self.mapping = Mapping()
        self.registerAllocator = RegisterAllocator(self)

    def nothing(self):
        pass
    def subFrameRegister(self, GPR=[]):
        number = 0xf5 | GPR[0] << 8 | GPR[1] << 11
        self.byteCodeList.append(number)
        return number
    def divideRegister(self):
        pass
    def multiplyRegister(self, GPR=[]):
        number = 0xf6 | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        self.byteCodeList.append(number)
        return number

    def loadMultiple(self, GPR=[]):
        number = 0xf7 | GPR[0] << 8 | GPR[1] << 11
        self.byteCodeList.append(number)
        return number
    def assignRegister(self, GPR=[]):
    #Assign FirstRegister into Second Register and store into targetRegister
        number = 0xf8 | GPR[0] << 8 | GPR[1] << 11
        self.byteCodeList.append(number)
        return number

    def storeMultiple(self, GPR=[]):
        number = 0xf9 | GPR[0] << 8 | GPR[1] << 11
        self.byteCodeList.append(number)
        return number

    def addRegister(self,GPR =[]):
        number = 0xfa | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        self.byteCodeList.append(number)
        return number

    def subRegister(self,GPR=[]):
        number = 0xfb | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        self.byteCodeList.append(number)
        return number

    def loadValue(self, GPR=[]):
        number = 0xfc | GPR[0] << 8 | GPR[1] << 11
        self.byteCodeList.append(number)
        return number

    def storeValue(self, GPR=[]):
        number = 0xfd | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 14
        self.byteCodeList.append(number)
        return number

    def loadRegister(self, GPR=[]):
        number = 0xfe | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 17
        self.byteCodeList.append(number)
        return number

    def storeRegister(self, GPR=[]):
        number = 0xff | GPR[0] << 8 | GPR[1] << 11 | GPR[2] << 17
        self.byteCodeList.append(number)
        return number

    def generateRightCodeFirst(self, token):
        secondTime = 0
        for index in range(len(token.data)-1, -1, -1):
            if token.data[index].id == '(identifier)':
                if secondTime == 0:
                    self.loadRegister([self.mapping.getAFreeWorkingRegister(), 7, self.variablesInThisAST[token.data[index].data[0]]])
                else:
                    self.loadRegister([self.mapping.getALargestWorkingRegister(), 7, self.variablesInThisAST[token.data[index].data[0]]])
            elif token.data[index].id == '(literal)':
                if secondTime == 0:
                    self.loadValue([self.mapping.getAFreeWorkingRegister(), token.data[index].data[0]])
                else:
                    self.loadValue([self.mapping.getALargestWorkingRegister(), token.data[index].data[0]])
            else:
                token.data[index].generateByteCode()
            secondTime += 1

    def generateLeftCodeFirst(self, token):
        secondTime = 0
        for index in range(0, len(token.data)):
            if token.data[index].id == '(identifier)':
                if secondTime == 0:
                    self.loadRegister([self.mapping.getAFreeWorkingRegister(), self.mapping.framePointerRegister, self.variablesInThisAST[token.data[index].data[0]]])
                else:
                    self.loadRegister([self.mapping.getALargestWorkingRegister(), self.mapping.framePointerRegister, self.variablesInThisAST[token.data[index].data[0]]])
            elif token.data[index].id == '(literal)':
                if secondTime == 0:
                    self.loadValue([self.mapping.getAFreeWorkingRegister(), token.data[index].data[0]])
                else:
                    self.loadValue([self.mapping.getALargestWorkingRegister(), token.data[index].data[0]])
            else:
                token.data[index].generateByteCode()
            secondTime += 1

    def findOutAndGenerateCorrectSideCode(self, token):
        if token.weight[2] >= token.weight[1]:
            self.generateRightCodeFirst(token)
        else:
            self.generateLeftCodeFirst(token)

    def decideWhetherToSaveSlotForPopValue(self, status, generateByteCode):
        GPR=[]
        firstRegister = self.mapping.releaseALargestWorkingRegister()
        secondRegister = self.mapping.releaseAWorkingRegister()
        if status != 0:
            count = self.mapping.getASmallestFreeRegisterBeforePop(status)
            GPR.insert(0,count)
            GPR.insert(1,secondRegister)
            GPR.insert(2,firstRegister)
            #self.oracle.getALargestWorkingRegister()
        else:
            GPR.insert(0,secondRegister)
            GPR.insert(1,secondRegister)
            GPR.insert(2,firstRegister)
            self.mapping.getAFreeWorkingRegister()

        if generateByteCode == self.assignRegister:
            GPR[0] = secondRegister
            GPR[1] = firstRegister
        generateByteCode(GPR)
    def initGeneration(self):
        thisGenerator = self

        def initialization(self,token):
            variableCounter = 0
            if token.id in thisGenerator.byteRequired:
                variableCounter += 1

            thisGenerator.subFrameRegister([thisGenerator.mapping.framePointerRegister, thisGenerator.byteRequired[token.id]*variableCounter])
            return thisGenerator.byteCodeList

        respectiveByteCodeFunction = {'int': initialization, '=': self.assignRegister, '+': self.addRegister, \
                                            '-': self.subRegister, '*': self.multiplyRegister, '/': self.divideRegister, \
                                            '(systemToken)': self.nothing, ';': self.nothing, ',': self.nothing, '}': self.nothing, '{': self.nothing}

        def generateByteCode(self):
            if thisGenerator.isADeclaration(self.id):
                return initialization(None, self)
            else:
                pushed = thisGenerator.registerAllocator.decideWhetherToPush(self)
                thisGenerator.findOutAndGenerateCorrectSideCode(self)

                thisGenerator.decideWhetherToSaveSlotForPopValue(pushed, respectiveByteCodeFunction[self.id])

                thisGenerator.registerAllocator.decideWhetherToPop(pushed)
                return thisGenerator.byteCodeList


        #Start the initialization
        self.byteCodeList = []
        for context in self.contextManager.currentContexts:
            for token in context.symbolTable:
                context.symbolTable[token].generateByteCode = generateByteCode

    def isADeclaration(self, unknownToken):
        if unknownToken in ByteCodeGenerator.byteRequired:
            return True
        else:
            return False



    #For the moment, these function is not been used
    """

        def generateByteCode(self, token):
        if token[0].id == '{':
            token = token[0].data

        self.byteCodeList =[]
        index = 0
        index = self.generateInitializationCode(token, index)

        for value in range(index, len(token)):
            self.injectregisterRequiredAtThatLevel(token[value])
            self.generateProcessCode(token[value])


    #define the sub-routine that generate byteCode(Infix)
        def generateInfixByteCode():
            for dataIndex in range(0, len(token.data)):
                if not isinstance(token.data[dataIndex], int):
                    token.data[dataIndex].generateByteCode()
            suitableFunction = self.respectiveByteCodeFunction[self.getAFreeWorkingRegister()]
            code = suitableFunction()
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
        #define the sub-routine that generate byteCode(literal)
        def generateLiteralByteCode():
            self.updateTheWorkingRegisterCounterAndStatus()
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | token.data[0])
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
    def injectLevel(self, token):
        levels =[]
        for element in token.data:
            if element.id == '(identifier)' or element.id == '(literal)':
                element.level = 0
                tempLevel = 0
            else:
                tempLevel = self.injectLevel(element)

            levels.append(tempLevel)
        if abs(levels[0]) >= abs(levels[1]):
            largest = -abs(levels[0])

        else:
            largest = abs(levels[1])
        if largest >= 0:
            largest += 1
        else:
            largest -= 1
        token.level = largest
        return largest

    def assignRegisters(self, register1, register2):
        number = 0xfa | register1 << 8 | register2 << 11
        self.byteCodeList.append(number)
        return number

        #Start to make a fake switch case.
        def storeIntoWorkingRegisterTwo():
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | self.workingRegisterCounter-2 << 8 | self.workingRegisterCounter-1)
            self.registerStatus[self.workingRegisterCounter-1] = 0
            self.registerStatus[self.workingRegisterCounter-2] = 0
            return code
        def storeIntoWorkingRegisterOne():
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | self.workingRegisterCounter+1 << 8 | self.workingRegisterCounter-1)
            self.registerStatus[self.workingRegisterCounter+1] = 0
            self.registerStatus[self.workingRegisterCounter-1] = 0
            return code
        def storeIntoWorkingRegisterZero():
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | self.workingRegisterCounter+1 << 8 | self.workingRegisterCounter+2)
            self.registerStatus[self.workingRegisterCounter+1] = 0
            self.registerStatus[self.workingRegisterCounter+2] = 0
            return code
        storeLocation = {0: storeIntoWorkingRegisterZero, 1: storeIntoWorkingRegisterOne, 2: storeIntoWorkingRegisterTwo}
        ###############################################################################################################
        thisGenerator = self
        #define the sub-routine that generate byteCode(Infix)
        def generateInfixByteCode():
            for dataIndex in range(0, len(token.data)):
                if not isinstance(token.data[dataIndex], int):
                    token.data[dataIndex].generateByteCode()
            self.updateTheWorkingRegisterCounterAndStatus()
            suitableFunction = storeLocation[self.workingRegisterCounter]
            code = suitableFunction()
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
        #define the sub-routine that generate byteCode(literal)
        def generateLiteralByteCode():
            self.updateTheWorkingRegisterCounterAndStatus()
            code = hex(self.byteCodeDictionaty[token.id] << 24 | self.workingRegisterCounter << 16 | token.data[0])
            self.workingRegisterCounter += 1
            thisGenerator.byteCodeList.append(str(code))
            return thisGenerator.byteCodeList
        #end define the generation subroutine
        ###############################################################################################################
        #Start the initialization
        self.byteCodeList = []
        if token.id == '(literal)':
            token.generateByteCode = generateLiteralByteCode
        else:
            for context in self.contextManager.currentContexts:
                if token.id in context.symbolTable:
                    if token.arity == self.context.BINARY:
                        token.generateByteCode = generateInfixByteCode
        for dataIndex in range(0, len(token.data)):
            if token.id != '(literal)':
                self.initGeneration(token.data[dataIndex])
    """
