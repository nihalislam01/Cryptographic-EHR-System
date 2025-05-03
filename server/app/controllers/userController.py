from flask import jsonify
from app.models.user import User
from app.utils.auth import jwt_required

@jwt_required
def get_all_patients(user_id):
    try:
        patients = User.query.filter_by(role='patient').all()
        
        patient_list = [
            {
                "id": patient.id,
                "email": patient.email,
            }
            for patient in patients
        ]
        
        return jsonify({"success": True, "patients": patient_list}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500