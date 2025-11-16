import os
import json
import datetime
from groq import Groq

def suggest_events_from_profile(profile_filepath="profile.txt"):
    """
    Reads a student profile from a text file and uses the Groq LLM API
    to suggest actionable events, habits, and interventions.

    Args:
        profile_filepath (str): The path to the profile.txt file.
        
    Returns:
        str: The natural language suggestion text, or None if an error occurred.
    """
    
    # --- 1. Read the profile.txt file ---
    try:
        with open(profile_filepath, 'r', encoding='utf-8') as f:
            student_profile = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{profile_filepath}' was not found.")
        print("Please run the quiz script first to generate the profile.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # --- 2. Set up the Groq API Client ---
    try:
        client = Groq()
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        print("Please ensure your GROQ_API_KEY is set correctly.")
        return None

    # --- 3. Define the LLM Prompts ---
    
    # This prompt tells the AI its role, context, and desired output format.
    system_prompt = """
    You're a expert daily planner helping your client get the best day possible within the constraints listed. Please list the best 
    possible actions based on their preferences. Do not suggest times that don't align with their ideal sleep schedule.
    
    When should they go to eat based on their meal preferences? 
    Where and when should they study based on their preferences in locations and weekly time goals?
    When should they go to the gym?
    
    All events should be placed based on their wake hours and preferably within their preferred 'work' hours.
    
    """

    print("--- Analyzing Student Profile ---")
    print("Sending profile to Groq API for suggestions...\n")

    # --- 4. Call the Groq API ---
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"Here is the student's profile:\n\n{student_profile}",
                }
            ],
            model="llama-3.1-8b-instant", 
        )

        # --- 5. Print and return the LLM's Response ---
        response_content = chat_completion.choices[0].message.content
        print("--- Advisor Suggestions ---")
        print(response_content)
        return response_content # Return the text for the next function

    except Exception as e:
        print(f"Error during API call: {e}")
        print("Please check your internet connection and API key.")
        return None

def convert_text_to_json_events(suggestion_text: str):
    """
    Takes the natural language suggestion text and converts it into a
    strict JSON object of calendar events using the Groq API.
    
    Args:
        suggestion_text (str): The text output from suggest_events_from_profile.
        
    Returns:
        dict: The parsed JSON object, or None if an error occurred.
    """
    
    print("\n--- Converting Suggestions to JSON ---")
    
    # --- 1. Set up the Groq API Client ---
    try:
        client = Groq()
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        print("Please ensure your GROQ_API_KEY is set correctly.")
        return None
        
    # --- 2. Define Time/Timezone for the Prompt ---
    current_datetime = datetime.datetime.now().isoformat()
    # Using the example timezone from your prompt.
    # For dynamic detection, you might use a library like 'tzlocal'.
    user_timezone = "America/New_York" 

    # --- 3. Define the JSON extraction prompt ---
    system_prompt_json = f"""
    You are an expert daily planner and academic strategist for students. Your primary function is to help students build productive, realistic, and stress-reducing daily schedules.

    Your entire methodology is preference-driven. You understand that no two students work the same way. Your goal is not to create a generic, one-size-fits-all schedule, but to design a hyper-personalized plan that adapts to the specific user's study habits, energy levels, and academic load.
    
    Extract all calendar-worthy events from the provided text into a strict JSON object.
    Your output must be ONLY the JSON object, with no other text or markdown formatting.
    
    The JSON object must have a single key "events", which is an array of event objects.
    Each event object should have:
    - "title": (string) A short, human-friendly title.
    - "start": (string) The event start time in ISO 8601 format.
    - "end": (string, optional) The event end time in ISO 8601 format.
    - "allday": (boolean) True if it's an all-day event.
    - "location": (string, optional) The event location.
    - "description": (string, optional) Any notes or description.
    - "timezone": (string) The IANA timezone (e.g., "America/New_York").
    
    RULES:
    1. Resolve relative dates like "tomorrow" or "next Tuesday" relative to the current time: {current_datetime}.
    2. The user's local timezone is: {user_timezone}. All events should default to this timezone unless a different one is explicitly mentioned in the text.
    3. If an end time is not provided for a timed event, infer a 60-minute duration.
    4. For all-day events, the 'start' and 'end' time should be just the date part (e.g., "2025-10-28").
    """

    # --- 4. Call the Groq API for JSON ---
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt_json,
                },
                {
                    "role": "user",
                    "content": f"Here is the schedule text to convert:\n\n{suggestion_text}",
                }
            ],
            model="llama-3.1-8b-instant",
            # This is crucial for forcing the model to output *only* JSON
            response_format={"type": "json_object"}, 
        )

        json_string = chat_completion.choices[0].message.content
        
        # --- 5. Validate, Print, and Return the JSON ---
        try:
            # Validate and pretty-print the JSON
            event_data = json.loads(json_string)
            print("--- Extracted Calendar JSON ---")
            print(json.dumps(event_data, indent=2))
            return event_data
        except json.JSONDecodeError:
            print("Error: LLM did not return valid JSON.")
            print("Raw output:", json_string)
            return None

    except Exception as e:
        print(f"Error during API call: {e}")
        print("Please check your internet connection and API key.")
        return None

# --- Main execution block to run the pipeline ---
if __name__ == "__main__":
    # This will run the function when you execute `python routine.py`
    
    # 1. Get the natural language suggestions
    suggestion_text = suggest_events_from_profile()
    
    # 2. If suggestions were successfully generated, convert them to JSON
    if suggestion_text:
        json_events = convert_text_to_json_events(suggestion_text)
        
        if json_events:
            print("\nSuccessfully generated JSON events.")
            # You could now save this to a file or send to an API
            # with open('events.json', 'w') as f:
            #     json.dump(json_events, f, indent=2)