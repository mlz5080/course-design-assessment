from abc import ABC, abstractmethod
from typing import List, Any

from app.model.course import Course


class CourseDAOInterface():
    """
    Course DAO interface definition.
    Moving to another persistance should always implement these functions.
    """

    @abstractmethod
    def get_courses_list(self) -> List[Any]:
        pass

    @abstractmethod
    def get_course_by_id(self, course_id) -> Any:
        pass

    @abstractmethod
    def create_course(self, course_name) -> int:
        pass

    @abstractmethod
    def delete_course(self, course_id) -> bool:
        pass

    @abstractmethod
    def is_course_valid(self, course_id) -> bool:
        pass

    @abstractmethod
    def enroll_student(self, course_id, student_id) -> bool:
        pass

    @abstractmethod
    def is_student_enrolled(self, course_id, student_id) -> bool:
        pass

    @abstractmethod
    def dropout_student(self, course_id, student_id) -> bool:
        pass

    @abstractmethod
    def get_enrollment_list(self, course_id) -> List[str]:
        pass
