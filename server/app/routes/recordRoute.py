from flask import Blueprint
from app.controllers.recordController import upload_record, get_all_records, download_record

record_bp = Blueprint('record', __name__, url_prefix='/api/record')

record_bp.route('/upload/<patient_id>', methods=['POST'])(upload_record)
record_bp.route('/get', methods=['GET'])(get_all_records)
record_bp.route('/download/<int:record_id>', methods=['GET'])(download_record)
