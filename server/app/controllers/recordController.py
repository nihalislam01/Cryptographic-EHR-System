from datetime import datetime
import io
from flask import jsonify, request, send_file
from app.utils.aes import decrypt, decrypt_pdf, encrypt, encrypt_pdf
from app.utils.rsa import sign_bytes, verify_signature
from app.models.record import Record, db
from app.utils.auth import jwt_required
from app.models.user import User

@jwt_required
def get_all_records(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        if user.role == 'patient':
            records = Record.query.filter_by(patient_id=user_id).all()
        else:
            records = Record.query.all()

        record_list = [
            {
                "id": record.id,
                "pdf_name": decrypt(record.filename),
                "insert_date": record.insert_date.strftime('%A, %Y-%m-%d'),
                "verified": verify_signature(record.doctor_id, record.encrypted_pdf, record.digital_signature),
            }
            for record in records
        ]
        return jsonify({"success": True, "records": record_list}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@jwt_required
def upload_record(user_id, patient_id):
    file = request.files['file']
    raw_pdf_data = file.read()
    filename = request.form.get('filename')

    encrypted_filename = encrypt(filename)
    encrypted_pdf = encrypt_pdf(raw_pdf_data)

    signature = sign_bytes(user_id, encrypted_pdf)

    record = Record(
        filename=encrypted_filename,
        encrypted_pdf=encrypted_pdf,
        insert_date=datetime.now(),
        patient_id=patient_id,
        doctor_id=user_id,
        digital_signature=signature
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'message': 'Encrypted record uploaded and signed successfully'}), 201

@jwt_required
def download_record(user_id, record_id):
    record = Record.query.get(record_id)
    if not record:
        return jsonify({'message': 'Record not found'}), 404

    decrypted_pdf = decrypt_pdf(record.encrypted_pdf)
    pdf_stream = io.BytesIO(decrypted_pdf)
    pdf_stream.seek(0)

    filename = decrypt(record.filename)

    return send_file(
        pdf_stream,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
