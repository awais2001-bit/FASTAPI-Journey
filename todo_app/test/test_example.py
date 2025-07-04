# import pytest
#
# class Student:
#     def __init__(self, first_name:str, last_name:str, major:str, years:int):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.major = major
#         self.years = years
#
#
#
#
# @pytest.fixture
# def default_student():
#     return Student('John', 'Doe', 'Math', 3)
#
#
# def test_person_initialization(default_student):
#     assert default_student.first_name == "John",'first name should be john'
#     assert default_student.last_name == "Doe", 'last name should be doe'
#     assert default_student.major == "Math"
#     assert default_student.years == 5
#
#
#
#
#
#
#
#
#
#
# def test_example():
#     assert 3==3
#
#
# def test_is_instance():
#
#     assert isinstance('this is a string', str)
#     assert not isinstance('this is a string', int)///