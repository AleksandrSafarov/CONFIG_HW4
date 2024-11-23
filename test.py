import unittest
from io import BytesIO
from main import UVMInstruction, UVMAssembler, UVMInterpreter  # Замените your_module на имя файла

class TestUVM(unittest.TestCase):
    def test_instruction_encoding(self):
        # Загрузка константы
        instr = UVMInstruction(2, 29)
        self.assertEqual(instr.to_bytes(), b'\xD2\x01\x00\x00')
        
        # Чтение из памяти
        instr = UVMInstruction(12, 234)
        self.assertEqual(instr.to_bytes(), b'\xAC\x0E\x00\x00')
        
        # Запись в память
        instr = UVMInstruction(11, 361)
        self.assertEqual(instr.to_bytes(), b'\x9B\x16\x00\x00')
        
        # Операция "=="
        instr = UVMInstruction(7, 626)
        self.assertEqual(instr.to_bytes(), b'\x27\x27\x00\x00')

    def test_instruction_decoding(self):
        # Загрузка константы
        data = b'\xD2\x01\x00\x00'
        instr = UVMInstruction.from_bytes(data)
        self.assertEqual(instr.opcode, 2)
        self.assertEqual(instr.operand, 29)
        
        # Чтение из памяти
        data = b'\xAC\x0E\x00\x00'
        instr = UVMInstruction.from_bytes(data)
        self.assertEqual(instr.opcode, 12)
        self.assertEqual(instr.operand, 234)
        
        # Запись в память
        data = b'\x9B\x16\x00\x00'
        instr = UVMInstruction.from_bytes(data)
        self.assertEqual(instr.opcode, 11)
        self.assertEqual(instr.operand, 361)
        
        # Операция "=="
        data = b'\x27\x27\x00\x00'
        instr = UVMInstruction.from_bytes(data)
        self.assertEqual(instr.opcode, 7)
        self.assertEqual(instr.operand, 626)

    def test_interpreter(self):
        interpreter = UVMInterpreter()
        interpreter.memory[5] = 42
        interpreter.memory[10] = 99

        # Загрузка константы
        instr = UVMInstruction(2, 123)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 123)

        # Чтение из памяти
        instr = UVMInstruction(12, 5)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 42)

        # Запись в память
        instr = UVMInstruction(11, 10)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.memory[10], 42)

        # Операция "=="
        instr = UVMInstruction(7, 5)
        interpreter._execute_instruction(instr)
        self.assertEqual(interpreter.accumulator, 1)  # True в Python представляется как 1

    def test_assembler_and_interpreter(self):
        # Тестовая программа на языке ассемблера
        source_code = """
        2 42
        11 0
        2 99
        11 1
        12 0
        7 1
        """
        
        assembler = UVMAssembler()
        assembler.assemble(source_code)
        
        # Сохранение бинарных данных в буфер для тестирования
        binary_data = BytesIO()
        for instr in assembler.instructions:
            binary_data.write(instr.to_bytes())
        
        # Проверка интерпретации программы
        interpreter = UVMInterpreter()
        binary_data.seek(0)  # Переместить указатель в начало
        binary = binary_data.read()
        with open('test_binary.bin', 'wb') as f:
            f.write(binary)
        interpreter.execute('test_binary.bin', 'test_result.yml', (0, 2))
        self.assertEqual(interpreter.memory[0], 42)
        self.assertEqual(interpreter.memory[1], 99)
        self.assertEqual(interpreter.accumulator, 0)

if __name__ == "__main__":
    unittest.main()
