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
                You have two files in your knowledge context: synthetic_student_grades.xlsx and assignment_to_course_outcomes_map.xlsx        

                In both files, the courses are organized in sheets with the course number being the first part of the sheet name.
                In the assignment_to_course_outcomes.xlsx file, each sheet is appended with the course name.
                               
                The synthetic_student_grades.xlsx excel file is organized as follows:
                    1. Each sheet has a header row
                    2. Students are listed in rows with a unique ID per student
                    3. Assignment names and grades are in columns 
                                 
                The assignment_to_course_outcomes_map.xlsx file is organized as follows:
                    2. The first column of each sheet contains the course outcomes
                    3. All columns from the second column contain the names of the assignments used for assessment
                               
                For each student, and for each course, provide a course outcomes assessment using a 5 point Likert scale.
                               
                Create a summary table displaying the Likert scale results for each course and student. Make sure to list the
                        course name (i.e. the Sheet Name)
            """),
            agent=self,
            expected_output="A table with the course outcomes assessment for each student for each course."
        )
    

