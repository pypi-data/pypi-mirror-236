# CssSelectorBuilder

This Package helps you to build css selectors for selenium or playwright tests.

## Installation
    pip install CssSelectorBuilder

## Examples
### Simple Selector
    import CssSelector from CssSelectorBuilder
    
    print(CssSelector().class_name("someClass"))

Results in:
.someClass

### Combine Selectors
    import CssSelector from CssSelectorBuilder

    print(CssSelector().class_name("someClass).is_not(CssSelector().id(someId)))

Results in:
.someClass:not(#someId)
