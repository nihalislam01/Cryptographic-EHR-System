import React, { useEffect, useRef, useState } from 'react';
import '../styles/Popup.css';

const UploadRecordModal = ({ onClose, onSubmit, patients }) => {
    const modalRef = useRef();
    const [selectedId, setSelectedId] = useState(0);
    const [pdfFile, setPdfFile] = useState(null);

    const handleOutsideClick = (e) => {
        if (modalRef.current && !modalRef.current.contains(e.target)) {
            onClose();
        }
    };

    useEffect(() => {
        document.addEventListener('mousedown', handleOutsideClick);
        return () => document.removeEventListener('mousedown', handleOutsideClick);
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (selectedId && pdfFile) {
            onSubmit({ id: selectedId, file: pdfFile });
            onClose();
        }
    };

    return (
        <div className="popup-overlay">
            <div ref={modalRef} className="popup-content border">
                <div className='w-100'>
                    <h2>Upload Patient Record</h2>
                    <hr />
                    <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)} className="w-100 mb-3" required>
                        <option value={0}>Select patient email</option>
                        {patients.map((patient, idx) => (
                            <option key={idx} value={patient.id}>{patient.email}</option>
                        ))}
                    </select>
                    <input type="file" accept="application/pdf" onChange={(e) => setPdfFile(e.target.files[0])} className="w-100"required/>
                    <hr />
                    <div className="d-flex gap-2">
                        <button onClick={onClose} className='w-100'>Cancel</button>
                        <button onClick={handleSubmit} className="w-100">Upload</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadRecordModal;