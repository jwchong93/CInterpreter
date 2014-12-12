#include "unity.h"
#include "Disassembler.h"
#include "Instruction.h"
#include "Exception.h"
#include <stdio.h>

void setUp(void)
{
}

void tearDown(void)
{
}

void test_dissembleBytecode(void) {
  char buffer[100] = {0};
  int bytecode[10] = {0};
  bytecode[0] = ldrImm(0, 4);
  bytecode[1] = ldrMem(0, 1, 8);
  bytecode[2] = strMem(0, 1, 8);
  bytecode[3] = 0xFFFFFFFF;

	disassembleBytecode(&buffer[0], &bytecode[0]);
  printf("%s\n", buffer);
	disassembleBytecode(&buffer[20], &bytecode[1]);
  printf("%s\n", &buffer[20]);
	disassembleBytecode(&buffer[40], &bytecode[2]);
  printf("%s\n", &buffer[40]);
}

void test_disassembleBytecodes_should_disassemble_an_array_of_bytecode(void) {
  char buffer[200] = {0};
  int bytecode[20] = {0};
  bytecode[0] = ldrImm(R4, 128);
  bytecode[1] = ldrMem(R0, R1, 8);
  bytecode[2] = strMem(R0, R1, 8);
  bytecode[3] = ldrMemSafe(R0, R1, 8);
  bytecode[4] = strMemSafe(R0, R1, 8);
  bytecode[5] = movReg(R0, DATA, R4, NOP, NOP);
  bytecode[6] = movReg(R0, DATA, R4, LSL, 4);
  bytecode[7] = movReg(R0, DATA, R4, LSR, 2);
  bytecode[8] = movReg(R0, DATA, R4, ASR, 6);
  bytecode[9] = movReg(R0, DATA, R4, RR, 5);
  bytecode[10] = 0xFFFFFFFF; // Indicates end of bytecodes

  disassembleBytecodes(&buffer[0], &bytecode[0]);
  printf("%s\n", &buffer[0]);
}