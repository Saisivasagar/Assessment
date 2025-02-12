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
                Given assignment grades in the knowledge excel file and
                   the mapping of assignments to course outcomes in knowledge folder

                For each student, provide a course assessment using a 5 point Likert scale using
                   categories: far exceeds, exceeds, meets, nearly meets, does not meet. 
                               
                Each student has a unique student id. If you find the same student id in different
                    courses, it is the same student.

                Create a summary table.
            """),
            agent=self,
            expected_output="A table with the course assessment for each student"
        )
    

