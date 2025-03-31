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

               You have access to the following files for Course 101 and Course 103:

                Course 101 Files:
                1. grades_101.xlsx – Contains student grades for various assignments.
                2. COMP-101.xlsx – Describes mappings of each assignment specification to the course outcomes.
                                
                Course 103 Files:
                1. grades_103.xlsx – Contains student grades for various assignments.
                2. COMP-103.xlsx – Describes mappings of each assignment specification to the course outcomes.
                                
                
                File Structure:
                - Assessments are limited to COMP-101, COMP-103.
                - All necessary data, including outcome mappings, student grades, and assignment specifications, are provided.
                - Student grade files contain student IDs, assignment names, and grades.
                - Ensure that student IDs are correctly mapped to their respective courses:
                    COMP-101: 11, 12, 13, 14, 15
                    COMP-103: Student_1, Student_2, Student_3, Student_4, Student_5
                    
                Task:
                - Assess student capabilities for each course outcome for COMP-101, COMP-103.
                - Utilize assignment grades (Final Exam and Final Project) to determine student performance.
                - Use assignment specifications to understand the context and learning objectives of each assignment.
                - Map assignments to outcomes using the provided course mapping files.
                - Ensure that student IDs are correctly linked to their respective courses.
                - Calculate the average grade for each student per course outcome based on their performance in the mapped assignments.
                - Generate a summary table displaying the correctly mapped student IDs and their average grades for each course outcome.
                                
                Output Requirements:
                - Clearly label the final report for COMP-101, COMP-103.
                - Include five student IDs in the assessment output for each course.
                - Limit the analysis to:
                    Four course outcomes for COMP-101
                    Seven course outcomes for COMP-103
                    
                - Ensure the output structure contains student IDs as rows and course outcomes as columns, with each cell containing the correct average grade for that outcome.
                - The outcome column headings should be structured as follows:
                    COMP-101: Outcome:1, Outcome:2, Outcome:3, Outcome:4
                    COMP-103: Outcome:1, Outcome:2, … Outcome:7
                    
                                 
                Expected Output:

                -    Provide five well-structured reports, one for COMP-101, COMP-103, showing each student's average grade for each course outcome based on their performance.
                -    Ensure the correct mapping of student IDs and their corresponding average grades per outcome.
                -    Provide a brief summary explaining key insights from the assessment, including identifying top-performing students and areas where students may need improvement.

                                            
            """),

            


            agent=self,
            expected_output="Tables with the course outcomes assessment for course 101, course 103.
        )
    

