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
