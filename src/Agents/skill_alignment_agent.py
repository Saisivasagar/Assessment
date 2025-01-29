from typing import Dict, List
from .conversable_agent import MyConversableAgent

class SkillAlignmentAgent(MyConversableAgent):
    description = """
        SkillAlignmentAgent is responsible for simulating how course content aligns with industry standards and benchmarks.
        The agent evaluates course content against industry skill requirements and incorporates benchmarks from job market
        trends and other data sources. It validates simulation results across various programs and student demographics,
        including interdisciplinary courses.
        """

    system_message = """
        You are SkillAlignmentAgent, responsible for evaluating and simulating the alignment of course content with industry
        standards and skill requirements.Simulating how course content aligns with industry standards and skill requirements.
        Incorporating benchmarks from industry data or standards (e.g., job market trends).Validating simulation results for 
        different programs and student demographics. Handling interdisciplinary courses and ensuring accurate mappings.
        """

    def __init__(self, **kwargs):
        super().__init__(
            name="SkillAlignmentAgent",
            human_input_mode="NEVER",
            system_message=kwargs.pop('system_message', self.system_message),
            description=kwargs.pop('description', self.description),
            **kwargs
        )

    def simulate_alignment(self, course_content: List[str]) -> Dict:
        simulated_results = {
            "course_content": course_content,
            "aligned_skills": [
                "Problem Solving", "Critical Thinking", "Team Collaboration"
            ],
            "alignment_score": 85  # Example alignment score
        }
        return simulated_results

    def incorporate_benchmarks(self, alignment_data: Dict) -> Dict:
        alignment_data["benchmarks"] = {
            "job_market_trends": ["AI/ML", "Cloud Computing", "Data Analysis"],
            "average_alignment_score": 78  # Example benchmark score
        }
        alignment_data["comparison_to_benchmarks"] = {
            "above_average": True
        }
        return alignment_data

    def validate_results(self, alignment_data: Dict, program_data: Dict, demographics_data: Dict) -> bool:
        # Example: Cross-reference alignment with program-specific and demographic data
        program_alignment = program_data.get(alignment_data["course_content"], 0)
        demographic_factor = demographics_data.get("diversity", 1.0)
        
        adjusted_score = alignment_data["alignment_score"] * demographic_factor + program_alignment
        return adjusted_score >= 75

    def handle_interdisciplinary_courses(self, alignment_data: Dict, courses: List[str], interdisciplinary_data: Dict) -> Dict:
        # Example: Adjust alignment score based on interdisciplinary course data
        for course in courses:
            if course in interdisciplinary_data:
                alignment_data["adjusted_alignment_score"] += interdisciplinary_data[course]
        return alignment_data

    def handle_message(self, course_content: List[str], courses: List[str], program_data: Dict, demographics_data: Dict, interdisciplinary_data: Dict) -> Dict:
        alignment_data = self.simulate_alignment(course_content)
        alignment_data = self.incorporate_benchmarks(alignment_data)
        
        # Validate results based on program and demographics data
        is_valid = self.validate_results(alignment_data, program_data, demographics_data)
        if not is_valid:
            return {"error": "Alignment validation failed. Please review the course content."}

        alignment_data = self.handle_interdisciplinary_courses(alignment_data, courses, interdisciplinary_data)
        return alignment_data
