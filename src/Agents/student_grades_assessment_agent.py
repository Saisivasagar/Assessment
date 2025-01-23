from typing import Dict
from .conversable_agent import MyConversableAgent


class StudentGradesAssessmentAgent(MyConversableAgent):
    description = """
            StudentGradesAssessmentAgent is responsible for parsing and validating user input about program and course assessments. 
            It identifies key elements such as skills, learning outcomes, and course modules, validates the input, 
            and collaborates with SimulationAgent for processing and generating actionable results.
            """
    
    system_message = """
            You are StudentGradesAssessmentAgent, responsible for parsing and validating user input about program and course assessments. 
            Your goal is to ensure accurate input handling by identifying key elements such as skills, learning outcomes, 
            and course modules, and validating their relevance and accuracy. Once validated, collaborate with SimulationAgent 
            to process the data and generate results aligned with user queries.
            """

    def __init__(self, **kwargs):
        super().__init__(
            name="StudentGradesAssessmentAgent",
            human_input_mode="NEVER",
            system_message=kwargs.pop('system_message', self.system_message),
            description=kwargs.pop('description', self.description),
            **kwargs
        )
    
    def parse_input(self, user_input: str) -> Dict:
        """
        Task 1: Parse user input to extract key elements about program effectiveness.

        Args:
            user_input (str): The natural language input query.

        Returns:
            dict: A dictionary containing the parsed input and identified key elements.
        """
        # Extract key elements from the input
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
        """
        Task 2: Identify key elements such as skills, learning outcomes, and course modules.

        Args:
            parsed_input (dict): Parsed input dictionary.

        Returns:
            dict: Updated dictionary with detailed identification.
        """
        parsed_elements = parsed_input.get("parsed_elements", {})
        # Example processing to refine or enrich the elements (if required)
        return parsed_elements

    def validate_input(self, parsed_input: Dict) -> bool:
        """
        Task 3: Validate the input to ensure it's accurate and meaningful.

        Args:
            parsed_input (dict): Parsed input dictionary.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if not parsed_input["is_valid"]:
            return False
        # Additional validation criteria can be added here
        return True

    def collaborate_with_simulation_agent(self, parsed_input: Dict):
        """
        Task 4: Collaborate with SimulationAgent for data processing.

        Args:
            parsed_input (dict): Validated input data.

        Returns:
            dict: Results from the SimulationAgent.
        """
        if not self.validate_input(parsed_input):
            return {"error": "Invalid input. Please provide meaningful details about the program or course."}
        
        # Simulate collaboration with SimulationAgent
        simulation_agent = self.find_agent_by_type(SimulationAgent)
        if simulation_agent is None:
            return {"error": "SimulationAgent not found. Cannot process input."}
        
        results = simulation_agent.process_data(parsed_input["parsed_elements"])
        return results
