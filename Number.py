import random

class Binary16:
    def __init__(self, number):
        if isinstance(number, str):
            self.number = self.str_to_list(number)
        elif isinstance(number, int):
            self.number = self.int_to_list(number)
        elif isinstance(number, list):
            self.number = number
            if len(self.number) < 16:
                self.number = [False] * (16 - len(self.number)) + self.number
        else:
            raise ValueError("Неверный тип данных.")

    def __lshift__(self, places):
        copy = self.number.copy()
        binary16 = Binary16(copy)
        for _ in range(places):
            binary16.number = binary16.number[1:] + [False]
        return binary16

    def __rshift__(self, places):
        copy = self.number.copy()
        binary16 = Binary16(copy)
        for _ in range(places):
            binary16.number = [False] + binary16.number[:-1]
        return binary16

    def __add__(self, other):
        result = []
        carry = False

        copy = other.number.copy()
        binary16 = Binary16(copy)

        for bit_a, bit_b in zip(reversed(self.number), reversed(binary16.number)):
            sum_bit = bit_a ^ bit_b ^ carry
            carry = (bit_a and bit_b) or (bit_a and carry) or (bit_b and carry)
            result.append(sum_bit)

        return Binary16(list(reversed(result)))

    def __getitem__(self, index):
        return self.number[index]

    def __str__(self):
        bs = ''.join('1' if bit else '0' for bit in self.number)
        return f"{bs} ({int(bs, 2)})"

    def __eq__(self, other):
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, Binary16):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(tuple(self.number))
    
    @staticmethod
    def generate_random_number(m):
        number_list = [random.choice([False, True]) for _ in range(m)]
        return Binary16(number_list)

    @staticmethod
    def str_to_list(number):
        if len(number) != 16:
            raise ValueError("Введённые числа должны иметь 16 цифр.")
        if any(bit not in '01' for bit in number):
            raise ValueError("Введённые числа должны быть двоичными.")
        return [bit == '1' for bit in number]

    @staticmethod
    def int_to_list(value):
        x = bin(value)[2:]
        if len(x) > 16:
            substr = x[-16:]
            return Binary16.str_to_list(substr)
        str_value = x.rjust(16, '0')
        return Binary16.str_to_list(str_value)

    ZERO = None

class Binary8:
    def __init__(self, number):
        if isinstance(number, str):
            self.number = self.str_to_list(number)
        elif isinstance(number, int):
            self.number = self.int_to_list(number)
        elif isinstance(number, list):
            self.number = number
        else:
            raise ValueError("Неверный тип данных.")

    def __lshift__(self, places):
        copy = self.number.copy()
        binary16 = Binary16(copy)
        for _ in range(places):
            binary16.number = binary16.number[1:] + [False]
        return binary16

    def __rshift__(self, places):
        copy = self.number.copy()
        binary8 = Binary8(copy)
        for _ in range(places):
            binary8.number = [False] + binary8.number[:-1]
        return binary8

    def __add__(self, other):
            result = []
            carry = 0
            for bit_a, bit_b in zip(reversed(self.number), reversed(other.number)):
                sum_bit = bit_a ^ bit_b ^ carry
                carry = (bit_a and bit_b) or (bit_a and carry) or (bit_b and carry)
                result.append(sum_bit)

            if carry:
                result.append(carry)

            result = result[::-1]
            if len(result) > 8:
                return Binary16(int(''.join(map(str, result)), 2))
            else:
                return Binary8(int(''.join(map(str, result)), 2))

    def __mul__(self, other):
        result = Binary16.ZERO
        for i in range(8):
            if other[7 - i]:
                result += self << i
        return result

    def __getitem__(self, index):
        return self.number[index]

    def __str__(self):
        bs = ''.join('1' if bit else '0' for bit in self.number)
        return f"{bs} ({int(bs, 2)})"

    def __eq__(self, other):
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, Binary8):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(tuple(self.number))
    
    @staticmethod
    def generate_random_number(m):
        number_list = [random.choice([False, True]) for _ in range(m)]
        return Binary8(number_list)

    @staticmethod
    def str_to_list(number):
        if len(number) != 8:
            raise ValueError("Введённые числа должны иметь 8 цифр.")
        if any(bit not in '01' for bit in number):
            raise ValueError("Введённые числа должны быть двоичными.")
        return [bit == '1' for bit in number]

    @staticmethod
    def int_to_list(value):
        x = bin(value)[2:]
        if len(x) > 8:
            substr = x[-8:]
            return Binary8.str_to_list(substr)
        str_value = x.rjust(8, '0')
        return Binary8.str_to_list(str_value)

    ZERO = None