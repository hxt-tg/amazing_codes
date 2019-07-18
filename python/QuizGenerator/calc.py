import random

DIGITS_MAX = 6
REPEAT_TRY = 10
EXTERNAL_SPACES = 2

OP_STR = {
    '+': '＋',
    '-': '－',
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


def _gen_vertical_expr(n1, op, n2):
    sn1 = str(n1).replace('', ' ').strip()
    sn2 = str(n2).replace('', ' ').strip()
    if op in '+-*':
        max_len = max(len(sn1), len(sn2))
        expr = ' ' * (EXTERNAL_SPACES + 3 + max_len - len(sn1)) + sn1 + '\n'
        expr += ' {}{}{}'.format(OP_STR[op], ' ' * (EXTERNAL_SPACES + max_len - len(sn2)), sn2) + '\n'
        expr += '-' * (4 + EXTERNAL_SPACES + max_len) + ('\n' * (len(str(n2)) + 1))
    else:
        sn2 = str(n2)
        len_ans = len(str(n1 // n2))
        expr = ' ' * (len(sn2) + 4) + '_' * (len(sn1) + 2) + '\n'
        expr += ' {} √ {}'.format(sn2, sn1) + '\n' * (2 * len_ans)
    return expr


class RNG:
    def __init__(self):
        pass

    def get(self):
        raise TypeError("RNG get() is not callable.")


class RangeRNG(RNG):
    def __init__(self, min_digits, max_digits, multiple=1):
        RNG.__init__(self)
        _chk_min_max(min_digits)
        _chk_min_max(max_digits)
        if min_digits > max_digits:
            raise ValueError('min_digits should be less than or equals to max_digits.')
        self._multiple = multiple
        self._min = (10 ** (min_digits - 1)) // multiple
        self._max = (10 ** max_digits - 1) // multiple

    def get(self):
        return random.randint(self._min, self._max) * self._multiple


class IntegerCalculateGenerator:
    _all_expr = {
        '+': dict(),
        '-': dict(),
        '*': dict(),
        '/': dict()
    }
    n_expr = 1

    def __init__(self, operator, num1_rng: RNG, num2_rng: RNG, no_repeat=False):
        if operator not in '+-*/':
            raise ValueError('operator should be in "+-*/".')
        self._op = operator
        self._no_repeat = no_repeat
        self.rng1 = num1_rng
        self.rng2 = num2_rng

    def gen(self, n1=None, n2=None, number_format: object = '[{}] ', vertical=False):
        cnt = 0
        if n1 is None or n2 is None:
            while True:
                n1 = self.rng1.get()
                n2 = self.rng2.get()
                if not self._no_repeat: break
                cnt += 1
                if (n1, n2) not in self._all_expr[self._op]:
                    break
                if cnt == REPEAT_TRY: return None
        num = number_format.format(self.n_expr) if isinstance(number_format, str) else ''
        self.n_expr += 1
        ans = OP_FUNC[self._op](n1, n2)
        self._all_expr[self._op][(n1, n2)] = ans
        if vertical:
            expr = _gen_vertical_expr(n1, self._op, n2)
            if num != '':
                expr = num + '\n' + expr
        else:
            expr = '{}{} {} {} ='.format(num, n1, OP_STR[self._op], n2)
        ans = '{}{}'.format(num, ans)
        return expr, ans

    @property
    def idx(self):
        return self.n_expr - 1


class AddGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RNG, num2_rng: RNG, no_repeat=False):
        IntegerCalculateGenerator.__init__(self, '+', num1_rng, num2_rng, no_repeat)


class MinusGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RNG, num2_rng: RNG, no_repeat=False, no_minus=True):
        IntegerCalculateGenerator.__init__(self, '-', num1_rng, num2_rng, no_repeat)
        self._no_minus = no_minus

    def gen(self, **kwargs):
        n1 = self.rng1.get()
        n2 = self.rng2.get()
        if self._no_minus and n1 < n2: n1, n2 = n2, n1
        return IntegerCalculateGenerator.gen(self, n1, n2, **kwargs)


class MultiplyGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RNG, num2_rng: RNG, no_repeat=False):
        IntegerCalculateGenerator.__init__(self, '*', num1_rng, num2_rng, no_repeat)


class DivideGenerator(IntegerCalculateGenerator):
    def __init__(self, num1_rng: RNG, num2_rng: RNG, no_repeat=False, larger_than_1=True):
        IntegerCalculateGenerator.__init__(self, '/', num1_rng, num2_rng, no_repeat)
        self._larger = larger_than_1

    def gen(self, number_format: object = '{}', **kwargs):
        n1 = self.rng1.get()
        n2 = self.rng2.get()
        if self._larger and n1 < n2: n1, n2 = n2, n1
        return IntegerCalculateGenerator.gen(self, n1, n2, **kwargs)


def gen_one_day():
    add_h = AddGenerator(RangeRNG(2, 3), RangeRNG(2, 2))
    add_v = AddGenerator(RangeRNG(4, 4), RangeRNG(2, 2, 2))
    sub_h = MinusGenerator(RangeRNG(4, 4), RangeRNG(2, 2, 2))
    sub_v = MinusGenerator(RangeRNG(4, 4, 5), RangeRNG(2, 2, 2))
    mul_h = MultiplyGenerator(RangeRNG(4, 4, 5), RangeRNG(2, 2, 2))
    mul_v = MultiplyGenerator(RangeRNG(4, 4, 5), RangeRNG(2, 2, 2))
    div_h = DivideGenerator(RangeRNG(4, 4, 5), RangeRNG(2, 2, 2))
    div_v = DivideGenerator(RangeRNG(4, 4, 5), RangeRNG(2, 2, 2))
    print(add_h.gen())


if __name__ == '__main__':
    gen_one_day()

