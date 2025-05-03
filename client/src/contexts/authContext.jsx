import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const getToken = () => localStorage.getItem('token');

    const setAuthHeader = () => {
        const token = getToken();
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            delete axios.defaults.headers.common['Authorization'];
        }
    };

    useEffect(() => {
        setAuthHeader();

        const checkAuthStatus = async () => {
            try {
                const response = await axios.get('/api/auth/status');
                setUser(response?.data?.user || null);
            } catch (error) {
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkAuthStatus();
    }, []);

    const login = async (credentials) => {
        try {
            const response = await axios.post('/api/auth/login', credentials);
            const { token, user } = response.data;

            localStorage.setItem('token', token);
            setAuthHeader();
            setUser(user);
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;