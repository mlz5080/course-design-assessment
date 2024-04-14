import random
from app.course_service_impl import CourseServiceImpl

if __name__ == "__main__":
  course_service = CourseServiceImpl()
  course_names = ("Big Data Analysis", "Algorithm and Data Structure")
  assignment_names = ("Midterm Exam", "Final Exam")
  students_list = list(range(1, 12))
  expected_top_students = set([1, 2, 3, 5, 7, 11])

  # Start receiving requests...
  courses_id = [course_service.create_course(name) for name in course_names]
  course_assignments_map = { cid:list() for cid in courses_id}
  
  # Create assignments
  for cid in courses_id:
    for name in assignment_names:
      aid = course_service.create_assignment(cid, name)
      course_assignments_map[cid].append(aid)

  big_data_assignment_id = course_assignments_map[courses_id[0]][0]

  # Enrolling students and submit assignments
  # Student 2,3,5,7,11 are expected top students
  for cid in courses_id:
    for sid in students_list:
        course_service.enroll_student(cid, sid)
        for aid in course_assignments_map[cid]:
            grade = 100 if sid in expected_top_students else random.randint(50, 90)
            if not course_service.submit_assignment(cid, sid, aid, grade):
                raise Exception(
                    "Student {} could not submit assignment {}".format(sid, aid))
  
  assignment_grade_avg = course_service.get_assignment_grade_avg(
    courses_id[0], big_data_assignment_id)

  print("{} assignment 1 average grade: {}".format(
    course_names[0], assignment_grade_avg))

  print(
    "Student 1 average grade: {}".format(
        course_service.get_student_grade_avg(courses_id[0], 1)))

  print("Student 1 dropped from Big Data Analysis, expecting average grade change")
  course_service.dropout_student(courses_id[0], 1)
  expected_top_students.remove(1)

  print(
    "{} assignment 1 average grade after student 1 dropout: {}\n".format(
        course_names[0],
        course_service.get_assignment_grade_avg(courses_id[0], big_data_assignment_id))
  )

  print(
    "Expected top student id 2 grade: {}".format(
        course_service.get_student_grade_avg(courses_id[0], 2)))
  
  print(
    "Top 5 students from {} are: {}\n".format(
        course_names[0], course_service.get_top_five_students(courses_id[0])))
  
  print("All courses name:",
    [course["course_name"] for course in course_service.get_courses()])

  print("Use get_course_by_id to read second course name")

  print("Second course name: {}\n".format(
    course_service.get_course_by_id(courses_id[1])["course_name"]))

  print("Deleting second course")
  course_service.delete_course(courses_id[1])
  try:
    print("Try reading second course")
    course_service.get_course_by_id(courses_id[1])
  except Exception as e:
    print(e)
    print("Second course is deleted as expected")

