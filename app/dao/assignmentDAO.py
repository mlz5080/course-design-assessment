from abc import ABC, abstractmethod


class AssignmentDAOInterface():
    """
    Course DAO interface definition.
    Moving to another persistance should always implement these functions.
    """

    @abstractmethod
    def get_assignment_by_id(self, assignment_id) -> str:
        pass

    @abstractmethod
    def create_assignment(self, course_id, assignment_name) -> int:
        pass

    @abstractmethod
    def is_assignment_attached(self, couse_id, assignment_id) -> bool:
        pass

    @abstractmethod
    def submit_assignment(self, assignment_id, student_id, grade) -> bool:
        pass

    @abstractmethod
    def delete_student_submissions(self, course_id, student_id) -> bool:
        pass

    @abstractmethod
    def delete_course_assignments(self, course_id) -> bool:
        pass

    @abstractmethod
    def get_student_grades(self, course_id, student_id) -> list:
        pass

    @abstractmethod
    def get_assignment_submissions(self, course_id, assignment_id) -> list:
        pass
