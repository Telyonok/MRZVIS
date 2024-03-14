from collections import deque
from Number import Binary16

class Pipeline:
    def __init__(self, *steps):
        self.tickCount = 0
        self.steps = list(steps)

    def run(self, *input):
        input_list = list(input)
        original_size = len(input_list)
        output = deque()

        while len(output) != original_size:
            self.tick(input_list, output)

        return list(output)

    def pre_tick(self):
        pass

    def post_tick(self):
        pass

    def tick(self, input_list, output):
        self.tickCount += 1
        for i in range(len(self.steps) - 1, 0, -1):
            self.steps[i].content = self.steps[i - 1].content
            self.steps[i - 1].content = None

        if input_list:
            self.steps[0].content = input_list.pop()

        self.pre_tick()
        for step in self.steps:
            step.do_work()
        self.post_tick()

        if self.steps[-1].content is not None:
            output.appendleft(self.steps[-1].content)
            self.steps[-1].content = None


class Step:
    def __init__(self):
        self.content = None

    def do_work(self):
        if self.content is not None:
            self.content = self.do_specific_work(self.content)

    def do_specific_work(self, input):
        raise NotImplementedError


class MultiplicationSet:
    def __init__(self, multiplicand, factor, partial_multiplication, partial_sum):
        self.multiplicand = multiplicand
        self.factor = factor
        self.partial_multiplication = partial_multiplication
        self.partial_sum = partial_sum


class MultiplicationStep(Step):
    def do_specific_work(self, input):
        new_multiplicand = input.multiplicand >> 1
        new_partial_multiplication = new_multiplicand if input.factor[0] else Binary16.ZERO
        new_partial_sum = input.partial_sum + new_partial_multiplication
        new_factor = input.factor << 1
        return MultiplicationSet(new_multiplicand, new_factor, new_partial_multiplication, new_partial_sum)