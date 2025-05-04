import React, { useContext, useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import AuthContext from '../contexts/authContext';
import axios from "axios";

const AuthenticatedRoute = ({ children, redirect }) => {

    const { user } = useContext(AuthContext);
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                const response = await axios.get('/api/auth/status');
                if (response?.data?.user) {
                    setIsAuthenticated(true);
                } else {
                    setIsAuthenticated(false);
                }
            } catch (error) {
                setIsAuthenticated(false);
            }
        };

        checkAuthStatus();
    }, []);

    if (isAuthenticated === null) {
        return (
            <div className="d-flex flex-column justify-content-center align-items-center w-100 min-vh-100">
                <h2>Loading...</h2>
                <h4>Please be patient while the page loads</h4>
            </div>
        );
    }

    return isAuthenticated ? children : redirect || <Navigate to="/" />;
};

export default AuthenticatedRoute;
