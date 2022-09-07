from typing import Union, List


class Title:
    pass


class AbstractTitle(str):
    pass


class Abstract(str):
    pass


class Keywords(str):
    pass


class TitleEN:
    pass


class AbstractTitleEN(str):
    pass


class AbstractEN(str):
    pass


class KeywordsEN(str):
    pass


class CatalogTitle(str):
    pass


class Heading(str):
    level: int


class Normal:
    pass


class Picture(str):
    pass


class Table(str):
    pass


class Chapter(List[Union[Heading, Normal, Picture, Table]]):
    title: Heading


class ConclusionTitle(str):
    pass


class ReferencesTitle(str):
    pass


class Reference(str):
    pass


class Appendix(List[Union[Normal, Picture, Table]]):
    title: Heading


class ThanksTitle(str):
    pass


class Body:
    title = Title()
    abstract_title = AbstractTitle()
    abstract = Abstract()
    keywords = Keywords()
    title_en = TitleEN()
    abstract_title_en = AbstractTitleEN()
    abstract_en = AbstractEN()
    keywords_en = KeywordsEN()
    catalog_title = CatalogTitle()

    chapters: List[Chapter] = list()
    conclusion_title = ConclusionTitle()

    references_title = ReferencesTitle()
    references: List[Reference] = list()

    appendixes: List[Appendix] = list()
    thanks_title = ThanksTitle()
