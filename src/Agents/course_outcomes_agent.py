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
                               
                You have access to two files:
                1. Student_synthetic_data_grades.xlsx– Contains student grades for various assignments.
                2. assignment_to_course_outcomes_map.xlsx– Maps assignments to course outcomes.
                
                File Structure:
                - Both files are structured with multiple sheets, where the sheet name begins with the course number.
                - In assignment_to_course_outcomes_map.xlsx, each sheet is appended with the course name.
                
                Student_synthetic_data_grades.xlsx Structure:
                - Each sheet has a header row.
                - Students are listed in rows with a unique student ID.
                - Assignment names and corresponding grades are in columns.
                
                assignment_to_course_outcomes_map.xlsx Structure:
                - Each sheet represents a specific course.
                - The first column lists course outcomes.
                - All subsequent columns contain assignment names linked to each outcome.
                
               Courses Covered:
                -Coding Adventures I
                -Coding Adventures II
                -Computer Architecture
                -Computer Science Fundamentals
                -Networking
                -Algorithms
                -Database Management Systems
                -Object-Oriented Java Programming
                -Software Engineering
                -Operating Systems
                -Capstone Project
                
                Task:
                - For each student and each course, assess the course outcomes based on assignment grades.
                - Use a 5-point Likert scale to evaluate each course outcome.
                - Generate a summary table displaying Likert scale results for each course and student.
                - Ensure the course name (Sheet Name) is clearly listed in the final report.
                - Limit the student IDs to five for the assessment output.
            """),
            agent=self,
            expected_output="A table with the course outcomes assessment for each student for each course."
        )
    

