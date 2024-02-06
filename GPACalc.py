# streamlit (frontend framework)
import streamlit as st
# pandas (library for data manipulation and analysis)
import pandas as pd

from functions import *  # Make sure functions.py is in the same directory


# Function to change the background color
def set_bg_color():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #D0E8F2;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to change the background color
set_bg_color()

# Display the logo (replace 'path_to_logo.png' with the path to your logo file or URL)
st.image('FBLA.png', width=200)  # You can adjust the width as per your requirement

# Your main app code goes here
# ...

# Define functions for calculations
# calculate_ap_weight is a function that determines whether weighthed/unweighted
def calculate_ap_weight(course_name):
    if course_name.lower().startswith('ap'):
        return 1
    if course_name.lower().startswith('dual'):
        return 1
    if course_name.lower().startswith('ib'):
        return 1
    return 0

# calculate_weight is a function that determines grade point
def calculate_weight(grade):
    try:
        grade = int(grade)
        if grade > 89:
            return 4
        if grade > 79:
            return 3
        if grade > 69:
            return 2
    except:
         print("An exception occurred")
           
    return 0

def main():

     # Use the empty method to create vertical space. Increase the range to add more space.
    for _ in range(50):  # Adjust the range to push the chat to the bottom
        st.empty()
    
    # Use columns to create a sidebar on the right for the chat feature
    col1, chat_col = st.columns([10, 21])  # Adjust the ratio to push the chat to the right

    with chat_col:

        # Display the logo (replace 'path_to_logo.png' with the path to your logo file or URL)
        st.image('Eagle.png', width=200)  # You can adjust the width as per your requirement

        st.header('Ask Eagle')
        # Provide user instructions
        st.write("""
### Eagle FAQ's:
- Q1: What is GPA ?.
- Q2: What is difference between weighted and unweighted GPA?.
- Q3: Could you provide guidance on how to raise my GPA?.
""")
   
        # The text_input now has a key ensuring it's unique
        user_input = st.text_input("Enter your Query:", key="chat_user_query")

        send_button = st.button("Send", key="send_button")
        if send_button:
            st.write("You:", user_input)
            response = get_assistant_response(user_input)
            st.write("Eagle:", response)


st.title(':blue[GPA Calculator]')



# variable = num_scores to store number of courses
# st.number_input inbuilt function within streamlit library
num_courses = st.number_input('How many courses do you want to input?', min_value=1, max_value=60, value=7, step=1)

# below are lists comma separated (lists are data structures)
course_names = []
grades = []
credits = []

default_courses = ["Enter a new course name", "AP Human Geography", "Biology", "Band","Chemistry","Physics","Spanish I","Spanish II","Spanish III","Spanish IV","German I","German II","German III","German IV","AP Precalculus","AP Statistics","Accelerated Geometry B/Advanced Algebra Honors","9th Grade Literature","10th Grade Literature"]

# Provide user instructions
st.write("""
### Instructions:
- **Numer of courses:** Enter the total number of courses (e.g., 1,2,3,4,5,6,7).
- **Course Name:** Enter the name of your course (e.g., "AP Physics", "IB Biology").
- **NOTE: Weighted courses always need to prefix with AP, Dual or IB.
- **Grade:** Enter your grade as a number (e.g., "85" for 85%).
- **Credits:** Enter the credit value of the course (e.g., "0.5" or "1").
""")

# using a for loop to iterate to your courses
for i in range(num_courses):
    
    # Let the user select between a default course or entering a new one
    course_selection = st.selectbox(f"Select or Enter Course Name {i+1}", default_courses, key=f"Course Selection {i+1}")

    # If the user chooses to enter a new course name
    if course_selection == "Enter a new course name":
        course_name = st.text_input(f"Enter Course Name {i+1}", key=f"New Course Name {i+1}")
    else:
        course_name = course_selection
        
    #course_name = st.text_input(f"Course Name {i+1}", key=f"Course Name {i+1}")
    
    grade = st.number_input(f"Grade {i+1}", key=f"Grade {i+1}")
    credit = st.number_input(f"Credit {i+1}", key=f"Credit {i+1}")
   
    course_names.append(course_name)
    grades.append(grade)
    credits.append(credit)

if st.button('Calculate GPA'):
    # Convert lists to DataFrame
    df = pd.DataFrame({
        'Course Name': course_names,
        'Grade': grades,
        'Credits': credits
    })

   
    #adding colums to the dataframe
    df['AP Weight'] = df['Course Name'].apply(calculate_ap_weight)
    df['Weight'] = df['Grade'].apply(calculate_weight)
    df['Credits'] = pd.to_numeric(df['Credits'], errors='coerce')
    df['Total GPA Weight'] = (df['AP Weight'] + df['Weight']) * df['Credits']

     #sum of credits
    total_credits = df['Credits'].sum()
    total_gpa_weight = df['Total GPA Weight'].sum()
    total_gpa_unweight = df['Weight'].sum()

    GPA = 0
    Unweighted_GPA = 0
    if total_credits != 0:
        GPA = total_gpa_weight / total_credits
        Unweighted_GPA = total_gpa_unweight / num_courses
       
       

    st.markdown("### Calculated GPA")
    st.dataframe(df.set_index(df.columns[0]))
    st.markdown(f"**Your Weighted GPA is:** `{GPA:.2f}`")
    st.markdown(f"**Your Unweighted GPA is:** `{Unweighted_GPA:.2f}`")

if __name__ == "__main__":
    main()
