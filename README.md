🎓 Timetable Viewer (Streamlit App)

This is a Streamlit app to view and download your university timetable easily from an uploaded Excel file.
You can check your schedule for Today, Tomorrow, Custom Date, or the Whole Week!


---

✨ Features

Upload your timetable (Excel .xlsx file).

View today's, tomorrow's, a custom day's, or the full week's schedule.

See course details like Instructor, Department, Mode, Status, etc.

Download your schedule as a CSV file.



---

🚀 How to Run Locally

1. Install required Python packages:

pip install streamlit pandas


2. Save the provided code as a Python file, e.g., app.py.


3. Run the app:

streamlit run app.py


4. Open the app in your browser (usually at http://localhost:8501).




---

🛠 Step-by-Step Usage

1. Open the app.


2. In the sidebar:

Enter your University Name.

Choose whether you want to view Today, Tomorrow, Custom Date, or This Week.

If needed, pick a Custom Date.



3. Upload your timetable Excel file.


4. Your schedule will appear automatically!


5. You can expand each class to see more details.


6. Download your schedule as a CSV file if needed.




---

☁️ How Streamlit Cloud Works (Behind the Scenes)

Streamlit Cloud is a platform to host and share Streamlit apps easily.

You connect your GitHub repo (where your app code lives) to Streamlit Cloud.

Streamlit Cloud automatically installs your Python libraries (like streamlit and pandas) by reading a requirements.txt file.

It runs your streamlit run app.py command on their servers.

Then, it serves your app live on a public web link, which you can share with others!


Important:

You need a requirements.txt file listing required Python packages (example below).

You don't need to manually run anything – Streamlit Cloud handles it!


Example requirements.txt:

streamlit
pandas


---

📂 Files You Need in GitHub Repo

app.py (your Streamlit code)

requirements.txt (with package names)


Then you can deploy easily!


---