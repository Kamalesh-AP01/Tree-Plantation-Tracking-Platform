import { useState } from "react";
import axios from "axios";

function Register({ onBackToLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    setMessage("");

    const formData = new URLSearchParams();

    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/register",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      setMessage(response.data.message);

      setName("");
      setEmail("");
      setPassword("");

    } catch (error) {
      console.error(error);

      if (error.response) {
        setMessage(
          error.response.data.message || "Registration failed."
        );
      } else {
        setMessage("Cannot connect to the backend.");
      }
    }
  };

  return (
    <div style={{ padding: "40px", maxWidth: "500px", margin: "auto" }}>
      <h2>Create User Account</h2>

      <form onSubmit={handleRegister}>

        <div className="mb-3">
          <label>Name</label>

          <input
            type="text"
            className="form-control"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label>Email</label>

          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label>Password</label>

          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          className="btn btn-success"
        >
          Register
        </button>

      </form>

      {message && (
        <div className="alert alert-info mt-4">
          {message}
        </div>
      )}

      <button
        type="button"
        className="btn btn-secondary mt-3"
        onClick={onBackToLogin}
      >
        ← Back to Login
      </button>
    </div>
  );
}

export default Register;