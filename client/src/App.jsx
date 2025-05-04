import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { AuthProvider } from "./contexts/authContext";
import Dashboard from "./pages/Dashboard";
import AuthenticatedRoute from "./utils/AuthenticatedRoute.jsx";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<AuthenticatedRoute><Dashboard /></AuthenticatedRoute>} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
