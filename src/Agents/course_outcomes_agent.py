from typing import Dict
from .conversable_agent import MyConversableAgent


class CourseOutcomesAgent(MyConversableAgent):
    description = """
            CourseOutcomesAgent is responsible for mapping course outcomes to student grades.
            """
    
    system_message = """
            You are CourseOutcomesAgent, responsible for mapping course outcomes to student grades.
            """

    def __init__(self, **kwargs):
        super().__init__(
            name="CourseOutcomesAgent",
            human_input_mode="NEVER",
            system_message=kwargs.pop('system_message', self.system_message),
            description=kwargs.pop('description', self.description),
            **kwargs
        )
    

