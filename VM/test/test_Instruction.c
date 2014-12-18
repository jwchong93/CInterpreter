#include "unity.h"
#include "Instruction.h"
#include <stdio.h>
#include "Exception.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_explore_typecasting(void) {
  char a = 0xaa;
  unsigned char b = 0xaa;
  printf("%d\n", a);
  printf("%d\n", (int) a);
  printf("%d\n", (unsigned int) a);
  printf("%d\n", b);
  printf("%d\n", (int) b);
  printf("%d\n", (unsigned int) b);
  printf("%d\n", 0xaa);
  printf("%d\n", (int) 0xaa);
  printf("%d\n", (unsigned int) 0xaa);
}

void test_explore_addressing(void) {
  int value = 0x5A;   // 0x0028FE2C
  int value2 = 0xA5;  // 0x0028FE28
  int value3 = 0x12345678;  // 0x0028FE24
  printf("value: %p, value2: %p, value3: %p\n", &value, &value2, &value3);
  printf("0x0028FE2C: %x\n", *(int *)((char *)&value)); // 0000005A
  printf("0x0028FE2B: %x\n", *(int *)((char *)&value-1)); // 00005A00
  printf("0x0028FE2A: %x\n", *(int *)((char *)&value-2)); // 005A0000
  printf("0x0028FE29: %x\n", *(int *)((char *)&value-3)); // 5A000000
  printf("0x0028FE28: %x\n", *(int *)((char *)&value-4)); // A5

  printf("&value3+3: %x\n", *(int *)((char *)&value3+3)); // 12
  printf("&value3+2: %x\n", *(int *)((char *)&value3+2)); // 34
  printf("&value3+1: %x\n", *(int *)((char *)&value3+1)); // 56
  printf("&value3+0: %x\n", *(int *)((char *)&value3)); // 78

  printf("&value3+3: %x\n", *(char *)((char *)&value3+3)); // 12
  printf("&value3+2: %x\n", *(char *)((char *)&value3+2)); // 34
  printf("&value3+1: %x\n", *(char *)((char *)&value3+1)); // 56
  printf("&value3+0: %x\n", *(char *)((char *)&value3)); // 78
}

void test_getBits(void) {
  int result;

  result = getBits(0x240002, 23, 3); // getBits from bit 23 to bit 21
  TEST_ASSERT_EQUAL(1, result);
  result = getBits(0x240002, 20, 21); // getBits from bit 20 to bit 19
  TEST_ASSERT_EQUAL(0x40002, result);
}

void test_loadRegisterWithLiteral(void) {
  loadRegisterWithLiteral(ldrImm(REG_0, 2)); // ldr r0, #2
  TEST_ASSERT_EQUAL(2, reg[0].data);
  loadRegisterWithLiteral(ldrImm(REG_1, 2)); // ldr REG_1, #2
  TEST_ASSERT_EQUAL(2, reg[1].data);
  loadRegisterWithLiteral(ldrImm(REG_2, 2)); // ldr r2, #2
  TEST_ASSERT_EQUAL(2, reg[2].data);
  loadRegisterWithLiteral(ldrImm(REG_7, 2)); // ldr r7, #2
  TEST_ASSERT_EQUAL(2, reg[7].data);
}

void test_loadRegisterWithLiteral_should_keep_data_signed_value(void) {
  loadRegisterWithLiteral(ldrImm(0, -1)); // ldr r0, #-1
  TEST_ASSERT_EQUAL(-1, reg[0].data);
}

void test_loadRegisterFromMemory_should_load_register_with_value_in_reference(void) {
  int heap[10] = {0};
  heap[0] = 0x12345678;
  heap[1] = 0x87654321;
  heap[2] = 0x12121212;
  heap[3] = 0x55665566;
  
  reg[0].data = 0;
  reg[1].data = (int)&heap[0];
  reg[2].data = (int)&heap[3];

  loadRegisterFromMemory(ldrMem(REG_0, REG_1, 0)); // ldr r0, [r1 + 0]
  TEST_ASSERT_EQUAL_HEX(0x12345678, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_1, 4)); // ldr r0, [r1 + 4]
  TEST_ASSERT_EQUAL_HEX(0x87654321, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_1, 8)); // ldr r0, [r1 + 8]
  TEST_ASSERT_EQUAL_HEX(0x12121212, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_2, 0)); // ldr r0, [r2 + 0]
  TEST_ASSERT_EQUAL_HEX(0x55665566, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_2, -4)); // ldr r0, [r2 + -4]
  TEST_ASSERT_EQUAL_HEX(0x12121212, reg[0].data);
  loadRegisterFromMemory(ldrMem(REG_0, REG_2, -8)); // ldr r0, [r2 + -8]
  TEST_ASSERT_EQUAL_HEX(0x87654321, reg[0].data);
}

void test_storeRegisterIntoMemory_should_store_register_into_reference(void) {
  int heap[10] = {0};

  reg[1].data = (int)&heap[0];
  reg[2].data = (int)&heap[1];
  reg[0].data = 0xA5;
  storeRegisterIntoMemory(strMem(REG_0, REG_1, 0)); // str r0, [r1 + 0]
  TEST_ASSERT_EQUAL_HEX(0xA5, heap[0]);
  reg[0].data = 0x20;
  storeRegisterIntoMemory(strMem(REG_0, REG_1, 4)); // str r0, [r1 + 4]
  TEST_ASSERT_EQUAL_HEX(0x20, heap[1]);
  storeRegisterIntoMemory(strMem(REG_0, REG_2, -4)); // str r0, [r2 + #-4]
  TEST_ASSERT_EQUAL_HEX(0x20, heap[0]);
}

void test_moveRegister_r0_REG_1_should_move_REG_1_to_r0(void) {
  reg[0].data = 0;
  reg[1].data = 0xA5;
  moveRegister(movReg(REG_0, DATA, REG_1, NOP, NOP)); // mov r0.data, r1, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0xA5, reg[0].data);
}

void test_moveRegister_r7_data_or_base_or_limit_r0_should_move_r0_to_r7_data_or_base_or_limit_correctly(void) {
  reg[0].data = 0x01020304;
  moveRegister(movReg(REG_7, DATA, REG_0, NOP, NOP)); // mov r7.data, r0, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0x01020304, reg[7].data);
  moveRegister(movReg(REG_7, BASE, REG_0, NOP, NOP)); // mov r7.base, r0, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0x01020304, reg[7].data);
  moveRegister(movReg(REG_7, LIMIT, REG_0, NOP, NOP)); // mov r7.limit, r0, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0x01020304, reg[7].data);
}

void test_moveRegister_r0_given_0xFF07FF07_should_return_correct_values_for_each_shift_rotate_operations(void) {
  reg[0].data = 0;
  reg[1].data = 0xFF07FF07;
  moveRegister(movReg(REG_0, DATA, REG_1, NOP, NOP)); // mov r0.data, r1, NOP, #0
  TEST_ASSERT_EQUAL_HEX(0xFF07FF07, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, LSL, 8)); // mov r0.data, r1, LSL, #8
  TEST_ASSERT_EQUAL_HEX(0x07FF0700, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, LSR, 8)); // mov r0.data, r1, LSR, #8
  TEST_ASSERT_EQUAL_HEX(0x00FF07FF, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, ASR, 8)); // mov r0.data, r1, ASR, #8
  TEST_ASSERT_EQUAL_HEX(0xFFFF07FF, reg[0].data);
  moveRegister(movReg(REG_0, DATA, REG_1, RR, 8));  // mov r0.data, r1, RR, #8
  TEST_ASSERT_EQUAL_HEX(0x07FF07FF, reg[0].data);
}

void test_loadRegisterFromMemorySafe_should_not_throw_an_exception_if_access_to_valid_memory(void) {
  int heap[10] = {0};
  
  heap[9] = 2;

  reg[7].data = (int)&heap[0];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  Try {
    loadRegisterFromMemorySafe(ldrMemSafe(REG_0, REG_7, 36)); // ldrs r0, [r7 + 36]
    TEST_ASSERT_EQUAL(2, reg[0].data);
    freeException(exception);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_loadRegisterFromMemorySafe_should_throw_an_exception_if_access_to_invalid_memory(void) {
  int heap[10] = {0};
  
  heap[0] = 2;
  heap[1] = 4;
  heap[2] = 6;
  reg[7].data = (int)&heap[0];  // 0
  reg[7].base = (int)&heap[0];  
  reg[7].limit = 40;
  Try {
    loadRegisterFromMemorySafe(ldrMemSafe(REG_0, REG_7, 37)); // ldrs r0, [r7 + 37]
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_storeRegisterIntoMemorySafe_should_not_throw_an_exception_if_access_to_valid_memory(void) {
  int heap[10] = {0};
  
  reg[7].data = (int)&heap[0];
  reg[7].base = (int)&heap[0];  
  reg[7].limit = 40;
  reg[0].data = 0x5A;
  Try {
    storeRegisterIntoMemorySafe(strMemSafe(REG_0, REG_7, 0)); // strs r0, [r7 + 0]
    TEST_ASSERT_EQUAL(0x5A, heap[0]);
    freeException(exception);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_storeRegisterIntoMemorySafe_should_throw_an_exception_if_access_to_invalid_memory(void) {
  int memory = 0;
  reg[7].data = (int)&memory;
  reg[7].base = (int)&memory;
  reg[7].limit = 40;
  reg[0].data = 0x5A;
  Try {
    storeRegisterIntoMemorySafe(ldrMemSafe(REG_0, REG_7, 37)); // strs r0, [r7 + 37]
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_loadMultipleRegistersFromMemory_should_load_register_with_data_in_memory(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  
  reg[7].data = (int)&heap[5];
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;

  loadMultipleRegistersFromMemory(ldm(REG_7, R1|R2|R3, INC, NO_UPDATE)); // ldmi r7, [r1, r2, r3]
  TEST_ASSERT_EQUAL(-100, reg[1].data);
  TEST_ASSERT_EQUAL(-50, reg[2].data);
  TEST_ASSERT_EQUAL(-30, reg[3].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  
  loadMultipleRegistersFromMemory(ldm(REG_7, R4|R5|R6, DEC, NO_UPDATE)); // ldmd r7, [r4, r5, r6]
  TEST_ASSERT_EQUAL(-100, reg[4].data);
  TEST_ASSERT_EQUAL(-20, reg[5].data);
  TEST_ASSERT_EQUAL(-10, reg[6].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  
  loadMultipleRegistersFromMemory(ldm(REG_7, R4|R5|R6, INC, UPDATE)); // ldmi r7!, [r4, r5, r6]  r7->heap[8]
  TEST_ASSERT_EQUAL(-100, reg[4].data);
  TEST_ASSERT_EQUAL(-50, reg[5].data);
  TEST_ASSERT_EQUAL(-30, reg[6].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[8], reg[7].data);
  
  loadMultipleRegistersFromMemory(ldm(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, UPDATE)); // ldmd r7!, [r1 - r6]
  TEST_ASSERT_EQUAL(20, reg[0].data);
  TEST_ASSERT_EQUAL(-30, reg[1].data);
  TEST_ASSERT_EQUAL(-50, reg[2].data);
  TEST_ASSERT_EQUAL(-100, reg[3].data);
  TEST_ASSERT_EQUAL(-20, reg[4].data);
  TEST_ASSERT_EQUAL(-10, reg[5].data);
  TEST_ASSERT_EQUAL(100, reg[6].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[1], reg[7].data);
}

void test_loadMultipleRegistersFromMemory_load_stack_pointer_address(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  
  reg[7].data = (int)&heap[5];
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;
  
  loadMultipleRegistersFromMemory(ldm(REG_7, R7, INC, UPDATE)); // ldmi r7!, [r7]  r7->heap[6]
  TEST_ASSERT_EQUAL_HEX((int)&heap[6], reg[7].data);
  
  loadMultipleRegistersFromMemory(ldm(REG_7, R7, INC, NO_UPDATE)); // ldmi r7, [r7]
  TEST_ASSERT_EQUAL(-50, reg[7].data);                             // Will have serious problem when used as stack pointer next time
}

void test_storeMultipleRegistersIntoMemory_should_load_register_with_data_in_memory(void) {
  int heap[10] = {0};
  
  reg[7].data = (int)&heap[5];
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;
  
  storeMultipleRegistersIntoMemory(stm(REG_7, R0|R1|R2, INC, NO_UPDATE)); // stmi r7, [r0, r1, r2]
  TEST_ASSERT_EQUAL(10, heap[5]);
  TEST_ASSERT_EQUAL(-20, heap[6]);
  TEST_ASSERT_EQUAL(30, heap[7]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  
  storeMultipleRegistersIntoMemory(stm(REG_7, R3|R4|R5|R6, DEC, NO_UPDATE)); // stmd r7, [r3, r4, r5, r6]
  TEST_ASSERT_EQUAL(-40, heap[5]);
  TEST_ASSERT_EQUAL(50, heap[4]);
  TEST_ASSERT_EQUAL(-60, heap[3]);
  TEST_ASSERT_EQUAL(70, heap[2]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  
    
  storeMultipleRegistersIntoMemory(stm(REG_7, R0|R1|R2, INC, UPDATE)); // stmi r7!, [r0, r1, r2]
  TEST_ASSERT_EQUAL(10, heap[5]);
  TEST_ASSERT_EQUAL(-20, heap[6]);
  TEST_ASSERT_EQUAL(30, heap[7]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[8], reg[7].data);
  
  storeMultipleRegistersIntoMemory(stm(REG_7, R3|R4|R5|R6, DEC, UPDATE)); // stmd r7!, [r3, r4, r5, r6]
  TEST_ASSERT_EQUAL(-40, heap[8]);
  TEST_ASSERT_EQUAL(50, heap[7]);
  TEST_ASSERT_EQUAL(-60, heap[6]);
  TEST_ASSERT_EQUAL(70, heap[5]);
  TEST_ASSERT_EQUAL_HEX((int)&heap[4], reg[7].data);
}

void test_storeMultipleRegistersIntoMemory_store_stack_pointer_address(void) {
  int heap[10] = {0};
  
  reg[7].data = (int)&heap[5];
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;
  
  storeMultipleRegistersIntoMemory(stm(REG_7, R7, INC, UPDATE)); // stmi r7!, [r7]  r7->heap[6]
  TEST_ASSERT_EQUAL_HEX((int)&heap[6], reg[7].data);
  TEST_ASSERT_EQUAL_HEX((int)&heap[5], heap[5]);
  
  storeMultipleRegistersIntoMemory(stm(REG_7, R7, INC, NO_UPDATE)); // stmi r7, [r7]
  TEST_ASSERT_EQUAL_HEX((int)&heap[6], reg[7].data);
}

void test_loadMultipleRegistersFromMemorySafe_should_not_throw_exception_when_memory_is_valid(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  
  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;
  
  Try {
    loadMultipleRegistersFromMemorySafe(ldms(REG_7, R1|R2|R3, INC, NO_UPDATE));
    TEST_ASSERT_EQUAL(-100, reg[1].data);
    TEST_ASSERT_EQUAL(-50, reg[2].data);
    TEST_ASSERT_EQUAL(-30, reg[3].data);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_loadMultipleRegistersFromMemorySafe_should_throw_exception_when_stack_pointer_increases_and_exceed_limit_of_valid_memory(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  
  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;
  
  Try {
    loadMultipleRegistersFromMemorySafe(ldms(REG_7, R0|R1|R2|R3|R4|R5|R6, INC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(-100, reg[0].data);
    TEST_ASSERT_EQUAL(-50, reg[1].data);
    TEST_ASSERT_EQUAL(-30, reg[2].data);
    TEST_ASSERT_EQUAL(20, reg[3].data);
    TEST_ASSERT_EQUAL(70, reg[4].data);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
    
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_loadMultipleRegistersFromMemorySafe_should_throw_exception_when_stack_pointer_decreases_and_exceed_base_of_valid_memory(void) {
  int heap[10] = {10, 50, 100, -10, -20, -100, -50, -30, 20, 70};
  
  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 0;
  reg[1].data = 0;
  reg[2].data = 0;
  reg[3].data = 0;
  reg[4].data = 0;
  reg[5].data = 0;
  reg[6].data = 0;
  
  Try {
    loadMultipleRegistersFromMemorySafe(ldms(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(-100, reg[0].data);
    TEST_ASSERT_EQUAL(-20, reg[1].data);
    TEST_ASSERT_EQUAL(-10, reg[2].data);
    TEST_ASSERT_EQUAL(100, reg[3].data);
    TEST_ASSERT_EQUAL(50, reg[4].data);
    TEST_ASSERT_EQUAL(10, reg[5].data);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
    
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_storeMultipleRegistersIntoMemorySafe_should_not_throw_exception_when_memory_is_valid(void) {
  int heap[10] = {0};
  
  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;
  
  Try {
    storeMultipleRegistersIntoMemorySafe(stms(REG_7, R1|R2|R3, INC, NO_UPDATE));
    TEST_ASSERT_EQUAL(-20, heap[5]);
    TEST_ASSERT_EQUAL(30, heap[6]);
    TEST_ASSERT_EQUAL(-40, heap[7]);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
  } Catch(exception) {
    TEST_FAIL_MESSAGE("Should not throw exception\n");
  }
}

void test_storeMultipleRegistersIntoMemorySafe_should_throw_exception_when_stack_pointer_increases_and_exceed_limit_of_valid_memory(void) {
  int heap[10] = {0};
  
  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;
  
  Try {
    storeMultipleRegistersIntoMemorySafe(stms(REG_7, R0|R1|R2|R3|R4|R5|R6, INC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(10, heap[5]);
    TEST_ASSERT_EQUAL(-20, heap[6]);
    TEST_ASSERT_EQUAL(30, heap[7]);
    TEST_ASSERT_EQUAL(-40, heap[8]);
    TEST_ASSERT_EQUAL(50, heap[9]);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
    
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_storeMultipleRegistersIntoMemorySafe_should_throw_exception_when_stack_pointer_decreases_and_exceed_base_of_valid_memory(void) {
  int heap[10] = {0};
  
  reg[7].data = (int)&heap[5];
  reg[7].base = (int)&heap[0];
  reg[7].limit = 40;
  reg[0].data = 10;
  reg[1].data = -20;
  reg[2].data = 30;
  reg[3].data = -40;
  reg[4].data = 50;
  reg[5].data = -60;
  reg[6].data = 70;
  
  Try {
    storeMultipleRegistersIntoMemorySafe(stms(REG_7, R0|R1|R2|R3|R4|R5|R6, DEC, NO_UPDATE));
    TEST_FAIL_MESSAGE("Should throw exception\n");
  } Catch(exception) {
    TEST_ASSERT_EQUAL(10, heap[5]);
    TEST_ASSERT_EQUAL(-20, heap[4]);
    TEST_ASSERT_EQUAL(30, heap[3]);
    TEST_ASSERT_EQUAL(-40, heap[2]);
    TEST_ASSERT_EQUAL(50, heap[1]);
    TEST_ASSERT_EQUAL(-60, heap[0]);
    TEST_ASSERT_EQUAL_HEX((int)&heap[5], reg[7].data);
    
    TEST_ASSERT_EQUAL(exception->errCode, INVALID_MEMORY_ACCESS);
    dumpException(exception);
    freeException(exception);
  }
}

void test_addRegisters_should_add_2_registers() {
  reg[0].data = 10;
  reg[1].data = -20;
  addRegisters(add(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-10, reg[0].data);
}

void test_subtractRegisters_should_subtract_reg1_from_reg0() {
  reg[0].data = -10;
  reg[1].data = 20;
  subtractRegisters(sub(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-30, reg[0].data);
}

// multiply function has not completed
void test_multiplyRegisters_should_multiply_2_registers() {
  reg[0].data = 10;
  reg[1].data = -20;
  multiplyRegisters(mul(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-200, reg[0].data);
}

void test_divideRegisters_should_divide_reg1_from_reg0() {
  reg[0].data = 20;
  reg[1].data = -10;
  divideRegisters(div(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL(-2, reg[0].data);
}

void test_andRegisters_should_bitwise_and_2_registers() {
  reg[0].data = 0x00ff00ff;
  reg[1].data = 0x0ff00ff0;
  andRegisters(and(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL_HEX(0x00f000f0, reg[0].data);
}

void test_orRegisters_should_bitwise_or_2_registers() {
  reg[0].data = 0x00ff00ff;
  reg[1].data = 0x0ff00ff0;
  orRegisters(or(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL_HEX(0x0fff0fff, reg[0].data);
}

void test_xorRegisters_should_bitwise_xor_2_registers() {
  reg[0].data = 0x00ff00ff;
  reg[1].data = 0x0ff00ff0;
  xorRegisters(xor(REG_0, REG_0, REG_1));
  TEST_ASSERT_EQUAL_HEX(0x0f0f0f0f, reg[0].data);
}

