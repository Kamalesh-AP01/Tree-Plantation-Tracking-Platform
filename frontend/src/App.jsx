import { useState } from "react";
import Dashboard from "./Dashboard";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);

    try {
      // FastAPI expects Form data
      const formData = new URLSearchParams();

      formData.append("email", email);
      formData.append("password", password);

      const response = await axios.post(
        "http://localhost:8000/login",
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
        setMessage(
          "Cannot connect to the backend."
        );
      }

    } finally {
      setLoading(false);
    }
  };

if (loggedIn) {
  return <Dashboard />;
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

          {/* Logo */}
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

          {/* Login Form */}
          <form onSubmit={handleLogin}>

            {/* Email */}
            <div className="mb-3">

              <label className="form-label fw-semibold">
                Email
              </label>

              <input
                type="email"
                className="form-control form-control-lg"
                placeholder="Enter your email"
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
                required
              />

            </div>

            {/* Password */}
            <div className="mb-4">

              <label className="form-label fw-semibold">
                Password
              </label>

              <input
                type="password"
                className="form-control form-control-lg"
                placeholder="Enter your password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                required
              />

            </div>

            {/* Login Button */}
            <button
              type="submit"
              className="btn btn-success btn-lg w-100"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>

          </form>

          {/* Message */}
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