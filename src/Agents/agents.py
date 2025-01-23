import autogen
import os
from .base_agent import MyBaseAgent
from .conversable_agent import MyConversableAgent
from .interaction_agent import InteractionAgent
from .student_grades_assessment_agent import StudentGradesAssessmentAgent
from .course_outcomes_agent import CourseOutcomesAgent

from src.Models.llm_config import gpt4_config
from enum import Enum

os.environ["AUTOGEN_USE_DOCKER"] = "False"

###############################################
# ChatGPT Model
###############################################
llm = gpt4_config

#################################################
# Define Agents
#################################################

interaction_agent = InteractionAgent(llm_config=llm)
student_grades_assessment_agent = StudentGradesAssessmentAgent(llm_config=llm)
course_outcomes_agent = CourseOutcomesAgent(llm_config=llm)

class AgentKeys(Enum):
    INTERACTION = 'interaction'
    STUDENT_GRADES_ASSESSMENT = 'student_grades_assessment'
    COURSE_OUTCOMES = 'course_outcomes'


agents_dict = {
    AgentKeys.INTERACTION.value: interaction_agent,
    AgentKeys.STUDENT_GRADES_ASSESSMENT.value: student_grades_assessment_agent,
    AgentKeys.COURSE_OUTCOMES.value: course_outcomes_agent
 }

agents_dict_by_name = {
    "InteractionAgent": interaction_agent,
    "StudentGradesAssessmentAgent" : student_grades_assessment_agent,
    "CourseOutcomesAgent" : course_outcomes_agent
}

avatars = {
    interaction_agent.name: "✏️",                 # Pencil
    student_grades_assessment_agent.name: "✏️",
    course_outcomes_agent.name: "🧑‍🎓",                  # Person with graduation hat
}
