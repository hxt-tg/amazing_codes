class A1:
    def bar(self, *args, **kwargs):
        print('A1')


class A2:
    def bar(self, *args, **kwargs):
        print('A2')


class B1(A1):
    pass


class B2(A2):
    pass


class C(B1, B2):
    def bar(self, data):
        super(C, self).bar(data)


class MySuper:
    def __init__(self, type1: type, type2):
        self.type1 = type1
        self.type2 = type2
        self.type2_isclass = isinstance(type2, type)

    def _search_mro(self, type1, type2, item):
        if not super().__getattribute__('type2_isclass'): type2 = type2.__class__

    def __getattribute__(self, item):
        type1 = super().__getattribute__('type1')
        type2 = super().__getattribute__('type2')
        type2_isclass = super().__getattribute__('type2_isclass')
        class2 = type2 if type2_isclass else type2.__class__

        mro = class2.__mro__
        idx = 0
        while idx < len(mro) and mro[idx] is not type1:
            idx += 1
        inherit_class = None
        for class_ in mro[idx:]:
            if item in class_.__dict__:
                inherit_class = class_
                break
        else:
            raise RuntimeError(f'Cannot find "{item}".')

        if type2_isclass:
            return inherit_class.__dict__[item]
        else:
            def wrapper(*args, **kwargs):
                return inherit_class.__dict__[item](type2, *args, **kwargs)

            return wrapper


# C().bar()
MySuper(B2, B2).bar(C(), 1)
MySuper(B1, C()).bar(2)

# c = C()
# c.bar()
# C.bar(c)
