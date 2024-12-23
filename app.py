from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

name = "Evan"
user_role = "Currently as a college student, I have a lot of responsibilities. I’m currently taking 15 credits of course in which I have a lot of assignments to do per week. I’m also part of the robotics club in the electric team where I’m currently working on designing a robot for a competition. I also work out in the gym every morning an work part time 10 hours a week."
user_goal = "Over the next three months, I want to get a lot of things. First, I want to work well in my part time job so I can get promoted and get a higher pay. Second, I want to maintain my 3.0. Third, I want to try becoming promoted to electrical lead in the robotics club next semester. Fourth, I want to increase my muscle strength."

prompt_for_goals = (f"Our app is a journaling app where we want to have deep understanding of the user and help users achieve his/her goals. We want to track user’s progress based on each of the goals weekly and give suggestions based on their daily journal entries. We asked the user in the app “What do you want to accomplish over the next three months? What are some things you want to achieve/get done? Where do you want to grow? Where do you want to get better?” Based on the user’s roles and user’s response to this question below, break down each of the user’s goals into a full sentence, each separate with exactly just one new line character, no number bullet lists, no extra formatting and syntax:\n"
                    f"User's role: {user_role}\n"
                    f"User's goals: {user_goal}")

def open_ai_call(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

goals = open_ai_call(prompt_for_goals)

# goals = (f"I want to improve my coding\n"
#         f"I want to finish building the mars tank\n"
#         f"I want to pass my classes and gain deep understanding in math and computers\n"
#         f"I want to explore my interests and explore different majors to decide one\n"
#         f"I want to go to gym more\n")

list_of_goals = []

for goal in goals.split("\n"):
    goal_dict = {
        "goal": goal,
        "progress": ""
    }
    if goal_dict["goal"] == "":
        continue
    list_of_goals.append(goal_dict)

df = pd.DataFrame(list_of_goals)

print(df)

daily_journal_1 = "I set up an alarm to go to the gym at 9 am. However, I was supposed to reach the gym at 9:15 but got 5 minutes late. I had an hour workout and then went straight to class. After that, at 11:30, I studied and worked on my assignments till 1 pm. I took a 10 minute walk to the dining hall and ate my lunch. At 2 pm, I reached my room intending to take a nap only till 2:30. However, I overslept and woke up at 4 pm. I then went to the library which is 5 minutes away and completed my speech for tomorrow. I stayed there until 8 pm and went to the dining hall to eat my dinner. I reached back into the residence hall by 9 pm, and hung out with my friends till 11pm. I then brushed my teeth and went to sleep."

prompt_to_decide_updating_the_progress = f"Our app is a journaling app where we want to have deep understanding of the user and help users achieve his/her goals. We want to track user’s progress based on each of the goals weekly and give suggestions based on their daily journal entries. Below is one of the user's goals and his daily journal for today. Produce a boolean value (true/false) that decides whether or not the user made progress towards the goal this day based on the journal entry for today with no extra text, formatting or syntax. JUST RESPOND IN ONE WORD"
prompt_to_update_progress = f"Our app is a journaling app where we want to have deep understanding of the user and help users achieve his/her goals. We want to track user’s progress based on each of the goals weekly and give suggestions based on their daily journal entries. Below is one of the user's goals and his daily journal for today. Produce a simple progress excerpt in pure text simply describing what the user did regarding making progress towards the goal for this day. Give no suggestions. No extra formatting and syntax."

def update_progress(goal, daily_journal):
    current_progress = df.loc[df["goal"] == goal, "progress"].iloc[0]
    
    # First check if we should update progress
    progress_check_prompt = prompt_to_decide_updating_the_progress + f"\nGoal: {goal}\nJournal: {daily_journal_1}"
    should_update = open_ai_call(progress_check_prompt).lower() == "true"

    print(f"Should update: {should_update}")
    if should_update:
        # Create prompt based on whether there's existing progress
        if current_progress:
            prompt = (prompt_to_update_progress + 
                     f"\nGoal: {goal}\n"
                     f"Previous Progress: {current_progress}\n"
                     f"Journal: {daily_journal_1}")
        else:
            prompt = (prompt_to_update_progress + 
                     f"\nGoal: {goal}\n"
                     f"Journal: {daily_journal_1}")
        
        response = open_ai_call(prompt)
        print(f"New progress: {response}")
        df.loc[df["goal"] == goal, "progress"] = response

print(df)

daily_journal_2 = "Luckily, I was able to wake up on time and not get late for my gym session. I had a class after that where I gave my speech. It went pretty well. Since it was a friday, I decided to just eat out with my friends during lunch and play badminton the whole day. I came back to my room at 11 pm and worked on a few assignments before going to sleep at 2 am."

for goal in df["goal"]:
    current_progress = df.loc[df["goal"] == goal, "progress"].iloc[0]
    
    # First check if we should update progress
    progress_check_prompt = prompt_to_decide_updating_the_progress + f"\nGoal: {goal}\nJournal: {daily_journal_2}"
    should_update = open_ai_call(progress_check_prompt).lower() == "true"

    print(f"Should update: {should_update}")
    if should_update:
        # Create prompt based on whether there's existing progress
        if current_progress:
            prompt = (prompt_to_update_progress + 
                     f"\nGoal: {goal}\n"
                     f"Previous Progress: {current_progress}\n"
                     f"Journal: {daily_journal_2}")
        else:
            prompt = (prompt_to_update_progress + 
                     f"\nGoal: {goal}\n"
                     f"Journal: {daily_journal_2}")
        
        response = open_ai_call(prompt)
        print(f"New progress: {response}")
        df.loc[df["goal"] == goal, "progress"] = response

print(df)