from enum import Enum, IntEnum, auto


class BaGua(IntEnum):
    """先天八卦"""

    乾 = 0
    兑 = 1
    离 = 2
    震 = 3
    巽 = 4
    坎 = 5
    艮 = 6
    坤 = 7

    def __str__(self):
        return self.name

    @classmethod
    def from_int(cls, int_value: int) -> "BaGua":
        """
        说明:
            从卦数值获取先天八卦
        """
        int_value %= 8
        return cls(int_value)

    @classmethod
    def from_binary(cls, binary: str) -> "BaGua":
        """
        说明:
            从二进制字符串获取先天八卦
        """
        return cls(int(binary, 2))

    def to_binary(self) -> str:
        """
        说明:
            获取先天八卦的二进制字符串
        """
        return format(self.value, "03b")


class Yao(IntEnum):
    """六爻"""

    初爻 = 1
    二爻 = 2
    三爻 = 3
    四爻 = 4
    五爻 = 5
    上爻 = 0

    def __str__(self):
        return self.name

    @classmethod
    def from_int(cls, int_value: int) -> "Yao":
        """
        说明:
            从整数获取动爻
        """
        int_value %= 6
        return cls(int_value)


class WuXing(Enum):
    """五行"""

    金 = auto()
    木 = auto()
    水 = auto()
    火 = auto()
    土 = auto()

    def __str__(self):
        return self.name

    @staticmethod
    def xiang_sheng(first: "WuXing", last: "WuXing") -> bool:
        """判断五行相生"""
        return (
            (first == WuXing.金 and last == WuXing.水)
            or (first == WuXing.水 and last == WuXing.木)
            or (first == WuXing.木 and last == WuXing.火)
            or (first == WuXing.火 and last == WuXing.土)
            or (first == WuXing.土 and last == WuXing.金)
        )

    @staticmethod
    def xiang_ke(first: "WuXing", last: "WuXing") -> bool:
        """判断五行相克"""
        return (
            (first == WuXing.金 and last == WuXing.木)
            or (first == WuXing.木 and last == WuXing.土)
            or (first == WuXing.土 and last == WuXing.水)
            or (first == WuXing.水 and last == WuXing.火)
            or (first == WuXing.火 and last == WuXing.金)
        )

    @classmethod
    def from_bagua(cls, gua: BaGua) -> "WuXing":
        """从八卦获取五行"""
        match gua:
            case BaGua.乾 | BaGua.兑:
                return WuXing.金
            case BaGua.震 | BaGua.巽:
                return WuXing.木
            case BaGua.坎:
                return WuXing.水
            case BaGua.离:
                return WuXing.火
            case BaGua.艮 | BaGua.坤:
                return WuXing.土


class GuaJie(Enum):
    """卦解"""

    体生用 = auto()
    用生体 = auto()
    体克用 = auto()
    用克体 = auto()
    体用比和 = auto()

    def __str__(self):
        return self.name

    @classmethod
    def get_guajie(cls, up_quadrant: BaGua, down_quadrant: BaGua) -> "GuaJie":
        """
        说明:
            从卦象获取卦解
        """
        up_wuxing = WuXing.from_bagua(up_quadrant)
        down_wuxing = WuXing.from_bagua(down_quadrant)
        if WuXing.xiang_sheng(up_wuxing, down_wuxing):
            return cls.体生用
        if WuXing.xiang_sheng(down_wuxing, up_wuxing):
            return cls.用生体
        if WuXing.xiang_ke(up_wuxing, down_wuxing):
            return cls.体克用
        if WuXing.xiang_ke(down_wuxing, up_wuxing):
            return cls.用克体
        return cls.体用比和

    def get_qiumou(self) -> str:
        """
        说明:
            通过卦解求谋
        """
        match self:
            case GuaJie.体生用:
                return "求事可成，但需时间"
            case GuaJie.用生体:
                return "求事不成，事反有害"
            case GuaJie.体克用:
                return "所求之事，不谋而成"
            case GuaJie.用克体:
                return "所求之事，事倍功半"
            case GuaJie.体用比和:
                return "称心如意，势在必得"


class Quadrant:
    """卦象"""

    up_quadrant: BaGua
    """上卦"""
    down_quadrant: BaGua
    """下卦"""
    dong_yao: Yao = 0
    """动爻"""

    def __init__(self, up_quadrant: BaGua, down_quadrant: BaGua):
        self.up_quadrant = up_quadrant
        self.down_quadrant = down_quadrant

    @classmethod
    def start(cls, up_value: int, down_value: int) -> "Quadrant":
        """
        说明:
            从上卦数和下卦数开始起卦
        """
        up_quadrant = BaGua.from_int(up_value)
        down_quadrant = BaGua.from_int(down_value)
        new = Quadrant(up_quadrant, down_quadrant)
        new.dong_yao = Yao.from_int(up_value + down_value)
        return new

    @classmethod
    def from_binary(cls, binary: str) -> "Quadrant":
        """
        说明:
            从二进制字符串获取卦象
        """
        up_binary = binary[:3]
        down_binary = binary[3:]
        return cls(
            up_quadrant=BaGua.from_binary(up_binary),
            down_quadrant=BaGua.from_binary(down_binary),
        )

    def to_binary(self) -> str:
        """
        说明:
            获取卦象的二进制字符串
        """
        return self.up_quadrant.to_binary() + self.down_quadrant.to_binary()

    def get_tigua(self) -> BaGua:
        """
        说明:
            获取本卦的“体卦”
        """
        match self.dong_yao:
            case Yao.初爻 | Yao.二爻 | Yao.三爻:
                return self.up_quadrant
            case _:
                return self.down_quadrant

    def get_yonggua(self) -> BaGua:
        """
        说明:
            获取本卦的“用卦”
        """
        match self.dong_yao:
            case Yao.初爻 | Yao.二爻 | Yao.三爻:
                return self.down_quadrant
            case _:
                return self.up_quadrant

    def get_hugua(self) -> "Quadrant":
        """
        说明:
            获取此卦象的“互卦”
        """
        binary = list(self.to_binary())
        up = "".join(binary[1:4])
        down = "".join(binary[2:5])
        return Quadrant.from_binary(up + down)

    def get_biangua(self) -> "Quadrant":
        """
        说明:
            获取此卦象的“变卦”
        """
        binary = list(self.to_binary())
        binary[-self.dong_yao - 1] = "0" if binary[-self.dong_yao - 1] else "1"
        return self.from_binary("".join(binary))

    def get_exception(self) -> GuaJie:
        """
        说明:
            获取此卦的“卦解”
        """
        return GuaJie.get_guajie(self.up_quadrant, self.down_quadrant)
