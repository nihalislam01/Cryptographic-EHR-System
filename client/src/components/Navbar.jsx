import { Link } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../contexts/authContext";
import '../styles/Navbar.css';

export default function Navbar() {
    const { user, logout } = useContext(AuthContext);

    return (
        <div className="navigation-bar" style={{ minHeight: "10vh" }}>
            <h3>CEHR</h3>
            <div className="d-flex gap-3">
                {user ? (
                    <>
                        <Link to="/dashboard">Dashboard</Link>
                        <Link to="/#" onClick={logout}>Logout</Link>
                    </>
                ) : (
                    <>
                        <Link to="/">Login</Link>
                        <Link to="/register">Signup</Link>
                    </>
                )}
            </div>
        </div>
    );
}