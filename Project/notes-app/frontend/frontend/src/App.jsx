import { useState } from "react";
import Login from "./pages/Login";
import Home from "./pages/Home";
import { getToken } from "./utils/auth";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!getToken());

  return (
    <div>
      <h1>Notes App</h1>

      {!isLoggedIn ? (
        <Login onLogin={() => setIsLoggedIn(true)} />
      ) : (
        <Home onLogout={() => setIsLoggedIn(false)} />
      )}
    </div>
  );
}

export default App;
