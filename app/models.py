# models.py
from datetime import datetime
from app import db

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    salary_range = db.Column(db.String(200))
    link = db.Column(db.String(500), unique=True)
    platform = db.Column(db.String(50))  # LinkedIn, Glassdoor ou Gupy
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'salary_range': self.salary_range,
            'link': self.link,
            'platform': self.platform,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'created_at': self.created_at.isoformat()
        }
