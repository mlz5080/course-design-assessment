from app.dao.assignmentDAO import AssignmentDAOInterface
from app.model.assignment import Assignment

class PyObjAssignmentDAO(AssignmentDAOInterface):
    """
    Using Python internal data structure to store data.

    Attributes:
        assignment_map (dict): A hashMap of assignment_id mapping to PyObj assignment
        course_assignments_map (dict): 
            A hashMap of course_id mapping to assignment_id set. An assignment belongs
            to a course if assignment_id in course's assignment_id set.
    """
    def __init__(self):
        self.assignment_map = {}
        self.course_assignments_map = {}

    def get_assignment_by_id(self, assignment_id):
        return self.assignment_map[assignment_id]
    
    def create_assignment(self, course_id, assignment_name) -> int:
        new_assignment = Assignment(assignment_name)
        assignment_id = id(new_assignment)
        self.assignment_map[assignment_id] = new_assignment

        # Build search index
        course_assignments_set = self.course_assignments_map.get(course_id, set())
        course_assignments_set.add(assignment_id)
        self.course_assignments_map[course_id] = course_assignments_set
        return assignment_id

    def is_assignment_attached(self, course_id, assignment_id) -> bool:
        validation_result = assignment_id in self.assignment_map
        validation_result &= assignment_id in self.course_assignments_map[course_id]
        return validation_result

    def submit_assignment(self, assignment_id, student_id, grade) -> bool:
        return self.assignment_map[assignment_id].submit_assignment(student_id, grade)

    def delete_student_submissions(self, course_id, student_id):
        for assignment_id in self.course_assignments_map[course_id]:
            self.assignment_map[assignment_id].delete_submission(student_id)

        return True

    def delete_course_assignments(self, course_id) -> bool:
        if course_id in self.course_assignments_map:
            for assignment_id in self.course_assignments_map[course_id]:
                del self.assignment_map[assignment_id]
            return True

    def get_student_grades(self, course_id, student_id) -> list:
        if course_id in self.course_assignments_map:
            return [
                self.assignment_map[aid].get_student_grade(student_id)
                    for aid in self.course_assignments_map[course_id]
            ]

    def get_assignment_submissions(self, assignment_id) -> list:
        return self.assignment_map[assignment_id].get_submissions()
