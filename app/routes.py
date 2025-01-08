# routes.py
from flask import jsonify, request
from app import app, db
from app.models import JobPosting
from app.services import update_job_postings
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        platform = request.args.get('platform')
        location = request.args.get('location')
        days = request.args.get('days', type=int, default=30)
        
        query = JobPosting.query
        
        if platform:
            query = query.filter(JobPosting.platform == platform)
        if location:
            query = query.filter(JobPosting.location.ilike(f'%{location}%'))
            
        # Filtrar por data
        if days:
            date_limit = datetime.utcnow() - timedelta(days=days)
            query = query.filter(JobPosting.posted_date >= date_limit)
            
        jobs = query.order_by(JobPosting.posted_date.desc()).all()
        return jsonify([job.to_dict() for job in jobs])
    except Exception as e:
        logger.error(f"Error getting jobs: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/jobs/refresh', methods=['POST'])
def refresh_jobs():
    try:
        update_job_postings()
        return jsonify({'message': 'Job postings updated successfully'})
    except Exception as e:
        logger.error(f"Error refreshing jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        total_jobs = JobPosting.query.count()
        jobs_by_platform = db.session.query(
            JobPosting.platform, 
            db.func.count(JobPosting.id)
        ).group_by(JobPosting.platform).all()
        
        return jsonify({
            'total_jobs': total_jobs,
            'jobs_by_platform': dict(jobs_by_platform),
            'last_update': JobPosting.query.order_by(
                JobPosting.created_at.desc()
            ).first().created_at.isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500