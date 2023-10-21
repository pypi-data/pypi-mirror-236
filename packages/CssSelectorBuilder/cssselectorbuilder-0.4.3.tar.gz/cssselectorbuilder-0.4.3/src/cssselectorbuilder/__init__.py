from typing import TypeVar
from enum import Enum
TCssSelector = TypeVar("TCssSelector", bound="CssSelector")

class SubStringSelector(Enum):
    begins_with = "^"
    ends_with = "$"
    contains = "*"
    none = ""

class CssSelector:
    def __init__(self) -> None:
        self.selectors = list()

    def __str__(self):
        return "".join(self.selectors)

    def class_name(self, value: str):
        if type(value) is not str:
            raise TypeError(f"The value must be type str not {type(value)}!")
        self.selectors.append(f".{value}")
        return self 
    
    def id(self, value: str):
        if type(value) is not str:
            raise TypeError(f"The value must be type str not {type(value)}!")
        self.selectors.append(f"#{value}")
        return self
    
    def element_type(self, element_type: str):
        if type(element_type) is not str:
            raise TypeError(f"The element_type must be type str not {type(element_type)}!")
        self.selectors.append(f"{element_type}")
        return self
    
    def is_not(self, selector: TCssSelector):
        if type(selector) is not CssSelector:
            raise TypeError(f"Selector has to be type CssSelector not {type(selector)}")
        self.selectors.append(f":not({selector})")
        return self
    
    def attribute(self, attribute_name: str, value: str, sub_string_selector: SubStringSelector = SubStringSelector.none):
        if type(attribute_name) is not str:
            raise TypeError(f"attribute_name has to be type str not {type(attribute_name)}")
        
        if type(value) is not str:
            raise TypeError(f"value has to be type str not {type(value)}")
        
        if type(sub_string_selector) is not SubStringSelector:
            raise TypeError(f"sub_string_selector has to be type SubStringSelector not {type(sub_string_selector)}")
        
        self.selectors.append(f"[{attribute_name}{sub_string_selector.value}='{value}']")
        return self 