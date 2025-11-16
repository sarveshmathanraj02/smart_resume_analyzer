import streamlit as st 
import pandas as pd
import plotly.express as px
import base64

def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def admin_panel(cursor):
    st.subheader("Admin Panel")
    role_filter = st.selectbox("Select Role to Filter Resumes", [
        "Cybersecurity Analyst", "UI/UX Designer", "Data Scientist",
        "Software Engineer", "Systems Analyst", "DevOps Engineer",
        "Product Manager", "Machine Learning Engineer", "Cloud Architect",
        "Business Analyst"
    ])
    if role_filter:
        query = "SELECT * FROM user_data WHERE Predicted_Field IS NOT NULL AND Predicted_Field != ''"
        query += " AND LOWER(Predicted_Field) = LOWER(%s)"
        query += " ORDER BY resume_score DESC"
        try:
            cursor.execute(query, (role_filter,))
            user_data = cursor.fetchall()
            if user_data:
                df = pd.DataFrame(user_data, columns=[
                    "ID", "Name", "Email_ID", "Resume Score", "Timestamp", "Page No",
                    "Predicted Field", "User Level", "Actual Skills",
                    "Recommended Skills", "Recommended Courses"
                ])
                df_filtered = df.drop(columns=["Recommended Skills", "Recommended Courses", "Page No"])
                st.dataframe(df_filtered)
                download_link = get_table_download_link(df_filtered, f"{role_filter}_filtered_data.csv", "Download Filtered Data as CSV")
                st.markdown(download_link, unsafe_allow_html=True)
            else:
                st.warning(f"No resumes found for the selected role: {role_filter}.")
        except Exception as e:
            st.error(f"Error executing query: {e}")
    view_scores = st.checkbox("View Resume Score Distribution")
    if view_scores:
        cursor.execute("SELECT resume_score FROM user_data")
        scores = [int(row[0]) for row in cursor.fetchall() if row[0].isdigit()]
        if scores:
            fig = px.histogram(scores, nbins=10, title="Resume Score Distribution")
            st.plotly_chart(fig)
    view_activity = st.checkbox("View User Activity Over Time")
    if view_activity:
        try:
            cursor.execute("SELECT Timestamp FROM user_data")
            timestamps = [row[0] for row in cursor.fetchall()]
            processed_timestamps = [ts.replace("_", " ") for ts in timestamps]
            timestamps_dt = [pd.to_datetime(ts) for ts in processed_timestamps]
            if timestamps_dt:
                activity_df = pd.DataFrame(timestamps_dt, columns=["Timestamp"])
                activity_df["Date"] = activity_df["Timestamp"].dt.date
                activity_counts = activity_df["Date"].value_counts().sort_index()
                fig = px.line(x=activity_counts.index, y=activity_counts.values,
                              title="User Activity Over Time", labels={"x": "Date", "y": "Activity Count"})
                st.plotly_chart(fig)
            else:
                st.warning("No activity data found.")
        except Exception as e:
            st.error(f"Error processing user activity data: {e}") 
