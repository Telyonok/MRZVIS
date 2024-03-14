#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#// Лабораторная работа №1 по дисциплине Модели решения задач в интеллектуальных системах
#// Выполнена студентами группы 121701 БГУИР Чвилёвом Ильёй Александровичем, Стронгиным Андреем Вадимовичем
#// Программа выполняет вычисление попарного произведения компонентов двух векторов чисел.
#// 03.03.2024

import datetime
import sys
from Pipeline import Pipeline
from Pipeline import MultiplicationSet
from Pipeline import MultiplicationStep
from Number import Binary16
from Number import Binary8

class InputData:
    def __init__(self):
        pass

    def random_init(self):
        self.m = self.user_input_m()
        self.initial_number_list1 = [Binary8.generate_random_number(8) for _ in range(self.m)]
        self.initial_number_list2 = [Binary8.generate_random_number(8) for _ in range(self.m)]
        self.number_list1 = [number.lshift_to_16(8) for number in self.initial_number_list1]
        self.number_list2 = self.initial_number_list2

    def file_init(self, filename):
        lines = read_file(filename)
        if len(lines) != 3:
            raise Exception("Ошибка: неверный формат файла.")
        
        m_input = lines[0]
        if not m_input.isdigit():
            raise Exception("Ошибка: m должно быть положительным целым числом.")
        m = int(m_input)
        if m <= 0:
            raise Exception("Ошибка: m должно быть положительным числом.")
        self.m = m
        self.number_list1 = validate_number_list([number << 8 for number in lines[1].replace(",", " ").split()], m)
        self.number_list2 = validate_number_list([number for number in lines[2].replace(",", " ").split()], m)

    def user_init(self):
        self.m = self.user_input_m()
        self.initial_number_list1 = self.user_input_number_list(f"Введите первый список (состоит из {self.m} двоичных чисел 8-го разряда). Вводите числа через пробелы или запятые:", self.m)
        self.initial_number_list2 = self.user_input_number_list(f"Введите первый список (состоит из {self.m} двоичных чисел 8-го разряда). Вводите числа через пробелы или запятые:", self.m)
        self.number_list1 = [number.lshift_to_16(8) for number in self.initial_number_list1]
        self.number_list2 = self.initial_number_list2
    
    @staticmethod
    def user_input_m():
        print("Введите m, количество чисел в списках:")
        while True:
            m_input = input()
            if not m_input.isdigit():
                print("Ошибка: m должно быть положительным целым числом.")
                continue
            m = int(m_input)
            if m <= 0:
                print("Ошибка: m должно быть положительным числом.")
                continue
            return m   
    
    @staticmethod
    def user_input_number_list(inquery_text, m):        
        while True:
            print(inquery_text)
            inputed_numbers = input().replace(",", " ").split()
            number_list = validate_number_list(inputed_numbers, m)
            if not number_list:
                continue
            return number_list
    
@staticmethod
def validate_number_list(inputed_numbers, m):
    if len(inputed_numbers) != m:
        print(f"Ошибка: количество чисел должно быть равно {m}.")
        return []

    number_list = []
    for number in inputed_numbers:
        if len(number) != 8 or not is_binary_number(number):
            print(f"Ошибка: число '{number}' должно быть двоичным числом длиной 8 разрядов.")
            return []
        number_list.append(Binary8(number))

    return number_list 

@staticmethod
def is_binary_number(number):
    try:
        int(number, 2)
        return True
    except ValueError:
        return False

@staticmethod
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    except IOError:
        raise Exception(f"Ошибка при чтении файла: {filename}")

@staticmethod
def main():
    pipeline_steps = 8
    try:
        data = InputData()
        if len(sys.argv) >= 2:
            if sys.argv[1] == '-f' and len(sys.argv) > 2:
                data.file_init(sys.argv[2])
            elif sys.argv[1] == '-r':
                data.random_init()
        else:
            data.user_init()

        print("Список множимых чисел:")
        for number in data.initial_number_list1:
            print(number)

        print("Список множителей:")
        for number in data.initial_number_list2:
            print(number)

        pipeline = Pipeline(*[MultiplicationStep() for _ in range(pipeline_steps)])

        def post_tick():
            print("Шаг", pipeline.tickCount)
            for i, step in enumerate(pipeline.steps):
                content = step.content
                print(f"{i}. Множимое: {content.multiplicand if content else ''}   Множитель: {content.factor if content else ''}   Частичное произведение: {content.partial_multiplication if content else ''}   Частичная сумма: {content.partial_sum if content else ''}")
            
            input("Нажмите Enter для перехода к следующему шагу...")

        pipeline.post_tick = post_tick

        multiplication_triples = []
        for i in range(data.m):
            multiplicand = data.number_list1[i]
            factor = data.number_list2[i]
            partial_sum = Binary16.ZERO
            partial_multiplication = Binary16.ZERO
            multiplication_triples.append(MultiplicationSet(multiplicand, factor, partial_multiplication, partial_sum))
        dt = datetime.datetime.now()
        res = pipeline.run(*multiplication_triples)
        print(datetime.datetime.now() - dt)
        print('Результаты:')
        for item in res:
            print(item.partial_sum)

    except Exception as e:
        print(f"Ошибка: {e} ({type(e).__name__})")

if __name__ == '__main__':
    Binary8.ZERO = Binary8(0)
    Binary16.ZERO = Binary16(0)
    main()