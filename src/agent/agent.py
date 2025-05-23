from empire_chain.agent.agent import Agent
from src.agent.agent_functions import (
    onboard_new_member,
    get_community_help,
    generate_content,
    general_chat,
    get_community_guidelines,
    get_upcoming_events,
    report_issue,
    get_community_stats,
    get_resource_links,
    get_chat_summary
)

class CommunityAgent:
    def __init__(self):
        self.agent = Agent()
        self._register_functions()

    def _register_functions(self):
        functions = [
            onboard_new_member,
            get_community_help,
            generate_content,
            general_chat,
            get_community_guidelines,
            get_upcoming_events,
            report_issue,
            get_community_stats,
            get_resource_links,
            get_chat_summary
        ]
        
        for func in functions:
            self.agent.register_function(func)

    def process_query(self, query: str) -> dict:
        return self.agent.process_query(query) 