class Course():
    """
    Python Class definition of Assignment.

    Attributes:
        course_name (str)
        enrollment_set (set): A hashset of student_id enrolled to this course.
    """

    def __init__(self, course_name):
        self.course_name = course_name
        self.enrollment_set = set()

    def enroll_student(self, student_id):
        self.enrollment_set.add(student_id)
        return True

    def is_student_enrolled(self, student_id):
        return student_id in self.enrollment_set

    def dropout_student(self, student_id):
        self.enrollment_set.remove(student_id)
        return True

    def get_enrollment_list(self):
        return list(self.enrollment_set)

    def dict_representation(self):
        return {
            "course_name": self.course_name,
            "course_id": id(self),
            "course_enrollment": str(self.enrollment_set)
        }
