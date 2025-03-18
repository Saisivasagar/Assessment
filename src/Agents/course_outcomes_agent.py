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

                                       
               You have access to the following files for Course 101:

                1.    grades_101.xlsx – Contains student grades for various assignments.
                2.    COMP-101.xlsx – Describes mappings of each assignment specification.
                                
                File Structure:

                -    Assessments are limited to Course 101.
                -    All necessary data, including outcome mappings, student grades, and assignment specifications, are provided.
                -    Student grade files contain student IDs, assignment names, and grades.
                    
                Task:

                -    Assess student capabilities for each course outcome for Course 101.
                -    Utilize assignment grades (Final Exam and Final Project) to determine student performance.
                -    Use assignment specifications to understand the context and learning objectives of each assignment.
                -    Map assignments to outcomes using the provided course mapping files.
                -    Ensure that student IDs are mapped correctly based on their enrollment in Course 101.
                -    Calculate the average grade for each student per course outcome based on their performance in the mapped assignments.
                -    Generate a summary table displaying the correctly mapped student IDs and their average grades for each course outcome.
                    
                Output Requirements:

                -    Clearly label the final report for Course 101.
                -    Include five student IDs in the assessment output.
                -    Limit the analysis to four course outcomes for Course 101.
                -    Ensure the output table is structured with student IDs as rows and course outcomes as columns, with each cell containing the correct average grade for that outcome.
                  
                Expected Output:

                -    A properly structured table showing each student's average grade for each course outcome based on their performance in the Final Exam and Final Project.
                -    Ensure the correct mapping of student IDs and their corresponding average grades per outcome.
                -    Provide a brief summary explaining key insights from the assessment, including identifying top-performing students and areas where students may need improvement.

                                            
            """),

            


            agent=self,
            expected_output="Tables with the course outcomes assessment for course 101."
        )
    

