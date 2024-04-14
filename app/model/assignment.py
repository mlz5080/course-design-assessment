class Assignment():
    """
    Python Class definition of Assignment.

    Attributes:
        assignment_name (str)
        student_submission (dict): A hash map of student_id and grade.
    """

    def __init__(self, assignment_name):
        self.assignment_name = assignment_name
        self.student_submission = {}

    def submit_assignment(self, student_id, grade):
        self.student_submission[student_id] = grade
        return True

    def delete_submission(self, student_id):
        if student_id in self.student_submission:
            del self.student_submission[student_id]

    def get_submissions(self):
        return self.student_submission.values()

    def get_student_grade(self, student_id):
        return self.student_submission.get(student_id, 0)
