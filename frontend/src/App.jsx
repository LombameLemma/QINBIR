
import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/schedule-entries/?schedule_id=2`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load schedule");
        }

        return response.json();
      })
      .then((data) => {
        setEntries(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not connect to QINBIR API.");
        setLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>QINBIR</h1>
          <p>Automatic University Course Scheduling System</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Connected
        </div>
      </header>

      <main className="main">
        <div className="page-title">
          <div>
            <h2>Generated Timetable</h2>
            <p>Semester 1 - 2026/2027</p>
          </div>

          <div className="summary">
            <strong>{entries.length}</strong>
            <span>Sessions</span>
          </div>
        </div>

        {loading && (
          <div className="message">
            Loading timetable...
          </div>
        )}

        {error && (
          <div className="message error">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="schedule-grid">
            {entries.map((entry) => (
              <div className="schedule-card" key={entry.id}>
                <div className="card-time">
                  <strong>{entry.start_time}</strong>
                  <span>{entry.end_time}</span>
                </div>

                <div className="card-content">
                  <h3>{entry.course}</h3>

                  <p>
                    <strong>Lecturer:</strong>{" "}
                    {entry.lecturer}
                  </p>

                  <p>
                    <strong>Section:</strong>{" "}
                    {entry.student_section}
                  </p>

                  <p>
                    <strong>Room:</strong>{" "}
                    {entry.room}
                  </p>
                </div>

                <div className="card-day">
                  {entry.day}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

