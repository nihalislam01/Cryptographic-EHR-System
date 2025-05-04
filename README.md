# Cryptographic Electronic Health Record (EHR) System

## Overview
The Cryptographic EHR System is a secure and efficient platform designed to manage electronic health records (EHRs) with a focus on data privacy and integrity. By employing cryptographic techniques, this system ensures that sensitive patient information is protected from unauthorized access while maintaining accessibility for authorized users.

<img width="1440" alt="CEHR-Doctor-Panel" src="https://github.com/user-attachments/assets/a377ae64-136d-4a0a-9d49-ac5599979503" />

## Features
- **User Info Encryption**: User Info such as email and role are encrypted using AES-EBC and other information are encrypted with AES-CBC. Password and salt is hashed using SHA-256.
- **Records Encryption**: All patient records are encrypted to ensure confidentiality. PDFs are encrypted with AES-CBC and digitally signed by doctors using RSA algorithm.
- **Record Verification**: Patients will be able to verify record authenticity using doctor's public key.
- **Access Control**: Role-based access to ensure only authorized personnel can view or modify records.
- **Scalability**: Designed to handle large volumes of data efficiently.

## Technologies Used
- **Frontend**: React.js
- **Backend**: Flask
- **Database**: MySQL
- **Cryptography**: AES-CBC, AES-EBC, RSA
