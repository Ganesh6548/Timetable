import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# === Page Setup ===
st.set_page_config("📅 Academic Dashboard", layout="wide")
st.title("🎓 Academic Calendar & Course Details Viewer")

# === Sidebar ===
with st.sidebar:
    st.header("Settings")
    university_name = st.text_input("University Name", "Tech University")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    selected_year = st.selectbox("Select Year", list(range(2023, 2031)), index=2)
    selected_month = st.selectbox("Select Month", list(calendar.month_name)[1:], index=datetime.today().month - 1)

# === Data Loader ===
@st.cache_data
def load_excel_data(file, university):
    xlsx = pd.ExcelFile(file)
    timetable_list, special_days, important_days, course_details = [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    for sheet in xlsx.sheet_names:
        df = xlsx.parse(sheet)
        df.columns = df.columns.str.strip()

        if sheet.lower() == "special_days" and 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            special_days = df.dropna(subset=['Date'])

        elif sheet.lower() == "important_days" and 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            important_days = df.dropna(subset=['Date'])

        elif sheet.lower() == "course details":
            course_details = df

        elif 'Date' in df.columns:
            df = df[df['Date'].astype(str).str.lower() != 'date']
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df['Department'] = sheet
            df['University'] = university
            timetable_list.append(df)

    timetable_df = pd.concat(timetable_list, ignore_index=True) if timetable_list else pd.DataFrame()
    return timetable_df, special_days, important_days, course_details

# === App Logic ===
if uploaded_file:
    timetable_df, special_days_df, important_days_df, course_df = load_excel_data(uploaded_file, university_name)

    tab1, tab2 = st.tabs(["📅 Academic Calendar", "📘 Course Detail Viewer"])

    with tab1:
        # === Calendar UI ===
        month_index = list(calendar.month_name).index(selected_month)
        cal = calendar.Calendar(firstweekday=6)
        month_dates = list(cal.itermonthdates(selected_year, month_index))
        weeks = [month_dates[i:i + 7] for i in range(0, len(month_dates), 7)]

        star_event_types = [
            "orientation", "seminar", "panel", "exhibition", "conference", "workshop",
            "awareness", "hackathon", "ideathon", "clean-up", "celebration", "showcase",
            "symposium", "campaign", "talk show", "tribute", "appreciation",
            "forum", "gathering", "expo", "week start", "week end"
        ]

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

        with col1:
            st.markdown("### Calendar View")
            weekday_labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            st.markdown(
                "<div style='display:grid;grid-template-columns:repeat(7,1fr);text-align:center;font-weight:bold;background:#f0f0f0;padding:5px;border:1px solid #ccc;'>"
                + "".join([f"<div style='padding:10px'>{day}</div>" for day in weekday_labels]) + "</div>",
                unsafe_allow_html=True
            )

            for week in weeks:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    display_text = f"**{day.day}**"
                    markers = ""

                    if day in events:
                        markers += "● "
                    if day in specials:
                        for s in specials[day]:
                            typ = str(s.get("Event Type", "")).lower().strip()
                            if any(keyword in typ for keyword in star_event_types):
                                markers += "⭐ "
                    if day in named_days:
                        markers += " "

                    if cols[i].button(f"{display_text}\n{markers}", key=f"{day}"):
                        st.session_state.selected_date = day

        with col2:
            selected = st.session_state.selected_date
            st.subheader(f"📌 Events on {selected.strftime('%A, %d %B %Y')}")

            if selected in events:
                for e in events[selected]:
                    st.markdown(f"""
                    🔹  {e.get('Activity', 'Class')}
                    🕒 {e.get('Access time', 'N/A')}  
                    👨‍🏫 {e.get('Expert Name', 'N/A')}  
                    🏛️ {e.get('Department', '')} | {e.get('Course', '')}  
                    💬 {e.get('Mode', '')}  
                    ✅ {e.get('Status 1', '')} {e.get('Status 2', '')}
                    """)

            if selected in specials:
                for s in specials[selected]:
                    event_type = s.get("Event Type", "Special Event") or "Special Event"
                    event_name = s.get("Event Name", "")
                    event_name = event_name.strip() if isinstance(event_name, str) else ""
                    if not event_name:
                        event_name = "*Unnamed Event*"
                    st.markdown(f"🎯 {event_type} – {event_name}")

            if selected in named_days:
                for n in named_days[selected]:
                    day_name = n.get("Day Name", "").strip() or "Special Day"
                    region = n.get("Region", "Global").strip()
                    st.markdown(f"🔹 **{day_name}** *(Region: {region})*")

            st.divider()
            st.markdown("### Legend")
            st.markdown("● : Regular Class")
            st.markdown("⭐ : Special Event / Special Day")

    with tab2:
        st.subheader("🔍 Search for a Course by Name or ID")

        if not course_df.empty:
            with st.expander("📊 Preview Course Data"):
                st.dataframe(course_df.head(10))

            search_term = st.text_input("Enter course name or course ID")

            if search_term:
                results = course_df[course_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)]

                if not results.empty:
                    row = results.iloc[0]

                    st.markdown("### 📝 Course Details")
                    try:
                        st.write(f"**Course Name:** {row[1]}")
                        st.write(f"**Course ID:** {row[2]}")
                        st.write(f"**Credit:** {row[3]}")
                        st.write(f"**Stream:** {row[4]}")
                        st.write(f"**Discipline:** {row[5]}")

                        st.markdown("#### 📅 Weekly Available Questions:")
                        for i in range(6, 21):  # Week 1 to 15
                            st.write(f"Week {i - 5}: {row[i]}")

                        st.write(f"**Project:** {row[22]}")
                        st.write(f"**Uploaded Name:** {row[26]}")
                        st.write(f"**Grand Total:** {row[24]}")

                    except Exception as e:
                        st.warning(f"⚠️ Some fields may be missing: {e}")
                else:
                    st.warning("❌ No matching course found.")
        else:
            st.info("No 'course details' sheet found in the file.")
else:
    st.info("📂 Upload an Excel file to begin.")

