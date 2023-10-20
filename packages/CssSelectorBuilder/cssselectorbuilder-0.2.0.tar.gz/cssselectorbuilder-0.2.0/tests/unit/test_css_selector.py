import pytest
from cssselectorbuilder import CssSelector, SubStringSelector

class TestClassName:
    def test_that_invalid_value_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().class_name(value=1)

    def test_that_class_name_results_correct_selector(self):
        result = str(CssSelector().class_name(value="Test"))

        assert result == ".Test"

class TestId:
    def test_that_invalid_value_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().class_name(value=1)

    def test_that_adding_id_results_correct_selector(self):
        result = str(CssSelector().id(value="Test"))

        assert result == "#Test"

class TestElementType:
    def test_that_invalid_type_value_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().element_type(element_type=1)

    def test_that_adding_element_type_results_correct_selector(self):
        result = str(CssSelector().element_type(element_type="input"))

        assert result == "input"

class TestIsNot:
    def test_that_invalid_type_for_selector_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().is_not(selector=1)

    def test_that_adding_is_not_results_correct_selector(self):
        result = str(CssSelector().is_not(selector=CssSelector().class_name("test")))

        assert result == ":not(.test)"

class TestAttribute:
    def test_that_invalid_type_for_attribute_name_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().attribute(attribute_name=1, value="test", sub_string_selector=SubStringSelector.begins_with)

    def test_that_invalid_type_for_value_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().attribute(attribute_name="test", value=1, sub_string_selector=SubStringSelector.begins_with)

    def test_that_invalid_type_for_sub_string_selector_throws_exception(self):
        with pytest.raises(TypeError):
            CssSelector().attribute(attribute_name="id", value="test", sub_string_selector=1)

    def test_that_adding_sub_string_selector_results_correct_selector(self):
        result = str(CssSelector().attribute("id", "test", sub_string_selector=SubStringSelector.begins_with))

        assert result == "[id^='test']"

class TestCombinedSelectors:
    def test_that_class_name_and_id_results_correct_selector(self):
        result = str(CssSelector().class_name("testClass").id("someId"))

        assert result == ".testClass#someId"

    def test_that_is_not_and_attribute_results_correct_selector(self):
        result = str(CssSelector().is_not(CssSelector().attribute("input", "input", sub_string_selector=SubStringSelector.begins_with)))

        assert result == ":not([input^='input'])"