import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

# App title and config
st.set_page_config(page_title="Timetable", layout="wide")
st.title("🎓 Timetable Viewer")

# Helper function to get week dates
def get_week_dates(reference_date):
    # Find Monday of the current week
    monday = reference_date - timedelta(days=reference_date.weekday())
    # Generate dates from Monday to Saturday
    return [monday + timedelta(days=i) for i in range(6)]  # 0-5 gives Monday to Saturday

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    university_name = st.text_input("University Name", "Tech University")
    date_option = st.radio(
        "Select Date",
        ["Today", "Tomorrow", "Custom Date", "This Week"],
        index=0
    )
    
    if date_option == "Custom Date":
        target_date = st.date_input("Select Date")
    elif date_option == "This Week":
        target_date = None  # Will handle week view separately
    else:
        today = datetime.today().date()
        target_date = today + timedelta(days=1) if date_option == "Tomorrow" else today
    
    uploaded_file = st.file_uploader(
        "Upload Timetable (Excel)",
        type=["xlsx"]
    )

# Main processing function (updated to handle multiple dates)
def get_timetable(target_dates, file_content):
    try:
        xlsx = pd.ExcelFile(file_content)
        all_tasks = []
        
        for date in target_dates:
            tasks = []
            for sheet in xlsx.sheet_names:
                df = xlsx.parse(sheet)
                df.columns = df.columns.str.strip()
                
                if 'Date' in df.columns:
                    df['Date'] = df['Date'].astype(str).str.strip()
                    df = df[df['Date'] != "Date"]
                    
                    parsed_dates = []
                    for date_str in df['Date']:
                        try:
                            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                        except ValueError:
                            try:
                                date_obj = datetime.strptime(date_str.split("-")[0], "%d-%m-%Y").date()
                            except ValueError:
                                date_obj = None
                        parsed_dates.append(date_obj)
                    
                    df['Date_parsed'] = parsed_dates
                    match_df = df[df['Date_parsed'] == date]
                    if not match_df.empty:
                        match_df['Department'] = sheet
                        match_df['Day'] = date.strftime("%A")
                        match_df['University'] = university_name  # Add university name
                        tasks.append(match_df)
            
            if tasks:
                daily_df = pd.concat(tasks)
                daily_df['Display_Date'] = date.strftime("%A, %d %B %Y")
                all_tasks.append(daily_df)
        
        return pd.concat(all_tasks) if all_tasks else pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return pd.DataFrame()

# Main app display
if uploaded_file:
    if date_option == "This Week":
        week_dates = get_week_dates(datetime.today().date())
        result_df = get_timetable(week_dates, uploaded_file)
        
        if not result_df.empty:
            st.header(f"📅 Weekly Schedule")
            
            # Group by date and display each day separately
            for date, group in result_df.groupby('Display_Date'):
                st.subheader(f"🗓️ {date}")
                
                for _, row in group.iterrows():
                    with st.expander(f"{row.get('Activity', 'Class')} - {row.get('Access time', '')}"):
                        cols = st.columns(3)  # Changed to 3 columns
                        cols[0].metric("University", row.get('University', 'N/A'))
                        cols[1].metric("Department", row.get('Department', 'N/A'))
                        cols[2].metric("Course", row.get('Course', 'N/A'))
                        st.write(f"**Instructor:** {row.get('Expert Name', 'N/A')}")
                        st.write(f"**Mode:** {row.get('Mode', 'N/A')}")
                        st.write(f"**Status:** {row.get('Status 1', '')} {row.get('Status 2', '')}")
            
            # Download button
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Weekly Schedule as CSV",
                data=csv,
                file_name=f"weekly_schedule_{week_dates[0].strftime('%Y%m%d')}_to_{week_dates[-1].strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )
        else:
            st.warning("No classes found for this week")
    else:
        result_df = get_timetable([target_date], uploaded_file)
        
        if not result_df.empty:
            date_str = target_date.strftime("%A, %d %B %Y")
            st.header(f"📅 Schedule for {date_str}")
            
            for _, row in result_df.iterrows():
                with st.expander(f"{row.get('Activity', 'Class')} - {row.get('Access time', '')}"):
                    cols = st.columns(3)  # Changed to 3 columns
                    cols[0].metric("University", row.get('University', 'N/A'))
                    cols[1].metric("Department", row.get('Department', 'N/A'))
                    cols[2].metric("Course", row.get('Course', 'N/A'))
                    st.write(f"**Instructor:** {row.get('Expert Name', 'N/A')}")
                    st.write(f"**Mode:** {row.get('Mode', 'N/A')}")
                    st.write(f"**Status:** {row.get('Status 1', '')} {row.get('Status 2', '')}")
            
            # Download button
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"schedule_{target_date.strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )
        else:
            st.warning(f"No classes found for {target_date.strftime('%A, %d %B %Y')}")
else:
    st.info("Please upload an Excel timetable file to begin")
if 
  st.button("refresh ")
  st.experimental_rerun()