from typing import NoReturn
from core.comm import NotMatched, PartError
from core.parser.contents import *
from core.scanner.parts import *


def remove_blanks(s: str) -> str:
    s = s.replace(' ', '')
    s = s.replace('\u3000', '')
    return s


class TextNotMatched(NotMatched):
    pass


class WordNotMatched(TextNotMatched):
    pass


class PrefixNotMatched(TextNotMatched):
    pass


class WrongContentError(PartError):
    pos: str


class EmptySectionError(PartError):
    pos: str


def check_word(val: str, req: str) -> NoReturn:
    if remove_blanks(val) != req:
        e = WordNotMatched()
        e.val, e.req = val, req
        raise e


def check_prefix(val: str, req: str) -> NoReturn:
    if not val.startswith(req):
        e = PrefixNotMatched()
        e.val, e.req = val, req
        raise e


def check_abstract_title(title: AbstractTitle) -> NoReturn:
    try:
        check_word(title, cnt.abstract_title_content)
    except WordNotMatched as nm:
        e = WrongContentError()
        e.pos = 'abstract title'
        raise e from nm


def check_abstract_title_en(title: AbstractTitleEN) -> NoReturn:
    try:
        check_word(title, cnt.abstract_title_en_content)
    except WordNotMatched as nm:
        e = WrongContentError()
        e.pos = 'English abstract title'
        raise e from nm


def check_keywords(keywords: Keywords) -> NoReturn:
    try:
        check_prefix(keywords, cnt.keywords_prefix)
    except PrefixNotMatched as nm:
        e = WrongContentError()
        e.pos = 'key words'
        raise e from nm


def check_keywords_en(keywords_en: KeywordsEN) -> NoReturn:
    try:
        check_prefix(keywords_en, cnt.keywords_en_prefix)
    except PrefixNotMatched as nm:
        e = WrongContentError()
        e.pos = 'English key words'
        raise e from nm


def check_catalog_title(title: CatalogTitle) -> NoReturn:
    try:
        check_word(title, cnt.catalog_title_content)
    except WordNotMatched as nm:
        e = WrongContentError()
        e.pos = 'catalog title'
        raise e from nm


def check_conclusion_title(title: ConclusionTitle) -> NoReturn:
    try:
        check_word(title, cnt.conclusion_title_content)
    except WordNotMatched as nm:
        e = WrongContentError()
        e.pos = 'conclusion title'
        raise e from nm


def check_references_title(title: ReferencesTitle) -> NoReturn:
    try:
        check_word(title, cnt.references_title_content)
    except WordNotMatched as nm:
        e = WrongContentError()
        e.pos = 'references title'
        raise e from nm


def check_thanks_title(title: ThanksTitle) -> NoReturn:
    try:
        check_word(title, cnt.thanks_title_content)
    except WordNotMatched as nm:
        e = WrongContentError()
        e.pos = 'thanks title'
        raise e from nm


class Section:
    title: str
    children: list


def get_children(beg: int, sequence: List[Union[Heading, Normal, Picture, Table]], level: int) -> (list, int):
    i = beg
    ans = list()
    while i < len(sequence):
        if type(sequence[i]) is Picture or type(sequence[i]) is Table or type(sequence[i]) is Normal:
            ans.append(sequence[i])
            i += 1
            continue
        if sequence[i].level > level:
            ans.append(Section())
            ans[-1].title = sequence[i]
            (ans[-1].children, i) = get_children(i + 1, sequence, sequence[i].level)
        else:
            break
    return ans, i


def check_section(sxn: Section, chapter_no: str, picture_no: int, table_no: int, title: str) -> (int, int):
    try:
        check_prefix(sxn.title, title)
    except PrefixNotMatched as nm:
        e = WrongContentError()
        e.pos = sxn.title
        raise e from nm
    if len(sxn.children) == 0:
        e = EmptySectionError
        e.pos = sxn.title
        raise e
    i = 1
    for child in sxn.children:
        if type(child) is Section:
            picture_no, table_no = check_section(child, chapter_no, picture_no, table_no,
                                                 cnt.heading_title_prefix.format(title[:-1], i))
            i += 1
            continue
        if type(child) is Picture:
            try:
                check_prefix(child, cnt.picture_prefix.format(chapter_no, picture_no))
            except PrefixNotMatched as nm:
                e = WrongContentError()
                e.pos = sxn.title
                raise e from nm
            picture_no += 1
            continue
        if type(child) is Table:
            try:
                check_prefix(child, cnt.table_prefix.format(chapter_no, table_no))
            except PrefixNotMatched as nm:
                e = WrongContentError()
                e.pos = sxn.title
                raise e from nm
            table_no += 1
            continue
    return picture_no, table_no


def check_chapter(chapter: Chapter, chapter_no: str):
    try:
        check_prefix(chapter.title, cnt.chapter_prefix.format(chapter_no))
    except PrefixNotMatched as nm:
        e = WrongContentError()
        e.pos = chapter.title
        raise e from nm
    sxn = Section()
    sxn.title = chapter_no + ' '
    sxn.children = get_children(0, chapter, 0)[0]
    check_section(sxn, chapter_no, 1, 1, chapter_no + ' ')


def main(body: Body, contents: Contents) -> Contents:
    global cnt
    cnt = contents

    check_abstract_title(body.abstract_title)
    check_abstract_title_en(body.abstract_title_en)
    check_keywords(body.keywords)
    check_keywords_en(body.keywords_en)
    check_catalog_title(body.catalog_title)
    check_conclusion_title(body.conclusion_title)
    check_references_title(body.references_title)
    check_thanks_title(body.thanks_title)
    i = 1
    for chapter in body.chapters:
        check_chapter(chapter, str(i))
        i += 1

    return cnt
