# app.py
import streamlit as st
import datetime
import random

st.set_page_config(page_title="Dynamic Daily Planner", layout="centered")
st.title("🧠 Dynamic Daily Planner Generator")
st.markdown("""
This planner learns your daily routine and helps you organize your time effectively. 
Enter your preferences below to generate a smart, adaptive plan.
""")

# --- Step 1: Get Basic Info from User ---
st.subheader("Step 1: Your Time Preferences")
wake_time = st.time_input("What time do you usually wake up?", value=datetime.time(7, 0))
sleep_time = st.time_input("What time do you usually go to sleep?", value=datetime.time(22, 0))
break_freq = st.slider("How often do you take breaks (in hours)?", 1, 4, 2)
focus_length = st.slider("Preferred work focus block (in minutes)?", 25, 120, 60, step=5)

# --- Step 2: Ask for Task Categories ---
st.subheader("Step 2: Define Your Priorities")
tasks = st.text_area("List the types of tasks you want to schedule (comma separated):",
                     "Study, Work, Exercise, Reading, Leisure")
task_list = [t.strip() for t in tasks.split(",") if t.strip() != ""]

# --- Step 3: Yesterday's Feedback ---
st.subheader("Step 3: Yesterday's Feedback")
feedback_col1, feedback_col2 = st.columns(2)
task_completion = feedback_col1.slider("How productive were you yesterday?", 0, 100, 70)
stress_level = feedback_col2.slider("How stressed were you yesterday?", 0, 100, 40)

# --- Simulate learning adjustment ---
def simulate_learning_behavior():
    focus_boost = 5 if task_completion > 70 else -5
    stress_penalty = -10 if stress_level > 60 else 0
    adjusted_focus = max(30, focus_length + focus_boost + stress_penalty)
    return adjusted_focus

# --- Build time slots ---
def generate_meal_times(start_dt):
    breakfast = start_dt + datetime.timedelta(minutes=60)
    lunch = breakfast + datetime.timedelta(hours=3)
    dinner = lunch + datetime.timedelta(hours=5)
    return [
        (breakfast, "Breakfast"),
        (lunch, "Lunch"),
        (dinner, "Dinner")
    ]

# --- Schedule Generator ---
if st.button("🧠 Generate My Planner"):
    st.subheader("📅 Your Dynamic Daily Plan")

    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, wake_time)
    end_dt = datetime.datetime.combine(today, sleep_time)
    adjusted_focus = simulate_learning_behavior()
    focus_block = datetime.timedelta(minutes=adjusted_focus)
    break_block = datetime.timedelta(minutes=15)
    break_freq_td = datetime.timedelta(hours=break_freq)

    schedule = []
    current = start_dt
    next_break = current + break_freq_td
    meal_times = generate_meal_times(start_dt)

    meal_inserted = {"Breakfast": False, "Lunch": False, "Dinner": False}

    while current + focus_block <= end_dt:
        # Insert meals if needed
        for meal_time, meal_name in meal_times:
            if not meal_inserted[meal_name] and current >= meal_time:
                end_meal = current + datetime.timedelta(minutes=30)
                schedule.append((current.time(), end_meal.time(), meal_name))
                current = end_meal
                meal_inserted[meal_name] = True
                break
        else:
            # Add task
            task = random.choice(task_list)
            end_block = current + focus_block
            if end_block > end_dt:
                break
            schedule.append((current.time(), end_block.time(), task))
            current = end_block

            # Add break if needed
            if current >= next_break:
                break_end = current + break_block
                if break_end <= end_dt:
                    schedule.append((current.time(), break_end.time(), "Break"))
                    current = break_end
                    next_break = current + break_freq_td

    # Final check to force-insert remaining meals
    for meal_time, meal_name in meal_times:
        if not meal_inserted[meal_name] and current + datetime.timedelta(minutes=30) <= end_dt:
            end_meal = current + datetime.timedelta(minutes=30)
            schedule.append((current.time(), end_meal.time(), meal_name))
            current = end_meal

    # Display final schedule
    for start, end, task in schedule:
        st.markdown(f"**🕒 {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}**: {task}")

    st.success("Plan generated dynamically with adaptive focus, feedback, and all meals included!")
