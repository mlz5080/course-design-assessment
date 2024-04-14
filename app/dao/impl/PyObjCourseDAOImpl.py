from typing import List, Any

from app.model.course import Course
from app.dao.courseDAO import CourseDAOInterface


class PyObjCourseDAO(CourseDAOInterface):
    """
    Using Python internal data structure to store data.

    Attributes:
        courses_map (dict): A hashMap of course_id mapping to PyObj course
    """
    def __init__(self):
        self.courses_map = {}

    def get_courses_list(self) -> List[Any]:
        return [course.dict_representation() for course in self.courses_map.values()]

    def get_course_by_id(self, course_id) -> Any:
        return self.courses_map[course_id].dict_representation()

    def create_course(self, course_name) -> int:
        new_course = Course(course_name)

        # Assuming that multiple course session can exist with same course_name
        # OS can handle the course id recycling once the course is released from memory
        course_id = id(new_course)
        self.courses_map[course_id] = new_course
        return course_id

    def delete_course(self, course_id) -> bool:
        del self.courses_map[course_id]
        return True

    def is_course_valid(self, course_id) -> bool:
        return course_id in self.courses_map

    def enroll_student(self, course_id, student_id) -> bool:
        course = self.courses_map[course_id]
        return course.enroll_student(student_id)

    def is_student_enrolled(self, course_id, student_id) -> bool:
        course = self.courses_map[course_id]
        return course.is_student_enrolled(student_id)

    def dropout_student(self, course_id, student_id) -> bool:
        course = self.courses_map[course_id]
        return course.dropout_student(student_id)

    def get_enrollment_list(self, course_id) -> List[str]:
        return self.courses_map[course_id].get_enrollment_list()
