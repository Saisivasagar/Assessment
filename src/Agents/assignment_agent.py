import re
from pydantic import BaseModel, Field
from textwrap import dedent
import crewai as crewai
from datetime import datetime
import os
from src.Agents.base_agent import BaseAgent


class AssignmentAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role='Assignment Agent',
            goal="Extract assignment grades from the crew context and provide other agent's with student scores",
            backstory='An expert in parsing and determining student grades on specific assignment',
            tools=[],
            **kwargs)
        
        self.previous_report = None

    def get_student_assignment_grades(self):
            

        return crewai.Task(
            description=dedent(f"""
                You have an excel file with students and assignment grades in your knowledge context. 

                The excel file is organized as follows:
                    1. Each sheet is for a unique course. 
                    2. The sheet name identifies the course
                    3. Each sheet has a header row
                    4. Students are listed in rows with a unique ID per student
                    5. Assignment names and grades are in columns 
                                               
                When requested, provide student grades to any Crew member that requests them.
                
            """),
            agent=self,
            expected_output="A table with the course assessment for 5 unique students"
        )
    

