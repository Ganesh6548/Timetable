
import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# === Page Setup ===
st.set_page_config("📅 Academic Calendar", layout="wide")
st.title("📅 My Academic Calendar")

# === Sidebar ===
with st.sidebar:
    st.header("Settings")
    university_name = st.text_input("University Name", "Tech University")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    selected_year = st.selectbox("Select Year", list(range(2023, 2031)), index=2)
    selected_month = st.selectbox("Select Month", list(calendar.month_name)[1:], index=datetime.today().month - 1)

# === Cache Loader ===
@st.cache_data
def load_excel_data(file, university):
    xlsx = pd.ExcelFile(file)
    timetable_list, special_days, important_days = [], pd.DataFrame(), pd.DataFrame()

    for sheet in xlsx.sheet_names:
        df = xlsx.parse(sheet)
        df.columns = df.columns.str.strip()

        if sheet.lower() == "special_days" and 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            special_days = df.dropna(subset=['Date'])

        elif sheet.lower() == "important_days" and 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            important_days = df.dropna(subset=['Date'])

        elif 'Date' in df.columns:
            df = df[df['Date'] != "Date"]
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df['Department'] = sheet
            df['University'] = university
            timetable_list.append(df)

    timetable_df = pd.concat(timetable_list, ignore_index=True) if timetable_list else pd.DataFrame()
    return timetable_df, special_days, important_days

# === Main App Logic ===
if uploaded_file:
    timetable_df, special_days_df, important_days_df = load_excel_data(uploaded_file, university_name)

    month_index = list(calendar.month_name).index(selected_month)
    cal = calendar.Calendar(firstweekday=6)
    month_dates = list(cal.itermonthdates(selected_year, month_index))
    weeks = [month_dates[i:i + 7] for i in range(0, len(month_dates), 7)]

    # Create event maps
    events, specials, named_days = {}, {}, {}
    for df, store, key in [(timetable_df, events, 'Activity'),
                           (special_days_df, specials, 'Event Name'),
                           (important_days_df, named_days, 'Day Name')]:
        for _, row in df.iterrows():
            dt = row['Date'].date()
            store.setdefault(dt, []).append(row)

    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = date.today()

    st.subheader(f"{selected_month} {selected_year}")
    col1, col2 = st.columns([2.5, 1])

    # === Calendar UI ===
    with col1:
        st.markdown("### Calendar View")
        weekday_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        st.markdown(
            "<div style='display:grid;grid-template-columns:repeat(7,1fr);text-align:center;font-weight:bold;'>"
            + "".join([f"<div>{day}</div>" for day in weekday_labels]) + "</div>", unsafe_allow_html=True
        )

        for week in weeks:
            cols = st.columns(7)
            for i, day in enumerate(week):
                style = "color:gray;" if day.month != month_index else ""
                display_text = f"**{day.day}**"

                # Add markers
                markers = ""
                if day in events:
                    markers += "● "
                if day in specials:
                    for s in specials[day]:
                        typ = str(s.get("Event Type", "")).lower()
                        if "workshop" in typ:
                            markers += "🔵 "
                        elif "orientation" in typ:
                            markers += "🟢 "
                if day in named_days:
                    markers += "⭐"

                if cols[i].button(f"{display_text}\n{markers}", key=f"{day}"):
                    st.session_state.selected_date = day

    # === Right Panel – Event Details ===
    with col2:
        selected = st.session_state.selected_date
        st.subheader(f"📌 Events on {selected.strftime('%A, %d %B %Y')}")

        if selected in events:
            for e in events[selected]:
                st.markdown(f"""
                🔹 **{e.get('Activity', 'Class')}**  
                🕒 {e.get('Access time', 'N/A')}  
                👨‍🏫 {e.get('Expert Name', 'N/A')}  
                🏛️ {e.get('Department', '')} | {e.get('Course', '')}  
                💬 {e.get('Mode', '')}  
                ✅ {e.get('Status 1', '')} {e.get('Status 2', '')}
                """)

        if selected in specials:
            for s in specials[selected]:
                st.markdown(f"""
                🎯 **{s.get("Event Type", "Special Event")}** – {s.get("Event Name", "")}
                """)

        if selected in named_days:
            for n in named_days[selected]:
                st.markdown(f"⭐ **{n.get('Day Name', 'Special Day')}** *(Region: {n.get('Region', 'Global')})*")

        st.divider()
        st.markdown("### Legend")
        st.markdown("● : Regular Class")
        st.markdown("🔵 : Workshop")
        st.markdown("🟢 : Orientation")
        st.markdown("⭐ : National/Special Day")

else:
    st.info("📂 Upload an Excel file containing `timetable`, `special_days`, and `important_days` sheets to get started.")

