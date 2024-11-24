import struct
import yaml
import argparse
# Сопоставление мнемоник и кодов операций
MNEMONICS_TO_OPCODE = {
    "ldc": 2,    # Загрузка константы
    "ldr": 12,   # Чтение из памяти
    "st": 11,    # Запись в память
    "eq": 7      # Операция "=="
}
OPCODE_TO_MNEMONICS = {v: k for k, v in MNEMONICS_TO_OPCODE.items()}

class UVMInstruction:
    def __init__(self, opcode, operand):
        self.opcode = opcode  # 4 бита
        self.operand = operand  # 28 бит

    def to_bytes(self):
        """Преобразовать команду в 4-байтовое представление."""
        combined = (self.opcode & 0xF) | ((self.operand & 0xFFFFFFF) << 4)
        return struct.pack("<I", combined)

    @staticmethod
    def from_bytes(data):
        """Создать команду из 4-байтов."""
        combined, = struct.unpack("<I", data)
        opcode = combined & 0xF
        operand = (combined >> 4) & 0xFFFFFFF
        return UVMInstruction(opcode, operand)

    def to_dict(self):
        """Преобразовать команду в словарь для лога."""
        mnemonic = OPCODE_TO_MNEMONICS.get(self.opcode, f"unknown({self.opcode})")
        return {"mnemonic": mnemonic, "operand": self.operand}

class UVMAssembler:
    def __init__(self):
        self.instructions = []

    def assemble(self, source_code):
        """Собрать текстовый код в бинарный."""
        for line in source_code.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Игнорировать пустые строки и комментарии

            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Некорректная строка: {line}")

            mnemonic = parts[0]
            operand = int(parts[1])

            if mnemonic not in MNEMONICS_TO_OPCODE:
                raise ValueError(f"Неизвестная мнемоника: {mnemonic}")

            opcode = MNEMONICS_TO_OPCODE[mnemonic]
            self.instructions.append(UVMInstruction(opcode, operand))

    def save_binary(self, filepath):
        """Сохранить бинарный файл."""
        with open(filepath, "wb") as f:
            for instr in self.instructions:
                f.write(instr.to_bytes())

    def save_log(self, filepath):
        """Сохранить лог файл в формате YAML."""
        log = [instr.to_dict() for instr in self.instructions]
        with open(filepath, "w") as f:
            yaml.dump(log, f, sort_keys=False)

class UVMInterpreter:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size  # Память УВМ
        self.accumulator = 0  # Регистр-аккумулятор

    def execute(self, binary_path, result_path, memory_range):
        """Выполнить команды из бинарного файла."""
        with open(binary_path, "rb") as f:
            data = f.read()

        instructions = [
            UVMInstruction.from_bytes(data[i:i + 4]) for i in range(0, len(data), 4)
        ]

        for instr in instructions:
            self._execute_instruction(instr)

        # Сохранить диапазон памяти в файл YAML
        result = self.memory[memory_range[0]:memory_range[1]]
        with open(result_path, "w") as f:
            yaml.dump(result, f, sort_keys=False)

    def _execute_instruction(self, instr):
        """Выполнить одну команду."""
        if instr.opcode == MNEMONICS_TO_OPCODE["ldc"]:  # Загрузка константы
            self.accumulator = instr.operand
        elif instr.opcode == MNEMONICS_TO_OPCODE["ldr"]:  # Чтение из памяти
            self.accumulator = self.memory[instr.operand]
        elif instr.opcode == MNEMONICS_TO_OPCODE["st"]:  # Запись в память
            self.memory[instr.operand] = self.accumulator
        elif instr.opcode == MNEMONICS_TO_OPCODE["eq"]:  # Операция "=="
            self.accumulator = int(self.accumulator == self.memory[instr.operand])
        else:
            raise ValueError(f"Неизвестная команда: {instr.opcode}")


def main():
    parser = argparse.ArgumentParser(description="UVM Toolchain")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда "assemble"
    assemble_parser = subparsers.add_parser("assemble", help="Ассемблировать программу")
    assemble_parser.add_argument("source", help="Путь к исходному коду программы")
    assemble_parser.add_argument("binary", help="Путь к бинарному файлу")
    assemble_parser.add_argument("log", help="Путь к файлу лога")

    # Подкоманда "interpret"
    interpret_parser = subparsers.add_parser("interpret", help="Интерпретировать программу")
    interpret_parser.add_argument("binary", help="Путь к бинарному файлу")
    interpret_parser.add_argument("result", help="Путь к файлу результата")
    interpret_parser.add_argument("memory_range", help="Диапазон памяти, формат: start:end")

    args = parser.parse_args()

    if args.command == "assemble":
        with open(args.source, "r") as f:
            source_code = f.read()

        assembler = UVMAssembler()
        assembler.assemble(source_code)
        assembler.save_binary(args.binary)
        assembler.save_log(args.log)

    elif args.command == "interpret":
        start, end = map(int, args.memory_range.split(":"))
        interpreter = UVMInterpreter()
        interpreter.execute(args.binary, args.result, (start, end))

if __name__ == "__main__":
    main()
