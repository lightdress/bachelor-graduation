from core.pp.engines import docx
from core.pp.properties import *
from core.scanner import check_formats
from core.parser import check_contents

from core.scanner.check_formats import MasterPageBreakError, MasterPageLayoutError, MasterPageHeaderError, \
    MasterPageFooterError, LackPartError, UnfamiliarPartError, \
    LackEmptyLineBeforeError, LackEmptyLineAfterError, LackLabelBeforeError, LackLabelAfterError, \
    LackPictureorTableNearError, WrongFormatError

from core.parser.check_contents import EmptySectionError, WrongContentError, WordNotMatched
import yaml
from yaml import YAMLObject



class Config(YAMLObject):
    yaml_tag = u'!Configuration'
    pass


def main(filename: str, yaml_str: str) -> str:
    ans = ''
    doc = docx.main(filename)
    try:

        # with open('config.yaml', 'r') as file:
        #     config: Config = yaml.load(file)
        config: Config = yaml.load(yaml_str)
        body, _ = check_formats.main(doc, config.formats)
        check_contents.main(body, config.contents)

        # with open('config.yaml', 'w') as file:
        #     yaml.dump(config, file, encoding='utf-8', allow_unicode=True)

    except MasterPageBreakError as e:
        ans = 'Can\'t find the {}!\nMaybe the section break before is lack.'.format(e.pos)
    except MasterPageLayoutError as e:
        ans = 'Page format of the {} is wrong!\n'.format(e.pos)
        fmt = ''
        if type(e.__cause__) is MarginBottomNotMatched:
            fmt = 'bottom margin (to footer)'
        elif type(e.__cause__) is MarginLeftNotMatched:
            fmt = 'left margin'
        elif type(e.__cause__) is MarginRightNotMatched:
            fmt = 'right margin'
        elif type(e.__cause__) is MarginTopNotMatched:
            fmt = 'top margin (to header)'
        elif type(e.__cause__) is PageHeightLeftNotMatched:
            fmt = 'page height'
        elif type(e.__cause__) is PageWidthLeftNotMatched:
            fmt = 'page width'
        elif type(e.__cause__) is HeaderMarginTopNotMatched:
            fmt = 'header margin'
        elif type(e.__cause__) is FooterMarginBottomNotMatched:
            fmt = 'footer margin'
        ans += 'The {} is "{}", which should be "{}"'.format(fmt, e.__cause__.val, e.__cause__.req)
    except MasterPageHeaderError as e:
        ans = 'Header format of the {} is wrong!\n'.format(e.pos)
        if type(e.__cause__) is ParaEmpty:
            ans += 'It should not be empty line!'
        elif type(e.__cause__) is ParaComplex:
            ans += 'Text in it should not have more than one formats!'
        else:
            fmt = ''
            if type(e.__cause__) is NameNotMatched:
                fmt = 'font'
            elif type(e.__cause__) is NameAsiaNotMatched:
                fmt = 'Asian font'
            elif type(e.__cause__) is SizeNotMatched:
                fmt = 'size'
            elif type(e.__cause__) is SizeAsiaNotMatched:
                fmt = 'Asian size'
            elif type(e.__cause__) is WeightNotMatched:
                fmt = 'weight'
            elif type(e.__cause__) is WeightAsiaNotMatched:
                fmt = 'Asian weight'
            elif type(e.__cause__) is LetterSpacingNotMatched:
                fmt = 'letter spacing'
            elif type(e.__cause__) is AlignNotMatched:
                fmt = 'alignment'
            elif type(e.__cause__) is LineHeightNotMatched:
                fmt = 'line height'
            ans += 'The {} is "{}", which should be "{}"'.format(fmt, e.__cause__.val, e.__cause__.req)
    except MasterPageFooterError as e:
        ans = 'Footer format of the {} is wrong!\n'.format(e.pos)
        if type(e.__cause__) is ParaEmpty:
            ans += 'It should not be empty line!'
        elif type(e.__cause__) is ParaComplex:
            ans += 'Text in it should not have more than one formats!'
        else:
            fmt = ''
            if type(e.__cause__) is NameNotMatched:
                fmt = 'font'
            elif type(e.__cause__) is NameAsiaNotMatched:
                fmt = 'Asian font'
            elif type(e.__cause__) is SizeNotMatched:
                fmt = 'size'
            elif type(e.__cause__) is SizeAsiaNotMatched:
                fmt = 'Asian size'
            elif type(e.__cause__) is WeightNotMatched:
                fmt = 'weight'
            elif type(e.__cause__) is WeightAsiaNotMatched:
                fmt = 'Asian weight'
            elif type(e.__cause__) is LetterSpacingNotMatched:
                fmt = 'letter spacing'
            elif type(e.__cause__) is AlignNotMatched:
                fmt = 'alignment'
            elif type(e.__cause__) is LineHeightNotMatched:
                fmt = 'line height'
            ans += 'The {} is "{}", which should be "{}"'.format(fmt, e.__cause__.val, e.__cause__.req)
    except LackPartError as e:
        ans = 'Line {} in {}:\nThe {} is lack! Be sure that its format is right.'.format(e.pos[1], e.pos[0], e.part)
    except UnfamiliarPartError as e:
        ans = 'Line {} in {}:\nFormat of this line is unfamiliar! What\'s it?'.format(e.pos[1], e.pos[0])
    except LackEmptyLineBeforeError as e:
        ans = 'Line {} in {}:\nThere should be an empty line before this {}!'.format(e.pos[1], e.pos[0], e.part)
    except LackEmptyLineAfterError as e:
        ans = 'Line {} in {}:\nThere should be an empty line after this {}!'.format(e.pos[1], e.pos[0], e.part)
    except LackLabelBeforeError as e:
        ans = 'Line {} in {}:\nThere should be a label before this {}!'.format(e.pos[1], e.pos[0], e.part)
    except LackLabelAfterError as e:
        ans = 'Line {} in {}:\nThere should be an label after this {}!'.format(e.pos[1], e.pos[0], e.part)
    except LackPictureorTableNearError as e:
        ans = 'Line {} in {}:\nThere should be a {} next to this label!'.format(e.pos[1], e.pos[0], e.part)
    except WrongFormatError as e:
        ans = 'Line {} in {}:\n'.format(e.pos[1], e.pos[0])
        if type(e.__cause__) is ParaEmpty:
            ans += 'This {} should not be empty line!'.format(e.part)
        elif type(e.__cause__) is ParaComplex:
            ans += 'Text in this {} should not have more than one formats!'.format(e.part)
        else:
            fmt = ''
            if type(e.__cause__) is NameNotMatched:
                fmt = 'font'
            elif type(e.__cause__) is NameAsiaNotMatched:
                fmt = 'Asian font'
            elif type(e.__cause__) is SizeNotMatched:
                fmt = 'size'
            elif type(e.__cause__) is SizeAsiaNotMatched:
                fmt = 'Asian size'
            elif type(e.__cause__) is WeightNotMatched:
                fmt = 'weight'
            elif type(e.__cause__) is WeightAsiaNotMatched:
                fmt = 'Asian weight'
            elif type(e.__cause__) is LetterSpacingNotMatched:
                fmt = 'letter spacing'
            elif type(e.__cause__) is AlignNotMatched:
                fmt = 'alignment'
            elif type(e.__cause__) is LineHeightNotMatched:
                fmt = 'line height'

            ans += 'The {} of this {} is "{}", which should be "{}"'.format(fmt, e.part, e.__cause__.val,
                                                                            e.__cause__.req)
    except EmptySectionError as e:
        ans = '{}:\nThis section is empty! There should be something.'.format(e.pos)
    except WrongContentError as e:
        if type(e.__cause__) is WordNotMatched:
            ans = 'The {} is "{}", which should be "{}".'.format(e.pos, e.__cause__.val, e.__cause__.req)
        else:
            ans = 'The {} contains "{}", which should start with "{}".'.format(e.pos, e.__cause__.val, e.__cause__.req)

    if ans == '':
        ans = "No error found.\nGood job."
    return ans
