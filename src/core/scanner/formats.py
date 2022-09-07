from core.pp.properties import TextProp, ParaProp
from typing import Optional
from yaml import YAMLObject


class PureParaProp(YAMLObject):
    yaml_tag = '!PureParagraphProperty'

    para_prop: ParaProp
    text_prop: Optional[TextProp]

    def __init__(self, para_prop: ParaProp, text_prop: Optional[TextProp] = None):
        self.para_prop = para_prop
        self.text_prop = text_prop


class Formats(YAMLObject):
    yaml_tag = u'!Formats'
    pass


