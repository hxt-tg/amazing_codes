import random

DIGITS_MAX = 6
EXTERNAL_SPACES = 2

OP_STR = {
    '+': '+',
    '-': '-',
    '*': '×',
    '/': '÷'
}
OP_FUNC = {
    '+': lambda x, y: str(x.__add__(y)),
    '-': lambda x, y: str(x.__sub__(y)),
    '*': lambda x, y: str(x.__mul__(y)),
    '/': lambda x, y: '{}...{}'.format(x // y, x % y)
}


def _chk_min_max(x):
    if x < 1 or x > DIGITS_MAX:
        raise ValueError('digits should be in [1, {}].'.format(DIGITS_MAX))


def _try_max_iter(func, condition, max_iter=20, **kwargs):
    cnt = 0
    while True:
        result = func(**kwargs)
        if condition(*result) if isinstance(result, tuple) or isinstance(result, list) else condition(result):
            return result
        cnt += 1
        if cnt == max_iter: raise RuntimeError('Try too much times.')


def _gen_vertical_expr(n1, op, n2):
    sn1 = str(n1).replace('', ' ').strip()
    sn2 = str(n2).replace('', ' ').strip()
    if op in '+-*':
        max_len = max(len(sn1), len(sn2))
        expr = ' ' * (EXTERNAL_SPACES + 2 + max_len - len(sn1)) + sn1 + '\n'
        expr += ' {}{}{}'.format(OP_STR[op], ' ' * (EXTERNAL_SPACES + max_len - len(sn2)), sn2) + '\n'
        expr += '-' * (4 + EXTERNAL_SPACES + max_len) + '\n'
        expr += '\n' * len(str(n2)) if op == '*' else ''
    else:
        sn2 = str(n2)
        len_ans = len(str(n1 // n2))
        expr = ' ' * (len(sn2) + 3) + '_' * (len(sn1) + 2) + '\n'
        expr += ' {} ⌡ {}'.format(sn2, sn1) + '\n' * (2 * len_ans)
    return expr


class RangeRNG:
    def __init__(self, min_val, max_val, multiple=1, allow_zero_end=True):
        self.multiple = multiple
        self.min_val = min_val // multiple
        self.max_val = max_val // multiple
        self._zero_end = allow_zero_end

    def get(self):
        return _try_max_iter((lambda: random.randint(self.min_val, self.max_val) * self.multiple),
                             (lambda x: (self._zero_end or x % 10 != 0)))


class DigitsRangeRNG(RangeRNG):
    def __init__(self, min_digits, max_digits, multiple=1, allow_zero_end=True):
        _chk_min_max(min_digits)
        _chk_min_max(max_digits)
        if min_digits > max_digits:
            raise ValueError('min_digits should be less than or equals to max_digits.')
        RangeRNG.__init__(self, (10 ** (min_digits - 1)), (10 ** max_digits - 1), multiple, allow_zero_end)
        self.min_digits = min_digits
        self.max_digits = max_digits


class IntegerCalculateGenerator:
    _expr = {
        '+': dict(),
        '-': dict(),
        '*': dict(),
        '/': dict()
    }
    next_idx = 1

    def __init__(self, operator, num1_rng: RangeRNG, num2_rng: RangeRNG, no_repeat=True):
        if operator not in '+-*/':
            raise ValueError('operator should be in "+-*/".')
        self._op = operator
        self._no_repeat = no_repeat
        self.rng1 = num1_rng
        self.rng2 = num2_rng

    def gen(self, n1=None, n2=None, number_format: object = '[{:d}] ', vertical=False):
        if n1 is None or n2 is None:
            n1, n2 = _try_max_iter(lambda: (self.rng1.get(), self.rng2.get()),
                                   (lambda _n1, _n2: not self._no_repeat or (_n1, _n2) not in self._expr[self._op]))
        num = number_format.format(IntegerCalculateGenerator.next_idx) if isinstance(number_format, str) else ''
        IntegerCalculateGenerator.next_idx += 1
        ans = OP_FUNC[self._op](n1, n2)
        self._expr[self._op][(n1, n2)] = ans
        if vertical:
            expr = _gen_vertical_expr(n1, self._op, n2)
            if num != '':
                expr = num + '\n' + expr
        else:
            expr = '{}{} {} {} \n ='.format(num, n1, OP_STR[self._op], n2)
        ans = '{}{}'.format(num, ans)
        return expr, ans

    @property
    def idx(self):
        return IntegerCalculateGenerator.next_idx - 1


class AddGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RangeRNG, num2_rng: RangeRNG, **kwargs):
        IntegerCalculateGenerator.__init__(self, '+', num1_rng, num2_rng, **kwargs)


class MinusGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RangeRNG, num2_rng: RangeRNG, **kwargs):
        IntegerCalculateGenerator.__init__(self, '-', num1_rng, num2_rng, **kwargs)

    def gen(self, positive=True, **kwargs):
        n1 = self.rng1.get()
        n2 = self.rng2.get()
        if positive and n1 < n2: n1, n2 = n2, n1
        return IntegerCalculateGenerator.gen(self, n1, n2, **kwargs)


class MultiplyGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RangeRNG, num2_rng: RangeRNG, **kwargs):
        IntegerCalculateGenerator.__init__(self, '*', num1_rng, num2_rng, **kwargs)


class DivideGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RangeRNG, num2_rng: RangeRNG, **kwargs):
        IntegerCalculateGenerator.__init__(self, '/', num1_rng, num2_rng, **kwargs)

    def gen(self, larger_than_2=True, with_division=True, **kwargs):
        rng1, rng2 = self.rng1, self.rng2
        n2 = rng2.get()
        if not with_division:
            rng1 = RangeRNG(rng1.min_val, rng1.max_val, multiple=n2)
        n1 = rng1.get()

        if larger_than_2 and n1 // n2 < 2:
            n1 = _try_max_iter(lambda: rng1.get(),
                               (lambda _n1: _n1 // n2 > 1))

        return IntegerCalculateGenerator.gen(self, n1, n2, **kwargs)


def one_group(idx):
    add_short = AddGenerator(DigitsRangeRNG(2, 2), RangeRNG(8, 30))
    add_long = AddGenerator(DigitsRangeRNG(3, 3), RangeRNG(50, 200))
    sub_short = MinusGenerator(DigitsRangeRNG(2, 2), DigitsRangeRNG(1, 2))
    sub_long = MinusGenerator(DigitsRangeRNG(3, 3), RangeRNG(50, 200))
    mul_random = MultiplyGenerator(DigitsRangeRNG(2, 2), RangeRNG(2, 9))
    mul_multiple = MultiplyGenerator(DigitsRangeRNG(2, 3, 5), RangeRNG(2, 9, 2))
    div_short = DivideGenerator(DigitsRangeRNG(2, 2), RangeRNG(2, 10))
    div_long = DivideGenerator(DigitsRangeRNG(3, 4), RangeRNG(2, 10))

    add_v = AddGenerator(DigitsRangeRNG(4, 4), DigitsRangeRNG(4, 4))
    sub_v = MinusGenerator(RangeRNG(1000, 11000), DigitsRangeRNG(4, 4))
    mul_random_v = MultiplyGenerator(RangeRNG(400, 1100), RangeRNG(11, 110, allow_zero_end=False))
    mul_multiple_v = MultiplyGenerator(RangeRNG(400, 1100, 5), RangeRNG(11, 110, 2, False))
    div_with_division_v = DivideGenerator(DigitsRangeRNG(4, 4), RangeRNG(11, 200))
    div_without_division_v = DivideGenerator(DigitsRangeRNG(4, 4), RangeRNG(11, 200, 5))

    def _write_to_file(generator, amount=1, **kwargs):
        for _ in range(amount):
            t, a = generator.gen(**kwargs)
            fq.write(t + '\n')
            fa.write(a + '\n')
            print(t)

    IntegerCalculateGenerator.next_idx = 1
    with open('ans.txt', 'a') as fa:
        with open('quiz.txt', 'a', encoding='utf8') as fq:
            if idx > 1: fq.write('<BREAK>')
            fq.write('第{:02d}组\n口算部分：\n'.format(idx))
            if idx > 1: fa.write('<BREAK>')
            fa.write('第{:02d}组\n'.format(idx))
            # Normal
            _write_to_file(add_short, amount=4)
            _write_to_file(add_long, amount=2)
            _write_to_file(sub_short, amount=4)
            _write_to_file(sub_long, amount=2)
            _write_to_file(mul_random, amount=6)
            _write_to_file(mul_multiple, amount=3)
            _write_to_file(div_short, amount=6)
            _write_to_file(div_long, amount=3, with_division=False)

            # Vertical
            fq.write('\n竖式部分：\n'.format(idx))
            _write_to_file(add_v, amount=4, vertical=True)
            _write_to_file(sub_v, amount=4, vertical=True)
            _write_to_file(mul_random_v, amount=4, vertical=True)
            _write_to_file(mul_multiple_v, amount=2, vertical=True)
            fq.write('<BREAK>')
            _write_to_file(div_with_division_v, amount=4, vertical=True, with_division=False)
            _write_to_file(div_without_division_v, amount=2, vertical=True)


if __name__ == '__main__':
    with open('ans.txt', 'w') as _fa:
        with open('quiz.txt', 'w', encoding='utf8') as _fq:
            _fq.write('')
            _fa.write('')
    for i in range(1, 21):
        one_group(i)
    # g = DivideGenerator(DigitsRangeRNG(3, 3), DigitsRangeRNG(2, 2))
    # for _ in range(5):
    #     print(g.gen(with_division=False, vertical=True)[0])
