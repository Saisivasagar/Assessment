from typing import Dict, List
from src.Agents.base_agent import BaseAgent
import json

class GapAnalysisAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role='Gap Analysis Agent',
            goal='Identify knowledge gaps by comparing course content with expected outcomes and student feedback',
            backstory='An expert in assessing knowledge gaps in educational programs',
            tools=[],
            **kwargs
        )
        
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
        report = {"program_level": {}, "course_level": {}}
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
            validated_gaps[gap] = {"issue": issue, "feedback": feedback_support}
        return validated_gaps

    def pass_insights_to_recommendation_agent(self, validated_gaps: Dict):
        recommendation_agent = self.find_agent_by_type("RecommendationAgent")
        if not recommendation_agent:
            return {"error": "RecommendationAgent not found. Cannot pass insights."}
        recommendation_agent.process_insights(validated_gaps)
        return {"status": "Insights successfully passed to RecommendationAgent."}
