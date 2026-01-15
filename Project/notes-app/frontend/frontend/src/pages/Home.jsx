import { useEffect, useState } from "react";
import api from "../api/axios";
import { logout } from "../utils/auth";
import Notes from "./Notes";

function Home({ onLogout }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    api.get("/me")
      .then((res) => setUser(res.data))
      .catch(() => {
        logout();
        onLogout();
      });
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h2>Welcome, {user.name}</h2>
      <p>Username: {user.username}</p>
      <p>Admin: {user.is_admin ? "Yes" : "No"}</p>

      <button onClick={() => {
        logout();
        onLogout();
      }}>
        Logout
      </button>
      <hr />
        <Notes />
        
    </div>
  );
}

export default Home;
