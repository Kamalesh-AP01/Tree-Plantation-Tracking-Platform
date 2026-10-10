import { useState } from "react";
import Dashboard from "./Dashboard";
import Register from "./Register";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

const API_URL = "https://tree-plantation-api.onrender.com";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);

    try {
      const formData = new URLSearchParams();

      formData.append("email", email);
      formData.append("password", password);

      const response = await axios.post(
        `${API_URL}/login`,
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          withCredentials: true,
        }
      );

      console.log(response.data);
      setLoggedIn(true);
    } catch (error) {
      console.error(error);

      if (error.response) {
        setMessage(
          error.response.data?.message ||
            "Invalid email or password"
        );
      } else {
        setMessage("Cannot connect to the backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  if (loggedIn) {
    return <Dashboard />;
  }

  if (showRegister) {
    return (
      <Register
        onBackToLogin={() => {
          setShowRegister(false);
          setMessage("");
        }}
      />
    );
  }

  return (
    <div
      className="min-vh-100 d-flex justify-content-center align-items-center"
      style={{
        backgroundColor: "#f5f7f6",
        padding: "30px",
      }}
    >
      <div
        className="card shadow-lg border-0"
        style={{
          width: "420px",
          borderRadius: "18px",
        }}
      >
        <div className="card-body p-5">
          <div className="text-center mb-4">
            <div
              style={{
                fontSize: "55px",
                marginBottom: "10px",
              }}
            >
              🌱
            </div>

            <h1 className="fw-bold text-success">
              Tree Plantation
            </h1>

            <h4 className="text-secondary">
              Tracking Platform
            </h4>

            <p className="text-muted mt-3">
              College Admin Login
            </p>
          </div>

          <form onSubmit={handleLogin}>
            <div className="mb-3">
              <label className="form-label fw-semibold">
                Email
              </label>

              <input
                type="email"
                className="form-control form-control-lg"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="form-label fw-semibold">
                Password
              </label>

              <input
                type="password"
                className="form-control form-control-lg"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-success btn-lg w-100"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <div className="text-center mt-4">
            <p className="text-muted mb-2">
              New student?
            </p>

            <button
              type="button"
              className="btn btn-outline-success"
              onClick={() => {
                setShowRegister(true);
                setMessage("");
              }}
            >
              Create User Account
            </button>
          </div>

          {message && (
            <div className="alert alert-info mt-4 text-center">
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
