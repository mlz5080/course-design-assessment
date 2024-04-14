import unittest
import random
from app.course_service_impl import CourseServiceImpl

class HappyPathTestCase(unittest.TestCase):

    def setUp(self):
        self.course_service = CourseServiceImpl()
        self.course_names = (
            "Big Data Analysis",
            "Algorithm and Data Structure"
        )
        self.assignment_names = (
            "Midterm Exam",
            "Final Exam"
        )
        self.course_id_list = [self.course_service.create_course(name) for name in self.course_names]
        
        self.course_assignment_map = {
            cid: [] for cid in self.course_id_list
        }

        for cid in self.course_id_list:
            for assignment_name in self.assignment_names:
                aid = self.course_service.create_assignment(cid, assignment_name)
                self.course_assignment_map[cid].append(aid)

        self.student_id = 1
        self.course_id_1 = self.course_id_list[0]
        self.assignment_id_1 = self.course_assignment_map[self.course_id_1][0]

        self.assignment_grades = [80, 85]
        self.expected_avg_grade = int(sum(self.assignment_grades)/len(self.assignment_grades))

        self.student_grades = [random.randint(0, 100) for i in range(30)]
        self.expected_course_avg_grade = int(sum(self.student_grades)/len(self.student_grades))

        self.expected_top_students = set([2, 3, 5, 7, 11])

    def tearDown(self):
        for cid in self.course_id_list:
            self.course_service.delete_course(cid)

class TestCourseServiceHappyPath(HappyPathTestCase):

    def test_get_courses(self):
        self.assertEqual(
            set([course["course_id"] for course in self.course_service.get_courses()]),
            set(self.course_id_list)
        )

    def test_get_course_by_id(self):
        course = self.course_service.get_course_by_id(self.course_id_1)
        self.assertEqual(self.course_id_1, course["course_id"])
        self.assertEqual(self.course_names[0], course["course_name"])

    def test_create_course(self):
        new_course = "Intro to Machine Learning"
        course_id = self.course_service.create_course(new_course)
        course = self.course_service.get_course_by_id(course_id)
        self.assertEqual(new_course, course["course_name"])
        self.assertEqual(course_id, course["course_id"])
        self.course_service.delete_course(course_id)

    def test_delete_course(self):
        course_id = self.course_id_list.pop(0)
        self.course_service.delete_course(course_id)
        courses_list = set([course["course_id"] for course in self.course_service.get_courses()])
        self.assertTrue(course_id not in courses_list)

    def test_create_assignment(self):
        self.assertIsNotNone(self.course_service.create_assignment(self.course_id_1, "Quiz"))
    
    def test_enroll_student(self):
        for cid in self.course_id_list:
            for sid in range(1, 31):
                self.assertTrue(self.course_service.enroll_student(cid, sid))

    def test_submit_assignments(self):
        self.course_service.enroll_student(self.course_id_1, self.student_id)
        self.assertTrue(
            self.course_service.submit_assignment(
                self.course_id_1, self.student_id, self.assignment_id_1, 80))

        self.assertEqual(
            self.course_service.get_assignment_grade_avg(self.course_id_1, self.assignment_id_1),80)

    def test_dropout_student(self):
        self.course_service.enroll_student(self.course_id_1, self.student_id)
        self.assertTrue(self.course_service.dropout_student(self.course_id_1, self.student_id))

    def test_get_student_grade_avg(self):
        self.course_service.enroll_student(self.course_id_1, self.student_id)
        for i, aid in enumerate(self.course_assignment_map[self.course_id_1]):
            self.course_service.submit_assignment(self.course_id_1, self.student_id, aid, self.assignment_grades[i])

        self.assertEqual(
            self.expected_avg_grade,
            self.course_service.get_student_grade_avg(self.course_id_1, self.student_id))

    def test_get_assignment_grade_avg(self):
        for sid in range(1, 31):
            self.assertTrue(self.course_service.enroll_student(self.course_id_1, sid))
            self.assertTrue(
                self.course_service.submit_assignment(
                    self.course_id_1,
                    sid,
                    self.assignment_id_1,
                    self.student_grades[sid-1])
            )

        self.assertTrue(
            self.expected_course_avg_grade,
            self.course_service.get_assignment_grade_avg(self.course_id_1, self.assignment_id_1))

    def test_get_top_five_students(self):
        for cid in self.course_id_list:
            for sid in range(1, 31):
                self.course_service.enroll_student(cid, sid)
                grade = 100 if sid in self.expected_top_students else random.randint(0, 80)
                for aid in self.course_assignment_map[cid]:
                    self.course_service.submit_assignment(cid, sid, aid, grade)
            get_top_5_students = set(self.course_service.get_top_five_students(cid))
            self.assertEqual(get_top_5_students, self.expected_top_students)

if __name__ == '__main__':
    unittest.main()
