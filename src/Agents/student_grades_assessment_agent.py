from typing import Dict
import json
import logging
from .base_agent import BaseAgent


class StudentGradesAssessmentAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role='Student Grades Assessment Agent',
            goal="Analyze student performance based on program and course assessments.",
            backstory="An expert in validating and assessing student performance based on key academic criteria.",
            tools=[],
            **kwargs
        )
        
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        try:
            with open("student_data.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.logger.warning("student_data.json not found. Using empty dataset.")
            self.data = {}

    def parse_input(self, user_input: str) -> Dict:
       
        key_elements = {
            "skills": [],
            "learning_outcomes": [],
            "course_modules": []
        }

        # Simple parsing logic (can be enhanced with NLP)
        if "skill" in user_input.lower():
            key_elements["skills"].append("Skill identified in query")
        if "learning outcome" in user_input.lower():
            key_elements["learning_outcomes"].append("Learning outcome identified in query")
        if "module" in user_input.lower():
            key_elements["course_modules"].append("Course module identified in query")

        return {
            "raw_input": user_input,
            "parsed_elements": key_elements,
            "is_valid": any(key_elements.values())
        }

    def identify_key_elements(self, parsed_input: Dict) -> Dict:
       
        parsed_elements = parsed_input.get("parsed_elements", {})
        for key in parsed_elements:
            parsed_elements[key] = [item + " (validated)" for item in parsed_elements[key]]

        return parsed_elements

    def validate_input(self, parsed_input: Dict) -> bool:
       
        if not parsed_input["is_valid"]:
            return False
        return True

    def collaborate_with_simulation_agent(self, parsed_input: Dict):
        
        if not self.validate_input(parsed_input):
            return {"error": "Invalid input. Please provide meaningful details about the program or course."}

        simulation_agent = self.find_agent_by_type("SimulationAgent")
        if simulation_agent is None:
            self.logger.error("SimulationAgent not found.")
            return {"error": "SimulationAgent not found. Cannot process input."}

        results = simulation_agent.process_data(parsed_input["parsed_elements"])
        return results
