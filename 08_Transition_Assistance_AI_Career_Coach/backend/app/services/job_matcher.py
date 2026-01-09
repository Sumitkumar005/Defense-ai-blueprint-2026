"""
Job Matching Service
Matches veterans to civilian jobs based on skills and experience
"""

import httpx
from typing import List, Dict
from app.core.config import settings


class JobMatcher:
    """Match veterans to jobs"""
    
    async def find_jobs(
        self,
        skills: List[str],
        location: str = None,
        job_title: str = None
    ) -> List[Dict]:
        """
        Find matching jobs from multiple sources
        
        PLACEHOLDER: In production, would query Indeed, LinkedIn, USAJobs APIs
        """
        
        jobs = []
        
        # Try Indeed API (placeholder)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.indeed.com/v1/jobs",
                    params={
                        "q": job_title or " ".join(skills),
                        "location": location or "",
                        "api_key": settings.INDEED_API_KEY
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    jobs.extend(data.get('results', [])[:10])
        except:
            pass
        
        # Fallback: Mock jobs
        if not jobs:
            jobs = [
                {
                    "title": "Security Manager",
                    "company": "Defense Contractor Inc",
                    "location": location or "Remote",
                    "match_score": 85,
                    "url": "https://example.com/job/1"
                },
                {
                    "title": "Project Manager",
                    "company": "Tech Solutions LLC",
                    "location": location or "Remote",
                    "match_score": 78,
                    "url": "https://example.com/job/2"
                }
            ]
        
        return jobs
    
    def calculate_match_score(
        self,
        job_requirements: List[str],
        user_skills: List[str]
    ) -> float:
        """Calculate job match score"""
        # Simple matching algorithm
        matching_skills = set(job_requirements) & set(user_skills)
        score = (len(matching_skills) / max(len(job_requirements), 1)) * 100
        return min(100, score)
