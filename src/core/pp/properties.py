from typing import Optional, Union
from yaml import YAMLObject

from core.comm import satisfy, inherent, EnumError, NotMatched


class PropNotMatched(NotMatched):
    pass


class ParaNotPure(PropNotMatched):
    pass


class ParaEmpty(ParaNotPure):
    pass


class ParaComplex(ParaNotPure):
    pass


class UnitError(EnumError):
    pass


class Length(YAMLObject):
    yaml_tag = '!Length'

    value: float
    unit: str

    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit

    def __eq__(self, other):
        if other is None:
            return False
        return self.unit == other.unit and 0.01 > self.value - other.value > -0.01

    def __str__(self):
        return str(self.value) + ' ' + self.unit

    def __mul__(self, other: float):
        return Length(self.value * other, self.unit)

    def __sub__(self, other):
        if self.unit != other.unit:
            pass
        return Length(self.value - other.value, self.unit)


Size = Union[Length, float]


class TextPropNotMatched(PropNotMatched):
    pass


class NameNotMatched(TextPropNotMatched):
    pass


class NameAsiaNotMatched(TextPropNotMatched):
    pass


class SizeNotMatched(TextPropNotMatched):
    pass


class SizeAsiaNotMatched(TextPropNotMatched):
    pass


class WeightNotMatched(TextPropNotMatched):
    pass


class WeightAsiaNotMatched(TextPropNotMatched):
    pass


class Font(YAMLObject):
    yaml_tag = '!Font'

    name: Optional[str]

    name_asia: Optional[str]

    size: Optional[Size]

    size_asia: Optional[Size]

    weight: Optional[str]

    weight_asia: Optional[str]

    def __init__(self,
                 name: Optional[str] = None,
                 name_asia: Optional[str] = None,
                 size: Optional[Size] = None,
                 size_asia: Optional[Size] = None,
                 weight: Optional[str] = None,
                 weight_asia: Optional[str] = None,
                 ):
        self.name = name
        self.name_asia = name_asia
        self.size = size
        self.size_asia = size_asia
        self.weight = weight
        self.weight_asia = weight_asia

    def __eq__(self, other):
        return self.name == other.name \
               and self.name_asia == other.name_asia \
               and self.size == other.size \
               and self.size_asia == other.size_asia \
               and self.weight == other.weight \
               and self.weight_asia == other.weight_asia

    def __satisfy__(self, other):

        if not satisfy(self.name, other.name):
            e = NameNotMatched()
            e.val, e.req = self.name, other.name
            raise e
        if not satisfy(self.name_asia, other.name_asia):
            e = NameAsiaNotMatched()
            e.val, e.req = self.name_asia, other.name_asia
            raise e
        if not satisfy(self.size, other.size):
            e = SizeNotMatched()
            e.val, e.req = self.size, other.size
            raise e
        if not satisfy(self.size_asia, other.size_asia):
            e = SizeAsiaNotMatched()
            e.val, e.req = self.size_asia, other.size_asia
            raise e
        if not satisfy(self.weight, other.weight):
            e = WeightNotMatched()
            e.val, e.req = self.weight, other.weight
            raise e
        if not satisfy(self.weight_asia, other.weight_asia):
            e = WeightAsiaNotMatched()
            e.val, e.req = self.weight_asia, other.weight_asia
            raise e
        return True

    def __inherent__(self,
                     other):
        ans = self
        if other is not None:
            ans.name = inherent(ans.name, other.name)
            ans.name_asia = inherent(ans.name_asia, other.name_asia)
            ans.size = inherent(ans.size, other.size)
            ans.size_asia = inherent(ans.size_asia, other.size_asia)
            ans.weight = inherent(ans.weight, other.weight)
            ans.weight_asia = inherent(ans.weight_asia, other.weight_asia)
        return ans


class LetterSpacingNotMatched(TextPropNotMatched):
    pass


class TextProp(YAMLObject):
    yaml_tag = '!TextProperty'

    font: Font

    letter_spacing: Optional[Size]

    def __init__(self,
                 font: Font = Font(),
                 letter_spacing: Optional[Size] = None):
        self.font = font
        self.letter_spacing = letter_spacing

    def __eq__(self, other):
        return self.font == other.font \
               and self.letter_spacing == other.letter_spacing

    def __satisfy__(self, other):
        satisfy(self.font, other.font)

        if not satisfy(self.letter_spacing, other.letter_spacing):
            e = LetterSpacingNotMatched()
            e.val, e.req = self.letter_spacing, other.letter_spacing
            raise e

    def __inherent__(self, other):
        ans = self
        if other is not None:
            ans.font = inherent(ans.font, other.font)
            ans.letter_spacing = inherent(ans.letter_spacing, other.letter_spacing)
        return ans


class ParaPropNotMatched(PropNotMatched):
    pass


class AlignNotMatched(ParaPropNotMatched):
    pass


class AlignError(EnumError):
    pass


class LineHeightNotMatched(ParaPropNotMatched):
    pass


class ParaProp(YAMLObject):
    yaml_tag = '!ParagraphProperty'

    align: Optional[str]

    line_height: Optional[Size]

    def __init__(self,
                 align: Optional[str] = None,
                 line_height: Optional[Size] = None,
                 ):
        self.align = align
        self.line_height = line_height

    def __satisfy__(self, other):
        if not satisfy(self.align, other.align):
            e = AlignNotMatched()
            e.val, e.req = self.align, other.align
            raise e
        if not satisfy(self.line_height, other.line_height):
            e = LineHeightNotMatched()
            e.val, e.req = self.line_height, other.line_height
            raise e

    def __inherent__(self, other):
        ans = self
        if other is not None:
            ans.align = inherent(ans.align, other.align)
            ans.line_height = inherent(ans.line_height, other.line_height)
        return ans


class PageLayoutNotMatched(PropNotMatched):
    pass


class MarginBottomNotMatched(PageLayoutNotMatched):
    pass


class MarginLeftNotMatched(PageLayoutNotMatched):
    pass


class MarginRightNotMatched(PageLayoutNotMatched):
    pass


class MarginTopNotMatched(PageLayoutNotMatched):
    pass


class PageHeightLeftNotMatched(PageLayoutNotMatched):
    pass


class PageWidthLeftNotMatched(PageLayoutNotMatched):
    pass


class PageProp(YAMLObject):
    yaml_tag = '!PageProperty'

    margin_bottom: Optional[Size]

    margin_left: Optional[Size]

    margin_right: Optional[Size]

    margin_top: Optional[Size]

    page_height: Optional[Size]

    page_width: Optional[Size]

    def __init__(self,
                 margin_bottom: Optional[Size] = None,
                 margin_left: Optional[Size] = None,
                 margin_right: Optional[Size] = None,
                 margin_top: Optional[Size] = None,

                 page_height: Optional[Size] = None,
                 page_width: Optional[Size] = None,
                 ):
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top

        self.page_height = page_height
        self.page_width = page_width

    def __eq__(self, other):
        return self.margin_bottom == other.margin_bottom and self.margin_left == other.margin_left and self.margin_right == other.margin_right and self.margin_top == other.margin_top and self.page_height == other.page_height and self.page_width == other.page_width

    def __satisfy__(self, other):
        if not satisfy(self.margin_bottom, other.margin_bottom):
            e = MarginBottomNotMatched()
            e.val, e.req = self.margin_bottom, other.margin_bottom
            raise e
        if not satisfy(self.margin_left, other.margin_left):
            e = MarginLeftNotMatched()
            e.val, e.req = self.margin_left, other.margin_left
            raise e
        if not satisfy(self.margin_right, other.margin_right):
            e = MarginRightNotMatched()
            e.val, e.req = self.margin_right, other.margin_right
            raise e
        if not satisfy(self.margin_top, other.margin_top):
            e = MarginTopNotMatched()
            e.val, e.req = self.margin_top, other.margin_top
            raise e
        if not satisfy(self.page_height, other.page_height):
            e = PageHeightLeftNotMatched()
            e.val, e.req = self.page_height, other.page_height
            raise e
        if not satisfy(self.page_width, other.page_width):
            e = PageWidthLeftNotMatched()
            e.val, e.req = self.page_width, other.page_width
            raise e
        return True


class HeaderMarginTopNotMatched(PageLayoutNotMatched):
    pass


class HeaderStyle(YAMLObject):
    yaml_tag = '!HeaderProperty'

    margin_top: Optional[Size]

    def __init__(self, margin_top: Optional[Size] = None):
        self.margin_top = margin_top

    def __eq__(self, other):
        return self.margin_top == other.margin_top

    def __satisfy__(self, other):
        if not satisfy(self.margin_top, other.margin_top):
            e = HeaderMarginTopNotMatched()
            e.val, e.req = self.margin_top, other.margin_top
            raise e
        return True


class FooterMarginBottomNotMatched(PageLayoutNotMatched):
    pass


class FooterStyle(YAMLObject):
    yaml_tag = '!FooterProperty'

    margin_bottom: Optional[Size]

    def __init__(self, margin_bottom: Optional[Size] = None):
        self.margin_bottom = margin_bottom

    def __eq__(self, other):
        return self.margin_bottom == other.margin_bottom

    def __satisfy__(self, other):
        if not satisfy(self.margin_bottom, other.margin_bottom):
            e = FooterMarginBottomNotMatched()
            e.val, e.req = self.margin_bottom, other.margin_bottom
            raise e
        return True


class PageLayout(YAMLObject):
    yaml_tag = '!PageLayout'

    prop: PageProp

    header_style: Optional[HeaderStyle]

    footer_style: Optional[FooterStyle]

    def __init__(self,
                 prop: PageProp,
                 header_style: Optional[HeaderStyle] = None,
                 footer_style: Optional[FooterStyle] = None,
                 ):
        self.prop = prop
        self.header_style = header_style
        self.footer_style = footer_style

    def __eq__(self, other):
        return self.prop == other.prop and self.header_style == other.header_style and self.footer_style == other.footer_style

    def __satisfy__(self, other):
        satisfy(self.prop, other.prop)
        satisfy(self.header_style, other.header_style)
        satisfy(self.footer_style, other.footer_style)
        return True
