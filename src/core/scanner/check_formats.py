from typing import NoReturn, Tuple

from core.pp.elements import Doc, Para, EmptyPara, MasterPage, Break, Table as Tbl, Frame, Math, Span, Image
from core.scanner.formats import *
from core.comm import satisfy, inherent, PartError
from core.pp.properties import PropNotMatched, ParaEmpty, ParaComplex
from core.scanner.parts import *

section_name: str = ''
line_base: int = 0
n_line: int = 0


class MasterPageBreakError(PartError):
    pos: str


class MasterPageLayoutError(PartError):
    pos: str


class MasterPageHeaderError(PartError):
    pos: str


class MasterPageFooterError(PartError):
    pos: str


class LackPartError(PartError):
    pos: Tuple[str, int]
    part: str


class UnfamiliarPartError(PartError):
    pos: Tuple[str, int]


class WrongFormatError(PartError):
    pos: Tuple[str, int]
    part: str


class LackEmptyLineBeforeError(WrongFormatError):
    pass


class LackLabelBeforeError(WrongFormatError):
    pass


class LackPictureorTableNearError(WrongFormatError):
    pass


class LackLabelAfterError(WrongFormatError):
    pass


class LackEmptyLineAfterError(WrongFormatError):
    pass


def is_empty_span(s: Span) -> bool:
    blank = [' ', '\u3000', '\n']
    for c in s:
        if c not in blank:
            return False
    return True


def is_empty_para(p: Para) -> bool:
    for s in p:
        if type(s) is not Span or not (is_empty_span(s)):
            return False
    return True


def check_pure_para(para: Para, pure_para_prop: PureParaProp) -> str:
    if len(para) == 0:
        raise ParaEmpty
    if len(para) > 1 or type(para[0]) is not Span:
        raise ParaComplex
    satisfy(inherent(para.prop, fmt.default_fmt.para_prop), pure_para_prop.para_prop)
    satisfy(inherent(para[0].prop, fmt.default_fmt.text_prop), pure_para_prop.text_prop)
    return para[0]


def check_master_page(master_page: MasterPage, pos: str) -> NoReturn:
    try:
        satisfy(master_page.page_layout, fmt.page_fmt[0])
    except PropNotMatched as nm:
        e = MasterPageLayoutError()
        e.pos = pos
        raise e from nm
    try:
        # for h in master_page.header_first:
        #     check_pure_para(h, page_fmt[1])
        for h in master_page.header:
            check_pure_para(h, fmt.page_fmt[1])
    except PropNotMatched as nm:
        e = MasterPageHeaderError()
        e.pos = pos
        raise e from nm
    try:
        pass
        # for h in master_page.footer_first:
        #     check_pure_para(h, page_fmt[2])
        # for h in master_page.footer:
        #     check_pure_para(h, page_fmt[2])
    except PropNotMatched as nm:
        e = MasterPageFooterError()
        e.pos = pos
        raise e from nm


def check_title(para: Para) -> NoReturn:
    global section_name
    global line_base
    global n_line
    try:
        check_pure_para(para, fmt.title_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'title'
        e.pos = section_name, n_line - line_base
        raise e from nm


def check_abstract_title(para: Para) -> str:
    global section_name
    global line_base
    global n_line
    try:
        return check_pure_para(para, fmt.abstract_title_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'abstract title'
        e.pos = section_name, n_line - line_base
        raise e from nm


def check_abstract(para: Para) -> NoReturn:
    global section_name
    global line_base
    global n_line
    try:
        check_pure_para(para, fmt.abstract_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'abstract'
        e.pos = section_name, n_line - line_base
        raise e from nm


def is_keywords(para: Para) -> (bool, str):
    try:
        content = check_pure_para(para, fmt.keywords_fmt)
    except PropNotMatched:
        return False, ''
    return True, content


def check_title_en(para: Para) -> NoReturn:
    global section_name
    global line_base
    global n_line
    try:
        check_pure_para(para, fmt.title_en_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'English title'
        e.pos = section_name, n_line - line_base
        raise e from nm


def check_abstract_title_en(para: Para) -> str:
    global section_name
    global line_base
    global n_line
    try:
        return check_pure_para(para, fmt.abstract_title_en_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'English abstract title'
        e.pos = section_name, n_line - line_base
        raise e from nm


def check_abstract_en(para: Para) -> NoReturn:
    global section_name
    global line_base
    global n_line
    try:
        check_pure_para(para, fmt.abstract_en_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'English abstract'
        e.pos = section_name, n_line - line_base
        raise e from nm


def is_keywords_en(para: Para) -> (bool, str):
    try:
        content = check_pure_para(para, fmt.keywords_en_fmt)
    except PropNotMatched:
        return False, ''
    return True, content


def check_catalog_title(para: Para) -> str:
    global section_name
    global line_base
    global n_line
    try:
        return check_pure_para(para, fmt.catalog_title_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'catalog title'
        e.pos = section_name, n_line - line_base
        raise e from nm


def is_heading(para: Para, level: int) -> (bool, str):
    try:
        heading_content = check_pure_para(para, fmt.heading_fmts[level])
    except PropNotMatched:
        return False, ''
    return True, heading_content


def is_conclusion_title(para: Para) -> (bool, str):
    try:
        content = check_pure_para(para, fmt.conclusion_title_fmt)
    except PropNotMatched:
        return False, ''
    return True, content


def is_references_title(para: Para) -> (bool, str):
    try:
        content = check_pure_para(para, fmt.references_title_fmt)
    except PropNotMatched:
        return False, ''
    return True, content


def check_reference(para: Para) -> str:
    global section_name
    global line_base
    global n_line
    try:
        return check_pure_para(para, fmt.reference_fmt)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'references'
        e.pos = section_name, n_line - line_base
        raise e from nm


def is_appendix_title(para: Para) -> (bool, str):
    try:
        content = check_pure_para(para, fmt.appendix_title_fmt)
    except PropNotMatched:
        return False, ''
    return True, content


def is_thanks_title(para: Para) -> (bool, str):
    try:
        content = check_pure_para(para, fmt.thanks_title_fmt)
    except PropNotMatched:
        return False, ''
    return True, content


def is_label(para: Para) -> (bool, str):
    try:
        label_content = check_pure_para(para, fmt.label_fmt)
    except PropNotMatched:
        return False, ''
    return True, label_content


def is_normal(para: Para) -> bool:
    try:
        satisfy(inherent(para.prop, fmt.default_fmt.para_prop), fmt.normal_fmt.para_prop)
        for s in para:
            if type(s) is Frame:
                if type(s.obj) is not Math:
                    return False
            else:
                if type(s) is not Span:
                    return False
                else:
                    satisfy(inherent(s.prop, fmt.default_fmt.text_prop), fmt.normal_fmt.text_prop)
    except PropNotMatched:
        return False
    else:
        return True


def check_normal(para: Para, pos: int):
    global section_name
    try:
        satisfy(inherent(para.prop, fmt.default_fmt.para_prop), fmt.normal_fmt.para_prop)
        for s in para:
            if type(s) is Frame:
                pass
            else:
                if type(s) is not Span:
                    pass
                else:
                    satisfy(inherent(s.prop, fmt.default_fmt.text_prop), fmt.normal_fmt.text_prop)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'normal'
        e.pos = section_name, pos
        raise e from nm


def is_picture(para: Para) -> bool:
    if len(para) != 1:
        return False
    if type(para[0]) is not Frame or type(para[0].obj) is not Image:
        return False
    return True


def check_picture(para: Para, pos: int):
    global section_name
    try:
        satisfy(inherent(para.prop, fmt.default_fmt.para_prop), fmt.picture_fmt.para_prop)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'picture'
        e.pos = section_name, pos
        raise e from nm


def check_table(table: Tbl, pos: int):
    global section_name
    try:
        satisfy(inherent(table.prop, fmt.default_fmt.para_prop), fmt.table_fmt.para_prop)
    except PropNotMatched as nm:
        e = WrongFormatError()
        e.part = 'table'
        e.pos = section_name, pos
        raise e from nm


def main(doc: Doc, formats: Formats) -> (Body, Formats):
    global fmt
    fmt = formats

    global section_name
    global line_base
    # purify all paragraphs
    for i in range(len(doc)):
        if type(doc[i]) is Para:
            if is_empty_para(doc[i]):
                doc[i] = EmptyPara(doc[i].prop)
            else:
                last_is_span: bool = False
                new_para = Para(inherent(doc[i].prop, fmt.default_fmt.para_prop))
                for s in doc[i]:
                    if type(s) is not Span:
                        new_para.append(s)
                        last_is_span = False
                    else:
                        if s == '':
                            continue
                        s.prop = inherent(s.prop, fmt.default_fmt.text_prop)
                        if last_is_span and s.prop == new_para[-1].prop:
                            new_end = Span(new_para[-1] + s)
                            new_end.prop = new_para[-1].prop
                            new_para[-1] = new_end
                        else:
                            new_para.append(s)
                        last_is_span = True
                doc[i] = new_para

    ans = Body()
    ans.chapters = []
    ans.appendixes = []
    ans.references = []

    # check cover and statements
    global n_line
    n_line = 0

    (n_section, section_names) = (
        1,
        [
            'cover and statements',
        ],
    ) if fmt.merge_cover_and_statements else (
        2,
        [
            'cover',
            'statements',
        ]
    )
    for i in range(n_section):
        if n_line >= len(doc) or type(doc[n_line]) is not MasterPage:
            e = MasterPageBreakError()
            e.pos = section_names[i]
            raise e
        check_master_page(doc[n_line], section_names[i])
        n_line += 1
        while n_line < len(doc):
            if type(doc[n_line]) is MasterPage:
                break
            else:
                n_line += 1

    line_base = n_line
    section_name = 'abstracts and catalog' if fmt.merge_abstracts_and_catalog else 'abstract'
    if n_line >= len(doc) or type(doc[n_line]) is not MasterPage:
        e = MasterPageBreakError()
        e.pos = section_name
        raise e
    check_master_page(doc[n_line], section_name)
    n_line += 1
    if n_line >= len(doc) or type(doc[n_line]) is not Para:
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'title'
        raise e
    check_title(doc[n_line])
    n_line += 1
    if n_line >= len(doc) or type(doc[n_line]) is not Para:
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'abstract title'
        raise e
    ans.abstract_title = check_abstract_title(doc[n_line])
    n_line += 1
    while n_line < len(doc) and not is_keywords(doc[n_line])[0]:
        if type(doc[n_line]) is not EmptyPara:
            check_abstract(doc[n_line])
        n_line += 1
    if n_line >= len(doc):
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'key words'
        raise e
    if type(doc[n_line - 1]) is not EmptyPara:
        e = LackEmptyLineBeforeError()
        e.pos = section_name, n_line - line_base
        e.part = 'key words'
        raise e
    ans.keywords = is_keywords(doc[n_line])[1]
    n_line += 1
    while n_line < len(doc) and type(doc[n_line]) is EmptyPara:
        n_line += 1

    if not fmt.merge_abstracts_and_catalog:
        section_name = 'English abstract'
        line_base = n_line
        if n_line >= len(doc) or type(doc[n_line]) is not MasterPage:
            e = MasterPageBreakError()
            e.pos = section_name
            raise e
        check_master_page(doc[n_line], section_name)
        n_line += 1
    if n_line >= len(doc) or type(doc[n_line]) is not Para:
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'English title'
        raise e
    check_title_en(doc[n_line])
    n_line += 1
    if n_line >= len(doc) or type(doc[n_line]) is not EmptyPara:
        e = LackEmptyLineBeforeError()
        e.pos = section_name, n_line - line_base
        e.part = 'English abstract title'
        raise e
    n_line += 1
    if n_line >= len(doc) or type(doc[n_line]) is not Para:
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'English abstract title'
        raise e
    ans.abstract_title_en = check_abstract_title_en(doc[n_line])
    n_line += 1
    while n_line < len(doc) and not is_keywords_en(doc[n_line])[0]:
        if type(doc[n_line]) is not EmptyPara:
            check_abstract_en(doc[n_line])
        n_line += 1
    if n_line >= len(doc):
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'English key words'
        raise e
    if type(doc[n_line - 1]) is not EmptyPara:
        e = LackEmptyLineBeforeError()
        e.pos = section_name, n_line - line_base
        e.part = 'English key words'
        raise e
    ans.keywords_en = is_keywords_en(doc[n_line])[1]
    n_line += 1
    while n_line < len(doc) and type(doc[n_line]) is EmptyPara:
        n_line += 1

    if not fmt.merge_abstracts_and_catalog:
        section_name = 'catalog'
        line_base = n_line
        if n_line >= len(doc) or type(doc[n_line]) is not MasterPage:
            e = MasterPageBreakError()
            e.pos = section_name
            raise e
        check_master_page(doc[n_line], section_name)
        n_line += 1
    if n_line >= len(doc) or type(doc[n_line]) is not Para:
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'catalog title'
        raise e
    ans.catalog_title = check_catalog_title(doc[n_line])
    n_line += 1
    while n_line < len(doc):
        if type(doc[n_line]) is MasterPage:
            break
        else:
            n_line += 1

    # enter the last section
    section_name = 'chapters, conclusion, references, appendixes and thanks'
    line_base = n_line
    if n_line >= len(doc) or type(doc[n_line]) is not MasterPage:
        e = MasterPageBreakError()
        e.pos = section_name
        raise e
    check_master_page(doc[n_line], section_name)
    n_line += 1

    while n_line < len(doc):
        if type(doc[n_line]) is Break or type(doc[n_line]) is EmptyPara:
            n_line += 1
            continue
        if type(doc[n_line]) is Tbl:
            e = LackLabelBeforeError()
            e.pos = section_name, n_line - line_base
            e.part = 'table'
            raise e
        n_heading_fmt: int = 0
        while n_heading_fmt < len(fmt.heading_fmts):
            (heading, heading_content) = is_heading(doc[n_line], n_heading_fmt)
            if heading:
                if n_heading_fmt == 0:
                    ans.chapters.append(Chapter())
                    ans.chapters[-1].title = heading_content
                else:
                    ans.chapters[-1].append(Heading(heading_content))  # out of range!
                    ans.chapters[-1][-1].level = n_heading_fmt
                break
            else:
                n_heading_fmt += 1
        if n_heading_fmt < len(fmt.heading_fmts):
            n_line += 1
            continue
        (label, label_content) = is_label(doc[n_line])
        if label:
            if n_line + 1 < len(doc) and type(doc[n_line + 1]) is Tbl:
                check_table(doc[n_line + 1], n_line + 1 - line_base)
                if type(doc[n_line - 1]) is EmptyPara:
                    if n_line + 2 < len(doc) and type(doc[n_line + 2]) is EmptyPara:
                        ans.chapters[-1].append(Table(label_content))
                        n_line += 3
                        continue
                    else:
                        e = LackEmptyLineAfterError()
                        e.pos = section_name, n_line - line_base + 1
                        e.part = 'table'
                        raise e
                else:
                    e = LackEmptyLineBeforeError()
                    e.pos = section_name, n_line - line_base
                    e.part = 'table'
                    raise e
            else:
                e = LackPictureorTableNearError()
                e.pos = section_name, n_line - line_base + 1
                e.part = 'table'
                raise e
        if is_picture(doc[n_line]):
            check_picture(doc[n_line], n_line - line_base)
            if n_line + 1 < len(doc) and is_label(doc[n_line + 1])[0]:
                if type(doc[n_line - 1]) is EmptyPara:
                    if n_line + 2 < len(doc) and type(doc[n_line + 2]) is EmptyPara:
                        ans.chapters[-1].append(Picture(is_label(doc[n_line + 1])[1]))
                        n_line += 3
                        continue
                    else:
                        e = LackEmptyLineAfterError()
                        e.pos = section_name, n_line - line_base + 1
                        e.part = 'picture'
                        raise e
                else:
                    e = LackEmptyLineBeforeError()
                    e.pos = section_name, n_line - line_base
                    e.part = 'picture'
                    raise e
            else:
                e = LackLabelAfterError()
                e.pos = section_name, n_line - line_base
                e.part = 'picture'
                raise e
        normal = is_normal(doc[n_line])
        if normal:
            ans.chapters[-1].append(Normal())
            n_line += 1
            continue
        (conclusion_title, _) = is_conclusion_title(doc[n_line])
        if conclusion_title:
            break
        e = UnfamiliarPartError()
        e.pos = section_name, n_line - line_base
        raise e

    if n_line >= len(doc):
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'conclusion title'
        raise e
    if type(doc[n_line - 1]) is not EmptyPara:
        e = LackEmptyLineBeforeError()
        e.pos = section_name, n_line - line_base
        e.part = 'conclusion title'
        raise e
    (_, conclusion_title_content) = is_conclusion_title(doc[n_line])
    ans.conclusion_title = conclusion_title_content
    n_line += 1
    while n_line < len(doc) and not is_references_title(doc[n_line])[0]:
        if type(doc[n_line]) is not EmptyPara and type(doc[n_line]) is not Break:
            check_normal(doc[n_line], n_line - line_base)
        n_line += 1

    if n_line >= len(doc):
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'references title'
        raise e
    if type(doc[n_line - 1]) is not EmptyPara:
        e = LackEmptyLineBeforeError()
        e.pos = section_name, n_line - line_base
        e.part = 'references title'
        raise e
    ans.references_title = is_references_title(doc[n_line])[1]
    n_line += 1
    while n_line < len(doc) and type(doc[n_line]) is not EmptyPara and type(doc[n_line]) is not Break:
        reference_content = check_reference(doc[n_line])
        ans.references.append(Reference(reference_content))
        n_line += 1
    while n_line < len(doc) and type(doc[n_line]) is EmptyPara or type(doc[n_line]) is Break:
        n_line += 1

    if n_line >= len(doc):
        e = LackPartError()
        e.pos = section_name, n_line - line_base
        e.part = 'appendix title'
        raise e
    n_line_r = len(doc) - 1
    while n_line_r >= n_line and type(doc[n_line_r]) is EmptyPara or type(doc[n_line_r]) is Break:
        n_line_r -= 1
    while n_line_r >= n_line and not is_thanks_title(doc[n_line_r])[0]:
        if type(doc[n_line_r]) is not EmptyPara and type(doc[n_line_r]) is not Break:
            if not is_normal(doc[n_line_r]):
                check_normal(doc[n_line_r], n_line_r - line_base)
        n_line_r -= 1
    if n_line_r < n_line:
        e = LackPartError()
        e.pos = section_name, n_line_r - line_base
        e.part = 'thanks title'
        raise e
    if type(doc[n_line_r - 1]) is not EmptyPara:
        e = LackEmptyLineBeforeError()
        e.pos = section_name, n_line_r - line_base
        e.part = 'thanks title'
        raise e
    ans.thanks_title = is_thanks_title(doc[n_line_r])[1]
    n_line_r -= 1

    while n_line < n_line_r:
        if type(doc[n_line]) is Break or type(doc[n_line]) is EmptyPara:
            n_line += 1
            continue
        if type(doc[n_line]) is Tbl:
            e = LackLabelBeforeError()
            e.pos = section_name, n_line - line_base
            e.part = 'table'
            raise e
        if is_appendix_title(doc[n_line])[0]:
            ans.appendixes.append(Appendix())
            ans.appendixes[-1].append(is_appendix_title(doc[n_line])[1])
            n_line += 1
            continue
        (label, label_content) = is_label(doc[n_line])
        if label:
            if n_line + 1 < len(doc) and type(doc[n_line + 1]) is Tbl:
                check_table(doc[n_line + 1], n_line + 1 - line_base)
                if type(doc[n_line - 1]) is EmptyPara:
                    if n_line + 2 < len(doc) and type(doc[n_line + 2]) is EmptyPara:
                        ans.appendixes[-1].append(Table(label_content))
                        n_line += 3
                        continue
                    else:
                        e = LackEmptyLineAfterError()
                        e.pos = section_name, n_line - line_base + 1
                        e.part = 'table'
                        raise e
                else:
                    e = LackEmptyLineBeforeError()
                    e.pos = section_name, n_line - line_base
                    e.part = 'table'
                    raise e
            else:
                e = LackPictureorTableNearError()
                e.pos = section_name, n_line - line_base + 1
                e.part = 'table'
                raise e
        if is_picture(doc[n_line]):
            check_picture(doc[n_line], n_line - line_base)
            if n_line + 1 < len(doc) and is_label(doc[n_line + 1])[0]:
                if type(doc[n_line - 1]) is EmptyPara:
                    if n_line + 2 < len(doc) and type(doc[n_line + 2]) is EmptyPara:
                        ans.appendixes[-1].append(Picture(is_label(doc[n_line + 1])[1]))
                        n_line += 3
                        continue
                    else:
                        e = LackEmptyLineAfterError()
                        e.pos = section_name, n_line - line_base + 1
                        e.part = 'picture'
                        raise e
                else:
                    e = LackEmptyLineBeforeError()
                    e.pos = section_name, n_line - line_base
                    e.part = 'picture'
                    raise e
            else:
                e = LackLabelAfterError()
                e.pos = section_name, n_line - line_base
                e.part = 'picture'
                raise e
        normal = is_normal(doc[n_line])
        if normal:
            ans.appendixes[-1].append(Normal())
            n_line += 1
            continue
        e = UnfamiliarPartError()
        e.pos = section_name, n_line - line_base
        raise e
    return ans, fmt
