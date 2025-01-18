import autogen
import os
from .base_agent import MyBaseAgent
from .conversable_agent import MyConversableAgent
from .interaction_agent import InteractionAgent
from .tutor_agent import TutorAgent

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
tutor = TutorAgent(llm_config=llm)


class AgentKeys(Enum):
    TUTOR = 'tutor'
    INTERACTION = 'interaction'

# Agents
interaction = InteractionAgent()
tutor = TutorAgent()

agents_dict = {
    AgentKeys.INTERACTION.value: interaction,
    AgentKeys.TUTOR.value: tutor,
 }

agents_dict_by_name = {
    "InteractionAgent": interaction,
    "TutorAgent": tutor,
}

avatars = {
    interaction.name: "✏️",                 # Pencil
    tutor.name: "🧑‍🎓",                  # Person with graduation hat
}
