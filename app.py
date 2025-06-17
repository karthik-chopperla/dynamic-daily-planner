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

# --- Step 4: Simulated Learning Engine ---
def simulate_learning_behavior():
    focus_boost = 5 if task_completion > 70 else -5
    stress_penalty = -10 if stress_level > 60 else 0
    adjusted_focus = max(30, focus_length + focus_boost + stress_penalty)
    return adjusted_focus

# --- Step 5: Plan Generation with Dynamic Meals ---
def insert_meal_slots_dynamic(start_dt, end_dt):
    breakfast = start_dt + datetime.timedelta(minutes=60)
    lunch = breakfast + datetime.timedelta(hours=3)
    snacks = lunch + datetime.timedelta(hours=4)
    dinner = min(end_dt - datetime.timedelta(hours=2), snacks + datetime.timedelta(hours=3))

    meal_slots = {
        (breakfast, "Breakfast"),
        (lunch, "Lunch"),
        (snacks, "Snacks"),
        (dinner, "Dinner")
    }

    return meal_slots

if st.button("🧠 Generate My Planner"):
    st.subheader("📅 Your Dynamic Daily Plan")

    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, wake_time)
    end_dt = datetime.datetime.combine(today, sleep_time)
    adjusted_focus = simulate_learning_behavior()

    delta = datetime.timedelta(minutes=adjusted_focus)
    break_delta = datetime.timedelta(hours=break_freq)
    next_break = start_dt + break_delta

    current = start_dt
    schedule = []
    meals = insert_meal_slots_dynamic(start_dt, end_dt)

    while current + delta <= end_dt:
        # Check for any meals to insert before next block
        for meal_time, meal_name in sorted(meals):
            if current <= meal_time < current + delta:
                schedule.append((meal_time.time(), (meal_time + datetime.timedelta(minutes=30)).time(), meal_name))
                current = meal_time + datetime.timedelta(minutes=30)
                meals.remove((meal_time, meal_name))
                break

        # Add task
        if current + delta > end_dt:
            break
        task = random.choice(task_list)
        end_block = current + delta
        schedule.append((current.time(), end_block.time(), task))
        current = end_block

        # Insert break if needed
        if current >= next_break:
            break_end = current + datetime.timedelta(minutes=15)
            if break_end <= end_dt:
                schedule.append((current.time(), break_end.time(), "Break"))
                current = break_end
                next_break = current + break_delta

    # Show Schedule
    for start, end, task in schedule:
        st.markdown(f"**🕒 {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}**: {task}")

    st.success("Plan generated dynamically with adaptive focus, feedback, and meal scheduling!")
