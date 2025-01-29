from typing import Dict, List
from .conversable_agent import MyConversableAgent
import json

class GapAnalysisAgent(MyConversableAgent):
    description = """
            GapAnalysisAgent is responsible for identifying knowledge gaps by comparing course content with expected outcomes and student feedback.
            """

    def __init__(self, **kwargs):
        super().__init__(name="GapAnalysisAgent", human_input_mode="NEVER", **kwargs)
        # Load course content and feedback data from JSON or database
        with open("course_content.json", "r") as file:
            self.course_content = json.load(file)
        with open("student_feedback.json", "r") as file:
            self.student_feedback = json.load(file)

    def identify_knowledge_gaps(self, expected_outcomes: List[str]) -> Dict:
        knowledge_gaps = {}
        for outcome in expected_outcomes:
            if outcome not in self.course_content.get("covered_outcomes", []):
                knowledge_gaps[outcome] = "Not adequately covered in the course content."
        return knowledge_gaps

    def generate_improvement_reports(self, knowledge_gaps: Dict) -> Dict:
        report = {
            "program_level": {},
            "course_level": {}
        }
        for gap, issue in knowledge_gaps.items():
            if "program" in gap.lower():
                report["program_level"][gap] = issue
            else:
                report["course_level"][gap] = issue
        return report

    def validate_gaps_with_feedback(self, knowledge_gaps: Dict) -> Dict:
        validated_gaps = {}
        for gap, issue in knowledge_gaps.items():
            feedback_support = self.student_feedback.get(gap, "No feedback available")
            if feedback_support:
                validated_gaps[gap] = {"issue": issue, "feedback": feedback_support}
        return validated_gaps

    def handle_message(self, message: Dict):
        expected_outcomes = message.get("expected_outcomes", [])
        knowledge_gaps = self.identify_knowledge_gaps(expected_outcomes)
        improvement_reports = self.generate_improvement_reports(knowledge_gaps)
        validated_gaps = self.validate_gaps_with_feedback(knowledge_gaps)
        return {
            "knowledge_gaps": knowledge_gaps,
            "improvement_reports": improvement_reports,
            "validated_gaps": validated_gaps
        }
