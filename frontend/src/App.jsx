
import { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  useLocation,
} from "react-router-dom";

const API_BASE_URL = "http://127.0.0.1:8000";

/* =========================================================
   API HELPER
========================================================= */

async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const contentType = response.headers.get("content-type");
  const data = contentType?.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof data === "object" && data?.detail
        ? data.detail
        : "Something went wrong.";

    throw new Error(message);
  }

  return data;
}

/* =========================================================
   TIME FORMATTER
   Backend keeps 24-hour time.
   Frontend displays 12-hour AM/PM time.
========================================================= */

function formatTime(time) {
  if (!time) {
    return "";
  }

  const cleanTime = String(time).slice(0, 5);
  const [hourString, minuteString] = cleanTime.split(":");

  const hour = Number(hourString);
  const minute = Number(minuteString);

  if (Number.isNaN(hour) || Number.isNaN(minute)) {
    return time;
  }

  const period = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;

  return `${displayHour}:${String(minute).padStart(2, "0")} ${period}`;
}

/* =========================================================
   SIDEBAR
========================================================= */

function Sidebar() {
  const navItems = [
    { path: "/", label: "Dashboard" },
    { path: "/departments", label: "Departments" },
    { path: "/programs", label: "Programs" },
    { path: "/courses", label: "Courses" },
    { path: "/lecturers", label: "Lecturers" },
    { path: "/student-sections", label: "Student Sections" },
    { path: "/rooms", label: "Rooms" },
    { path: "/time-slots", label: "Time Slots" },
    {
      path: "/lecturer-availability",
      label: "Lecturer Availability",
    },
    {
      path: "/course-requirements",
      label: "Course Requirements",
    },
    { path: "/constraints", label: "Constraints" },
    { path: "/generate-schedule", label: "Generate Schedule" },
    { path: "/timetable", label: "Timetable" },
  ];

  return (
    <aside className="sidebar">
      <div className="logo">
        <h1>QINBIR</h1>
        <span>Smart Scheduler</span>
      </div>

      <nav>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

/* =========================================================
   TOP BAR
========================================================= */

function TopBar() {
  const [apiConnected, setApiConnected] = useState(false);

  useEffect(() => {
    apiRequest("/health")
      .then(() => setApiConnected(true))
      .catch(() => setApiConnected(false));
  }, []);

  return (
    <header className="topbar">
      <div>
        <strong>QINBIR</strong>
      </div>

      <div className="api-status">
        <span
          style={{
            background: apiConnected ? "#22c55e" : "#ef4444",
          }}
        ></span>

        {apiConnected ? "API Connected" : "API Disconnected"}
      </div>
    </header>
  );
}

/* =========================================================
   LAYOUT
========================================================= */

function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />

      <div className="content">
        <TopBar />

        <main className="page-content">{children}</main>
      </div>
    </div>
  );
}

/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <p>
        Welcome to QINBIR, the automatic university course scheduling
        system.
      </p>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Departments</h3>
          <p>Manage university departments.</p>
        </div>

        <div className="dashboard-card">
          <h3>Programs</h3>
          <p>Manage academic programs.</p>
        </div>

        <div className="dashboard-card">
          <h3>Courses</h3>
          <p>Manage university courses.</p>
        </div>

        <div className="dashboard-card">
          <h3>Lecturers</h3>
          <p>Manage lecturers and instructors.</p>
        </div>

        <div className="dashboard-card">
          <h3>Student Sections</h3>
          <p>Manage student groups and sections.</p>
        </div>

        <div className="dashboard-card">
          <h3>Rooms</h3>
          <p>Manage classrooms and capacities.</p>
        </div>

        <div className="dashboard-card">
          <h3>Time Slots</h3>
          <p>Manage available university time slots.</p>
        </div>

        <div className="dashboard-card">
          <h3>Timetable</h3>
          <p>View automatically generated schedules.</p>
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   DEPARTMENTS
========================================================= */

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");

  async function loadDepartments() {
    try {
      const data = await apiRequest("/departments/");
      setDepartments(data);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadDepartments();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/departments/", {
        method: "POST",
        body: JSON.stringify({
          name,
          code,
        }),
      });

      setName("");
      setCode("");
      setMessage("Department created successfully.");
      loadDepartments();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>Departments</h1>
      <p>Manage university departments.</p>

      <div className="form-card">
        <h2>Add Department</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Computer Science"
                required
              />
            </div>

            <div className="form-group">
              <label>Code</label>

              <input
                value={code}
                onChange={(event) => setCode(event.target.value)}
                placeholder="CS"
                required
              />
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Department
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Department List</h2>

          <button
            className="secondary-button"
            onClick={loadDepartments}
          >
            Refresh
          </button>
        </div>

        {departments.length === 0 ? (
          <p className="empty-message">No departments found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Code</th>
              </tr>
            </thead>

            <tbody>
              {departments.map((department) => (
                <tr key={department.id}>
                  <td>{department.id}</td>
                  <td>{department.name}</td>
                  <td>{department.code}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   PROGRAMS
========================================================= */

function Programs() {
  const [programs, setPrograms] = useState([]);
  const [departments, setDepartments] = useState([]);

  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [departmentId, setDepartmentId] = useState("");

  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [programData, departmentData] = await Promise.all([
        apiRequest("/programs/"),
        apiRequest("/departments/"),
      ]);

      setPrograms(programData);
      setDepartments(departmentData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/programs/", {
        method: "POST",
        body: JSON.stringify({
          name,
          code,
          department_id: Number(departmentId),
        }),
      });

      setName("");
      setCode("");
      setDepartmentId("");
      setMessage("Program created successfully.");

      loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  function getDepartmentName(id) {
    const department = departments.find(
      (item) => item.id === id
    );

    return department
      ? `${department.name} (${department.code})`
      : `Department ${id}`;
  }

  return (
    <div>
      <h1>Programs</h1>
      <p>Manage academic programs.</p>

      <div className="form-card">
        <h2>Add Program</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Software Engineering"
                required
              />
            </div>

            <div className="form-group">
              <label>Code</label>

              <input
                value={code}
                onChange={(event) => setCode(event.target.value)}
                placeholder="SE"
                required
              />
            </div>

            <div className="form-group">
              <label>Department</label>

              <select
                value={departmentId}
                onChange={(event) =>
                  setDepartmentId(event.target.value)
                }
                required
              >
                <option value="">Select Department</option>

                {departments.map((department) => (
                  <option
                    key={department.id}
                    value={department.id}
                  >
                    {department.name} ({department.code})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Program
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Program List</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        {programs.length === 0 ? (
          <p className="empty-message">No programs found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Code</th>
                <th>Department</th>
              </tr>
            </thead>

            <tbody>
              {programs.map((program) => (
                <tr key={program.id}>
                  <td>{program.id}</td>
                  <td>{program.name}</td>
                  <td>{program.code}</td>
                  <td>
                    {getDepartmentName(program.department_id)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   COURSES
========================================================= */

function Courses() {
  const [courses, setCourses] = useState([]);
  const [programs, setPrograms] = useState([]);

  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [creditHours, setCreditHours] = useState("");
  const [programId, setProgramId] = useState("");

  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [courseData, programData] = await Promise.all([
        apiRequest("/courses/"),
        apiRequest("/programs/"),
      ]);

      setCourses(courseData);
      setPrograms(programData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/courses/", {
        method: "POST",
        body: JSON.stringify({
          code,
          name,
          credit_hours: Number(creditHours),
          program_id: Number(programId),
        }),
      });

      setCode("");
      setName("");
      setCreditHours("");
      setProgramId("");

      setMessage("Course created successfully.");

      loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  function getProgramName(id) {
    const program = programs.find((item) => item.id === id);

    return program
      ? `${program.name} (${program.code})`
      : `Program ${id}`;
  }

  return (
    <div>
      <h1>Courses</h1>
      <p>Manage university courses.</p>

      <div className="form-card">
        <h2>Add Course</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Course Code</label>

              <input
                value={code}
                onChange={(event) => setCode(event.target.value)}
                placeholder="SE201"
                required
              />
            </div>

            <div className="form-group">
              <label>Course Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Database Systems"
                required
              />
            </div>

            <div className="form-group">
              <label>Credit Hours</label>

              <input
                type="number"
                min="1"
                value={creditHours}
                onChange={(event) =>
                  setCreditHours(event.target.value)
                }
                placeholder="3"
                required
              />
            </div>

            <div className="form-group">
              <label>Program</label>

              <select
                value={programId}
                onChange={(event) =>
                  setProgramId(event.target.value)
                }
                required
              >
                <option value="">Select Program</option>

                {programs.map((program) => (
                  <option key={program.id} value={program.id}>
                    {program.name} ({program.code})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Course
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Course List</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        {courses.length === 0 ? (
          <p className="empty-message">No courses found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Code</th>
                <th>Name</th>
                <th>Credits</th>
                <th>Program</th>
              </tr>
            </thead>

            <tbody>
              {courses.map((course) => (
                <tr key={course.id}>
                  <td>{course.id}</td>
                  <td>{course.code}</td>
                  <td>{course.name}</td>
                  <td>{course.credit_hours}</td>
                  <td>{getProgramName(course.program_id)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   LECTURERS
========================================================= */

function Lecturers() {
  const [lecturers, setLecturers] = useState([]);
  const [users, setUsers] = useState([]);
  const [departments, setDepartments] = useState([]);

  const [userId, setUserId] = useState("");
  const [departmentId, setDepartmentId] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [name, setName] = useState("");

  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [lecturerData, userData, departmentData] =
        await Promise.all([
          apiRequest("/lecturers/"),
          apiRequest("/users/"),
          apiRequest("/departments/"),
        ]);

      setLecturers(lecturerData);
      setUsers(userData);
      setDepartments(departmentData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/lecturers/", {
        method: "POST",
        body: JSON.stringify({
          user_id: Number(userId),
          department_id: Number(departmentId),
          employee_id: employeeId,
          name,
        }),
      });

      setUserId("");
      setDepartmentId("");
      setEmployeeId("");
      setName("");

      setMessage("Lecturer created successfully.");

      loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  function getDepartmentName(id) {
    const department = departments.find(
      (item) => item.id === id
    );

    return department
      ? `${department.name} (${department.code})`
      : `Department ${id}`;
  }

  return (
    <div>
      <h1>Lecturers</h1>
      <p>Manage university lecturers.</p>

      <div className="form-card">
        <h2>Add Lecturer</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>User</label>

              <select
                value={userId}
                onChange={(event) =>
                  setUserId(event.target.value)
                }
                required
              >
                <option value="">Select User</option>

                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.full_name} - {user.email}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Department</label>

              <select
                value={departmentId}
                onChange={(event) =>
                  setDepartmentId(event.target.value)
                }
                required
              >
                <option value="">Select Department</option>

                {departments.map((department) => (
                  <option
                    key={department.id}
                    value={department.id}
                  >
                    {department.name} ({department.code})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Employee ID</label>

              <input
                value={employeeId}
                onChange={(event) =>
                  setEmployeeId(event.target.value)
                }
                placeholder="LEC003"
                required
              />
            </div>

            <div className="form-group">
              <label>Lecturer Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Dr. Name"
                required
              />
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Lecturer
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Lecturer List</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        {lecturers.length === 0 ? (
          <p className="empty-message">No lecturers found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Employee ID</th>
                <th>Name</th>
                <th>Department</th>
                <th>User ID</th>
              </tr>
            </thead>

            <tbody>
              {lecturers.map((lecturer) => (
                <tr key={lecturer.id}>
                  <td>{lecturer.id}</td>
                  <td>{lecturer.employee_id}</td>
                  <td>{lecturer.name}</td>
                  <td>
                    {getDepartmentName(lecturer.department_id)}
                  </td>
                  <td>{lecturer.user_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   STUDENT SECTIONS
========================================================= */

function StudentSections() {
  const [sections, setSections] = useState([]);
  const [programs, setPrograms] = useState([]);

  const [name, setName] = useState("");
  const [programId, setProgramId] = useState("");
  const [year, setYear] = useState("");
  const [semester, setSemester] = useState("");
  const [studentCount, setStudentCount] = useState("");

  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [sectionData, programData] = await Promise.all([
        apiRequest("/student-sections/"),
        apiRequest("/programs/"),
      ]);

      setSections(sectionData);
      setPrograms(programData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/student-sections/", {
        method: "POST",
        body: JSON.stringify({
          name,
          program_id: Number(programId),
          year: Number(year),
          semester: Number(semester),
          student_count: Number(studentCount),
        }),
      });

      setName("");
      setProgramId("");
      setYear("");
      setSemester("");
      setStudentCount("");

      setMessage("Student section created successfully.");

      loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  function getProgramName(id) {
    const program = programs.find((item) => item.id === id);

    return program
      ? `${program.name} (${program.code})`
      : `Program ${id}`;
  }

  return (
    <div>
      <h1>Student Sections</h1>
      <p>Manage student sections.</p>

      <div className="form-card">
        <h2>Add Student Section</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Section Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="SE Year 2 Section C"
                required
              />
            </div>

            <div className="form-group">
              <label>Program</label>

              <select
                value={programId}
                onChange={(event) =>
                  setProgramId(event.target.value)
                }
                required
              >
                <option value="">Select Program</option>

                {programs.map((program) => (
                  <option key={program.id} value={program.id}>
                    {program.name} ({program.code})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Year</label>

              <input
                type="number"
                min="1"
                value={year}
                onChange={(event) => setYear(event.target.value)}
                placeholder="2"
                required
              />
            </div>

            <div className="form-group">
              <label>Semester</label>

              <input
                type="number"
                min="1"
                value={semester}
                onChange={(event) =>
                  setSemester(event.target.value)
                }
                placeholder="1"
                required
              />
            </div>

            <div className="form-group">
              <label>Student Count</label>

              <input
                type="number"
                min="1"
                value={studentCount}
                onChange={(event) =>
                  setStudentCount(event.target.value)
                }
                placeholder="40"
                required
              />
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Section
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Student Section List</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        {sections.length === 0 ? (
          <p className="empty-message">
            No student sections found.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Section</th>
                <th>Program</th>
                <th>Year</th>
                <th>Semester</th>
                <th>Students</th>
              </tr>
            </thead>

            <tbody>
              {sections.map((section) => (
                <tr key={section.id}>
                  <td>{section.id}</td>
                  <td>{section.name}</td>
                  <td>{getProgramName(section.program_id)}</td>
                  <td>{section.year}</td>
                  <td>{section.semester}</td>
                  <td>{section.student_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   ROOMS
========================================================= */

function Rooms() {
  const [rooms, setRooms] = useState([]);

  const [name, setName] = useState("");
  const [building, setBuilding] = useState("");
  const [capacity, setCapacity] = useState("");
  const [roomType, setRoomType] = useState("");

  const [message, setMessage] = useState("");

  async function loadRooms() {
    try {
      const data = await apiRequest("/rooms/");
      setRooms(data);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadRooms();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/rooms/", {
        method: "POST",
        body: JSON.stringify({
          name,
          building,
          capacity: Number(capacity),
          room_type: roomType,
        }),
      });

      setName("");
      setBuilding("");
      setCapacity("");
      setRoomType("");

      setMessage("Room created successfully.");

      loadRooms();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>Rooms</h1>
      <p>Manage classrooms and rooms.</p>

      <div className="form-card">
        <h2>Add Room</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Room Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Room 203"
                required
              />
            </div>

            <div className="form-group">
              <label>Building</label>

              <input
                value={building}
                onChange={(event) =>
                  setBuilding(event.target.value)
                }
                placeholder="Main Building"
                required
              />
            </div>

            <div className="form-group">
              <label>Capacity</label>

              <input
                type="number"
                min="1"
                value={capacity}
                onChange={(event) =>
                  setCapacity(event.target.value)
                }
                placeholder="60"
                required
              />
            </div>

            <div className="form-group">
              <label>Room Type</label>

              <input
                value={roomType}
                onChange={(event) =>
                  setRoomType(event.target.value)
                }
                placeholder="Classroom"
                required
              />
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Room
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Room List</h2>

          <button
            className="secondary-button"
            onClick={loadRooms}
          >
            Refresh
          </button>
        </div>

        {rooms.length === 0 ? (
          <p className="empty-message">No rooms found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Building</th>
                <th>Capacity</th>
                <th>Type</th>
              </tr>
            </thead>

            <tbody>
              {rooms.map((room) => (
                <tr key={room.id}>
                  <td>{room.id}</td>
                  <td>{room.name}</td>
                  <td>{room.building}</td>
                  <td>{room.capacity}</td>
                  <td>{room.room_type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   TIME SLOTS
========================================================= */

function TimeSlots() {
  const [timeSlots, setTimeSlots] = useState([]);

  const [day, setDay] = useState("Monday");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  const [message, setMessage] = useState("");

  async function loadTimeSlots() {
    try {
      const data = await apiRequest("/time-slots/");
      setTimeSlots(data);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadTimeSlots();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/time-slots/", {
        method: "POST",
        body: JSON.stringify({
          day,
          start_time: startTime,
          end_time: endTime,
        }),
      });

      setStartTime("");
      setEndTime("");

      setMessage("Time slot created successfully.");

      loadTimeSlots();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>Time Slots</h1>
      <p>Manage university scheduling time slots.</p>

      <div className="form-card">
        <h2>Add Time Slot</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Day</label>

              <select
                value={day}
                onChange={(event) => setDay(event.target.value)}
              >
                <option>Monday</option>
                <option>Tuesday</option>
                <option>Wednesday</option>
                <option>Thursday</option>
                <option>Friday</option>
                <option>Saturday</option>
                <option>Sunday</option>
              </select>
            </div>

            <div className="form-group">
              <label>Start Time</label>

              <input
                type="time"
                value={startTime}
                onChange={(event) =>
                  setStartTime(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>End Time</label>

              <input
                type="time"
                value={endTime}
                onChange={(event) =>
                  setEndTime(event.target.value)
                }
                required
              />
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Time Slot
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Time Slot List</h2>

          <button
            className="secondary-button"
            onClick={loadTimeSlots}
          >
            Refresh
          </button>
        </div>

        {timeSlots.length === 0 ? (
          <p className="empty-message">No time slots found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Day</th>
                <th>Start Time</th>
                <th>End Time</th>
              </tr>
            </thead>

            <tbody>
              {timeSlots.map((slot) => (
                <tr key={slot.id}>
                  <td>{slot.id}</td>
                  <td>{slot.day}</td>

                  <td>{formatTime(slot.start_time)}</td>

                  <td>{formatTime(slot.end_time)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   LECTURER AVAILABILITY
========================================================= */

function LecturerAvailability() {
  const [availability, setAvailability] = useState([]);
  const [lecturers, setLecturers] = useState([]);
  const [timeSlots, setTimeSlots] = useState([]);

  const [lecturerId, setLecturerId] = useState("");
  const [timeSlotId, setTimeSlotId] = useState("");
  const [isAvailable, setIsAvailable] = useState(true);

  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [
        availabilityData,
        lecturerData,
        timeSlotData,
      ] = await Promise.all([
        apiRequest("/lecturer-availability/"),
        apiRequest("/lecturers/"),
        apiRequest("/time-slots/"),
      ]);

      setAvailability(availabilityData);
      setLecturers(lecturerData);
      setTimeSlots(timeSlotData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/lecturer-availability/", {
        method: "POST",
        body: JSON.stringify({
          lecturer_id: Number(lecturerId),
          time_slot_id: Number(timeSlotId),
          is_available: isAvailable,
        }),
      });

      setLecturerId("");
      setTimeSlotId("");
      setIsAvailable(true);

      setMessage("Lecturer availability saved successfully.");

      loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  function getLecturerName(id) {
    const lecturer = lecturers.find(
      (item) => item.id === id
    );

    return lecturer
      ? lecturer.name
      : `Lecturer ${id}`;
  }

  function getTimeSlot(id) {
    const slot = timeSlots.find((item) => item.id === id);

    return slot
      ? `${slot.day} ${formatTime(slot.start_time)} - ${formatTime(
          slot.end_time
        )}`
      : `Time Slot ${id}`;
  }

  return (
    <div>
      <h1>Lecturer Availability</h1>
      <p>Manage lecturer availability.</p>

      <div className="form-card">
        <h2>Add Availability</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Lecturer</label>

              <select
                value={lecturerId}
                onChange={(event) =>
                  setLecturerId(event.target.value)
                }
                required
              >
                <option value="">Select Lecturer</option>

                {lecturers.map((lecturer) => (
                  <option
                    key={lecturer.id}
                    value={lecturer.id}
                  >
                    {lecturer.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Time Slot</label>

              <select
                value={timeSlotId}
                onChange={(event) =>
                  setTimeSlotId(event.target.value)
                }
                required
              >
                <option value="">Select Time Slot</option>

                {timeSlots.map((slot) => (
                  <option key={slot.id} value={slot.id}>
                    {slot.day} {formatTime(slot.start_time)} -{" "}
                    {formatTime(slot.end_time)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Availability</label>

              <select
                value={isAvailable ? "true" : "false"}
                onChange={(event) =>
                  setIsAvailable(
                    event.target.value === "true"
                  )
                }
              >
                <option value="true">Available</option>
                <option value="false">Unavailable</option>
              </select>
            </div>
          </div>

          <button className="primary-button" type="submit">
            Save Availability
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Availability List</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        {availability.length === 0 ? (
          <p className="empty-message">
            No availability records found.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Lecturer</th>
                <th>Time Slot</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {availability.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>

                  <td>
                    {getLecturerName(item.lecturer_id)}
                  </td>

                  <td>
                    {getTimeSlot(item.time_slot_id)}
                  </td>

                  <td>
                    {item.is_available
                      ? "Available"
                      : "Unavailable"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   COURSE REQUIREMENTS
========================================================= */

function CourseRequirements() {
  const [requirements, setRequirements] = useState([]);
  const [courses, setCourses] = useState([]);
  const [sections, setSections] = useState([]);
  const [lecturers, setLecturers] = useState([]);

  const [courseId, setCourseId] = useState("");
  const [studentSectionId, setStudentSectionId] = useState("");
  const [lecturerId, setLecturerId] = useState("");
  const [sessionsPerWeek, setSessionsPerWeek] = useState("2");
  const [longSessionHours, setLongSessionHours] = useState("2");
  const [shortSessionHours, setShortSessionHours] = useState("1");

  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [
        requirementData,
        courseData,
        sectionData,
        lecturerData,
      ] = await Promise.all([
        apiRequest("/course-requirements/"),
        apiRequest("/courses/"),
        apiRequest("/student-sections/"),
        apiRequest("/lecturers/"),
      ]);

      setRequirements(requirementData);
      setCourses(courseData);
      setSections(sectionData);
      setLecturers(lecturerData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/course-requirements/", {
        method: "POST",
        body: JSON.stringify({
          course_id: Number(courseId),
          student_section_id: Number(studentSectionId),
          lecturer_id: Number(lecturerId),
          sessions_per_week: Number(sessionsPerWeek),
          long_session_hours: Number(longSessionHours),
          short_session_hours: Number(shortSessionHours),
        }),
      });

      setCourseId("");
      setStudentSectionId("");
      setLecturerId("");
      setSessionsPerWeek("2");
      setLongSessionHours("2");
      setShortSessionHours("1");

      setMessage(
        "Course requirement created successfully."
      );

      loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  function getCourseName(id) {
    const course = courses.find((item) => item.id === id);

    return course
      ? `${course.code} - ${course.name}`
      : `Course ${id}`;
  }

  function getSectionName(id) {
    const section = sections.find((item) => item.id === id);

    return section
      ? section.name
      : `Section ${id}`;
  }

  function getLecturerName(id) {
    const lecturer = lecturers.find(
      (item) => item.id === id
    );

    return lecturer
      ? lecturer.name
      : `Lecturer ${id}`;
  }

  return (
    <div>
      <h1>Course Requirements</h1>
      <p>
        Define which lecturer teaches which course for each
        student section.
      </p>

      <div className="form-card">
        <h2>Add Course Requirement</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Course</label>

              <select
                value={courseId}
                onChange={(event) =>
                  setCourseId(event.target.value)
                }
                required
              >
                <option value="">Select Course</option>

                {courses.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.code} - {course.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Student Section</label>

              <select
                value={studentSectionId}
                onChange={(event) =>
                  setStudentSectionId(event.target.value)
                }
                required
              >
                <option value="">Select Section</option>

                {sections.map((section) => (
                  <option key={section.id} value={section.id}>
                    {section.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Lecturer</label>

              <select
                value={lecturerId}
                onChange={(event) =>
                  setLecturerId(event.target.value)
                }
                required
              >
                <option value="">Select Lecturer</option>

                {lecturers.map((lecturer) => (
                  <option
                    key={lecturer.id}
                    value={lecturer.id}
                  >
                    {lecturer.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Sessions Per Week</label>

              <input
                type="number"
                min="1"
                value={sessionsPerWeek}
                onChange={(event) =>
                  setSessionsPerWeek(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Long Session Hours</label>

              <input
                type="number"
                min="1"
                value={longSessionHours}
                onChange={(event) =>
                  setLongSessionHours(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Short Session Hours</label>

              <input
                type="number"
                min="1"
                value={shortSessionHours}
                onChange={(event) =>
                  setShortSessionHours(event.target.value)
                }
                required
              />
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Requirement
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Requirement List</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        {requirements.length === 0 ? (
          <p className="empty-message">
            No course requirements found.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Course</th>
                <th>Section</th>
                <th>Lecturer</th>
                <th>Sessions</th>
                <th>Long Hours</th>
                <th>Short Hours</th>
              </tr>
            </thead>

            <tbody>
              {requirements.map((requirement) => (
                <tr key={requirement.id}>
                  <td>{requirement.id}</td>

                  <td>
                    {getCourseName(requirement.course_id)}
                  </td>

                  <td>
                    {getSectionName(
                      requirement.student_section_id
                    )}
                  </td>

                  <td>
                    {getLecturerName(requirement.lecturer_id)}
                  </td>

                  <td>{requirement.sessions_per_week}</td>
                  <td>{requirement.long_session_hours}</td>
                  <td>{requirement.short_session_hours}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   CONSTRAINTS
========================================================= */

function Constraints() {
  const [constraints, setConstraints] = useState([]);

  const [name, setName] = useState("");
  const [type, setType] = useState("HARD");
  const [description, setDescription] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [weight, setWeight] = useState("1");

  const [message, setMessage] = useState("");

  async function loadConstraints() {
    try {
      const data = await apiRequest("/constraints/");
      setConstraints(data);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadConstraints();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    try {
      await apiRequest("/constraints/", {
        method: "POST",
        body: JSON.stringify({
          name,
          type,
          description: description || null,
          is_active: isActive,
          weight: Number(weight),
        }),
      });

      setName("");
      setType("HARD");
      setDescription("");
      setIsActive(true);
      setWeight("1");

      setMessage("Constraint created successfully.");

      loadConstraints();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>Constraints</h1>
      <p>Manage scheduling constraints.</p>

      <div className="form-card">
        <h2>Add Constraint</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Name</label>

              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="No Lecturer Conflict"
                required
              />
            </div>

            <div className="form-group">
              <label>Type</label>

              <select
                value={type}
                onChange={(event) => setType(event.target.value)}
              >
                <option value="HARD">HARD</option>
                <option value="SOFT">SOFT</option>
              </select>
            </div>

            <div className="form-group">
              <label>Description</label>

              <input
                value={description}
                onChange={(event) =>
                  setDescription(event.target.value)
                }
                placeholder="Lecturer cannot teach two classes at once."
              />
            </div>

            <div className="form-group">
              <label>Weight</label>

              <input
                type="number"
                min="1"
                value={weight}
                onChange={(event) =>
                  setWeight(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Active</label>

              <select
                value={isActive ? "true" : "false"}
                onChange={(event) =>
                  setIsActive(event.target.value === "true")
                }
              >
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
            </div>
          </div>

          <button className="primary-button" type="submit">
            Add Constraint
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Constraint List</h2>

          <button
            className="secondary-button"
            onClick={loadConstraints}
          >
            Refresh
          </button>
        </div>

        {constraints.length === 0 ? (
          <p className="empty-message">
            No constraints found.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Description</th>
                <th>Active</th>
                <th>Weight</th>
              </tr>
            </thead>

            <tbody>
              {constraints.map((constraint) => (
                <tr key={constraint.id}>
                  <td>{constraint.id}</td>
                  <td>{constraint.name}</td>
                  <td>{constraint.type}</td>
                  <td>{constraint.description || "-"}</td>
                  <td>
                    {constraint.is_active
                      ? "Active"
                      : "Inactive"}
                  </td>
                  <td>{constraint.weight}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   GENERATE SCHEDULE
========================================================= */

function GenerateSchedule() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);

  async function generateSchedule() {
    setLoading(true);
    setMessage("");
    setResult(null);

    try {
      const data = await apiRequest("/schedules/generate", {
        method: "POST",
      });

      setResult(data);
      setMessage("Schedule generated successfully.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Generate Schedule</h1>

      <p>
        Generate an automatic university timetable using the
        scheduling engine.
      </p>

      <div className="form-card">
        <h2>Automatic Scheduler</h2>

        <p>
          The scheduler will create a new automatic draft schedule
          while respecting the configured scheduling rules.
        </p>

        <button
          className="primary-button"
          onClick={generateSchedule}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Schedule"}
        </button>

        {message && <p className="form-message">{message}</p>}

        {result && (
          <div className="form-message">
            <p>
              <strong>Schedule ID:</strong>{" "}
              {result.schedule_id}
            </p>

            <p>
              <strong>Status:</strong> {result.status}
            </p>

            <p>
              <strong>Entries Created:</strong>{" "}
              {result.entries_created}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   TIMETABLE
========================================================= */

function Timetable() {
  const [schedules, setSchedules] = useState([]);
  const [selectedScheduleId, setSelectedScheduleId] =
    useState("");
  const [scheduleData, setScheduleData] = useState(null);

  const [message, setMessage] = useState("");

  async function loadSchedules() {
    try {
      const data = await apiRequest("/schedules/");

      setSchedules(data);

      if (data.length > 0) {
        const automaticSchedule =
          [...data]
            .reverse()
            .find(
              (schedule) =>
                schedule.name ===
                  "Automatically Generated Schedule" &&
                schedule.status === "DRAFT"
            ) || data[data.length - 1];

        setSelectedScheduleId(
          String(automaticSchedule.id)
        );
      }
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function loadSchedule(scheduleId) {
    if (!scheduleId) {
      return;
    }

    try {
      const data = await apiRequest(
        `/schedules/${scheduleId}`
      );

      setScheduleData(data);
      setMessage("");
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadSchedules();
  }, []);

  useEffect(() => {
    if (selectedScheduleId) {
      loadSchedule(selectedScheduleId);
    }
  }, [selectedScheduleId]);

  return (
    <div>
      <h1>Timetable</h1>

      <p>View generated university schedules.</p>

      <div className="form-card">
        <div className="form-group">
          <label>Select Schedule</label>

          <select
            value={selectedScheduleId}
            onChange={(event) =>
              setSelectedScheduleId(event.target.value)
            }
          >
            <option value="">Select Schedule</option>

            {schedules.map((schedule) => (
              <option
                key={schedule.id}
                value={schedule.id}
              >
                #{schedule.id} - {schedule.name} (
                {schedule.status})
              </option>
            ))}
          </select>
        </div>
      </div>

      {message && <p className="form-message">{message}</p>}

      {scheduleData && (
        <>
          <div className="table-card">
            <div className="table-header">
              <div>
                <h2>{scheduleData.schedule.name}</h2>

                <p>
                  Status: {scheduleData.schedule.status}
                </p>
              </div>

              <button
                className="secondary-button"
                onClick={() =>
                  loadSchedule(selectedScheduleId)
                }
              >
                Refresh
              </button>
            </div>

            {scheduleData.entries.length === 0 ? (
              <p className="empty-message">
                No schedule entries found.
              </p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Day</th>
                    <th>Time</th>
                    <th>Course</th>
                    <th>Lecturer</th>
                    <th>Section</th>
                    <th>Students</th>
                    <th>Room</th>
                    <th>Capacity</th>
                  </tr>
                </thead>

                <tbody>
                  {scheduleData.entries.map((entry) => (
                    <tr key={entry.id}>
                      <td>{entry.day}</td>

                      <td>
                        {formatTime(entry.start_time)} -{" "}
                        {formatTime(entry.end_time)}
                      </td>

                      <td>{entry.course}</td>

                      <td>{entry.lecturer}</td>

                      <td>{entry.student_section}</td>

                      <td>{entry.student_count}</td>

                      <td>{entry.room}</td>

                      <td>{entry.room_capacity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}

            <p className="form-message">
              Total schedule entries:{" "}
              {scheduleData.entries_count}
            </p>
          </div>
        </>
      )}
    </div>
  );
}

/* =========================================================
   ROUTER
========================================================= */

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />

      <Route
        path="/departments"
        element={<Departments />}
      />

      <Route path="/programs" element={<Programs />} />

      <Route path="/courses" element={<Courses />} />

      <Route
        path="/lecturers"
        element={<Lecturers />}
      />

      <Route
        path="/student-sections"
        element={<StudentSections />}
      />

      <Route path="/rooms" element={<Rooms />} />

      <Route
        path="/time-slots"
        element={<TimeSlots />}
      />

      <Route
        path="/lecturer-availability"
        element={<LecturerAvailability />}
      />

      <Route
        path="/course-requirements"
        element={<CourseRequirements />}
      />

      <Route
        path="/constraints"
        element={<Constraints />}
      />

      <Route
        path="/generate-schedule"
        element={<GenerateSchedule />}
      />

      <Route
        path="/timetable"
        element={<Timetable />}
      />
    </Routes>
  );
}

/* =========================================================
   APP
========================================================= */

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <AppRoutes />
      </Layout>
    </BrowserRouter>
  );
}
