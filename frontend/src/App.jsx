import { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  Link,
} from "react-router-dom";

/* ============================================================
   API
============================================================ */

const API_BASE_URL = "http://127.0.0.1:8000";

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

/* ============================================================
   GLOBAL STYLES
============================================================ */

const styles = {
  app: {
    minHeight: "100vh",
    background: "#f5f7fb",
    color: "#172033",
    fontFamily:
      "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  },

  layout: {
    display: "flex",
    minHeight: "100vh",
  },

  sidebar: {
    width: "260px",
    minHeight: "100vh",
    background:
      "linear-gradient(180deg, #101b3d 0%, #17295c 55%, #102044 100%)",
    color: "white",
    position: "fixed",
    left: 0,
    top: 0,
    bottom: 0,
    overflowY: "auto",
    zIndex: 20,
    boxShadow: "4px 0 20px rgba(15, 23, 42, 0.12)",
  },

  brand: {
    padding: "25px 22px",
    borderBottom: "1px solid rgba(255,255,255,0.1)",
  },

  brandName: {
    fontSize: "27px",
    fontWeight: 800,
    letterSpacing: "1px",
  },

  brandSubtitle: {
    fontSize: "12px",
    color: "#aebbe2",
    marginTop: "5px",
  },

  nav: {
    padding: "18px 12px",
  },

  navSection: {
    fontSize: "10px",
    textTransform: "uppercase",
    letterSpacing: "1.4px",
    color: "#8190bd",
    fontWeight: 700,
    padding: "13px 12px 7px",
  },

  navLink: {
    display: "flex",
    alignItems: "center",
    gap: "11px",
    padding: "11px 13px",
    marginBottom: "3px",
    borderRadius: "9px",
    color: "#cbd5f0",
    textDecoration: "none",
    fontSize: "14px",
    fontWeight: 500,
  },

  navLinkActive: {
    background: "rgba(255,255,255,0.12)",
    color: "#ffffff",
    boxShadow: "inset 3px 0 0 #6ea8fe",
  },

  main: {
    marginLeft: "260px",
    width: "calc(100% - 260px)",
    minHeight: "100vh",
  },

  topbar: {
    height: "70px",
    background: "#ffffff",
    borderBottom: "1px solid #e7ebf2",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 30px",
    position: "sticky",
    top: 0,
    zIndex: 10,
  },

  topbarTitle: {
    fontSize: "18px",
    fontWeight: 700,
  },

  topbarSub: {
    fontSize: "12px",
    color: "#7b8497",
    marginTop: "2px",
  },

  content: {
    padding: "30px",
    maxWidth: "1600px",
    margin: "0 auto",
  },

  card: {
    background: "#ffffff",
    border: "1px solid #e7ebf2",
    borderRadius: "14px",
    padding: "22px",
    boxShadow: "0 4px 18px rgba(15, 23, 42, 0.035)",
  },

  sectionTitle: {
    fontSize: "19px",
    fontWeight: 750,
    margin: 0,
  },

  sectionSub: {
    fontSize: "13px",
    color: "#758096",
    marginTop: "5px",
  },

  grid: {
    display: "grid",
    gap: "18px",
  },

  statGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(5, minmax(0, 1fr))",
    gap: "16px",
    marginBottom: "25px",
  },

  statCard: {
    background: "#ffffff",
    border: "1px solid #e7ebf2",
    borderRadius: "14px",
    padding: "19px",
    boxShadow: "0 4px 18px rgba(15, 23, 42, 0.035)",
  },

  statIcon: {
    width: "42px",
    height: "42px",
    borderRadius: "10px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "20px",
    background: "#eef3ff",
    marginBottom: "13px",
  },

  statValue: {
    fontSize: "27px",
    fontWeight: 800,
    color: "#18233d",
  },

  statLabel: {
    fontSize: "12px",
    color: "#7a8497",
    marginTop: "3px",
  },

  button: {
    border: "none",
    borderRadius: "8px",
    padding: "10px 16px",
    fontSize: "13px",
    fontWeight: 650,
    cursor: "pointer",
  },

  primaryButton: {
    background: "#3156d3",
    color: "white",
  },

  secondaryButton: {
    background: "#eef2f7",
    color: "#25324d",
  },

  dangerButton: {
    background: "#feecec",
    color: "#c53030",
  },

  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "11px 12px",
    border: "1px solid #dce2eb",
    borderRadius: "8px",
    background: "#ffffff",
    color: "#1d293d",
    fontSize: "13px",
    outline: "none",
  },

  select: {
    width: "100%",
    boxSizing: "border-box",
    padding: "11px 12px",
    border: "1px solid #dce2eb",
    borderRadius: "8px",
    background: "#ffffff",
    color: "#1d293d",
    fontSize: "13px",
  },

  textarea: {
    width: "100%",
    boxSizing: "border-box",
    padding: "11px 12px",
    border: "1px solid #dce2eb",
    borderRadius: "8px",
    minHeight: "90px",
    resize: "vertical",
    fontSize: "13px",
  },

  label: {
    display: "block",
    fontSize: "12px",
    fontWeight: 650,
    color: "#46536b",
    marginBottom: "6px",
  },

  formGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: "14px",
  },

  tableWrap: {
    overflowX: "auto",
    marginTop: "18px",
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "13px",
  },

  th: {
    textAlign: "left",
    padding: "12px 10px",
    borderBottom: "1px solid #e5e9f0",
    color: "#69758c",
    fontSize: "11px",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
    whiteSpace: "nowrap",
  },

  td: {
    padding: "12px 10px",
    borderBottom: "1px solid #edf0f4",
    color: "#27344d",
    verticalAlign: "middle",
  },

  badge: {
    display: "inline-block",
    padding: "5px 9px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: 650,
    background: "#eef2ff",
    color: "#4058b8",
  },

  message: {
    padding: "11px 13px",
    borderRadius: "8px",
    background: "#eef8f0",
    color: "#26723a",
    fontSize: "13px",
    marginBottom: "15px",
  },

  error: {
    padding: "11px 13px",
    borderRadius: "8px",
    background: "#fff0f0",
    color: "#b72d2d",
    fontSize: "13px",
    marginBottom: "15px",
  },
};

/* ============================================================
   SMALL COMPONENTS
============================================================ */

function PageTitle({ title, description, action }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        marginBottom: "22px",
        gap: "20px",
      }}
    >
      <div>
        <h1
          style={{
            margin: 0,
            fontSize: "26px",
            fontWeight: 800,
            color: "#17233e",
          }}
        >
          {title}
        </h1>

        {description && (
          <p
            style={{
              margin: "6px 0 0",
              color: "#7a8498",
              fontSize: "13px",
            }}
          >
            {description}
          </p>
        )}
      </div>

      {action}
    </div>
  );
}

function FormField({ label, children }) {
  return (
    <div>
      <label style={styles.label}>{label}</label>
      {children}
    </div>
  );
}

function Loading() {
  return (
    <div
      style={{
        padding: "35px",
        textAlign: "center",
        color: "#7a8498",
        fontSize: "14px",
      }}
    >
      Loading...
    </div>
  );
}

function EmptyState({ text }) {
  return (
    <div
      style={{
        padding: "35px",
        textAlign: "center",
        color: "#7a8498",
        fontSize: "13px",
      }}
    >
      {text}
    </div>
  );
}

/* ============================================================
   SIDEBAR
============================================================ */

function Sidebar() {
  const menuSections = [
    {
      title: "Overview",
      items: [
        { path: "/", icon: "⌂", label: "Dashboard" },
      ],
    },
    {
      title: "Academic Structure",
      items: [
        { path: "/departments", icon: "▦", label: "Departments" },
        { path: "/programs", icon: "◈", label: "Programs" },
        { path: "/courses", icon: "▤", label: "Courses" },
        { path: "/student-sections", icon: "♙", label: "Student Sections" },
      ],
    },
    {
      title: "Resources",
      items: [
        { path: "/lecturers", icon: "♟", label: "Lecturers" },
        { path: "/rooms", icon: "▣", label: "Rooms" },
        { path: "/time-slots", icon: "◷", label: "Time Slots" },
        {
          path: "/lecturer-availability",
          icon: "✓",
          label: "Lecturer Availability",
        },
      ],
    },
    {
      title: "Scheduling",
      items: [
        {
          path: "/course-requirements",
          icon: "≡",
          label: "Course Requirements",
        },
        { path: "/constraints", icon: "⚙", label: "Constraints" },
        {
          path: "/generate-schedule",
          icon: "✦",
          label: "Generate Schedule",
        },
        { path: "/timetable", icon: "▥", label: "Timetable" },
      ],
    },
  ];

  return (
    <aside style={styles.sidebar}>
      <div style={styles.brand}>
        <div style={styles.brandName}>QINBIR</div>
        <div style={styles.brandSubtitle}>
          Smart University Scheduling
        </div>
      </div>

      <div style={styles.nav}>
        {menuSections.map((section) => (
          <div key={section.title}>
            <div style={styles.navSection}>{section.title}</div>

            {section.items.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === "/"}
                style={({ isActive }) => ({
                  ...styles.navLink,
                  ...(isActive ? styles.navLinkActive : {}),
                })}
              >
                <span
                  style={{
                    width: "20px",
                    textAlign: "center",
                    fontSize: "16px",
                  }}
                >
                  {item.icon}
                </span>

                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </div>

      <div
        style={{
          margin: "18px 14px",
          padding: "15px",
          borderRadius: "11px",
          background: "rgba(255,255,255,0.07)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            fontWeight: 700,
            color: "#dce5ff",
          }}
        >
          QINBIR
        </div>

        <div
          style={{
            fontSize: "11px",
            lineHeight: 1.6,
            color: "#8f9dc2",
            marginTop: "5px",
          }}
        >
          Intelligent timetable planning for modern universities.
        </div>
      </div>
    </aside>
  );
}

/* ============================================================
   TOP BAR
============================================================ */

function TopBar() {
  return (
    <header style={styles.topbar}>
      <div>
        <div style={styles.topbarTitle}>QINBIR Smart Scheduler</div>
        <div style={styles.topbarSub}>
          University Academic Scheduling Platform
        </div>
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
        }}
      >
        <span style={styles.badge}>● System Online</span>

        <div
          style={{
            width: "35px",
            height: "35px",
            borderRadius: "50%",
            background: "#e9eefc",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 800,
            color: "#3156d3",
          }}
        >
          Q
        </div>
      </div>
    </header>
  );
}

/* ============================================================
   LAYOUT
============================================================ */

function Layout({ children }) {
  return (
    <div style={styles.app}>
      <div style={styles.layout}>
        <Sidebar />

        <main style={styles.main}>
          <TopBar />

          <div style={styles.content}>{children}</div>
        </main>
      </div>
    </div>
  );
}

/* ============================================================
   DASHBOARD
============================================================ */

function Dashboard() {
  const [stats, setStats] = useState({
    departments: 0,
    programs: 0,
    courses: 0,
    lecturers: 0,
    rooms: 0,
    sections: 0,
    requirements: 0,
    timeSlots: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const results = await Promise.allSettled([
          apiRequest("/departments/"),
          apiRequest("/programs/"),
          apiRequest("/courses/"),
          apiRequest("/lecturers/"),
          apiRequest("/rooms/"),
          apiRequest("/student-sections/"),
          apiRequest("/course-requirements/"),
          apiRequest("/time-slots/"),
        ]);

        const getLength = (result) =>
          result.status === "fulfilled" && Array.isArray(result.value)
            ? result.value.length
            : 0;

        setStats({
          departments: getLength(results[0]),
          programs: getLength(results[1]),
          courses: getLength(results[2]),
          lecturers: getLength(results[3]),
          rooms: getLength(results[4]),
          sections: getLength(results[5]),
          requirements: getLength(results[6]),
          timeSlots: getLength(results[7]),
        });
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    loadStats();
  }, []);

  const statItems = [
    {
      label: "Departments",
      value: stats.departments,
      icon: "▦",
    },
    {
      label: "Programs",
      value: stats.programs,
      icon: "◈",
    },
    {
      label: "Courses",
      value: stats.courses,
      icon: "▤",
    },
    {
      label: "Lecturers",
      value: stats.lecturers,
      icon: "♟",
    },
    {
      label: "Rooms",
      value: stats.rooms,
      icon: "▣",
    },
  ];

  return (
    <div>
      {/* HERO */}

      <section
        style={{
          borderRadius: "20px",
          padding: "42px",
          marginBottom: "25px",
          color: "white",
          background:
            "linear-gradient(120deg, #101c43 0%, #1e3d86 55%, #3156d3 100%)",
          position: "relative",
          overflow: "hidden",
          boxShadow: "0 15px 35px rgba(30,61,134,0.22)",
        }}
      >
        <div
          style={{
            position: "absolute",
            right: "-80px",
            top: "-100px",
            width: "300px",
            height: "300px",
            borderRadius: "50%",
            background: "rgba(255,255,255,0.06)",
          }}
        />

        <div
          style={{
            position: "absolute",
            right: "100px",
            bottom: "-160px",
            width: "320px",
            height: "320px",
            borderRadius: "50%",
            border: "1px solid rgba(255,255,255,0.08)",
          }}
        />

        <div style={{ maxWidth: "850px", position: "relative" }}>
          <div
            style={{
              display: "inline-block",
              padding: "7px 12px",
              borderRadius: "20px",
              background: "rgba(255,255,255,0.12)",
              fontSize: "11px",
              fontWeight: 700,
              letterSpacing: "1px",
              marginBottom: "15px",
            }}
          >
            UNIVERSITY SCHEDULING PLATFORM
          </div>

          <h1
            style={{
              fontSize: "42px",
              lineHeight: 1.12,
              margin: "0 0 15px",
              fontWeight: 850,
              letterSpacing: "-1px",
            }}
          >
            Welcome to QINBIR
          </h1>

          <p
            style={{
              fontSize: "17px",
              lineHeight: 1.7,
              color: "#dce6ff",
              maxWidth: "760px",
              margin: 0,
            }}
          >
            QINBIR is a smart university scheduling system designed to
            transform complex academic scheduling into an organized,
            efficient, and intelligent process.
          </p>

          <p
            style={{
              fontSize: "13px",
              lineHeight: 1.7,
              color: "#b8c8ee",
              maxWidth: "720px",
              marginTop: "12px",
            }}
          >
            It brings together departments, academic programs, courses,
            lecturers, student sections, classrooms, time slots and
            scheduling constraints to create practical university
            timetables.
          </p>

          <div
            style={{
              display: "flex",
              gap: "12px",
              marginTop: "24px",
              flexWrap: "wrap",
            }}
          >
            <Link
              to="/generate-schedule"
              style={{
                textDecoration: "none",
                background: "white",
                color: "#2348b8",
                padding: "12px 18px",
                borderRadius: "9px",
                fontWeight: 750,
                fontSize: "13px",
              }}
            >
              ✦ Generate Schedule
            </Link>

            <Link
              to="/courses"
              style={{
                textDecoration: "none",
                color: "white",
                border: "1px solid rgba(255,255,255,0.25)",
                padding: "12px 18px",
                borderRadius: "9px",
                fontWeight: 650,
                fontSize: "13px",
              }}
            >
              Manage Courses →
            </Link>
          </div>
        </div>
      </section>

      {/* STATISTICS */}

      <div style={styles.statGrid}>
        {statItems.map((item) => (
          <div key={item.label} style={styles.statCard}>
            <div style={styles.statIcon}>{item.icon}</div>

            <div style={styles.statValue}>
              {loading ? "—" : item.value}
            </div>

            <div style={styles.statLabel}>{item.label}</div>
          </div>
        ))}
      </div>

      {/* SECONDARY STATS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "16px",
          marginBottom: "25px",
        }}
      >
        <div style={styles.card}>
          <div style={{ color: "#6e7a91", fontSize: "12px" }}>
            Student Sections
          </div>

          <div
            style={{
              fontSize: "25px",
              fontWeight: 800,
              marginTop: "7px",
            }}
          >
            {loading ? "—" : stats.sections}
          </div>

          <div
            style={{
              color: "#8490a4",
              fontSize: "11px",
              marginTop: "4px",
            }}
          >
            Sections available for scheduling
          </div>
        </div>

        <div style={styles.card}>
          <div style={{ color: "#6e7a91", fontSize: "12px" }}>
            Course Requirements
          </div>

          <div
            style={{
              fontSize: "25px",
              fontWeight: 800,
              marginTop: "7px",
            }}
          >
            {loading ? "—" : stats.requirements}
          </div>

          <div
            style={{
              color: "#8490a4",
              fontSize: "11px",
              marginTop: "4px",
            }}
          >
            Teaching requirements configured
          </div>
        </div>

        <div style={styles.card}>
          <div style={{ color: "#6e7a91", fontSize: "12px" }}>
            Available Time Slots
          </div>

          <div
            style={{
              fontSize: "25px",
              fontWeight: 800,
              marginTop: "7px",
            }}
          >
            {loading ? "—" : stats.timeSlots}
          </div>

          <div
            style={{
              color: "#8490a4",
              fontSize: "11px",
              marginTop: "4px",
            }}
          >
            Weekly scheduling periods
          </div>
        </div>
      </div>

      {/* HOW QINBIR WORKS */}

      <section style={{ marginBottom: "25px" }}>
        <div style={{ marginBottom: "16px" }}>
          <h2 style={styles.sectionTitle}>How QINBIR Works</h2>

          <p style={styles.sectionSub}>
            QINBIR connects academic information and scheduling resources
            into one intelligent workflow.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "16px",
          }}
        >
          {[
            {
              number: "01",
              title: "Build Academic Structure",
              text: "Define departments, programs, courses and student sections.",
              icon: "▦",
            },
            {
              number: "02",
              title: "Configure Resources",
              text: "Register lecturers, rooms, time slots and lecturer availability.",
              icon: "⚙",
            },
            {
              number: "03",
              title: "Define Requirements",
              text: "Specify which courses must be taught to each student section.",
              icon: "≡",
            },
            {
              number: "04",
              title: "Generate Timetable",
              text: "The scheduling engine searches for a timetable satisfying the configured constraints.",
              icon: "✦",
            },
          ].map((item) => (
            <div
              key={item.number}
              style={{
                ...styles.card,
                position: "relative",
              }}
            >
              <div
                style={{
                  fontSize: "11px",
                  color: "#8090b1",
                  fontWeight: 800,
                  marginBottom: "13px",
                }}
              >
                STEP {item.number}
              </div>

              <div
                style={{
                  width: "43px",
                  height: "43px",
                  borderRadius: "10px",
                  background: "#eef2ff",
                  color: "#3156d3",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "19px",
                  marginBottom: "13px",
                }}
              >
                {item.icon}
              </div>

              <h3
                style={{
                  margin: 0,
                  fontSize: "14px",
                  fontWeight: 750,
                }}
              >
                {item.title}
              </h3>

              <p
                style={{
                  margin: "8px 0 0",
                  fontSize: "12px",
                  lineHeight: 1.6,
                  color: "#7b8699",
                }}
              >
                {item.text}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* CAPABILITIES */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.35fr 1fr",
          gap: "20px",
          marginBottom: "25px",
        }}
      >
        <div style={styles.card}>
          <h2 style={styles.sectionTitle}>What QINBIR Considers</h2>

          <p style={styles.sectionSub}>
            A university timetable is a constraint-based problem. QINBIR
            organizes the information required to solve it.
          </p>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "10px",
              marginTop: "20px",
            }}
          >
            {[
              ["✓", "Lecturer availability"],
              ["✓", "Room capacity"],
              ["✓", "Student-section conflicts"],
              ["✓", "Lecturer conflicts"],
              ["✓", "Course requirements"],
              ["✓", "Time-slot availability"],
              ["✓", "Academic programs"],
              ["✓", "Scheduling constraints"],
            ].map(([icon, text]) => (
              <div
                key={text}
                style={{
                  display: "flex",
                  gap: "9px",
                  alignItems: "center",
                  padding: "10px",
                  background: "#f8f9fc",
                  borderRadius: "8px",
                  fontSize: "12px",
                  color: "#4e5b73",
                }}
              >
                <span
                  style={{
                    color: "#3156d3",
                    fontWeight: 800,
                  }}
                >
                  {icon}
                </span>

                {text}
              </div>
            ))}
          </div>
        </div>

        <div
          style={{
            ...styles.card,
            background:
              "linear-gradient(145deg, #f4f7ff 0%, #ffffff 100%)",
          }}
        >
          <h2 style={styles.sectionTitle}>QINBIR Vision</h2>

          <p
            style={{
              color: "#657188",
              fontSize: "13px",
              lineHeight: 1.75,
              marginTop: "14px",
            }}
          >
            The goal of QINBIR is to reduce the manual effort required to
            prepare university timetables while giving administrators a
            structured environment for managing academic scheduling.
          </p>

          <div
            style={{
              marginTop: "18px",
              padding: "15px",
              borderRadius: "10px",
              background: "#ffffff",
              border: "1px solid #e5eaf5",
            }}
          >
            <div
              style={{
                fontWeight: 750,
                fontSize: "13px",
                color: "#3156d3",
              }}
            >
              Smart Scheduling
            </div>

            <div
              style={{
                marginTop: "5px",
                color: "#768196",
                fontSize: "12px",
                lineHeight: 1.6,
              }}
            >
              From academic data → resources → requirements → constraints
              → optimized timetable.
            </div>
          </div>
        </div>
      </div>

      {/* QUICK ACTIONS */}

      <section>
        <div style={{ marginBottom: "16px" }}>
          <h2 style={styles.sectionTitle}>Quick Actions</h2>

          <p style={styles.sectionSub}>
            Frequently used areas of the QINBIR system.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "16px",
          }}
        >
          {[
            {
              to: "/courses",
              title: "Manage Courses",
              text: "Add, edit and organize university courses.",
              icon: "▤",
            },
            {
              to: "/lecturers",
              title: "Manage Lecturers",
              text: "Configure teaching staff and departments.",
              icon: "♟",
            },
            {
              to: "/rooms",
              title: "Manage Rooms",
              text: "Configure classrooms and capacities.",
              icon: "▣",
            },
            {
              to: "/generate-schedule",
              title: "Generate Schedule",
              text: "Run the automatic scheduling process.",
              icon: "✦",
            },
          ].map((item) => (
            <Link
              key={item.to}
              to={item.to}
              style={{
                textDecoration: "none",
                color: "inherit",
              }}
            >
              <div
                style={{
                  ...styles.card,
                  transition: "transform 0.15s ease",
                }}
              >
                <div
                  style={{
                    width: "42px",
                    height: "42px",
                    borderRadius: "10px",
                    background: "#eef2ff",
                    color: "#3156d3",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "18px",
                    marginBottom: "13px",
                  }}
                >
                  {item.icon}
                </div>

                <div
                  style={{
                    fontSize: "14px",
                    fontWeight: 750,
                  }}
                >
                  {item.title}
                </div>

                <div
                  style={{
                    marginTop: "6px",
                    color: "#7b8699",
                    fontSize: "12px",
                    lineHeight: 1.5,
                  }}
                >
                  {item.text}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

/* ============================================================
   DEPARTMENTS
============================================================ */

function Departments() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      setItems(await apiRequest("/departments/"));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      await apiRequest("/departments/", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          code: code.trim().toUpperCase(),
        }),
      });

      setName("");
      setCode("");
      setMessage("Department created successfully.");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <PageTitle
        title="Departments"
        description="Manage the university's academic departments."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Department</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Department Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Computational and Natural Science"
                required
              />
            </FormField>

            <FormField label="Department Code">
              <input
                style={styles.input}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="CNS"
                required
              />
            </FormField>

            <div style={{ display: "flex", alignItems: "end" }}>
              <button
                style={{
                  ...styles.button,
                  ...styles.primaryButton,
                }}
              >
                Add Department
              </button>
            </div>
          </div>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Code</th>
                <th style={styles.th}>Name</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>
                    <span style={styles.badge}>{item.code}</span>
                  </td>
                  <td style={styles.td}>{item.name}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {!items.length && <EmptyState text="No departments found." />}
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   PROGRAMS
============================================================ */

function Programs() {
  const [items, setItems] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [departmentId, setDepartmentId] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const [programData, departmentData] = await Promise.all([
        apiRequest("/programs/"),
        apiRequest("/departments/"),
      ]);

      setItems(programData);
      setDepartments(departmentData);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/programs/", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          code: code.trim().toUpperCase(),
          department_id: Number(departmentId),
        }),
      });

      setName("");
      setCode("");
      setDepartmentId("");
      setMessage("Program created successfully.");
      setError("");
      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Programs"
        description="Manage academic programs and their departments."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Program</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Program Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Software Engineering"
                required
              />
            </FormField>

            <FormField label="Program Code">
              <input
                style={styles.input}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="SE"
                required
              />
            </FormField>

            <FormField label="Department">
              <select
                style={styles.select}
                value={departmentId}
                onChange={(e) => setDepartmentId(e.target.value)}
                required
              >
                <option value="">Select department</option>

                {departments.map((department) => (
                  <option key={department.id} value={department.id}>
                    {department.code} — {department.name}
                  </option>
                ))}
              </select>
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Program
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Code</th>
                <th style={styles.th}>Program</th>
                <th style={styles.th}>Department</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>
                    <span style={styles.badge}>{item.code}</span>
                  </td>
                  <td style={styles.td}>{item.name}</td>
                  <td style={styles.td}>
                    {item.department_name ||
                      item.department_code ||
                      item.department_id ||
                      "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {!items.length && <EmptyState text="No programs found." />}
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   COURSES
============================================================ */

function Courses() {
  const [courses, setCourses] = useState([]);
  const [programs, setPrograms] = useState([]);

  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [creditHours, setCreditHours] = useState("3");
  const [selectedPrograms, setSelectedPrograms] = useState([]);

  const [editingCourseId, setEditingCourseId] = useState(null);
  const [editCode, setEditCode] = useState("");
  const [editName, setEditName] = useState("");
  const [editCreditHours, setEditCreditHours] = useState("3");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadData() {
    setLoading(true);

    try {
      const [courseData, programData] = await Promise.all([
        apiRequest("/courses/"),
        apiRequest("/programs/"),
      ]);

      setCourses(courseData);
      setPrograms(programData);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  function toggleProgram(programId) {
    const id = Number(programId);

    setSelectedPrograms((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id]
    );
  }

  async function handleAddCourse(e) {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      const newCourse = await apiRequest("/courses/", {
        method: "POST",
        body: JSON.stringify({
          code: code.trim().toUpperCase(),
          name: name.trim(),
          credit_hours: Number(creditHours),
        }),
      });

      for (const programId of selectedPrograms) {
        await apiRequest(`/courses/${newCourse.id}/programs`, {
          method: "POST",
          body: JSON.stringify({
            program_id: Number(programId),
          }),
        });
      }

      setCode("");
      setName("");
      setCreditHours("3");
      setSelectedPrograms([]);

      setMessage("Course created successfully.");

      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  function startEdit(course) {
    setEditingCourseId(course.id);
    setEditCode(course.code);
    setEditName(course.name);
    setEditCreditHours(String(course.credit_hours || 3));

    setMessage("");
    setError("");
  }

  function cancelEdit() {
    setEditingCourseId(null);
    setEditCode("");
    setEditName("");
    setEditCreditHours("3");
  }

  async function saveEdit(courseId) {
    setMessage("");
    setError("");

    try {
      await apiRequest(`/courses/${courseId}`, {
        method: "PUT",
        body: JSON.stringify({
          code: editCode.trim().toUpperCase(),
          name: editName.trim(),
          credit_hours: Number(editCreditHours),
        }),
      });

      setMessage("Course updated successfully.");
      cancelEdit();
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  function creditPattern(value) {
    if (Number(value) === 2) {
      return "1 × 2-hour session";
    }

    if (Number(value) === 3) {
      return "2 sessions: 2h + 1h";
    }

    if (Number(value) === 4) {
      return "2 × 2-hour sessions";
    }

    return "Scheduling pattern";
  }

  return (
    <div>
      <PageTitle
        title="Courses"
        description="Manage the university course catalog, credit hours and program relationships."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      {/* ADD COURSE */}

      <div style={{ ...styles.card, marginBottom: "20px" }}>
        <h2 style={styles.sectionTitle}>Add Course</h2>

        <p style={styles.sectionSub}>
          Select the credit-hour value used by this course.
        </p>

        <form onSubmit={handleAddCourse} style={{ marginTop: "20px" }}>
          <div style={styles.formGrid}>
            <FormField label="Course Code">
              <input
                style={styles.input}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="SE201"
                required
              />
            </FormField>

            <FormField label="Course Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Database Systems"
                required
              />
            </FormField>

            {/* IMPORTANT CREDIT HOURS DROPDOWN */}

            <FormField label="Credit Hours">
              <select
                style={{
                  ...styles.select,
                  border: "2px solid #3156d3",
                  background: "#f8faff",
                  fontWeight: 650,
                }}
                value={creditHours}
                onChange={(e) => setCreditHours(e.target.value)}
                required
              >
                <option value="2">2 Credit Hours</option>
                <option value="3">3 Credit Hours</option>
                <option value="4">4 Credit Hours</option>
              </select>

              <div
                style={{
                  marginTop: "6px",
                  fontSize: "11px",
                  color: "#68758e",
                }}
              >
                {creditPattern(creditHours)}
              </div>
            </FormField>
          </div>

          <div style={{ marginTop: "18px" }}>
            <label style={styles.label}>
              Programs — select one or more
            </label>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fill, minmax(180px, 1fr))",
                gap: "8px",
                padding: "12px",
                background: "#f8f9fc",
                borderRadius: "9px",
                border: "1px solid #e6eaf0",
                maxHeight: "220px",
                overflowY: "auto",
              }}
            >
              {programs.map((program) => (
                <label
                  key={program.id}
                  style={{
                    display: "flex",
                    gap: "7px",
                    alignItems: "center",
                    fontSize: "12px",
                    color: "#4c5870",
                    cursor: "pointer",
                  }}
                >
                  <input
                    type="checkbox"
                    checked={selectedPrograms.includes(program.id)}
                    onChange={() => toggleProgram(program.id)}
                  />

                  {program.code} — {program.name}
                </label>
              ))}
            </div>
          </div>

          <button
            type="submit"
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "17px",
            }}
          >
            + Add Course
          </button>
        </form>
      </div>

      {/* COURSE LIST */}

      <div style={styles.card}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <h2 style={styles.sectionTitle}>Course Catalog</h2>

            <p style={styles.sectionSub}>
              {courses.length} courses currently registered.
            </p>
          </div>
        </div>

        {loading ? (
          <Loading />
        ) : (
          <div style={styles.tableWrap}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>ID</th>
                  <th style={styles.th}>Code</th>
                  <th style={styles.th}>Course Name</th>
                  <th style={styles.th}>Credit Hours</th>
                  <th style={styles.th}>Programs</th>
                  <th style={styles.th}>Actions</th>
                </tr>
              </thead>

              <tbody>
                {courses.map((course) => {
                  const isEditing =
                    editingCourseId === course.id;

                  if (isEditing) {
                    return (
                      <tr key={course.id}>
                        <td style={styles.td}>{course.id}</td>

                        <td style={styles.td}>
                          <input
                            style={styles.input}
                            value={editCode}
                            onChange={(e) =>
                              setEditCode(e.target.value)
                            }
                          />
                        </td>

                        <td style={styles.td}>
                          <input
                            style={styles.input}
                            value={editName}
                            onChange={(e) =>
                              setEditName(e.target.value)
                            }
                          />
                        </td>

                        <td style={styles.td}>
                          {/* EDIT CREDIT HOURS DROPDOWN */}

                          <select
                            style={{
                              ...styles.select,
                              border: "2px solid #3156d3",
                            }}
                            value={editCreditHours}
                            onChange={(e) =>
                              setEditCreditHours(e.target.value)
                            }
                          >
                            <option value="2">
                              2 Credit Hours
                            </option>
                            <option value="3">
                              3 Credit Hours
                            </option>
                            <option value="4">
                              4 Credit Hours
                            </option>
                          </select>

                          <div
                            style={{
                              fontSize: "10px",
                              color: "#738098",
                              marginTop: "5px",
                            }}
                          >
                            {creditPattern(editCreditHours)}
                          </div>
                        </td>

                        <td style={styles.td}>
                          {course.programs?.length
                            ? course.programs
                                .map((p) => p.code)
                                .join(", ")
                            : "—"}
                        </td>

                        <td style={styles.td}>
                          <div
                            style={{
                              display: "flex",
                              gap: "6px",
                            }}
                          >
                            <button
                              style={{
                                ...styles.button,
                                ...styles.primaryButton,
                                padding: "7px 10px",
                              }}
                              onClick={() =>
                                saveEdit(course.id)
                              }
                            >
                              Save
                            </button>

                            <button
                              style={{
                                ...styles.button,
                                ...styles.secondaryButton,
                                padding: "7px 10px",
                              }}
                              onClick={cancelEdit}
                            >
                              Cancel
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  }

                  return (
                    <tr key={course.id}>
                      <td style={styles.td}>{course.id}</td>

                      <td style={styles.td}>
                        <span
                          style={{
                            ...styles.badge,
                            background: "#eef3ff",
                            color: "#3156d3",
                          }}
                        >
                          {course.code}
                        </span>
                      </td>

                      <td
                        style={{
                          ...styles.td,
                          fontWeight: 600,
                        }}
                      >
                        {course.name}
                      </td>

                      <td style={styles.td}>
                        <span
                          style={{
                            display: "inline-flex",
                            alignItems: "center",
                            padding: "6px 10px",
                            borderRadius: "7px",
                            background: "#f0f5ff",
                            color: "#3156d3",
                            fontWeight: 750,
                            fontSize: "12px",
                          }}
                        >
                          {course.credit_hours} CH
                        </span>
                      </td>

                      <td style={styles.td}>
                        {course.programs?.length ? (
                          <div
                            style={{
                              display: "flex",
                              gap: "5px",
                              flexWrap: "wrap",
                            }}
                          >
                            {course.programs.map((program) => (
                              <span
                                key={program.id}
                                style={styles.badge}
                              >
                                {program.code}
                              </span>
                            ))}
                          </div>
                        ) : (
                          "—"
                        )}
                      </td>

                      <td style={styles.td}>
                        <button
                          style={{
                            ...styles.button,
                            ...styles.secondaryButton,
                            padding: "7px 11px",
                          }}
                          onClick={() => startEdit(course)}
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            {!courses.length && (
              <EmptyState text="No courses found." />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/* ============================================================
   LECTURERS
============================================================ */

function Lecturers() {
  const [items, setItems] = useState([]);
  const [departments, setDepartments] = useState([]);

  const [userId, setUserId] = useState("");
  const [departmentId, setDepartmentId] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [name, setName] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const [lecturers, departments] = await Promise.all([
        apiRequest("/lecturers/"),
        apiRequest("/departments/"),
      ]);

      setItems(lecturers);
      setDepartments(departments);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/lecturers/", {
        method: "POST",
        body: JSON.stringify({
          user_id: Number(userId),
          department_id: Number(departmentId),
          employee_id: employeeId.trim(),
          name: name.trim(),
        }),
      });

      setUserId("");
      setDepartmentId("");
      setEmployeeId("");
      setName("");

      setMessage("Lecturer created successfully.");
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Lecturers"
        description="Manage university teaching staff and their academic departments."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Lecturer</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="User ID">
              <input
                type="number"
                style={styles.input}
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="1"
                required
              />
            </FormField>

            <FormField label="Employee ID">
              <input
                style={styles.input}
                value={employeeId}
                onChange={(e) =>
                  setEmployeeId(e.target.value)
                }
                placeholder="LEC-001"
                required
              />
            </FormField>

            <FormField label="Lecturer Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Dr. Abebe Kebede"
                required
              />
            </FormField>

            <FormField label="Department">
              <select
                style={styles.select}
                value={departmentId}
                onChange={(e) =>
                  setDepartmentId(e.target.value)
                }
                required
              >
                <option value="">Select department</option>

                {departments.map((department) => (
                  <option
                    key={department.id}
                    value={department.id}
                  >
                    {department.code} — {department.name}
                  </option>
                ))}
              </select>
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Lecturer
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Employee ID</th>
                <th style={styles.th}>Name</th>
                <th style={styles.th}>Department</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>{item.employee_id}</td>
                  <td style={styles.td}>{item.name}</td>
                  <td style={styles.td}>
                    {item.department_name ||
                      item.department_code ||
                      item.department_id ||
                      "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   STUDENT SECTIONS
============================================================ */

function StudentSections() {
  const [items, setItems] = useState([]);
  const [programs, setPrograms] = useState([]);

  const [name, setName] = useState("");
  const [programId, setProgramId] = useState("");
  const [year, setYear] = useState("1");
  const [semester, setSemester] = useState("1");
  const [studentCount, setStudentCount] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const [sections, programs] = await Promise.all([
        apiRequest("/student-sections/"),
        apiRequest("/programs/"),
      ]);

      setItems(sections);
      setPrograms(programs);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/student-sections/", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          program_id: Number(programId),
          year: Number(year),
          semester: Number(semester),
          student_count: Number(studentCount),
        }),
      });

      setName("");
      setProgramId("");
      setYear("1");
      setSemester("1");
      setStudentCount("");

      setMessage("Student section created successfully.");
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Student Sections"
        description="Manage student groups that participate in course scheduling."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Student Section</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Section Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="SE-1A"
                required
              />
            </FormField>

            <FormField label="Program">
              <select
                style={styles.select}
                value={programId}
                onChange={(e) =>
                  setProgramId(e.target.value)
                }
                required
              >
                <option value="">Select program</option>

                {programs.map((program) => (
                  <option key={program.id} value={program.id}>
                    {program.code} — {program.name}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Year">
              <select
                style={styles.select}
                value={year}
                onChange={(e) => setYear(e.target.value)}
              >
                <option value="1">Year 1</option>
                <option value="2">Year 2</option>
                <option value="3">Year 3</option>
                <option value="4">Year 4</option>
              </select>
            </FormField>

            <FormField label="Semester">
              <select
                style={styles.select}
                value={semester}
                onChange={(e) =>
                  setSemester(e.target.value)
                }
              >
                <option value="1">Semester 1</option>
                <option value="2">Semester 2</option>
              </select>
            </FormField>

            <FormField label="Student Count">
              <input
                type="number"
                style={styles.input}
                value={studentCount}
                onChange={(e) =>
                  setStudentCount(e.target.value)
                }
                min="1"
                required
              />
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Section
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Section</th>
                <th style={styles.th}>Program</th>
                <th style={styles.th}>Year</th>
                <th style={styles.th}>Semester</th>
                <th style={styles.th}>Students</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>{item.name}</td>
                  <td style={styles.td}>
                    {item.program_code ||
                      item.program_name ||
                      item.program_id}
                  </td>
                  <td style={styles.td}>{item.year}</td>
                  <td style={styles.td}>{item.semester}</td>
                  <td style={styles.td}>
                    {item.student_count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   ROOMS
============================================================ */

function Rooms() {
  const [items, setItems] = useState([]);

  const [name, setName] = useState("");
  const [building, setBuilding] = useState("");
  const [capacity, setCapacity] = useState("");
  const [roomType, setRoomType] = useState("Classroom");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      setItems(await apiRequest("/rooms/"));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/rooms/", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          building: building.trim(),
          capacity: Number(capacity),
          room_type: roomType.trim(),
        }),
      });

      setName("");
      setBuilding("");
      setCapacity("");
      setRoomType("Classroom");

      setMessage("Room created successfully.");
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Rooms"
        description="Manage classrooms and other teaching spaces."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Room</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Room Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Room 201"
                required
              />
            </FormField>

            <FormField label="Building">
              <input
                style={styles.input}
                value={building}
                onChange={(e) =>
                  setBuilding(e.target.value)
                }
                placeholder="Main Building"
                required
              />
            </FormField>

            <FormField label="Capacity">
              <input
                type="number"
                min="1"
                style={styles.input}
                value={capacity}
                onChange={(e) =>
                  setCapacity(e.target.value)
                }
                required
              />
            </FormField>

            <FormField label="Room Type">
              <select
                style={styles.select}
                value={roomType}
                onChange={(e) =>
                  setRoomType(e.target.value)
                }
              >
                <option>Classroom</option>
                <option>Laboratory</option>
                <option>Computer Lab</option>
                <option>Auditorium</option>
                <option>Workshop</option>
              </select>
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Room
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Room</th>
                <th style={styles.th}>Building</th>
                <th style={styles.th}>Capacity</th>
                <th style={styles.th}>Type</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>{item.name}</td>
                  <td style={styles.td}>{item.building}</td>
                  <td style={styles.td}>{item.capacity}</td>
                  <td style={styles.td}>{item.room_type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   TIME SLOTS
============================================================ */

function TimeSlots() {
  const [items, setItems] = useState([]);

  const [day, setDay] = useState("Monday");
  const [startTime, setStartTime] = useState("08:00");
  const [endTime, setEndTime] = useState("10:00");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      setItems(await apiRequest("/time-slots/"));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/time-slots/", {
        method: "POST",
        body: JSON.stringify({
          day,
          start_time: startTime,
          end_time: endTime,
        }),
      });

      setMessage("Time slot created successfully.");
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Time Slots"
        description="Define the weekly periods available for teaching."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Time Slot</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Day">
              <select
                style={styles.select}
                value={day}
                onChange={(e) => setDay(e.target.value)}
              >
                <option>Monday</option>
                <option>Tuesday</option>
                <option>Wednesday</option>
                <option>Thursday</option>
                <option>Friday</option>
              </select>
            </FormField>

            <FormField label="Start Time">
              <input
                type="time"
                style={styles.input}
                value={startTime}
                onChange={(e) =>
                  setStartTime(e.target.value)
                }
              />
            </FormField>

            <FormField label="End Time">
              <input
                type="time"
                style={styles.input}
                value={endTime}
                onChange={(e) =>
                  setEndTime(e.target.value)
                }
              />
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Time Slot
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Day</th>
                <th style={styles.th}>Start</th>
                <th style={styles.th}>End</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>{item.day}</td>
                  <td style={styles.td}>{item.start_time}</td>
                  <td style={styles.td}>{item.end_time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   LECTURER AVAILABILITY
============================================================ */

function LecturerAvailability() {
  const [items, setItems] = useState([]);
  const [lecturers, setLecturers] = useState([]);
  const [timeSlots, setTimeSlots] = useState([]);

  const [lecturerId, setLecturerId] = useState("");
  const [timeSlotId, setTimeSlotId] = useState("");
  const [isAvailable, setIsAvailable] = useState(true);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const [availability, lecturerData, slotData] =
        await Promise.all([
          apiRequest("/lecturer-availability/"),
          apiRequest("/lecturers/"),
          apiRequest("/time-slots/"),
        ]);

      setItems(availability);
      setLecturers(lecturerData);
      setTimeSlots(slotData);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/lecturer-availability/", {
        method: "POST",
        body: JSON.stringify({
          lecturer_id: Number(lecturerId),
          time_slot_id: Number(timeSlotId),
          is_available: isAvailable,
        }),
      });

      setMessage("Availability saved successfully.");
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Lecturer Availability"
        description="Define when lecturers are available or unavailable to teach."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>
          Add Availability Record
        </h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Lecturer">
              <select
                style={styles.select}
                value={lecturerId}
                onChange={(e) =>
                  setLecturerId(e.target.value)
                }
                required
              >
                <option value="">Select lecturer</option>

                {lecturers.map((lecturer) => (
                  <option
                    key={lecturer.id}
                    value={lecturer.id}
                  >
                    {lecturer.name}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Time Slot">
              <select
                style={styles.select}
                value={timeSlotId}
                onChange={(e) =>
                  setTimeSlotId(e.target.value)
                }
                required
              >
                <option value="">Select time slot</option>

                {timeSlots.map((slot) => (
                  <option key={slot.id} value={slot.id}>
                    {slot.day} {slot.start_time}–{slot.end_time}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Availability">
              <select
                style={styles.select}
                value={String(isAvailable)}
                onChange={(e) =>
                  setIsAvailable(e.target.value === "true")
                }
              >
                <option value="true">Available</option>
                <option value="false">Unavailable</option>
              </select>
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Save Availability
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Lecturer</th>
                <th style={styles.th}>Time Slot</th>
                <th style={styles.th}>Status</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>
                    {item.lecturer_name ||
                      item.lecturer_id}
                  </td>
                  <td style={styles.td}>
                    {item.time_slot ||
                      item.time_slot_id}
                  </td>
                  <td style={styles.td}>
                    <span
                      style={{
                        ...styles.badge,
                        background: item.is_available
                          ? "#edf8f0"
                          : "#fff0f0",
                        color: item.is_available
                          ? "#28753c"
                          : "#b72d2d",
                      }}
                    >
                      {item.is_available
                        ? "Available"
                        : "Unavailable"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   COURSE REQUIREMENTS
============================================================ */

function CourseRequirements() {
  const [items, setItems] = useState([]);
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
  const [error, setError] = useState("");

  async function load() {
    try {
      const [
        requirements,
        courseData,
        sectionData,
        lecturerData,
      ] = await Promise.all([
        apiRequest("/course-requirements/"),
        apiRequest("/courses/"),
        apiRequest("/student-sections/"),
        apiRequest("/lecturers/"),
      ]);

      setItems(requirements);
      setCourses(courseData);
      setSections(sectionData);
      setLecturers(lecturerData);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

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

      setMessage("Course requirement created successfully.");
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Course Requirements"
        description="Define which courses are taught to which student sections and by which lecturers."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>
          Add Course Requirement
        </h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Course">
              <select
                style={styles.select}
                value={courseId}
                onChange={(e) =>
                  setCourseId(e.target.value)
                }
                required
              >
                <option value="">Select course</option>

                {courses.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.code} — {course.name}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Student Section">
              <select
                style={styles.select}
                value={studentSectionId}
                onChange={(e) =>
                  setStudentSectionId(e.target.value)
                }
                required
              >
                <option value="">Select section</option>

                {sections.map((section) => (
                  <option key={section.id} value={section.id}>
                    {section.name}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Lecturer">
              <select
                style={styles.select}
                value={lecturerId}
                onChange={(e) =>
                  setLecturerId(e.target.value)
                }
                required
              >
                <option value="">Select lecturer</option>

                {lecturers.map((lecturer) => (
                  <option
                    key={lecturer.id}
                    value={lecturer.id}
                  >
                    {lecturer.name}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Sessions Per Week">
              <input
                type="number"
                min="1"
                style={styles.input}
                value={sessionsPerWeek}
                onChange={(e) =>
                  setSessionsPerWeek(e.target.value)
                }
              />
            </FormField>

            <FormField label="Long Session Hours">
              <input
                type="number"
                min="1"
                style={styles.input}
                value={longSessionHours}
                onChange={(e) =>
                  setLongSessionHours(e.target.value)
                }
              />
            </FormField>

            <FormField label="Short Session Hours">
              <input
                type="number"
                min="1"
                style={styles.input}
                value={shortSessionHours}
                onChange={(e) =>
                  setShortSessionHours(e.target.value)
                }
              />
            </FormField>
          </div>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Requirement
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Course</th>
                <th style={styles.th}>Section</th>
                <th style={styles.th}>Lecturer</th>
                <th style={styles.th}>Sessions</th>
                <th style={styles.th}>Long</th>
                <th style={styles.th}>Short</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>
                    {item.course_code ||
                      item.course_id}
                  </td>
                  <td style={styles.td}>
                    {item.section_name ||
                      item.student_section_id}
                  </td>
                  <td style={styles.td}>
                    {item.lecturer_name ||
                      item.lecturer_id}
                  </td>
                  <td style={styles.td}>
                    {item.sessions_per_week}
                  </td>
                  <td style={styles.td}>
                    {item.long_session_hours}h
                  </td>
                  <td style={styles.td}>
                    {item.short_session_hours}h
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   CONSTRAINTS
============================================================ */

function Constraints() {
  const [items, setItems] = useState([]);

  const [name, setName] = useState("");
  const [type, setType] = useState("HARD");
  const [description, setDescription] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [weight, setWeight] = useState("1");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      setItems(await apiRequest("/constraints/"));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e) {
    e.preventDefault();

    try {
      await apiRequest("/constraints/", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          type,
          description: description.trim(),
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
      setError("");

      load();
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div>
      <PageTitle
        title="Constraints"
        description="Configure rules that guide the scheduling engine."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Add Constraint</h2>

        <form onSubmit={submit} style={{ marginTop: "18px" }}>
          <div style={styles.formGrid}>
            <FormField label="Constraint Name">
              <input
                style={styles.input}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="No lecturer conflict"
                required
              />
            </FormField>

            <FormField label="Type">
              <select
                style={styles.select}
                value={type}
                onChange={(e) => setType(e.target.value)}
              >
                <option value="HARD">HARD</option>
                <option value="SOFT">SOFT</option>
              </select>
            </FormField>

            <FormField label="Weight">
              <input
                type="number"
                min="1"
                style={styles.input}
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
              />
            </FormField>
          </div>

          <div style={{ marginTop: "15px" }}>
            <FormField label="Description">
              <textarea
                style={styles.textarea}
                value={description}
                onChange={(e) =>
                  setDescription(e.target.value)
                }
                placeholder="Describe the scheduling rule..."
              />
            </FormField>
          </div>

          <label
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              fontSize: "13px",
              marginTop: "13px",
            }}
          >
            <input
              type="checkbox"
              checked={isActive}
              onChange={(e) =>
                setIsActive(e.target.checked)
              }
            />

            Active constraint
          </label>

          <button
            style={{
              ...styles.button,
              ...styles.primaryButton,
              marginTop: "16px",
            }}
          >
            Add Constraint
          </button>
        </form>

        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Name</th>
                <th style={styles.th}>Type</th>
                <th style={styles.th}>Weight</th>
                <th style={styles.th}>Active</th>
                <th style={styles.th}>Description</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>{item.name}</td>
                  <td style={styles.td}>
                    <span style={styles.badge}>
                      {item.type}
                    </span>
                  </td>
                  <td style={styles.td}>{item.weight}</td>
                  <td style={styles.td}>
                    {item.is_active ? "Yes" : "No"}
                  </td>
                  <td style={styles.td}>
                    {item.description || "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   GENERATE SCHEDULE
============================================================ */

function GenerateSchedule() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function generate() {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const result = await apiRequest("/schedules/generate", {
        method: "POST",
      });

      setMessage(
        typeof result === "string"
          ? result
          : result?.message ||
              "Schedule generated successfully."
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <PageTitle
        title="Generate Schedule"
        description="Run the QINBIR scheduling engine to create an automatic timetable."
      />

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}

      <div
        style={{
          ...styles.card,
          maxWidth: "900px",
        }}
      >
        <div
          style={{
            width: "60px",
            height: "60px",
            borderRadius: "15px",
            background: "#eef2ff",
            color: "#3156d3",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "27px",
            marginBottom: "18px",
          }}
        >
          ✦
        </div>

        <h2 style={styles.sectionTitle}>
          Automatic Timetable Generation
        </h2>

        <p
          style={{
            color: "#68758c",
            fontSize: "13px",
            lineHeight: 1.7,
            maxWidth: "700px",
          }}
        >
          QINBIR uses the configured courses, student sections,
          lecturers, rooms, time slots, availability records and
          scheduling requirements to search for a valid timetable.
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "12px",
            marginTop: "20px",
          }}
        >
          {[
            ["01", "Read Requirements"],
            ["02", "Apply Constraints"],
            ["03", "Build Timetable"],
          ].map(([number, title]) => (
            <div
              key={number}
              style={{
                padding: "15px",
                background: "#f8f9fc",
                borderRadius: "9px",
              }}
            >
              <div
                style={{
                  fontSize: "10px",
                  color: "#3156d3",
                  fontWeight: 800,
                }}
              >
                {number}
              </div>

              <div
                style={{
                  fontSize: "12px",
                  fontWeight: 700,
                  marginTop: "5px",
                }}
              >
                {title}
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={generate}
          disabled={loading}
          style={{
            ...styles.button,
            ...styles.primaryButton,
            marginTop: "24px",
            padding: "12px 20px",
            opacity: loading ? 0.65 : 1,
          }}
        >
          {loading
            ? "Generating Schedule..."
            : "✦ Generate Automatic Schedule"}
        </button>
      </div>
    </div>
  );
}

/* ============================================================
   TIMETABLE
============================================================ */

function Timetable() {
  const [schedules, setSchedules] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [schedule, setSchedule] = useState(null);
  const [error, setError] = useState("");

  const days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
  ];

  const timeRows = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
  ];

  async function loadSchedules() {
    try {
      setError("");

      const data = await apiRequest("/schedules/");
      setSchedules(data);

      if (data.length) {
        setSelectedId(String(data[0].id));
      }
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadSchedules();
  }, []);

  useEffect(() => {
    async function loadSchedule() {
      if (!selectedId) {
        setSchedule(null);
        return;
      }

      try {
        setError("");

        const data = await apiRequest(
          `/schedules/${selectedId}`
        );

        setSchedule(data);
      } catch (err) {
        setError(err.message);
      }
    }

    loadSchedule();
  }, [selectedId]);

  function getHour(time) {
    if (!time) return 8;

    const parts = time.split(":");
    return Number(parts[0]);
  }

  function getDuration(start, end) {
    if (!start || !end) return 1;

    const startHour = getHour(start);
    const endHour = getHour(end);

    return Math.max(1, endHour - startHour);
  }

  function getEntryStyle(entry) {
    const startHour = getHour(entry.start_time);
    const duration = getDuration(
      entry.start_time,
      entry.end_time
    );

    const top =
      (startHour - 8) * 60;

    const height =
      duration * 60 - 8;

    return {
      position: "absolute",
      top: `${top}px`,
      left: "4px",
      right: "4px",
      height: `${height}px`,
      padding: "8px",
      borderRadius: "8px",
      background:
        "linear-gradient(135deg, #2563eb, #1d4ed8)",
      color: "white",
      boxSizing: "border-box",
      overflow: "hidden",
      cursor: "default",
      boxShadow:
        "0 3px 8px rgba(0, 0, 0, 0.15)",
      zIndex: 2,
    };
  }

  function getEntriesForDay(day) {
    return (schedule?.entries || []).filter(
      (entry) => entry.day === day
    );
  }

  return (
    <div>
      <PageTitle
        title="Timetable"
        description="View schedules generated by the QINBIR scheduling engine."
      />

      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}

      {/* =====================================================
          SCHEDULE SELECTOR
      ===================================================== */}

      <div style={styles.card}>
        <FormField label="Schedule">
          <select
            style={{
              ...styles.select,
              maxWidth: "500px",
            }}
            value={selectedId}
            onChange={(e) =>
              setSelectedId(e.target.value)
            }
          >
            <option value="">
              Select schedule
            </option>

            {schedules.map((item) => (
              <option
                key={item.id}
                value={item.id}
              >
                {item.name} — {item.status}
              </option>
            ))}
          </select>
        </FormField>
      </div>

      {schedule && (
        <>
          {/* =================================================
              GRAPHICAL WEEKLY TIMETABLE
          ================================================= */}

          <div
            style={{
              ...styles.card,
              marginTop: "20px",
            }}
          >
            <div
              style={{
                marginBottom: "20px",
              }}
            >
              <h2 style={styles.sectionTitle}>
                Weekly Timetable
              </h2>

              <p style={styles.sectionSub}>
                Graphical view of the generated
                university schedule.
              </p>
            </div>

            <div
              style={{
                overflowX: "auto",
                border: "1px solid #e5e7eb",
                borderRadius: "10px",
              }}
            >
              <div
                style={{
                  minWidth: "900px",
                  background: "#ffffff",
                }}
              >
                {/* DAY HEADER */}

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "70px repeat(5, 1fr)",
                    borderBottom:
                      "1px solid #e5e7eb",
                  }}
                >
                  <div
                    style={{
                      padding: "14px 8px",
                      background: "#f8fafc",
                      borderRight:
                        "1px solid #e5e7eb",
                    }}
                  />

                  {days.map((day) => (
                    <div
                      key={day}
                      style={{
                        padding: "14px 8px",
                        textAlign: "center",
                        fontWeight: "700",
                        color: "#1e293b",
                        background: "#f8fafc",
                        borderRight:
                          "1px solid #e5e7eb",
                      }}
                    >
                      {day}
                    </div>
                  ))}
                </div>

                {/* TIME GRID */}

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "70px repeat(5, 1fr)",
                  }}
                >
                  {/* TIME COLUMN */}

                  <div>
                    {timeRows
                      .slice(0, -1)
                      .map((time) => (
                        <div
                          key={time}
                          style={{
                            height: "60px",
                            boxSizing:
                              "border-box",
                            padding:
                              "8px 6px",
                            textAlign:
                              "center",
                            fontSize:
                              "12px",
                            color: "#64748b",
                            borderRight:
                              "1px solid #e5e7eb",
                            borderBottom:
                              "1px solid #e5e7eb",
                            background:
                              "#f8fafc",
                          }}
                        >
                          {time}
                        </div>
                      ))}
                  </div>

                  {/* DAY COLUMNS */}

                  {days.map((day) => (
                    <div
                      key={day}
                      style={{
                        position: "relative",
                        height: "420px",
                        borderRight:
                          "1px solid #e5e7eb",
                        background:
                          "#ffffff",
                      }}
                    >
                      {/* HORIZONTAL TIME LINES */}

                      {timeRows
                        .slice(0, -1)
                        .map((time) => (
                          <div
                            key={time}
                            style={{
                              height: "60px",
                              boxSizing:
                                "border-box",
                              borderBottom:
                                "1px solid #e5e7eb",
                            }}
                          />
                        ))}

                      {/* SCHEDULE ENTRIES */}

                      {getEntriesForDay(day).map(
                        (entry) => (
                          <div
                            key={entry.id}
                            style={getEntryStyle(
                              entry
                            )}
                            title={`${entry.course} | ${entry.lecturer} | ${entry.student_section} | ${entry.room}`}
                          >
                            <div
                              style={{
                                fontWeight: "800",
                                fontSize: "13px",
                                marginBottom:
                                  "4px",
                              }}
                            >
                              {entry.course}
                            </div>

                            <div
                              style={{
                                fontSize: "11px",
                                opacity: 0.95,
                                marginBottom:
                                  "3px",
                              }}
                            >
                              {entry.room}
                            </div>

                            <div
                              style={{
                                fontSize: "10px",
                                opacity: 0.9,
                              }}
                            >
                              {entry.student_section}
                            </div>

                            <div
                              style={{
                                fontSize: "10px",
                                opacity: 0.9,
                                marginTop:
                                  "2px",
                              }}
                            >
                              {entry.start_time}–
                              {entry.end_time}
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* =================================================
              DETAILED TABLE
          ================================================= */}

          <div
            style={{
              ...styles.card,
              marginTop: "20px",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
                alignItems: "center",
                marginBottom: "20px",
              }}
            >
              <div>
                <h2 style={styles.sectionTitle}>
                  {schedule.name}
                </h2>

                <p style={styles.sectionSub}>
                  Schedule ID: {schedule.id}
                </p>
              </div>

              <span style={styles.badge}>
                {schedule.status}
              </span>
            </div>

            <div style={styles.tableWrap}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>
                      Course
                    </th>

                    <th style={styles.th}>
                      Lecturer
                    </th>

                    <th style={styles.th}>
                      Section
                    </th>

                    <th style={styles.th}>
                      Room
                    </th>

                    <th style={styles.th}>
                      Day
                    </th>

                    <th style={styles.th}>
                      Time
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {(schedule.entries || []).map(
                    (entry) => (
                      <tr key={entry.id}>
                        <td style={styles.td}>
                          {entry.course || "—"}
                        </td>

                        <td style={styles.td}>
                          {entry.lecturer || "—"}
                        </td>

                        <td style={styles.td}>
                          {entry.student_section ||
                            "—"}
                        </td>

                        <td style={styles.td}>
                          {entry.room || "—"}
                        </td>

                        <td style={styles.td}>
                          {entry.day || "—"}
                        </td>

                        <td style={styles.td}>
                          {entry.start_time &&
                          entry.end_time
                            ? `${entry.start_time}–${entry.end_time}`
                            : "—"}
                        </td>
                      </tr>
                    )
                  )}
                </tbody>
              </table>

              {!schedule.entries?.length && (
                <EmptyState
                  text="No schedule entries found."
                />
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
/* ============================================================
   APP
============================================================ */

function App() {
  return (
    <BrowserRouter>
      <Layout>
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
      </Layout>
    </BrowserRouter>
  );
}

export default App;