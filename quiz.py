""" Quiz Prompts: """

import textwrap

def get_input(prompt):
    """
    Gets a simple string input from the user, with appropriate spacing.
    """
    return input(f"{prompt} ").strip()

def get_choice(prompt, options):
    """
    Displays a list of options and gets a validated choice from the user.
    """
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice_num = int(get_input("\nEnter the number of your choice:"))
            if 1 <= choice_num <= len(options):
                # Return the text of the chosen option
                return options[choice_num - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_list_items(prompt, item_name):
    """
    Collects a list of items from the user until they type 'done'.
    """
    print(prompt)
    items = []
    while True:
        item = get_input(f"Enter a {item_name} (or type 'done' to finish):")
        if item.lower() == 'done':
            break
        items.append(item)
    return items

def get_fixed_commitments():
    """
    Collects a list of fixed commitments (event, time, location).
    """
    print("\nNext, let's add your fixed commitments (classes, work, etc.).")
    commitments = []
    while True:
        name = get_input("Enter event name (or type 'done' to finish):")
        if name.lower() == 'done':
            break
        
        days = get_input(f"  Days for {name} (e.g., MWF, TTh):")
        start_time = get_input(f"  Start time for {name}:")
        end_time = get_input(f"  End time for {name}:")
        location = get_input(f"  Location for {name}:")
        
        # Format as a nice string for the summary
        commitment_str = f"{name} ({location}) on {days} from {start_time} to {end_time}"
        commitments.append(commitment_str)
    return commitments

def print_summary(responses):
    """
    Prints a structured report for an advisor to review.
    """
    print("\n" + "="*70)
    print(" STUDENT WELLNESS & HABITS PROFILE")
    print("="*70)
    print("This report summarizes the student's self-reported daily habits,")
    print("commitments, and preferences to inform support strategies.\n")

    # --- Section 1: Logistics & Commitments ---
    print("--- 1. Logistics & Commitments ---")
    print(f"* Living Situation: {responses['living_situation']}")
    print(f"* Home Base / Parking: {responses['home_base']}")
    
    if 'commute_time' in responses:
        print(f"* Average Commute: {responses['commute_time']} (one-way)")
        print(f"  > Advisor Note: Student has a significant daily commute,")
        print(f"    which impacts available time and adds potential stress.")
    
    print("\n* Fixed Commitments:")
    if responses['commitments']:
        for item in responses['commitments']:
            print(f"  - {item}")
        print(f"\n  > Advisor Note: Review the density of this schedule.")
        print(f"    Check for 'buffer time' between classes and locations.")
    else:
        print("  - No fixed commitments reported.")

    # --- Section 2: Daily Rhythm & Energy ---
    print("\n--- 2. Daily Rhythm & Energy ---")
    print(f"* Ideal Sleep Schedule: {responses['wake_time']} to {responses['bed_time']}")
    print(f"* Preferred 'Workday': {responses['workday_start']} to {responses['workday_end']}")
    print(f"* Peak Focus Time: {responses['focus_time']}")
    print(f"\n  > Advisor Note: Compare ideal sleep with actual commitments.")
    print(f"    A '{responses['focus_time']}' preference may conflict with")
    print(f"    an early class schedule, creating a friction point.")

    # --- Section 3: Study & Work Preferences ---
    print("\n--- 3. Study & Work Preferences ---")
    print(f"* Preferred Study Style: {responses['study_style']}")
    print(f"* Task Management: {responses['task_approach']}")
    print(f"* Weekly Study Goal: {responses['study_hours_goal']} hours")
    
    spots = ", ".join(responses['study_spots']) if responses['study_spots'] else "None reported"
    print(f"* Favorite Study Spots: {spots}")
    
    print(f"\n  > Advisor Note: The goal of {responses['study_hours_goal']} hours/week")
    print(f"    is a key self-reported pressure point. The student's task")
    print(f"    approach ('{responses['task_approach']}') is a good indicator")
    print(f"    of their coping mechanism for difficult work.")

    # --- Section 4: Personal Habits & Well-being ---
    print("\n--- 4. Personal Habits & Well-being ---")
    print(f"* Meal Habits: {responses['meals']}")
    print(f"* Exercise Frequency: {responses['exercise_freq']}")
    print(f"* Exercise Duration: {responses['exercise_duration']}")
    print(f"* Scheduled Downtime: {responses['downtime']}")

    # --- Final Advisor Note (CRITICAL) ---
    if ('no' in responses['downtime'].lower() or 
        'fill' in responses['downtime'].lower() or 
        'just fill' in responses['downtime'].lower()):
        
        print(f"\n  *** KEY ADVISOR NOTE: BURNOUT RISK ***")
        print(f"  Student reported NOT scheduling dedicated downtime")
        print(f"  (Response: '{responses['downtime']}').")
        print(f"  This is a primary risk factor for burnout and a key")
        print(f"  area for intervention and discussion.")
    else:
        print(f"\n  > Advisor Note: The student's meal, exercise, and downtime")
        print(f"    habits are foundational to well-being. Their stated")
        print(f"    downtime preference is a good starting point for")
        print(f"    building a sustainable work-life balance.")

    print("\n" + "="*70)


def main():
    """
    Main function to run the quiz.
    """
    responses = {}

    print("--- Section 1: Logistics & Commitments ---")
    responses['living_situation'] = get_choice(
        "What's your living situation?",
        ["On-Campus Resident", "Off-Campus (Commuter)"]
    )
    
    responses['home_base'] = get_input("What's your primary 'home base' or parking spot? (e.g., North Campus, Lot 4):")
    
    if responses['living_situation'] == "Off-Campus (Commuter)":
        responses['commute_time'] = get_input("On average, how long is your one-way commute? (e.g., 30 minutes):")
    
    responses['commitments'] = get_fixed_commitments()

    print("\n--- Section 2: Daily Rhythm & Energy ---")
    responses['wake_time'] = get_input("What is your ideal wake up time? (e.g., 7:00 AM):")
    responses['bed_time'] = get_input("What is your ideal go to bed time? (e.g., 11:00 PM):")
    responses['workday_start'] = get_input("When do you want your 'workday' to start? (e.g., 9:00 AM):")
    responses['workday_end'] = get_input("When do you want your 'workday' to stop? (e.g., 5:00 PM):")
    responses['focus_time'] = get_choice(
        "When are you most focused?",
        ["Morning (I'm a 'morning person')", "Afternoon", "Evening / Late Night (I'm a 'night owl')"]
    )

    print("\n--- Section 3: Study & Work Preferences ---")
    responses['study_style'] = get_choice(
        "What's your preferred study style?",
        ["Short Bursts (e.g., Pomodoro - 25 min work, 5 min break)",
         "Standard Sessions (e.g., 50 min work, 10 min break)",
         "Deep Work Blocks (e.g., 90-120 min of focused work)"]
    )
    responses['task_approach'] = get_choice(
        "How do you like to tackle a big to-do list?",
        ["Schedule my hardest, most-dreaded tasks first",
         "Warm-Up (Schedule 1-2 easy tasks first)",
         "Mix it Up (Alternate between hard and easy tasks)"]
    )
    responses['study_spots'] = get_list_items(
        "\nWhere are your favorite places to study?",
        "study spot"
    )
    responses['study_hours_goal'] = get_input("As a goal, how many hours per week do you want to dedicate to studying? (e.g., 15):")

    print("\n--- Section 4: Personal Habits & Goals ---")
    responses['meals'] = get_choice(
        "How do you handle meals?",
        ["I go to the dining hall",
         "I cook my own meals",
         "I grab quick meals on the go"]
    )
    responses['exercise_freq'] = get_input("How often do you want to exercise? (e.g., 3 times a week):")
    responses['exercise_duration'] = get_input("How long are your typical workouts? (e.g., 60-90 minutes):")
    responses['downtime'] = get_input("Do you want to schedule dedicated downtime? (e.g., 'Yes, 8 PM - 10 PM', 'No, fill my free time'):")

    # Finally, print the summary
    print_summary(responses)

if __name__ == "__main__":
    main()