from flask import Blueprint, jsonify
from app.models import JobPosting
from app import db

bp = Blueprint('main', __name__)

@bp.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = JobPosting.query.all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'platform': job.platform,
        'link': job.link,
        'posted_date': job.posted_date.isoformat() if job.posted_date else None
    } for job in jobs])

@bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})