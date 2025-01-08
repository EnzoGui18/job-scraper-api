# services.py
from app import db
from app.models import JobPosting
from app.scraper import LinkedInScraper, GlassdoorScraper, GupyScraper
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def update_job_postings():
    scrapers = [
        LinkedInScraper(),
        GlassdoorScraper(),
        GupyScraper()
    ]
    
    new_jobs = []
    for scraper in scrapers:
        try:
            logger.info(f"Starting scraping with {scraper.__class__.__name__}")
            jobs = scraper.scrape()
            new_jobs.extend(jobs)
            logger.info(f"Found {len(jobs)} jobs from {scraper.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error scraping with {scraper.__class__.__name__}: {str(e)}")
    
    # Remove vagas antigas (mais de 30 dias)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    JobPosting.query.filter(JobPosting.created_at < thirty_days_ago).delete()
    
    # Adiciona novas vagas
    jobs_added = 0
    for job_data in new_jobs:
        try:
            existing_job = JobPosting.query.filter_by(link=job_data['link']).first()
            if not existing_job:
                job = JobPosting(**job_data)
                db.session.add(job)
                jobs_added += 1
        except Exception as e:
            logger.error(f"Error adding job to database: {str(e)}")
            continue
    
    try:
        db.session.commit()
        logger.info(f"Successfully added {jobs_added} new jobs to database")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error committing to database: {str(e)}")
        raise