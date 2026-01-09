"""
MOS (Military Occupational Specialty) Translation Service
Converts military experience to civilian job titles
"""

# PLACEHOLDER: In production, would use NLP model trained on MOS-to-job mappings
MOS_TO_CIVILIAN_MAPPING = {
    "11B": ["Security Manager", "Law Enforcement", "Security Consultant"],
    "25B": ["IT Specialist", "Network Administrator", "Systems Administrator"],
    "68W": ["EMT", "Paramedic", "Medical Assistant"],
    "92Y": ["Supply Chain Manager", "Logistics Coordinator", "Inventory Manager"],
    "35N": ["Intelligence Analyst", "Data Analyst", "Research Analyst"],
    "12B": ["Construction Manager", "Project Manager", "Engineer"],
    "88M": ["Truck Driver", "Logistics Coordinator", "Transportation Manager"],
    "19K": ["Heavy Equipment Operator", "Equipment Technician", "Maintenance Supervisor"]
}


class MOSTranslator:
    """Translate MOS to civilian job titles"""
    
    def translate_mos(self, mos_code: str) -> list:
        """Get civilian job titles for MOS"""
        return MOS_TO_CIVILIAN_MAPPING.get(mos_code, ["General Manager", "Operations Manager"])
    
    def extract_skills(self, military_experience: dict) -> list:
        """Extract transferable skills from military experience"""
        skills = []
        
        # PLACEHOLDER: Would use NLP to extract skills
        if "leadership" in str(military_experience).lower():
            skills.append("Leadership")
        if "management" in str(military_experience).lower():
            skills.append("Project Management")
        if "technical" in str(military_experience).lower():
            skills.append("Technical Skills")
        
        # Default skills for all veterans
        skills.extend([
            "Teamwork",
            "Discipline",
            "Problem Solving",
            "Time Management",
            "Adaptability"
        ])
        
        return list(set(skills))
