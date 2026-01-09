"""
AI Resume Builder Service
Generates civilian-friendly resumes from military experience
"""

import httpx
from app.core.config import settings


class ResumeBuilder:
    """Build resumes using AI"""
    
    async def generate_resume(
        self,
        user_id: int,
        military_experience: dict,
        target_job_title: str
    ) -> str:
        """
        Generate resume using AI
        
        PLACEHOLDER: In production, would use fine-tuned GPT model
        """
        
        # Try OpenAI API (placeholder)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a resume writing expert specializing in translating military experience to civilian terms."
                            },
                            {
                                "role": "user",
                                "content": f"Create a professional resume for a veteran with experience: {military_experience}, targeting job: {target_job_title}"
                            }
                        ]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
        except:
            pass
        
        # Fallback: Template-based resume
        return self._generate_template_resume(military_experience, target_job_title)
    
    def _generate_template_resume(self, military_experience: dict, target_job_title: str) -> str:
        """Generate resume from template"""
        return f"""
PROFESSIONAL SUMMARY
Experienced professional with {military_experience.get('years_of_service', 'extensive')} years of service, 
seeking to leverage leadership and technical skills in {target_job_title} role.

EXPERIENCE
{military_experience.get('mos', 'Military Service')} - {military_experience.get('rank', 'Rank')}
• Led teams of up to {military_experience.get('team_size', 'multiple')} personnel
• Managed complex operations and logistics
• Maintained high standards of performance and accountability

SKILLS
• Leadership & Team Management
• Problem Solving
• Project Management
• Technical Proficiency
• Communication
        """.strip()
