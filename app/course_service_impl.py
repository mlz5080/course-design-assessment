from dataclasses import dataclass
import heapq
from typing import List, Any, Annotated

from app.course_service import CourseService
from app.dao.impl.PyObjCourseDAOImpl import PyObjCourseDAO
from app.dao.impl.PyObjAssignmentDAOImpl import PyObjAssignmentDAO


class CourseServiceImpl(CourseService):
    """
    Please implement the CourseService interface according to the requirements.
    """
    def __init__(self):
        self.course_client = PyObjCourseDAO()
        self.assignment_client = PyObjAssignmentDAO()

    def get_courses(self) -> List[Any]:
        return self.course_client.get_courses_list()

    def get_course_by_id(self, course_id) -> Any:
        self.is_input_valid(course_id, is_raising_error=True)
        return self.course_client.get_course_by_id(course_id)
    
    def create_course(self, course_name) -> int:
        course_id = self.course_client.create_course(course_name)
        return course_id

    def delete_course(self, course_id) -> bool:
        if not self.is_input_valid(course_id, is_raising_error=False):
            return False
        result = self.course_client.delete_course(course_id)
        return result and self.assignment_client.delete_course_assignments(course_id)
    
    def create_assignment(self, course_id, assignment_name) -> int:
        # Assuming that system creates new assignment even a duplicate name exists
        assignment_id = self.assignment_client.create_assignment(course_id, assignment_name)
        return assignment_id
    
    def enroll_student(self, course_id, student_id) -> bool:
        if not self.is_input_valid(
            course_id, student_id=student_id, enrolling=True, is_raising_error=False
        ):
            return False
        return self.course_client.enroll_student(course_id, student_id)
    
    def dropout_student(self, course_id, student_id) -> bool:
        if not self.is_input_valid(course_id, student_id=student_id, is_raising_error=False):
            return False
        result = self.course_client.dropout_student(course_id, student_id)
        return result and self.assignment_client.delete_student_submissions(course_id, student_id)
    
    def submit_assignment(self, course_id, student_id, assignment_id, grade) -> bool:
        if not self.is_input_valid(
            course_id,
            student_id=student_id,
            assignment_id=assignment_id,
            grade=grade,
            is_raising_error=False
        ):
            return False
        # Assuming that student can submit an assignment multiple times
        return self.assignment_client.submit_assignment(assignment_id, student_id, grade)
    
    def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
        self.is_input_valid(
            course_id, assignment_id=assignment_id, is_raising_error=True)

        assignment_grades = self.assignment_client.get_assignment_submissions(assignment_id)

        if len(assignment_grades) == 0:
            # rasing error to prevent divisionByZero exception
            raise AttributeError(
                "No submissions received for this assignment {}".format(assignment_id))

        return int(sum(assignment_grades)/len(assignment_grades))
    
    def get_student_grade_avg(self, course_id, student_id) -> int:
        self.is_input_valid(course_id, student_id=student_id, is_raising_error=True)

        students_grades_list = self.assignment_client.get_student_grades(course_id, student_id)
        students_grades = sum(students_grades_list)
        len_grades = len(students_grades_list)

        # If no assignment attached for this course, raise error
        if len_grades == 0:
            raise AttributeError(
                "No assignments attached to this course_id {}".format(course_id))

        return int(students_grades/len_grades)
    
    def get_top_five_students(self, course_id) -> List[int]:
        self.is_input_valid(course_id, is_raising_error=True)

        enrollment_list = self.course_client.get_enrollment_list(course_id)
        student_id_grade_list = []
        for sid in enrollment_list:
            student_id_grade = (self.get_student_grade_avg(course_id, sid), sid)
            student_id_grade_list.append(student_id_grade)

        # Use heapq to keep track the top 5 students
        top_five_students_heap = []
        for sid_grade in student_id_grade_list:
            heapq.heappush(top_five_students_heap, sid_grade)
            if len(top_five_students_heap) > 5:
                heapq.heappop(top_five_students_heap)

        return [grade_id[1] for grade_id in top_five_students_heap]

    def is_input_valid(self, course_id, **kwargs):
        """Validation function to validate inputs
        
        Parameters:
        course_id (int)
        **kwargs:
            student_id (int)
            assignment_id (int)
            grade (int)
            is_raising_error (bool)

        Returns:
        bool: if is_raising_error flag is False

        Raise:
        ValueError 
        """
        error_message = lambda x, y: "Invalid {} {}".format(x, y)
        if not self.course_client.is_course_valid(course_id):
            if kwargs.get("is_raising_error", False):
                raise ValueError(error_message("course_id", course_id))
            return False
        elif kwargs.get("student_id", None) is not None:
            student_id = kwargs["student_id"]
            enrolling = kwargs.get("enrolling", False)
            # enrolling but already enrolled or not enrolled and not enrolling)
            if not (self.course_client.is_student_enrolled(course_id, student_id) != enrolling):
                if kwargs.get("is_raising_error", False):
                    raise ValueError(error_message("student_id", student_id))
                return False
        if kwargs.get("assignment_id", None) is not None:
            assignment_id = kwargs["assignment_id"]
            if not self.assignment_client.is_assignment_attached(course_id, assignment_id):
                if kwargs.get("is_raising_error", False):
                    raise ValueError(error_message("assignment_id", assignment_id))
                return False
        if kwargs.get("grade", None) is not None:
            grade = kwargs["grade"]
            if grade < 0 or grade > 100:
                # Validating grade never raise error
                return False
        return True
