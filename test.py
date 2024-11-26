import unittest
from io import BytesIO
from main import UVMInstruction, UVMAssembler, UVMInterpreter
import os

class TestUVM(unittest.TestCase):
    def test_instruction_encoding(self):
        test_cases = [
            (UVMInstruction(2, 29), b'\xD2\x01\x00\x00'),  # Загрузка константы
            (UVMInstruction(12, 234), b'\xAC\x0E\x00\x00'),  # Чтение из памяти
            (UVMInstruction(11, 361), b'\x9B\x16\x00\x00'),  # Запись в память
            (UVMInstruction(7, 626), b'\x27\x27\x00\x00'),  # Операция "=="
        ]
        for instr, expected_bytes in test_cases:
            with self.subTest(instr=instr):
                self.assertEqual(instr.to_bytes(), expected_bytes)

    def test_instruction_decoding(self):
        test_cases = [
            (b'\xD2\x01\x00\x00', 2, 29),  # Загрузка константы
            (b'\xAC\x0E\x00\x00', 12, 234),  # Чтение из памяти
            (b'\x9B\x16\x00\x00', 11, 361),  # Запись в память
            (b'\x27\x27\x00\x00', 7, 626),  # Операция "=="
        ]
        for data, expected_opcode, expected_operand in test_cases:
            with self.subTest(data=data):
                instr = UVMInstruction.from_bytes(data)
                self.assertEqual(instr.opcode, expected_opcode)
                self.assertEqual(instr.operand, expected_operand)

    def test_interpreter(self):
        interpreter = UVMInterpreter(memory_size=1024)
        interpreter.memory[0] = 42  # Память по адресу 0
        interpreter.memory[5] = 42  # Память по адресу 5

        # Загрузка константы
        instr = UVMInstruction(2, 42)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 42)

        # Чтение из памяти
        instr = UVMInstruction(12, 5)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 42)

        # Операция "=="
        instr = UVMInstruction(7, 0)  # Сравнить аккумулятор с памятью[0]
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 1)  # True

        instr = UVMInstruction(7, 1023)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 0)  # False

    def test_assembler_and_interpreter(self):
        # Тестовая программа с мнемониками
        source_code = """
        ldc 42
        st 0
        ldc 99
        st 1
        ldr 0
        eq 1
        """
        
        assembler = UVMAssembler()
        assembler.assemble(source_code)
        
        # Сохранение бинарных данных в буфер
        binary_data = BytesIO()
        for instr in assembler.instructions:
            binary_data.write(instr.to_bytes())
        
        # Проверка выполнения программы
        interpreter = UVMInterpreter()
        binary_data.seek(0)
        binary = binary_data.read()

        # Сохранение бинарных данных в файл
        binary_path = 'test_binary.bin'
        with open(binary_path, 'wb') as f:
            f.write(binary)

        # Интерпретируем бинарный файл
        result_path = 'test_result.yml'
        interpreter.execute(binary_path, result_path, (0, 2))

        # Проверка, что память и аккумулятор имеют ожидаемые значения
        self.assertEqual(interpreter.memory[0], 42)
        self.assertEqual(interpreter.memory[1], 99)
        self.assertEqual(interpreter.accumulator, 0)  # Последняя операция: 42 == 99 -> False

        # Удаление временных файлов
        os.remove(binary_path)
        os.remove(result_path)

    def test_assembler_parsing(self):
        # Проверка, что ассемблер правильно парсит мнемоники
        source_code = """
        ldc 5
        st 10
        ldr 20
        eq 30
        """
        assembler = UVMAssembler()
        assembler.assemble(source_code)
        
        expected_instructions = [
            UVMInstruction(2, 5),    # ldc 5
            UVMInstruction(11, 10),  # st 10
            UVMInstruction(12, 20),  # ldr 20
            UVMInstruction(7, 30),   # eq 30
        ]
        self.assertEqual(len(assembler.instructions), len(expected_instructions))
        for actual, expected in zip(assembler.instructions, expected_instructions):
            with self.subTest(actual=actual, expected=expected):
                self.assertEqual(actual.opcode, expected.opcode)
                self.assertEqual(actual.operand, expected.operand)

    def test_assembler_and_interpreter_extended(self):
        # Тестовая программа с мнемониками
        source_code = """
        ldc 1
        st 0
        ldc 2
        st 1
        ldc 3
        st 2
        ldc 4
        st 3
        ldc 5
        st 4
        ldc 1
        st 5
        ldc 0
        st 6
        ldc 3
        st 7
        ldc 0
        st 8
        ldc 5
        st 9
        ldr 0
        eq 5
        st 5
        ldr 1
        eq 6
        st 6
        ldr 2
        eq 7
        st 7
        ldr 3
        eq 8
        st 8
        ldr 4
        eq 9
        st 9
        """
        
        assembler = UVMAssembler()
        assembler.assemble(source_code)
        
        # Сохранение бинарных данных в буфер
        binary_data = BytesIO()
        for instr in assembler.instructions:
            binary_data.write(instr.to_bytes())
        
        # Проверка выполнения программы
        interpreter = UVMInterpreter()
        binary_data.seek(0)
        binary = binary_data.read()

        # Сохранение бинарных данных в файл
        binary_path = 'test_binary_extended.bin'
        with open(binary_path, 'wb') as f:
            f.write(binary)

        # Интерпретируем бинарный файл
        result_path = 'test_result_extended.yml'
        interpreter.execute(binary_path, result_path, (0, 10))

        expected_memory = [1, 2, 3, 4, 5, 1, 0, 1, 0, 1]
        self.assertEqual(interpreter.memory[:10], expected_memory)

        # Удаление временных файлов
        os.remove(binary_path)
        os.remove(result_path)


if __name__ == "__main__":
    unittest.main()
