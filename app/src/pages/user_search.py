import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def fetch_user_data(UserID):
    """
    Fetch user data from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        response = requests.get("http://api:4000/aa/users/view/" + str(UserID))
        response.raise_for_status() 
        users = response.json() 
        user_data = pd.DataFrame(users, columns=["UserID", 'Name', "Occupation", "Location,", "Age", "Bio", 'Industry', 'NUCollege'])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch  data from the API: {e}")
        return None

def fetch_user_data_industry(industry):
    """
    Fetch user data from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        response = requests.get("http://api:4000/aa/users/by-industry", json={'industry':industry})
        response.raise_for_status() 
        users = response.json() 
        user_data = pd.DataFrame(users, columns=["UserID", "Name", "Bio", "IndustryName", "NUCollege"])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch  data from the API: {e}")
        return None

def fetch_user_data_skills(soft_skills, tech_skills):
    """
    Fetch user data from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        skills_data = {'soft_skills' : soft_skills, 'tech_skills' : tech_skills}
        response = requests.get("http://api:4000/aa/users/by-skills", json=skills_data)
        response.raise_for_status() 
        users = response.json() 
        user_data = pd.DataFrame(users, columns=["UserID", "Name", "Bio", "IndustryName", "College"])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch  data from the API: {e}")
        return None


def main():
    """
    Main function to render the Streamlit app.
    """
    st.title('Users')

    st.write('search by users')
    with st.form("search_user_form"):
    
        UserID = int(st.number_input("UserID", step=1))
    
        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for User")
        
        # Validate all fields are filled when form is submitted
        if submit_button:
            if not UserID:
                st.error("Please enter a UserID")
            else:
                # Fetch user data from the API
                user_data = fetch_user_data(UserID)
            
                # show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available.")

    st.write('Search by Industry')
    with st.form('search_user_industry_form'):
        industry = st.text_area('Industry')

        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for User")

        if submit_button:
            if not industry:
                st.error("Please enter an Industry")
            else:
                st.write(f'searching for users in industry: {industry}')
                user_data = fetch_user_data_industry(industry)
                # show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available.")
    
    st.write('Search by Skills')
    with st.form('search_user_skills_form'):

        soft_skills = st.text_area('Soft Skills')
        tech_skills = st.text_area('Technical Skills')

        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for User")

        if submit_button:
            if not soft_skills or not tech_skills:
                st.error("Please enter skills")

            else:
                user_data = fetch_user_data_skills(soft_skills, tech_skills)
                # show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available.")


main()
