class Register:

    data: dict = {}

    @classmethod
    def register(cls, retcode):
        def registercls(re_cls):
            cls.data[retcode] = re_cls
        return registercls

    @classmethod
    def get_data(cls, retcode):
        re_cls = cls.data.get(retcode)
        return re_cls()


@Register.register(retcode=100)
class Test:
    retcode: int = 100

    def test(self):
        print("i am down")


a = Register.get_data(100)
a.test()
