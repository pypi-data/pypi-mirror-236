import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any


_ygrpc_official_types = [int, float, str, bool]


def convert_dict_that_has_enum_object_into_pure_dict(value: Any) -> dict[str, Any] | list[Any] | Any:
    if type(value) is list:
        new_list: list[Any] = []
        for one in value: #type: ignore
            new_list.append(convert_dict_that_has_enum_object_into_pure_dict(value=one)) 
        return new_list
    elif type(value) is dict:
        new_dict: dict[str, Any] = {}
        for key_, value_ in value.items(): #type: ignore
            new_dict[key_] = convert_dict_that_has_enum_object_into_pure_dict(value=value_) #type: ignore
        return new_dict
    else:
        if str(type(value)).startswith("<enum"):
            return value.name
        else:
            if type(value) in _ygrpc_official_types:
                return value
            else:
                # handle custom message data type
                if value == None:
                    return None
                elif str(type(value)).startswith("<class"):
                    return convert_dict_that_has_enum_object_into_pure_dict(
                        value=value.to_dict()
                    )
    return None


def convert_pure_dict_into_a_dict_that_has_enum_object(pure_value: Any, refrence_value: Any) -> Any:
    if type(pure_value) is list:
        new_list: list[Any] = []
        for one in pure_value: #type: ignore
            new_list.append(
                convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=one, refrence_value=refrence_value)
            ) 
        return new_list
    elif type(pure_value) is dict:
        if str(refrence_value).startswith("<class"):
            new_object = refrence_value()
            old_property_list = getattr(new_object, "_property_name_to_its_type_dict")
            for key in old_property_list.keys():
                if key in pure_value.keys():
                    setattr(new_object, key, convert_pure_dict_into_a_dict_that_has_enum_object(pure_value[key], old_property_list[key])) # type: ignore
            return new_object
        else:
            return None
    else:
        if str(refrence_value).startswith("<enum"):
            default_value = None
            for temp_index, temp_value in enumerate(refrence_value._member_names_):
                if temp_value == pure_value:
                    default_value = refrence_value(temp_value) 
                    break
            return default_value
        else:
            if refrence_value in _ygrpc_official_types:
                return pure_value
            else:
                return None


class YRPC_OBJECT_BASE_CLASS:
    def to_dict(self, ignore_null: bool=False) -> dict[str, Any]:
        old_dict = {}
        for key in self._property_name_to_its_type_dict.keys(): #type: ignore
            old_dict[key] = self.__dict__[key] #type: ignore
        new_dict = convert_dict_that_has_enum_object_into_pure_dict(value=old_dict.copy())
        return new_dict.copy() #type: ignore

    def from_dict(self, dict: dict[str, Any]) -> Any:
        new_object = convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=dict.copy(), refrence_value=self.__class__)

        new_object_dict = new_object.__dict__.copy() 
        for key, value in new_object_dict.items():
            if key in self.__dict__:
                setattr(self, key, value)

        return new_object

    def _clone(self) -> Any:
        return copy.deepcopy(self)




        
@dataclass()
class An_App(YRPC_OBJECT_BASE_CLASS):
    create_time_in_10_numbers_timestamp_format: int | None = None
    name: str | None = None
    description: str | None = None
    url: str | None = None
    app_icon_in_base64: str | None = None
    author_contact_method: str | None = None
    click_number: int | None = None

    _property_name_to_its_type_dict = {
        "create_time_in_10_numbers_timestamp_format": int,
        "name": str,
        "description": str,
        "url": str,
        "app_icon_in_base64": str,
        "author_contact_method": str,
        "click_number": int,
    }

    @dataclass()
    class _key_string_dict:
        create_time_in_10_numbers_timestamp_format: str = "create_time_in_10_numbers_timestamp_format"
        name: str = "name"
        description: str = "description"
        url: str = "url"
        app_icon_in_base64: str = "app_icon_in_base64"
        author_contact_method: str = "author_contact_method"
        click_number: str = "click_number"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: An_App = super().from_dict(dict)
        return new_variable


@dataclass()
class Add_App_Request(YRPC_OBJECT_BASE_CLASS):
    question: str | None = None
    answer: str | None = None
    an_app: An_App | None = None

    _property_name_to_its_type_dict = {
        "question": str,
        "answer": str,
        "an_app": An_App,
    }

    @dataclass()
    class _key_string_dict:
        question: str = "question"
        answer: str = "answer"
        an_app: str = "an_app"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Add_App_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Add_App_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    app_name: str | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "app_name": str,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        app_name: str = "app_name"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Add_App_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Search_App_Request(YRPC_OBJECT_BASE_CLASS):
    search_input: str | None = None
    page_size: int | None = None
    page_number: int | None = None

    _property_name_to_its_type_dict = {
        "search_input": str,
        "page_size": int,
        "page_number": int,
    }

    @dataclass()
    class _key_string_dict:
        search_input: str = "search_input"
        page_size: str = "page_size"
        page_number: str = "page_number"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Search_App_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Search_App_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    app_list: list[An_App] | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "app_list": An_App,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        app_list: str = "app_list"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Search_App_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_App_Detail_Request(YRPC_OBJECT_BASE_CLASS):
    name: str | None = None

    _property_name_to_its_type_dict = {
        "name": str,
    }

    @dataclass()
    class _key_string_dict:
        name: str = "name"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_App_Detail_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_App_Detail_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    an_app: An_App | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "an_app": An_App,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        an_app: str = "an_app"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_App_Detail_Response = super().from_dict(dict)
        return new_variable


@dataclass()
class Export_Data_Request(YRPC_OBJECT_BASE_CLASS):


    _property_name_to_its_type_dict = {

    }

    @dataclass()
    class _key_string_dict:
        pass

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Export_Data_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Export_Data_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    file_name: str | None = None
    file_bytes_in_base64_format: str | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "file_name": str,
        "file_bytes_in_base64_format": str,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        file_name: str = "file_name"
        file_bytes_in_base64_format: str = "file_bytes_in_base64_format"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Export_Data_Response = super().from_dict(dict)
        return new_variable