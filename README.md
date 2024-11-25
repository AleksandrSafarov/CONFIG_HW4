# Домашнее задание №4 по конфигурационному управлению
## Сделал студент группы ИКБО-11-23, Сафаров Александр Алексеевич
## Номер варианта: 20
## **Формулировка задачи**

Разработать ассемблер и интерпретатор для учебной виртуальной машины  
(УВМ). Система команд УВМ представлена далее.  
Для ассемблера необходимо разработать читаемое представление команд  
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к  
которой задается из командной строки. Результатом работы ассемблера является  
бинарный файл в виде последовательности байт, путь к которому задается из  
командной строки. Дополнительный ключ командной строки задает путь к файлу-  
логу, в котором хранятся ассемблированные инструкции в духе списков  
“ключ=значение”, как в приведенных далее тестах.  

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ  
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон  
также указывается из командной строки.  
Форматом для файла-лога и файла-результата является yaml.  
Необходимо реализовать приведенные тесты для всех команд, а также  
написать и отладить тестовую программу.  

---

### Загрузка константы  
| A | B           |  
|---|-------------|  
| Биты 0—3 | Биты 4—26 |  
| 2 | Константа |  

Размер команды: 4 байт. Операнд: поле B. Результат: регистр-аккумулятор.  
**Тест (A=2, B=29):**  
`0xD2, 0x01, 0x00, 0x00`  

---

### Чтение значения из памяти  
| A | B           |  
|---|-------------|  
| Биты 0—3 | Биты 4—27 |  
| 12 | Адрес |  

Размер команды: 4 байт. Операнд: значение в памяти по адресу, которым  
является поле B. Результат: регистр-аккумулятор.  
**Тест (A=12, B=234):**  
`0xAC, 0x0E, 0x00, 0x00`  

---

### Запись значения в память  
| A | B           |  
|---|-------------|  
| Биты 0—3 | Биты 4—27 |  
| 11 | Адрес |  

Размер команды: 4 байт. Операнд: регистр-аккумулятор. Результат: значение  
в памяти по адресу, которым является поле B.  
**Тест (A=11, B=361):**  
`0x9B, 0x16, 0x00, 0x00`  

---

### Бинарная операция: "=="  
| A | B           |  
|---|-------------|  
| Биты 0—3 | Биты 4—27 |  
| 7 | Адрес |  

Размер команды: 4 байт. Первый операнд: регистр-аккумулятор. Второй  
операнд: значение в памяти по адресу, которым является поле B. Результат:  
регистр-аккумулятор.  
**Тест (A=7, B=626):**  
`0x27, 0x27, 0x00, 0x00`  

---

### Тестовая программа  
Выполнить поэлементно операцию "==" над двумя векторами длины 5.  
Результат записать во второй вектор.  

---   
## Описание
Проект написан на языке программирования Python. Ссылка на проект: https://github.com/AleksandrSafarov/CONFIG_HW4
### Запуск программы
1. Склонировать проект
2. Перейти в папку с проектом в терминале
3. Заполнить текстовый файл командами (или использовать уже готовый source.txt)
4. Ввести команду (для запуска ассемблера)
```
python main.py assemble source.txt program.bin log.yaml
```
5. Ввести команду (для запуска ассемблера)
```
python main.py interpret program.bin result.yaml <диапозон памяти (пример 0:10)>
```
### Запуск тестовой программы
1. Склонировать проект
2. Перейти в папку с проектом в терминале
3. Ввести команду (для запуска ассемблера)
```
python main.py assemble test.txt program.bin log.yaml
```
4. Ввести команду (для запуска ассемблера)
```
python main.py interpret program.bin result.yaml 0:10
```
### Запуск юнит тестов
1. Склонировать проект
2. Перейти в папку с проектом в терминале
3. Запустить тесты
```
python test.py
```

## Описание функций и настроек

### Функции

#### 1. `UVMInstruction.to_bytes()`
Преобразует инструкцию УВМ в бинарное представление (4 байта).

- **Параметры**: 
  - Нет параметров.
  
- **Возвращает**: 
  - `bytes`: Бинарное представление инструкции.

- **Описание**:
  - Комбинирует `opcode` и `operand` в одно 4-байтовое целое число с помощью битовых операций.

#### 2. `UVMInstruction.from_bytes(data)`
Создаёт инструкцию УВМ из её бинарного представления.

- **Параметры**: 
  - `data` (`bytes`): 4-байтовое бинарное представление инструкции.

- **Возвращает**: 
  - Объект `UVMInstruction`.

- **Описание**:
  - Декодирует `opcode` и `operand` из бинарных данных с помощью битовых операций.

#### 3. `UVMInstruction.to_dict()`
Преобразует инструкцию УВМ в словарь для сохранения в лог.

- **Параметры**: 
  - Нет параметров.
  
- **Возвращает**: 
  - `dict`: Словарь с ключами `opcode` и `operand`.

#### 4. `UVMAssembler.assemble(source_code)`
Собирает текстовый исходный код программы УВМ в список инструкций.

- **Параметры**: 
  - `source_code` (`str`): Текстовый код программы, каждая строка которого содержит `opcode` и `operand`.

- **Возвращает**: 
  - Нет.

- **Исключения**:
  - `ValueError`, если строка некорректна.

#### 5. `UVMAssembler.save_binary(filepath)`
Сохраняет инструкции в бинарном формате.

- **Параметры**: 
  - `filepath` (`str`): Путь к файлу для сохранения.

- **Возвращает**: 
  - Нет.

#### 6. `UVMAssembler.save_log(filepath)`
Сохраняет лог инструкций в формате YAML.

- **Параметры**: 
  - `filepath` (`str`): Путь к файлу для сохранения.

- **Возвращает**: 
  - Нет.

#### 7. `UVMInterpreter.execute(binary_path, result_path, memory_range)`
Интерпретирует команды из бинарного файла и сохраняет диапазон памяти в YAML.

- **Параметры**: 
  - `binary_path` (`str`): Путь к бинарному файлу с инструкциями.
  - `result_path` (`str`): Путь для сохранения результата в формате YAML.
  - `memory_range` (`tuple`): Диапазон памяти (начало, конец).

- **Возвращает**: 
  - Нет.

- **Описание**:
  - Читает бинарный файл, выполняет команды и сохраняет результат памяти.

#### 8. `UVMInterpreter._execute_instruction(instr)`
Выполняет одну инструкцию УВМ.

- **Параметры**: 
  - `instr` (`UVMInstruction`): Инструкция для выполнения.

- **Возвращает**: 
  - Нет.

- **Исключения**:
  - `ValueError`, если opcode неизвестен.

#### 9. `main()`
Основная функция обработки командной строки для ассемблирования или интерпретации программы.

- **Параметры**: 
  - Нет параметров.

- **Описание**:
  - Читает аргументы командной строки, выбирает режим работы (`assemble` или `interpret`) и выполняет соответствующие действия.

## Описание тестовой программы
Текстовый файл содержит следующие команды:  
```
# Инициализация данных
ldc 1        # Загрузка 1
st 0         # Запись в память[0]
ldc 2        # Загрузка 2
st 1         # Запись в память[1]
ldc 3        # Загрузка 3
st 2         # Запись в память[2]
ldc 4        # Загрузка 4
st 3         # Запись в память[3]
ldc 5        # Загрузка 5
st 4         # Запись в память[4]

ldc 1        # Загрузка 1
st 5         # Запись в память[5]
ldc 0        # Загрузка 0
st 6         # Запись в память[6]
ldc 3        # Загрузка 3
st 7         # Запись в память[7]
ldc 0        # Загрузка 0
st 8         # Запись в память[8]
ldc 5        # Загрузка 5
st 9         # Запись в память[9]

# Сравнение элементов
ldr 0        # Чтение первого элемента (вектор 1, индекс 0)
eq 5         # Сравнение с элементом вектор 2 (индекс 0)
st 5         # Запись результата в вектор 2 (индекс 0)

ldr 1        # Чтение первого элемента (вектор 1, индекс 1)
eq 6         # Сравнение с элементом вектор 2 (индекс 1)
st 6         # Запись результата в вектор 2 (индекс 1)

ldr 2        # Чтение первого элемента (вектор 1, индекс 2)
eq 7         # Сравнение с элементом вектор 2 (индекс 2)
st 7         # Запись результата в вектор 2 (индекс 2)

ldr 3        # Чтение первого элемента (вектор 1, индекс 3)
eq 8         # Сравнение с элементом вектор 2 (индекс 3)
st 8         # Запись результата в вектор 2 (индекс 3)

ldr 4        # Чтение первого элемента (вектор 1, индекс 4)
eq 9         # Сравнение с элементом вектор 2 (индекс 4)
st 9         # Запись результата в вектор 2 (индекс 4)

```

Файл результата result.yaml будет содержать следующее:  
```
- mnemonic: ldc
  operand: 1
- mnemonic: st
  operand: 0
- mnemonic: ldc
  operand: 2
- mnemonic: st
  operand: 1
- mnemonic: ldc
  operand: 3
- mnemonic: st
  operand: 2
- mnemonic: ldc
  operand: 4
- mnemonic: st
  operand: 3
- mnemonic: ldc
  operand: 5
- mnemonic: st
  operand: 4
- mnemonic: ldc
  operand: 1
- mnemonic: st
  operand: 5
- mnemonic: ldc
  operand: 0
- mnemonic: st
  operand: 6
- mnemonic: ldc
  operand: 3
- mnemonic: st
  operand: 7
- mnemonic: ldc
  operand: 0
- mnemonic: st
  operand: 8
- mnemonic: ldc
  operand: 5
- mnemonic: st
  operand: 9
- mnemonic: ldr
  operand: 0
- mnemonic: eq
  operand: 5
- mnemonic: st
  operand: 5
- mnemonic: ldr
  operand: 1
- mnemonic: eq
  operand: 6
- mnemonic: st
  operand: 6
- mnemonic: ldr
  operand: 2
- mnemonic: eq
  operand: 7
- mnemonic: st
  operand: 7
- mnemonic: ldr
  operand: 3
- mnemonic: eq
  operand: 8
- mnemonic: st
  operand: 8
- mnemonic: ldr
  operand: 4
- mnemonic: eq
  operand: 9
- mnemonic: st
  operand: 9

```
