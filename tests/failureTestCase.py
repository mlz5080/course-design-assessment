import unittest
from app.course_service_impl import CourseServiceImpl

class ExpectedFailureTestCase(unittest.TestCase):

    def setUp(self):
        self.course_service = CourseServiceImpl()
        self.course_name = "Big Data Analysis"
        self.assignment_name = "Midterm Exam"
        self.student_id = 1
        self.course_id = self.course_service.create_course(self.course_name)
        self.assignment_id = self.course_service.create_assignment(self.course_id, self.assignment_name)
        self.invalid_course_id = self.course_id + 1
        self.invalid_student_id = self.student_id + 1
        self.invalid_assignment_id = self.assignment_id + 1

    def tearDown(self):
        self.course_service.delete_course(self.course_id)

class TestCourseServiceUnhappyPath(ExpectedFailureTestCase):

    @unittest.expectedFailure
    def test_get_course_by_invalid_id(self):
        course = self.course_service.get_course_by_id(self.invalid_course_id)

    def test_delete_course_with_invalid_course_id(self):
        self.assertFalse(self.course_service.delete_course(self.invalid_course_id))

    def test_enroll_student_with_invalid_course_id(self):
        self.assertFalse(self.course_service.enroll_student(self.invalid_course_id, self.student_id))

    def test_dropout_student_with_invalid_inputs(self):
        self.assertFalse(self.course_service.dropout_student(self.invalid_course_id, self.invalid_student_id))
        self.assertFalse(self.course_service.dropout_student(self.course_id, self.invalid_student_id))

    def test_submit_assignment_with_invalid_inputs(self):
        self.course_service.enroll_student(self.course_id, self.student_id)
        self.assertFalse(
            self.course_service.submit_assignment(
                self.course_id, self.student_id, self.assignment_id, -10))

        self.assertFalse(
            self.course_service.submit_assignment(
                self.invalid_course_id, self.student_id, self.assignment_id, 100))

        self.assertFalse(
            self.course_service.submit_assignment(
                self.course_id, self.invalid_student_id, self.assignment_id, 100))

        self.assertFalse(
            self.course_service.submit_assignment(
                self.course_id, self.student_id, self.invalid_assignment_id, 100))

        self.assertFalse(
            self.course_service.submit_assignment(
                self.invalid_course_id, self.invalid_student_id, self.invalid_assignment_id, -10))

    @unittest.expectedFailure
    def test_get_assignment_grade_avg_with_invalid_course_id(self):
        self.course_service.get_assignment_grade_avg(self.invalid_course_id, self.assignment_id)
    
    @unittest.expectedFailure
    def test_get_assignment_grade_avg_with_invalid_assignment_id(self):
        self.course_service.get_assignment_grade_avg(self.course_id, self.invalid_assignment_id)

    @unittest.expectedFailure
    def test_get_assignment_grade_avg_without_submission(self):
        self.course_service.get_assignment_grade_avg(self.course_id, self.assignment_id)

    @unittest.expectedFailure
    def test_get_assignment_grade_avg_with_different_assignment(self):
        assignment_id = self.course_service.create_assignment(self.course_id, "Test")
        self.course_service.enroll_student(self.course_id, self.student_id)
        self.assertTrue(self.course_service.submit_assignment(self.course_id, self.student_id, self.assignment_id, 60))
        self.assertEqual(self.course_service.get_assignment_grade_avg(self.course_id, assignment_id), 0)

    @unittest.expectedFailure
    def test_get_student_grade_avg_with_invalid_course_id(self):
        self.course_service.enroll_student(self.course_id, self.student_id)
        self.course_service.get_student_grade_avg(self.invalid_course_id, self.student_id)
    
    @unittest.expectedFailure
    def test_get_student_grade_avg_with_invalid_student_id(self):
        self.course_service.get_student_grade_avg(self.course_id, self.student_id)

    @unittest.expectedFailure
    def test_get_student_grade_avg_with_no_assignment(self):
        course_id = self.course_service.create_course(self.course_name)
        self.course_service.enroll_student(course_id, self.student_id)
        self.course_service.get_student_grade_avg(course_id, self.student_id)
        self.assertTrue(self.course_service.delete_course(course_id))

    @unittest.expectedFailure
    def test_get_top_five_students_with_invalid_course_id(self):
        self.course_service.get_top_five_students(self.invalid_course_id)

    @unittest.expectedFailure
    def test_get_top_five_students_with_no_submission(self):
        course_id = self.course_service.create_course(self.course_name)
        self.course_service.enroll_student(course_id, self.student_id)
        self.assertTrue(len(self.course_service.get_top_five_students(self.course_id))==0)
        self.assertTrue(self.course_service.delete_course(course_id))
