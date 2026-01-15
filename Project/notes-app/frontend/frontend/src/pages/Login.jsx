import { useState } from "react";
import api from "../api/axios";
import { setToken } from "../utils/auth";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    console.log("LOGIN BUTTON CLICKED");

    try {
      const res = await api.post("/login", {
        username,
        password,
      });

      console.log("RESPONSE:", res);

      setToken(res.data.access_token);
      onLogin();
    } catch (err) {
      console.log("ERROR:", err);
      setError("Invalid username or password");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleLogin}>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br /><br />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
