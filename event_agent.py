from empire_chain.agent.agent import Agent
from dotenv import load_dotenv
import openai
from supabase import create_client
import os
from datetime import datetime, timedelta
import json

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

def onboard_new_member(name: str, email: str, interests: str) -> str:
    supabase = create_client(supabase_url, supabase_key)
    supabase.table('members').insert({
        'name': name,
        'email': email,
        'interests': interests
    }).execute()
    return f"Welcome {name}! You've been successfully onboarded to our community. We're excited to have you here!"

def get_community_help() -> str:
    return """Here are some ways I can help you:
1. Onboarding new members
2. Community guidelines and rules
3. Event announcements and scheduling
4. Content generation
5. Moderation assistance
6. Community engagement
7. Resource sharing
Just ask me about any of these topics!"""

def generate_content(query: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful community assistant. Provide clear, concise, and friendly responses."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def general_chat(query: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful community assistant. Provide clear, concise, and friendly responses."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def get_community_guidelines() -> str:
    return """Community Guidelines:
1. Be respectful and inclusive
2. No spam or self-promotion without permission
3. Keep discussions relevant and constructive
4. Respect privacy and confidentiality
5. Report inappropriate behavior to moderators
6. Use appropriate channels for different topics
7. Help others and share knowledge
8. Follow Discord's Terms of Service"""

def get_upcoming_events() -> str:
    supabase = create_client(supabase_url, supabase_key)
    events = supabase.table('events').select('*').gte('date', datetime.now().isoformat()).order('date').limit(5).execute()
    
    if not events.data:
        return "No upcoming events scheduled at the moment."
    
    response = "Upcoming Events:\n"
    for event in events.data:
        date = datetime.fromisoformat(event['date']).strftime('%B %d, %Y at %I:%M %p')
        response += f"\n• {event['title']} - {date}\n  {event['description']}\n"
    return response

def report_issue(issue_type: str, description: str, reporter: str) -> str:
    supabase = create_client(supabase_url, supabase_key)
    supabase.table('reports').insert({
        'type': issue_type,
        'description': description,
        'reporter': reporter,
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }).execute()
    return f"Thank you for your report. Our moderation team has been notified and will address this issue."

def get_community_stats() -> str:
    supabase = create_client(supabase_url, supabase_key)
    
    # Get member count
    members = supabase.table('members').select('*').execute()
    member_count = len(members.data)
    
    # Get event count
    events = supabase.table('events').select('*').execute()
    event_count = len(events.data)
    
    # Get active discussions
    discussions = supabase.table('discussions').select('*').gte('last_activity', (datetime.now() - timedelta(days=7)).isoformat()).execute()
    active_discussions = len(discussions.data)
    
    return f"""Community Statistics:
• Total Members: {member_count}
• Total Events: {event_count}
• Active Discussions (Last 7 Days): {active_discussions}"""

def get_resource_links() -> str:
    return """Helpful Resources:
1. Community Documentation: [link]
2. Getting Started Guide: [link]
3. FAQ: [link]
4. Code of Conduct: [link]
5. Event Calendar: [link]
6. Community Projects: [link]
7. Learning Resources: [link]
8. Support Channels: [link]"""

def get_chat_summary() -> str:
    supabase = create_client(supabase_url, supabase_key)
    discussions = supabase.table('discussions').select('title, content').order('last_activity', desc=True).limit(50).execute()
    
    if not discussions.data:
        return "No chat history found."
    
    # Prepare the discussions for summarization
    chat_history = "\n".join([f"Title: {d['title']}\nContent: {d['content']}\n" for d in discussions.data])
    
    # Use GPT to summarize the chat history
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes chat discussions. Provide a clear and concise summary of the main topics and interactions."},
            {"role": "user", "content": f"Please summarize the following chat history:\n\n{chat_history}"}
        ]
    )
    
    return response.choices[0].message.content

def main():
    # Create agent
    agent = Agent()
    
    # Register functions
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
        agent.register_function(func)
    
    # Example queries
    queries = [
        "Onboard new member with name: Manas Chopra, email: manas@ai.com, interests: AI and Machine Learning",
        "Get community help",
        "Generate content about AI and Machine Learning",
        "What is the weather in Tokyo?",
        "Show community guidelines",
        "What are the upcoming events?",
        "Report an issue: Spam in general channel",
        "Show community statistics",
        "Get resource links",
        "Get chat summary"
    ]
    
    # Process queries
    for query in queries:
        try:
            result = agent.process_query(query)
            print(f"\nQuery: {query}")
            print(f"Result: {result['result']}")
        except Exception as e:
            print(f"Error processing query '{query}': {str(e)}")

if __name__ == "__main__":
    main()