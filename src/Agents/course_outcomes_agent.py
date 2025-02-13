import re
from pydantic import BaseModel, Field
from textwrap import dedent
import crewai as crewai
from datetime import datetime
import os
from src.Agents.base_agent import BaseAgent


class CourseOutcomesAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role='Course Outcomes Agent',
            goal="Map student assignment grades to course outcomes",
            backstory='An expert in assessing course outcomes',
            tools=[],
            **kwargs)
        
        self.previous_report = None

    def assess_course_outcomes_from_assignment_grades(self):
            

        return crewai.Task(
            description=dedent(f"""
                You have assignment to course outcomes mappings excel file in your context knowledge.
                               
                The file is organized as follows:
                    1. There are sheets where the name of the sheet is the name of the course
                    2. The first column contains the course outcomes
                    3. All columns from the second column contain the names of the assignments used for assessment
                               
                As Assignment Agent can provide you with the student scores for each course and assignment

                For each student, provide a course outcomes assessment using a 5 point Likert scale using
                   categories: does not meet, nearly meets, meets, exceeds, far exceeds. 

                For each course, assess the course outcomes for each student. 
                               
                Create a summary table displaying the Likert scale results for each course. Make sure to list the
                        course name (i.e. the Sheet Name)
            """),
            agent=self,
            expected_output="A table with the course outcomes assessment for each student"
        )
    

