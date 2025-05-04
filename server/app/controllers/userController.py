from flask import jsonify
from app.models.user import User
from app.utils.auth import authorized
from app.utils.aes import aes_ecb_decrypt, aes_ecb_encrypt

@authorized(['doctor'])
def get_all_patients(user_id):
    try:
        patients = User.query.filter_by(role=aes_ecb_encrypt('patient')).all()
        
        patient_list = [
            {
                "id": patient.id,
                "email": aes_ecb_decrypt(patient.email),
            }
            for patient in patients
        ]
        return jsonify({"success": True, "patients": patient_list}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500