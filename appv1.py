import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar
import datetime
import json
import os

# Simulated AI Advertising Writer
def ai_advertising_writer(platform, topic):
    templates = {
        "X": f"🚀 {topic} is here! Join the conversation and share your thoughts! #Marketing",
        "Instagram": f"🌟 Discover {topic}! Swipe up to learn more! #InstaVibes",
        "LinkedIn": f"Unlock the potential of {topic} in your business. Read our latest insights! #BusinessGrowth"
    }
    return templates.get(platform, f"Engage with {topic}!")

# Mock Hootsuite/Buffer API integration
def post_to_platform(platform, content, schedule_time):
    return f"Scheduled post to {platform} at {schedule_time}: {content}"

# Initialize session state for posts
if 'posts' not in st.session_state:
    st.session_state.posts = pd.DataFrame(columns=['Date', 'Platform', 'Content', 'Topic', 'Likes', 'Shares'])

# Streamlit App
st.title("📅 Social Media Content Planner")
st.markdown("Plan, schedule, and analyze your social media posts with ease!")

# Sidebar for navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", ["Content Calendar", "Post Creator", "Analytics", "Export Plan"])

# Content Calendar
if section == "Content Calendar":
    st.header("Content Calendar")
    st.markdown("Drag and drop to schedule your posts.")

    # Calendar configuration
    calendar_options = {
        "editable": "true",
        "selectable": "true",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "initialView": "dayGridMonth",
    }

    # Load existing posts as calendar events
    events = []
    for _, row in st.session_state.posts.iterrows():
        events.append({
            "title": f"{row['Platform']}: {row['Topic']}",
            "start": row['Date'].strftime("%Y-%m-%dT%H:%M:%S"),
            "end": row['Date'].strftime("%Y-%m-%dT%H:%M:%S")
        })

    # Render calendar
    calendar_data = calendar(events=events, options=calendar_options)
    st.write("Use the calendar to view and schedule posts.")

# Post Creator
elif section == "Post Creator":
    st.header("Create a New Post")
    with st.form("post_form"):
        platform = st.selectbox("Platform", ["X", "Instagram", "LinkedIn"])
        topic = st.text_input("Post Topic", "Enter a topic for AI to generate content")
        content = st.text_area("Post Content", ai_advertising_writer(platform, topic))
        schedule_date = st.date_input("Schedule Date", datetime.date.today())
        schedule_time = st.time_input("Schedule Time", datetime.time(9, 0))
        submit = st.form_submit_button("Schedule Post")

        if submit:
            schedule_datetime = datetime.datetime.combine(schedule_date, schedule_time)
            # Mock API call
            post_result = post_to_platform(platform, content, schedule_datetime)
            # Add to posts DataFrame
            new_post = pd.DataFrame({
                'Date': [schedule_datetime],
                'Platform': [platform],
                'Content': [content],
                'Topic': [topic],
                'Likes': [0],  # Placeholder for analytics
                'Shares': [0]
            })
            st.session_state.posts = pd.concat([st.session_state.posts, new_post], ignore_index=True)
            st.success(post_result)

# Analytics
elif section == "Analytics":
    st.header("Post Engagement Analytics")
    if st.session_state.posts.empty:
        st.warning("No posts scheduled yet. Create a post to see analytics!")
    else:
        # Simulate engagement data
        st.session_state.posts['Likes'] = st.session_state.posts.index * 10 + 50
        st.session_state.posts['Shares'] = st.session_state.posts.index * 5 + 20

        # Plot engagement
        fig = px.bar(st.session_state.posts, x='Date', y=['Likes', 'Shares'], 
                     color='Platform', barmode='group', 
                     title="Engagement by Platform")
        st.plotly_chart(fig)

        # Display raw data
        st.subheader("Raw Engagement Data")
        st.dataframe(st.session_state.posts[['Date', 'Platform', 'Topic', 'Likes', 'Shares']])

# Export Plan
elif section == "Export Plan":
    st.header("Export Content Plan")
    if st.session_state.posts.empty:
        st.warning("No posts to export. Schedule some posts first!")
    else:
        st.subheader("Preview Content Plan")
        st.dataframe(st.session_state.posts[['Date', 'Platform', 'Content', 'Topic']])

        # Export to CSV
        csv = st.session_state.posts.to_csv(index=False)
        st.download_button(
            label="Download Content Plan as CSV",
            data=csv,
            file_name="social_media_plan.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Mock integration with Hootsuite/Buffer APIs | Powered by xAI")
