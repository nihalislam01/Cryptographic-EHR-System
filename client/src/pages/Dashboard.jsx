import React, { use, useContext, useEffect, useState } from 'react';
import AuthContext from '../contexts/authContext';
import Navbar from '../components/Navbar';
import Table from '../components/Table';
import UploadRecordModal from '../components/UploadRecordModal';
import axios from 'axios';

const Dashboard = () => {

    const [showModal, setShowModal] = useState(false);
    const [patients, setPatients] = useState([]);
    const { user } = useContext(AuthContext);
    const [rows, setRows] = useState([]);

    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const response = await axios.get('/api/user/get');
                setPatients(response?.data?.patients);
            } catch (error) {
                console.error('Error fetching patients:', error);
            }
        };
        const fetchRecords = async () => {
            try {
                const response = await axios.get('/api/record/get');
                setRows(response?.data?.records);
            }
            catch (error) {
                console.error('Error fetching records:', error);
            }
        }
        fetchRecords();
        fetchPatients();
    }, []);

    const handleSubmit = async (data) => {
        try {
            const formData = new FormData();
            
            const file = data.file;
            const originalName = file.name;
    
            formData.append('file', file);
            formData.append('filename', originalName);
    
            const response = await axios.post(`/api/record/upload/${data.id}`,formData);
            console.log('Upload successful:', response.data);
        } catch (error) {
            console.error('Error uploading file:', error.response?.data || error.message);
        }
    };    

    const downloadPdf = async (recordId) => {
        try {
            const response = await axios.get(`/api/record/download/${recordId}`, {
                responseType: 'blob',
            });
            const disposition = response.headers['content-disposition'];
            let filename = `record-${recordId}.pdf`;
            if (disposition && disposition.includes('filename=')) {
                filename = disposition
                    .split('filename=')[1]
                    .replace(/['"]/g, '')
                    .trim();
            }
    
            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
            const link = document.createElement('a');
            link.href = url;
    
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Error downloading PDF:', error);
        }
    };
    

    const renderActions = (row) => (
        <button onClick={() => downloadPdf(row.id)}><i className="fa-solid fa-download"></i></button>
    );

    return (
        <>
            <Navbar />
            {showModal && <UploadRecordModal patients={patients} onClose={() => setShowModal(false)} onSubmit={handleSubmit}/>}
            <div style={{ padding: '20px 200px' }}>
                <div className='d-flex justify-content-between align-items-center'>
                    <div className='d-flex align-items-center gap-4'>
                        <h2>{user?.name}</h2>
                        <h6><span style={{backgroundColor: "rgb(1, 42, 74, 0.6)", border: "1px solid rgb(1, 42, 74)", padding: "5px 10px", color: "white", borderRadius: "25px"}}>{user?.role === 'patient' ? 'Patient' : 'Doctor'} Panel</span></h6>
                    </div>
                    {user?.role === 'doctor' && <button onClick={() => setShowModal(true)}>Insert PDF</button>}
                </div>
                <hr />
                <div className='border' style={{boxShadow: "5px 5px 12px 1px rgba(171, 171, 171, 0.41)", height: "72vh", padding: "20px", overflow: "auto"}}>
                    <Table keys={["insert_date", "pdf_name", "verified"]} rows={rows} renderActions={renderActions} />
                </div>
            </div>
        </>
    );
};

export default Dashboard;