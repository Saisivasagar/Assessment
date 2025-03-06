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
                               
                You have access to three files:
                1. student_synthetic_grades_552.xlsx – Contains student grades for various assignments.
                2. COMP-552_MAPPING.xlsx – Describes mappings of each assignment specification.
                3. Assignment_Specification_552.xlsx – Describes assignment specifications for each assignment.
                
                File Structure:
                - The assessment is limited to Course 552.
                - All necessary data, including outcome mappings, student synthetic grades, and assignment specifications, are provided.
                - student_synthetic_grades_552.xlsx contains student IDs, assignment names, and grades.

                 Task:
                - Assess student capabilities for each course outcome based on their grades.
                - Utilize assignment grades for students in Course 552 to determine their performance.
                - Use assignment specifications to understand the context and learning objectives of each assignment.
                - Map assignments to outcomes using the provided course mapping file.
                - Generate a summary table displaying the average grade for each student per course outcome.

                Output Requirements:
                - Clearly label Course 552 in the final report.
                - Include five student IDs in the assessment output.
                - Limit the analysis to twelve course outcomes.

                Expected Output:
                - Each student's capability (average grade) for each course outcome based on their performance in the mapped assignments.         
            """),


            agent=self,
            expected_output="A table with the course outcomes assessment for each student for each course."
        )
    

