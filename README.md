🎓 
📅 Academic Calendar & Timetable Viewer (Streamlit App)

This is a fully interactive Streamlit app that allows users to view and explore their university academic calendar and timetable from an uploaded Excel file.

You can view regular classes, special events (like seminars, workshops, orientations), and important/national days—all presented on a dynamic calendar interface.


---

✨ Features

✅ Upload your Academic Excel (.xlsx) file with sheets like timetable, special_days, and important_days.
✅ Calendar grid view with clear visual markers for each type of event.
✅ ⭐ Special icons for Workshops, Seminars, National Days, and more.
✅ 🔍 Click on any date to view full event details below the calendar.
✅ 📤 Export your schedule for any day or week to a CSV file (optional add-on).
✅ 📊 See course details like Instructor, Access Time, Mode, Status, and Department.


---

📅 Smart UI Highlights

🟦 Regular Classes: Black dots

⭐ Special Events / Days: Red exclamations and yellow stars

📌 Event Panel: Appears dynamically below the calendar when a date is clicked

🎨 Clean design with responsive layout and CSS-based calendar styling

🎯 Supports up to 2030 and works for all universities (just change the Excel!)



---

🚀 How to Run Locally

Step 1: Install required Python packages

pip install streamlit pandas openpyxl

Step 2: Save your app code

Save your main Python code as app.py.

Step 3: Run the Streamlit app

streamlit run app.py

Step 4: Open the app in your browser

Streamlit will launch the app at:
http://localhost:8501


---

🛠 How to Use the App

1. Open the app in your browser.


2. In the sidebar:

Enter your University Name

Select Year and Month

Upload your .xlsx file



3. View your academic calendar with:

📅 Weekly layout

⭐ Event highlights



4. Click on any date to see detailed info for:

Regular Classes

Special Events (Workshops, Hackathons, etc.)

National/Important Days



5. Event details update instantly below the calendar!




---

☁️ Deploy on Streamlit Cloud

You can deploy this app to Streamlit Cloud easily.

Required Files for Deployment

app.py – Your main Streamlit code

requirements.txt – List of dependencies


Example requirements.txt

streamlit
pandas
openpyxl

Just push these files to a GitHub repo and connect it to Streamlit Cloud.


---

📂 Excel File Format (Required Sheets)

timetable: Contains your class schedules

special_days: Events like workshops, hackathons, orientations

important_days: National or university-level observances


Each sheet must have a Date column with valid Excel date format.


---

✅ New Additions from Previous Version

🆕 Full calendar grid layout UI

🆕 ⭐ Support for special event types (over 20+ types auto-highlighted)

🆕 📌 Event detail panel moved below calendar

🆕 🖼️ UI redesigned to match uploaded calendar image exactly

🆕 📂 Multi-sheet Excel parsing with dynamic classification