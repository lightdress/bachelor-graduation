from typing import Optional, Union, List

from core.pp.properties import TextProp, ParaProp, PageLayout


class Span(str):
    prop: TextProp


class Image:
    pass


class Math:
    pass


class Frame:
    anchor_type: str
    obj: Union[Image, Math]

    def __init__(self, anchor_type: str, obj: Union[Image, Math]):
        self.anchor_type = anchor_type
        self.obj = obj


class Para(List[Union[Span, Frame]]):
    prop: ParaProp

    def __init__(self, prop: ParaProp):
        super().__init__(self)
        self.prop = prop


class EmptyPara(Para):
    def __str__(self):
        return 'Empty Paragraph.'


class Cell(List[Para]):
    pass


class Row(List[Cell]):
    pass


class Table(List[Row]):
    prop: ParaProp

    def __init__(self, prop: ParaProp):
        super().__init__(self)
        self.prop = prop


class Break(str):
    before: bool = True

    def __eq__(self, other):
        return self.before == other.before


class Header(List[Para]):
    pass


class Footer(List[Para]):
    pass


class MasterPage:
    page_layout: PageLayout

    header: Optional[Header]
    header_first: Optional[Header]
    footer: Optional[Footer]
    footer_first: Optional[Footer]

    def __init__(self,
                 page_layout: PageLayout,
                 header: Optional[Header] = None,
                 header_first: Optional[Header] = None,
                 footer: Optional[Footer] = None,
                 footer_first: Optional[Footer] = None,
                 ):
        self.page_layout = page_layout
        self.header = header
        self.header_first = header_first
        self.footer = footer
        self.footer_first = footer_first


class Doc(List[Union[MasterPage, Para, Table, Break]]):
    pass
