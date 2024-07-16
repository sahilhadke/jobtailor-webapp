import streamlit as st
from jobtailor import JobTailor
import tempfile

try:
    # check if the key exists in session state
    generated_resume = st.session_state.generated_resume
    generated_coverletter = st.session_state.generated_coverletter
except AttributeError:
    # otherwise set it to false
    st.session_state.generated_resume = False
    st.session_state.generated_coverletter = False


# Function to process the inputs and generate output links
def process_inputs(api_key, resume_file, job_description):
    # Example processing function - replace with your actual processing logic
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary file path
        temp_directory = f"{temp_dir}/output/"
        optional_params = {
            "write_function": placeholder_status.text,
            # "pdflatex_path": '/usr/local/texlive/2024/bin/universal-darwin/pdflatex',
            "output_dir": temp_directory,
        }
        jt = JobTailor(resume_file, job_description, api_key, optional_params)

        # Dummy links - replace with actual links generated from your processing
        resume_file_path = jt.tailored_resume_path
        coverletter_file_path = jt.tailored_coverletter_path

        return resume_file_path, coverletter_file_path

# Streamlit app
st.title("JobTailor Streamlit App")

# Input field for API key
api_key = st.text_input("Enter your API key")

# Input field for uploading file (PDF resume)
uploaded_file = st.file_uploader("Upload your PDF resume", type="pdf")

# Text input field for job description
job_description = st.text_area("Enter the job description")

placeholder_status = st.empty()

# Button to process the inputs
if st.button("Generate Personalized Resume and Cover Letter"):

    st.session_state.generated_resume = False
    st.session_state.generated_coverletter = False

    if api_key and uploaded_file and job_description:

        # clear session

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name  # Get the temporary file path

        resume_file_path, coverletter_file_path = process_inputs(api_key, temp_path, job_description)
        
        # Read the file contents
        with open(resume_file_path, 'rb') as file:
            resume_file = file.read()

        with open(coverletter_file_path, 'rb') as file:
            coverletter_file = file.read()
        
        st.success("Processing complete!")
        st.session_state.generated_resume = resume_file
        st.session_state.generated_coverletter = coverletter_file
    else:
        st.error("Please fill in all fields")

if st.session_state.generated_resume:
    st.download_button("Download tailored resume", st.session_state.generated_resume, file_name='tailored_resume.pdf')

if st.session_state.generated_coverletter:
    st.download_button("Download tailored cover letter", st.session_state.generated_coverletter, file_name='tailored_coverletter.docx')