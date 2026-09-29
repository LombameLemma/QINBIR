from app.database import engine, Base

from app.models.user import User
from app.models.department import Department
from app.models.program import Program
from app.models.course import Course
from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.student_section import StudentSection
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.models.lecturer_availability import LecturerAvailability
from app.models.course_requirement import CourseRequirement
from app.models.schedule import Schedule
from app.models.schedule_entry import ScheduleEntry
from app.models.constraint import Constraint


Base.metadata.create_all(bind=engine)


print("QINBIR database created successfully!")
print("Users table created successfully!")
print("Departments table created successfully!")
print("Programs table created successfully!")
print("Courses table created successfully!")
print("Lecturers table created successfully!")
print("Students table created successfully!")
print("Student sections table created successfully!")
print("Rooms table created successfully!")
print("Time slots table created successfully!")
print("Lecturer availability table created successfully!")
print("Course requirements table created successfully!")
print("Schedules table created successfully!")
print("Schedule entries table created successfully!")
print("Constraints table created successfully!")