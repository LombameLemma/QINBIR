
import { useEffect, useState } from "react";
import {
  BrowserRouter,
  NavLink,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";

const API_URL = "http://localhost:8000";

/* =========================================================
   API HELPER
========================================================= */

async function apiRequest(url, options = {}) {
  const response = await fetch(`${API_URL}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();

  let data = null;

  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      "Request failed.";

    throw new Error(message);
  }

  return data;
}

/* =========================================================
   SIDEBAR
========================================================= */

function Sidebar() {
  const links = [
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
    {
      path: "/generate-schedule",
      label: "Generate Schedule",
    },
    { path: "/timetable", label: "Timetable" },
  ];

  return (
    <aside className="sidebar">
      <div className="logo">
        <h1>QINBIR</h1>
        <span>Smart Scheduler</span>
      </div>

      <nav>
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            end={link.path === "/"}
            className={({ isActive }) =>
              `nav-link ${isActive ? "active" : ""}`
            }
          >
            {link.label}
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
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    async function checkApi() {
      try {
        await apiRequest("/health");
        setConnected(true);
      } catch {
        setConnected(false);
      }
    }

    checkApi();

    const interval = setInterval(checkApi, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <header className="topbar">
      <strong>Automatic University Course Scheduling System</strong>

      <div className="api-status">
        <span
          style={{
            background: connected ? "#22c55e" : "#ef4444",
          }}
        ></span>

        {connected ? "API Connected" : "API Disconnected"}
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

        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
}

/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard() {
  const cards = [
    {
      title: "Departments",
      description: "Manage university departments.",
      path: "/departments",
    },
    {
      title: "Programs",
      description: "Manage academic programs.",
      path: "/programs",
    },
    {
      title: "Courses",
      description: "Manage university courses.",
      path: "/courses",
    },
    {
      title: "Lecturers",
      description: "Manage lecturers and instructors.",
      path: "/lecturers",
    },
    {
      title: "Student Sections",
      description: "Manage student groups and sections.",
      path: "/student-sections",
    },
    {
      title: "Rooms",
      description: "Manage classrooms and capacities.",
      path: "/rooms",
    },
    {
      title: "Time Slots",
      description: "Manage available teaching periods.",
      path: "/time-slots",
    },
    {
      title: "Course Requirements",
      description: "Define teaching requirements.",
      path: "/course-requirements",
    },
  ];

  return (
    <div>
      <h1>Dashboard</h1>

      <p>
        Welcome to QINBIR, the automatic university course
        scheduling system.
      </p>

      <div className="dashboard-grid">
        {cards.map((card) => (
          <a
            key={card.path}
            href={card.path}
            style={{
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <div className="dashboard-card">
              <h3>{card.title}</h3>
              <p>{card.description}</p>
            </div>
          </a>
        ))}
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
  const [loading, setLoading] = useState(false);

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

  async function handleSubmit(e) {
    e.preventDefault();

    if (!name.trim() || !code.trim()) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
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
      setMessage("Department added successfully.");

      await loadDepartments();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
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
              <label>Department Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Computer Science"
              />
            </div>

            <div className="form-group">
              <label>Department Code</label>

              <input
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="CS"
              />
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Department"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Departments</h2>

          <button
            className="secondary-button"
            onClick={loadDepartments}
          >
            Refresh
          </button>
        </div>

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
  const [loading, setLoading] = useState(false);

  async function loadData() {
    try {
      const [programData, departmentData] =
        await Promise.all([
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

  async function handleSubmit(e) {
    e.preventDefault();

    if (!name.trim() || !code.trim() || !departmentId) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
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

      setMessage("Program added successfully.");

      await loadData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function departmentName(id) {
    const department = departments.find(
      (item) => item.id === id
    );

    return department
      ? `${department.name} (${department.code})`
      : id;
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
              <label>Program Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Software Engineering"
              />
            </div>

            <div className="form-group">
              <label>Program Code</label>

              <input
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="SE"
              />
            </div>

            <div className="form-group">
              <label>Department</label>

              <select
                value={departmentId}
                onChange={(e) =>
                  setDepartmentId(e.target.value)
                }
              >
                <option value="">
                  Select Department
                </option>

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

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Program"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Programs</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

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
                  {departmentName(program.department_id)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
  const [loading, setLoading] = useState(false);

  async function loadData() {
    try {
      const [courseData, programData] =
        await Promise.all([
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

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !code.trim() ||
      !name.trim() ||
      !creditHours ||
      !programId
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
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

      setMessage("Course added successfully.");

      await loadData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function programName(id) {
    const program = programs.find(
      (item) => item.id === id
    );

    return program
      ? `${program.name} (${program.code})`
      : id;
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
                onChange={(e) => setCode(e.target.value)}
                placeholder="SE201"
              />
            </div>

            <div className="form-group">
              <label>Course Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Database Systems"
              />
            </div>

            <div className="form-group">
              <label>Credit Hours</label>

              <input
                type="number"
                min="1"
                value={creditHours}
                onChange={(e) =>
                  setCreditHours(e.target.value)
                }
              />
            </div>

            <div className="form-group">
              <label>Program</label>

              <select
                value={programId}
                onChange={(e) =>
                  setProgramId(e.target.value)
                }
              >
                <option value="">
                  Select Program
                </option>

                {programs.map((program) => (
                  <option
                    key={program.id}
                    value={program.id}
                  >
                    {program.name} ({program.code})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Course"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Courses</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

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
                <td>
                  {programName(course.program_id)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
  const [loading, setLoading] = useState(false);

  async function loadData() {
    try {
      const [
        lecturerData,
        userData,
        departmentData,
      ] = await Promise.all([
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

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !userId ||
      !departmentId ||
      !employeeId.trim() ||
      !name.trim()
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
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

      setMessage("Lecturer added successfully.");

      await loadData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function departmentName(id) {
    const department = departments.find(
      (item) => item.id === id
    );

    return department
      ? `${department.name} (${department.code})`
      : id;
  }

  return (
    <div>
      <h1>Lecturers</h1>
      <p>Manage lecturers and instructors.</p>

      <div className="form-card">
        <h2>Add Lecturer</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>User</label>

              <select
                value={userId}
                onChange={(e) =>
                  setUserId(e.target.value)
                }
              >
                <option value="">Select User</option>

                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.full_name} — {user.email}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Department</label>

              <select
                value={departmentId}
                onChange={(e) =>
                  setDepartmentId(e.target.value)
                }
              >
                <option value="">
                  Select Department
                </option>

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
                onChange={(e) =>
                  setEmployeeId(e.target.value)
                }
                placeholder="LEC003"
              />
            </div>

            <div className="form-group">
              <label>Lecturer Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Dr. Example"
              />
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Lecturer"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Lecturers</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Employee ID</th>
              <th>Name</th>
              <th>User ID</th>
              <th>Department</th>
            </tr>
          </thead>

          <tbody>
            {lecturers.map((lecturer) => (
              <tr key={lecturer.id}>
                <td>{lecturer.id}</td>
                <td>{lecturer.employee_id}</td>
                <td>{lecturer.name}</td>
                <td>{lecturer.user_id}</td>
                <td>
                  {departmentName(
                    lecturer.department_id
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
  const [loading, setLoading] = useState(false);

  async function loadData() {
    try {
      const [sectionData, programData] =
        await Promise.all([
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

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !name.trim() ||
      !programId ||
      !year ||
      !semester ||
      !studentCount
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    if (
      Number(year) < 1 ||
      Number(semester) < 1 ||
      Number(studentCount) < 1
    ) {
      setMessage(
        "Year, semester, and student count must be at least 1."
      );
      return;
    }

    setLoading(true);
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

      setMessage(
        "Student section added successfully."
      );

      await loadData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function programName(id) {
    const program = programs.find(
      (item) => item.id === id
    );

    return program
      ? `${program.name} (${program.code})`
      : id;
  }

  return (
    <div>
      <h1>Student Sections</h1>

      <p>
        Manage student groups, academic years,
        semesters, and section sizes.
      </p>

      <div className="form-card">
        <h2>Add Student Section</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Section Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="SE Year 2 Section A"
              />
            </div>

            <div className="form-group">
              <label>Program</label>

              <select
                value={programId}
                onChange={(e) =>
                  setProgramId(e.target.value)
                }
              >
                <option value="">
                  Select Program
                </option>

                {programs.map((program) => (
                  <option
                    key={program.id}
                    value={program.id}
                  >
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
                onChange={(e) => setYear(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Semester</label>

              <input
                type="number"
                min="1"
                value={semester}
                onChange={(e) =>
                  setSemester(e.target.value)
                }
              />
            </div>

            <div className="form-group">
              <label>Student Count</label>

              <input
                type="number"
                min="1"
                value={studentCount}
                onChange={(e) =>
                  setStudentCount(e.target.value)
                }
              />
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading
              ? "Adding..."
              : "Add Student Section"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Student Sections</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Section Name</th>
              <th>Program</th>
              <th>Year</th>
              <th>Semester</th>
              <th>Student Count</th>
            </tr>
          </thead>

          <tbody>
            {sections.map((section) => (
              <tr key={section.id}>
                <td>{section.id}</td>
                <td>{section.name}</td>
                <td>
                  {programName(section.program_id)}
                </td>
                <td>{section.year}</td>
                <td>{section.semester}</td>
                <td>{section.student_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
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
  const [loading, setLoading] = useState(false);

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

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !name.trim() ||
      !building.trim() ||
      !capacity ||
      !roomType.trim()
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
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

      setMessage("Room added successfully.");

      await loadRooms();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Rooms</h1>
      <p>Manage classrooms, buildings, and room capacities.</p>

      <div className="form-card">
        <h2>Add Room</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Room Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Room 203"
              />
            </div>

            <div className="form-group">
              <label>Building</label>

              <input
                value={building}
                onChange={(e) =>
                  setBuilding(e.target.value)
                }
                placeholder="Main Building"
              />
            </div>

            <div className="form-group">
              <label>Capacity</label>

              <input
                type="number"
                min="1"
                value={capacity}
                onChange={(e) =>
                  setCapacity(e.target.value)
                }
                placeholder="60"
              />
            </div>

            <div className="form-group">
              <label>Room Type</label>

              <input
                value={roomType}
                onChange={(e) =>
                  setRoomType(e.target.value)
                }
                placeholder="Classroom"
              />
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Room"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Rooms</h2>

          <button
            className="secondary-button"
            onClick={loadRooms}
          >
            Refresh
          </button>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Building</th>
              <th>Capacity</th>
              <th>Room Type</th>
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
  const [loading, setLoading] = useState(false);

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

  async function handleSubmit(e) {
    e.preventDefault();

    if (!day || !startTime || !endTime) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
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

      setMessage("Time slot added successfully.");

      await loadTimeSlots();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Time Slots</h1>
      <p>Manage available university teaching periods.</p>

      <div className="form-card">
        <h2>Add Time Slot</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Day</label>

              <select
                value={day}
                onChange={(e) => setDay(e.target.value)}
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
                onChange={(e) =>
                  setStartTime(e.target.value)
                }
              />
            </div>

            <div className="form-group">
              <label>End Time</label>

              <input
                type="time"
                value={endTime}
                onChange={(e) =>
                  setEndTime(e.target.value)
                }
              />
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Time Slot"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Time Slots</h2>

          <button
            className="secondary-button"
            onClick={loadTimeSlots}
          >
            Refresh
          </button>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Day</th>
              <th>Start</th>
              <th>End</th>
            </tr>
          </thead>

          <tbody>
            {timeSlots.map((slot) => (
              <tr key={slot.id}>
                <td>{slot.id}</td>
                <td>{slot.day}</td>
                <td>{String(slot.start_time).slice(0, 5)}</td>
                <td>{String(slot.end_time).slice(0, 5)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* =========================================================
   LECTURER AVAILABILITY
========================================================= */

function LecturerAvailability() {
  const [records, setRecords] = useState([]);
  const [lecturers, setLecturers] = useState([]);
  const [timeSlots, setTimeSlots] = useState([]);

  const [lecturerId, setLecturerId] = useState("");
  const [timeSlotId, setTimeSlotId] = useState("");
  const [isAvailable, setIsAvailable] = useState(true);

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

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

      setRecords(availabilityData);
      setLecturers(lecturerData);
      setTimeSlots(timeSlotData);
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!lecturerId || !timeSlotId) {
      setMessage("Please select lecturer and time slot.");
      return;
    }

    setLoading(true);
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

      setMessage(
        "Lecturer availability saved successfully."
      );

      await loadData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function lecturerName(id) {
    const lecturer = lecturers.find(
      (item) => item.id === id
    );

    return lecturer
      ? lecturer.name
      : id;
  }

  function timeSlotName(id) {
    const slot = timeSlots.find(
      (item) => item.id === id
    );

    return slot
      ? `${slot.day} ${String(slot.start_time).slice(
          0,
          5
        )}-${String(slot.end_time).slice(0, 5)}`
      : id;
  }

  return (
    <div>
      <h1>Lecturer Availability</h1>

      <p>
        Define when lecturers are available for teaching.
      </p>

      <div className="form-card">
        <h2>Add Availability</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Lecturer</label>

              <select
                value={lecturerId}
                onChange={(e) =>
                  setLecturerId(e.target.value)
                }
              >
                <option value="">
                  Select Lecturer
                </option>

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
                onChange={(e) =>
                  setTimeSlotId(e.target.value)
                }
              >
                <option value="">
                  Select Time Slot
                </option>

                {timeSlots.map((slot) => (
                  <option
                    key={slot.id}
                    value={slot.id}
                  >
                    {slot.day}{" "}
                    {String(slot.start_time).slice(0, 5)}
                    -
                    {String(slot.end_time).slice(0, 5)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Availability</label>

              <select
                value={isAvailable ? "true" : "false"}
                onChange={(e) =>
                  setIsAvailable(
                    e.target.value === "true"
                  )
                }
              >
                <option value="true">Available</option>
                <option value="false">Unavailable</option>
              </select>
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save Availability"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Availability Records</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Lecturer</th>
              <th>Time Slot</th>
              <th>Availability</th>
            </tr>
          </thead>

          <tbody>
            {records.map((record) => (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td>
                  {lecturerName(record.lecturer_id)}
                </td>
                <td>
                  {timeSlotName(record.time_slot_id)}
                </td>
                <td>
                  {record.is_available
                    ? "Available"
                    : "Unavailable"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
  const [studentSectionId, setStudentSectionId] =
    useState("");
  const [lecturerId, setLecturerId] = useState("");
  const [sessionsPerWeek, setSessionsPerWeek] =
    useState("2");
  const [longSessionHours, setLongSessionHours] =
    useState("2");
  const [shortSessionHours, setShortSessionHours] =
    useState("1");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

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

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !courseId ||
      !studentSectionId ||
      !lecturerId ||
      !sessionsPerWeek ||
      !longSessionHours ||
      !shortSessionHours
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      await apiRequest("/course-requirements/", {
        method: "POST",
        body: JSON.stringify({
          course_id: Number(courseId),
          student_section_id: Number(studentSectionId),
          lecturer_id: Number(lecturerId),
          sessions_per_week: Number(sessionsPerWeek),
          long_session_hours: Number(
            longSessionHours
          ),
          short_session_hours: Number(
            shortSessionHours
          ),
        }),
      });

      setCourseId("");
      setStudentSectionId("");
      setLecturerId("");
      setSessionsPerWeek("2");
      setLongSessionHours("2");
      setShortSessionHours("1");

      setMessage(
        "Course requirement added successfully."
      );

      await loadData();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function courseName(id) {
    const course = courses.find(
      (item) => item.id === id
    );

    return course
      ? `${course.code} - ${course.name}`
      : id;
  }

  function sectionName(id) {
    const section = sections.find(
      (item) => item.id === id
    );

    return section ? section.name : id;
  }

  function lecturerName(id) {
    const lecturer = lecturers.find(
      (item) => item.id === id
    );

    return lecturer ? lecturer.name : id;
  }

  return (
    <div>
      <h1>Course Requirements</h1>

      <p>
        Define which lecturer teaches which course
        for each student section.
      </p>

      <div className="form-card">
        <h2>Add Course Requirement</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Course</label>

              <select
                value={courseId}
                onChange={(e) =>
                  setCourseId(e.target.value)
                }
              >
                <option value="">
                  Select Course
                </option>

                {courses.map((course) => (
                  <option
                    key={course.id}
                    value={course.id}
                  >
                    {course.code} - {course.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Student Section</label>

              <select
                value={studentSectionId}
                onChange={(e) =>
                  setStudentSectionId(e.target.value)
                }
              >
                <option value="">
                  Select Student Section
                </option>

                {sections.map((section) => (
                  <option
                    key={section.id}
                    value={section.id}
                  >
                    {section.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Lecturer</label>

              <select
                value={lecturerId}
                onChange={(e) =>
                  setLecturerId(e.target.value)
                }
              >
                <option value="">
                  Select Lecturer
                </option>

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
                onChange={(e) =>
                  setSessionsPerWeek(e.target.value)
                }
              />
            </div>

            <div className="form-group">
              <label>Long Session Hours</label>

              <input
                type="number"
                min="1"
                value={longSessionHours}
                onChange={(e) =>
                  setLongSessionHours(e.target.value)
                }
              />
            </div>

            <div className="form-group">
              <label>Short Session Hours</label>

              <input
                type="number"
                min="1"
                value={shortSessionHours}
                onChange={(e) =>
                  setShortSessionHours(e.target.value)
                }
              />
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Requirement"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Course Requirements</h2>

          <button
            className="secondary-button"
            onClick={loadData}
          >
            Refresh
          </button>
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Course</th>
              <th>Section</th>
              <th>Lecturer</th>
              <th>Sessions/Week</th>
              <th>Long</th>
              <th>Short</th>
            </tr>
          </thead>

          <tbody>
            {requirements.map((requirement) => (
              <tr key={requirement.id}>
                <td>{requirement.id}</td>
                <td>
                  {courseName(requirement.course_id)}
                </td>
                <td>
                  {sectionName(
                    requirement.student_section_id
                  )}
                </td>
                <td>
                  {lecturerName(
                    requirement.lecturer_id
                  )}
                </td>
                <td>
                  {requirement.sessions_per_week}
                </td>
                <td>
                  {requirement.long_session_hours}h
                </td>
                <td>
                  {requirement.short_session_hours}h
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
  const [loading, setLoading] = useState(false);

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

  async function handleSubmit(e) {
    e.preventDefault();

    if (!name.trim() || !type || !weight) {
      setMessage("Please fill in all required fields.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      await apiRequest("/constraints/", {
        method: "POST",
        body: JSON.stringify({
          name,
          type,
          description,
          is_active: isActive,
          weight: Number(weight),
        }),
      });

      setName("");
      setType("HARD");
      setDescription("");
      setIsActive(true);
      setWeight("1");

      setMessage(
        "Constraint added successfully."
      );

      await loadConstraints();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Constraints</h1>

      <p>
        Manage scheduling rules and optimization
        constraints.
      </p>

      <div className="form-card">
        <h2>Add Constraint</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Constraint Name</label>

              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="No Lecturer Conflict"
              />
            </div>

            <div className="form-group">
              <label>Type</label>

              <select
                value={type}
                onChange={(e) =>
                  setType(e.target.value)
                }
              >
                <option value="HARD">HARD</option>
                <option value="SOFT">SOFT</option>
              </select>
            </div>

            <div className="form-group">
              <label>Description</label>

              <input
                value={description}
                onChange={(e) =>
                  setDescription(e.target.value)
                }
                placeholder="A lecturer cannot teach two classes at once."
              />
            </div>

            <div className="form-group">
              <label>Weight</label>

              <input
                type="number"
                min="1"
                value={weight}
                onChange={(e) =>
                  setWeight(e.target.value)
                }
              />
            </div>

            <div className="form-group">
              <label>Active</label>

              <select
                value={isActive ? "true" : "false"}
                onChange={(e) =>
                  setIsActive(
                    e.target.value === "true"
                  )
                }
              >
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
            </div>
          </div>

          <button
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Constraint"}
          </button>
        </form>

        {message && (
          <p className="form-message">{message}</p>
        )}
      </div>

      <div className="table-card">
        <div className="table-header">
          <h2>Constraints</h2>

          <button
            className="secondary-button"
            onClick={loadConstraints}
          >
            Refresh
          </button>
        </div>

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
                <td>{constraint.description}</td>
                <td>
                  {constraint.is_active
                    ? "Yes"
                    : "No"}
                </td>
                <td>{constraint.weight}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* =========================================================
   GENERATE SCHEDULE
========================================================= */

function GenerateSchedule() {
  const navigate = useNavigate();

  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);

  async function generateSchedule() {
    setGenerating(true);
    setMessage("");
    setResult(null);

    try {
      const data = await apiRequest(
        "/schedules/generate",
        {
          method: "POST",
        }
      );

      setResult(data);

      setMessage(
        "Schedule generated successfully."
      );
    } catch (error) {
      setMessage(
        `Schedule generation failed: ${error.message}`
      );
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div>
      <h1>Generate Schedule</h1>

      <p>
        Use the QINBIR optimization engine to generate
        a valid university timetable.
      </p>

      <div className="form-card">
        <h2>Automatic Scheduler</h2>

        <p>
          The scheduler uses courses, student sections,
          lecturers, rooms, time slots, and lecturer
          availability.
        </p>

        <button
          className="primary-button"
          onClick={generateSchedule}
          disabled={generating}
        >
          {generating
            ? "Generating Schedule..."
            : "Generate Schedule"}
        </button>

        {message && (
          <p className="form-message">{message}</p>
        )}

        {result && (
          <div
            style={{
              marginTop: "20px",
              padding: "20px",
              background: "#f8fafc",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
            }}
          >
            <h3>Generation Result</h3>

            <p>
              <strong>Status:</strong>{" "}
              {result.status}
            </p>

            <p>
              <strong>Schedule ID:</strong>{" "}
              {result.schedule_id}
            </p>

            <p>
              <strong>Entries Created:</strong>{" "}
              {result.entries_created}
            </p>

            <button
              className="secondary-button"
              onClick={() =>
                navigate("/timetable")
              }
            >
              View Timetable
            </button>
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
  const [scheduleId, setScheduleId] = useState("");
  const [schedule, setSchedule] = useState(null);
  const [entries, setEntries] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadSchedules() {
    try {
      const data = await apiRequest("/schedules/");

      setSchedules(data);

      if (data.length > 0) {
        const automaticSchedules = data.filter(
          (item) =>
            item.name ===
              "Automatically Generated Schedule" &&
            item.status === "DRAFT"
        );

        const latest =
          automaticSchedules.length > 0
            ? automaticSchedules[
                automaticSchedules.length - 1
              ]
            : data[data.length - 1];

        setScheduleId(String(latest.id));
      }
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function loadSchedule(id) {
    if (!id) return;

    setLoading(true);
    setMessage("");

    try {
      const data = await apiRequest(
        `/schedules/${id}`
      );

      setSchedule(data.schedule);
      setEntries(data.entries || []);
    } catch (error) {
      setMessage(error.message);
      setSchedule(null);
      setEntries([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSchedules();
  }, []);

  useEffect(() => {
    if (scheduleId) {
      loadSchedule(scheduleId);
    }
  }, [scheduleId]);

  function dayOrder(day) {
    const order = {
      Monday: 1,
      Tuesday: 2,
      Wednesday: 3,
      Thursday: 4,
      Friday: 5,
      Saturday: 6,
      Sunday: 7,
    };

    return order[day] || 99;
  }

  const sortedEntries = [...entries].sort((a, b) => {
    const dayDifference =
      dayOrder(a.day) - dayOrder(b.day);

    if (dayDifference !== 0) {
      return dayDifference;
    }

    return a.start_time.localeCompare(
      b.start_time
    );
  });

  return (
    <div>
      <h1>Timetable</h1>

      <p>
        View the generated university course
        timetable.
      </p>

      <div className="form-card">
        <h2>Select Schedule</h2>

        <div className="form-grid">
          <div className="form-group">
            <label>Schedule</label>

            <select
              value={scheduleId}
              onChange={(e) =>
                setScheduleId(e.target.value)
              }
            >
              <option value="">
                Select Schedule
              </option>

              {schedules.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  #{item.id} — {item.name} —{" "}
                  {item.status}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          className="secondary-button"
          onClick={loadSchedules}
        >
          Refresh Schedules
        </button>
      </div>

      {message && (
        <p className="form-message">{message}</p>
      )}

      {loading && (
        <p className="form-message">
          Loading timetable...
        </p>
      )}

      {schedule && (
        <div className="table-card">
          <div className="table-header">
            <div>
              <h2>{schedule.name}</h2>

              <p>
                Status: <strong>{schedule.status}</strong>
              </p>
            </div>

            <button
              className="secondary-button"
              onClick={() =>
                loadSchedule(scheduleId)
              }
            >
              Refresh
            </button>
          </div>

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
              {sortedEntries.map((entry) => (
                <tr key={entry.id}>
                  <td>{entry.day}</td>

                  <td>
                    {entry.start_time} -{" "}
                    {entry.end_time}
                  </td>

                  <td>{entry.course}</td>

                  <td>{entry.lecturer}</td>

                  <td>
                    {entry.student_section}
                  </td>

                  <td>{entry.student_count}</td>

                  <td>{entry.room}</td>

                  <td>{entry.room_capacity}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <p
            style={{
              marginTop: "20px",
              color: "#64748b",
            }}
          >
            Total timetable entries:{" "}
            <strong>{entries.length}</strong>
          </p>
        </div>
      )}
    </div>
  );
}

/* =========================================================
   APP
========================================================= */

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/departments"
            element={<Departments />}
          />

          <Route
            path="/programs"
            element={<Programs />}
          />

          <Route
            path="/courses"
            element={<Courses />}
          />

          <Route
            path="/lecturers"
            element={<Lecturers />}
          />

          <Route
            path="/student-sections"
            element={<StudentSections />}
          />

          <Route
            path="/rooms"
            element={<Rooms />}
          />

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
      </Layout>
    </BrowserRouter>
  );
}

export default App;
