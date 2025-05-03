import React, { useContext } from 'react';
import AuthContext from '../contexts/authContext';
import Navbar from '../components/Navbar';

const Dashboard = () => {
    const { user } = useContext(AuthContext);

    return (
        <>
            <Navbar />
            <div style={{ padding: '20px' }}>
                <h1>Dashboard</h1>
                <div style={{ marginTop: '20px' }}>
                    <p><strong>Name:</strong> {user?.name}</p>
                    <p><strong>Email:</strong> {user?.email}</p>
                </div>
            </div>
        </>
    );
};

export default Dashboard;