import streamlit as st
import datetime
import random

# Title
st.set_page_config(page_title="Dynamic Daily Planner")
st.title("🧠 AI-Powered Dynamic Daily Planner")
st.markdown("Create your personalized day schedule using AI logic — no preset templates, no static logic, 100% generated dynamically based on your input.")

# Session state for persistent planning if rerun
if "daily_plan" not in st.session_state:
    st.session_state.daily_plan = []

# --- Step 1: Collect user data ---
st.header("📥 Step 1: Your Day Preferences")

# Time range for the day
wake_time = st.time_input("Wake-up Time", value=datetime.time(7, 0))
sleep_time = st.time_input("Sleep Time", value=datetime.time(22, 0))

# Convert to datetime objects
def convert_time(t):
    return datetime.datetime.combine(datetime.date.today(), t)

start_dt = convert_time(wake_time)
end_dt = convert_time(sleep_time)
total_minutes = int((end_dt - start_dt).total_seconds() / 60)

# Tasks and preferences
st.markdown("### Enter your key priorities for today:")
tasks = st.text_area("Separate tasks by commas (e.g. Study ML, Exercise, Freelance work)", placeholder="Task 1, Task 2, Task 3")
task_list = [t.strip() for t in tasks.split(",") if t.strip() != ""]

break_pref = st.slider("🛑 Break Frequency (per hour)", 0, 4, 1)
focus_span = st.slider("⚡ Focus Block Duration (minutes)", 30, 120, 60)

# Simulate learning from past performance (optional feedback)
feedback = st.selectbox("📊 Did you complete your planner yesterday?", ["I’m new", "Yes", "Partially", "No"])

adjustment_factor = {
    "I’m new": 1.0,
    "Yes": 1.1,
    "Partially": 0.9,
    "No": 0.7
}[feedback]

# --- Step 2: Generate Plan ---
st.header("⚙️ Step 2: AI Generated Plan")

if st.button("Generate My Planner"):
    if not task_list:
        st.warning("Please enter at least one task.")
    else:
        st.session_state.daily_plan = []
        remaining_minutes = int(total_minutes * adjustment_factor)
        random.shuffle(task_list)

        current_time = start_dt
        i = 0
        while remaining_minutes > 0 and i < len(task_list):
            block = min(focus_span, remaining_minutes)
            task = task_list[i % len(task_list)]

            st.session_state.daily_plan.append({
                "time": current_time.strftime("%I:%M %p"),
                "task": task,
                "duration": block
            })

            current_time += datetime.timedelta(minutes=block)
            remaining_minutes -= block

            if break_pref > 0:
                break_time = int(60 / break_pref)
                current_time += datetime.timedelta(minutes=break_time)
                remaining_minutes -= break_time

            i += 1

# --- Step 3: Show the Plan ---
st.header("📅 Your Dynamic Planner")

if st.session_state.daily_plan:
    for i, entry in enumerate(st.session_state.daily_plan):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(entry["time"])
        with col2:
            st.markdown(f"**{entry['task']}** — _{entry['duration']} mins_")

    st.success("Planner created successfully. Refresh or modify inputs to regenerate.")
else:
    st.info("Your planner will appear here after generation.")

# --- Step 4: Feedback & Save (optional future extension) ---
# You can build persistent storage with Google Sheets or SQLite if needed (optional enhancement)
