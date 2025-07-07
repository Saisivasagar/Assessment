import streamlit as st
import os
import json
import re
import pandas as pd
from acat import ACAT
import glob
from crewai import Agent, Task, Crew
import plotly.express as px
import io
import zipfile

st.set_page_config(page_title="Outcome Assessment System", layout="wide")

def safe_read_excel(filepath):
    try:
        return pd.read_excel(filepath)
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        st.error(f"Error: File not found - {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        st.error(f"Error reading {filepath}: {e}")
    return None

def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Config file not found - {config_path}")
        st.error(f"Error: Config file not found - {config_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from config file: {e}")
        st.error(f"Error decoding JSON from config file: {e}")
    return {}

def read_outcomes(outcomes_file):
    df = safe_read_excel(outcomes_file)
    if df is None:
        return []
    df.columns = [col.strip() for col in df.columns]
    co_cols = [col for col in df.columns if col.lower() == 'course outcome']
    if not co_cols:
        print(f"Warning: 'Course Outcome' column not found in {outcomes_file}")
        st.warning(f"Warning: 'Course Outcome' column not found in {outcomes_file}")
        return []
    outcomes = df[co_cols[0]].dropna().tolist()
    return outcomes

def read_assignments(assignments_file, outcomes):
    df = safe_read_excel(assignments_file)
    if df is None:
        return {}
    df.columns = [str(col).strip() for col in df.columns]
    assignments = {}
    for outcome in outcomes:
        row_matches = df[df.iloc[:, 0] == outcome]
        if not row_matches.empty:
            assignment_names = row_matches.iloc[0, 1:].dropna().tolist()
            assignments[outcome] = assignment_names
    return assignments

def read_grades(grades_file, required_columns):
    df = safe_read_excel(grades_file)
    if df is None:
        return {}
    cleaned_columns = {
        col: re.sub(r"\s*\(.*?\)", "", str(col)).strip()
        for col in df.columns
    }
    df.rename(columns=cleaned_columns, inplace=True)
    if 'SIS User ID' not in df.columns:
        print(f"Error: 'SIS User ID' column missing in grades file {grades_file}")
        st.error(f"Error: 'SIS User ID' column missing in grades file {grades_file}")
        return {}
    relevant_columns = ['SIS User ID'] + [col for col in required_columns if col in df.columns]
    df = df[relevant_columns].dropna(subset=['SIS User ID'])
    df.set_index('SIS User ID', inplace=True)
    return df.to_dict(orient='index')

def load_all_cos_from_folder(folder_path):
    co_map = {}
    search_path = os.path.join(folder_path, '*.xlsx')
    files = glob.glob(search_path)
    if not files:
        print(f"Warning: No Excel files found in {folder_path}")
        st.warning(f"Warning: No Excel files found in {folder_path}")
    for filepath in files:
        course_code = os.path.splitext(os.path.basename(filepath))[0]
        df = safe_read_excel(filepath)
        if df is None:
            continue
        df.columns = [str(col).strip() for col in df.columns]
        if 'Course Outcome' in df.columns:
            cos = df['Course Outcome'].dropna().tolist()
            co_map[course_code] = cos
        else:
            print(f"Warning: 'Course Outcome' column not found in {filepath}")
            st.warning(f"Warning: 'Course Outcome' column not found in {filepath}")
    return co_map

def generate_co_po_mapping(co_map, po_count=12):
    data = []
    for course, cos in co_map.items():
        for co in cos:
            row = [f"{course}: {co}"] + [1 if i % 2 == 0 else 0 for i in range(po_count)]
            data.append(row)
    columns = ['Course Outcome'] + [f"PO{i+1}" for i in range(po_count)]
    return pd.DataFrame(data, columns=columns)

def generate_po_io_mapping(po_count=12, io_count=6):
    data = []
    for i in range(po_count):
        row = [f"PO{i+1}"] + [1 if j % 2 == 0 else 0 for j in range(io_count)]
        data.append(row)
    columns = ['Program Outcome'] + [f"IO{j+1}" for j in range(io_count)]
    return pd.DataFrame(data, columns=columns)

def generate_mappings():
    folder_path = r'course_outcomes\FA24'
    output_folder = 'mappings_output'
    os.makedirs(output_folder, exist_ok=True)
    co_map = load_all_cos_from_folder(folder_path)
    if not co_map:
        print("No Course Outcomes loaded; skipping mapping generation.")
        st.warning("No Course Outcomes loaded; skipping mapping generation.")
        return
    print(f"Loaded COs for courses: {list(co_map.keys())}")
    st.info(f"Loaded COs for courses: {list(co_map.keys())}")
    co_po_df = generate_co_po_mapping(co_map)
    po_io_df = generate_po_io_mapping()
    co_po_path = os.path.join(output_folder, 'CO_to_PO_Mapping.xlsx')
    po_io_path = os.path.join(output_folder, 'PO_to_IO_Mapping.xlsx')
    try:
        co_po_df.to_excel(co_po_path, index=False)
        po_io_df.to_excel(po_io_path, index=False)
        print(f"Generated CO-to-PO mapping at: {co_po_path}")
        st.success(f"Generated CO-to-PO mapping at: {co_po_path}")
        print(co_po_df)
        st.dataframe(co_po_df)
        print(f"Generated PO-to-IO mapping at: {po_io_path}")
        st.success(f"Generated PO-to-IO mapping at: {po_io_path}")
        print(po_io_df)
        st.dataframe(po_io_df)
    except Exception as e:
        print(f"Error writing mapping files: {e}")
        st.error(f"Error writing mapping files: {e}")

def compute_program_outcomes(config, course_name, semester, section, co_excel_file, output_folder):
    co_df = safe_read_excel(co_excel_file)
    if co_df is None:
        print(f"Error: Could not read CO Excel file {co_excel_file}")
        st.error(f"Error: Could not read CO Excel file {co_excel_file}")
        return
    if 'SIS User ID' not in co_df.columns or 'Course Outcome' not in co_df.columns:
        print(f"Error: Missing required columns in {co_excel_file}")
        st.error(f"Error: Missing required columns in {co_excel_file}")
        return
    student_co_scores = co_df.set_index('SIS User ID').filter(like='CO').dropna()
    class_co_avg = student_co_scores.mean().to_dict()
    co_po_mapping_file = config.get('output', {}).get('co_po_mapping_file')
    if not co_po_mapping_file:
        print("Error: CO-to-PO mapping file not specified in config")
        st.error("Error: CO-to-PO mapping file not specified in config")
        return
    co_po_df = safe_read_excel(co_po_mapping_file)
    if co_po_df is None:
        print(f"Error: Could not read CO-to-PO mapping file {co_po_mapping_file}")
        st.error(f"Error: Could not read CO-to-PO mapping file {co_po_mapping_file}")
        return
    if 'Course Outcome' not in co_po_df.columns:
        print(f"Error: 'Course Outcome' column missing in {co_po_mapping_file}")
        st.error(f"Error: 'Course Outcome' column missing in {co_po_mapping_file}")
        return
    po_columns = [col for col in co_po_df.columns if col.startswith('PO')]
    if not po_columns:
        print(f"Error: No PO columns found in {co_po_mapping_file}")
        st.error(f"Error: No PO columns found in {co_po_mapping_file}")
        return
    course_co_prefix = f"{course_name}: "
    co_po_df = co_po_df[co_po_df['Course Outcome'].str.startswith(course_co_prefix)]
    if co_po_df.empty:
        print(f"Warning: No CO-to-PO mappings found for course {course_name}")
        st.warning(f"Warning: No CO-to-PO mappings found for course {course_name}")
        return
    student_po_scores = {sid: {po: 0.0 for po in po_columns} for sid in student_co_scores.index}
    class_po_scores = {po: 0.0 for po in po_columns}
    co_counts = {po: 0 for po in po_columns}
    for _, row in co_po_df.iterrows():
        co = row['Course Outcome'].replace(course_co_prefix, '')
        if co not in student_co_scores.columns:
            print(f"Warning: CO {co} not found in CO scores for {course_name}")
            st.warning(f"Warning: CO {co} not found in CO scores for {course_name}")
            continue
        for po in po_columns:
            weight = row[po]
            if weight > 0:
                for sid in student_co_scores.index:
                    co_score = student_co_scores.at[sid, co]
                    if pd.notna(co_score):
                        student_po_scores[sid][po] += co_score * weight
                class_co_score = class_co_avg.get(co, 0)
                class_po_scores[po] += class_co_score * weight
                co_counts[po] += 1
    for po in po_columns:
        if co_counts[po] > 0:
            class_po_scores[po] /= co_counts[po]
            for sid in student_po_scores:
                student_po_scores[sid][po] /= co_counts[po]
    student_po_df = pd.DataFrame(student_po_scores).T.reset_index().rename(columns={'index': 'SIS User ID'})
    class_po_df = pd.DataFrame([class_po_scores], index=['Class Average'])
    output_df = pd.concat([student_po_df, class_po_df.reset_index().rename(columns={'index': 'SIS User ID'})])
    po_output_file = os.path.join(
        output_folder,
        f"{course_name}_{semester}_{section}_po_outcomes.xlsx"
    )
    try:
        output_df.to_excel(po_output_file, index=False)
        print(f"Saved PO outcomes to {po_output_file}")
        st.success(f"Saved PO outcomes to {po_output_file}")
    except Exception as e:
        print(f"Error saving PO outcomes to {po_output_file}: {e}")
        st.error(f"Error saving PO outcomes to {po_output_file}: {e}")
    return po_output_file

def compute_institutional_outcomes(config, course_name, semester, section, po_excel_file, output_folder):
    po_df = safe_read_excel(po_excel_file)
    if po_df is None:
        print(f"Error: Could not read PO Excel file {po_excel_file}")
        st.error(f"Error: Could not read PO Excel file {po_excel_file}")
        return
    if 'SIS User ID' not in po_df.columns:
        print(f"Error: Missing 'SIS User ID' column in {po_excel_file}")
        st.error(f"Error: Missing 'SIS User ID' column in {po_excel_file}")
        return
    student_po_scores = po_df[po_df['SIS User ID'] != 'Class Average'].set_index('SIS User ID').filter(like='PO').dropna()
    class_po_avg = po_df[po_df['SIS User ID'] == 'Class Average'].filter(like='PO').iloc[0].to_dict()
    po_io_mapping_file = config.get('output', {}).get('po_io_mapping_file')
    if not po_io_mapping_file:
        print("Error: PO-to-IO mapping file not specified in config")
        st.error("Error: PO-to-IO mapping file not specified in config")
        return
    po_io_df = safe_read_excel(po_io_mapping_file)
    if po_io_df is None:
        print(f"Error: Could not read PO-to-IO mapping file {po_io_mapping_file}")
        st.error(f"Error: Could not read PO-to-IO mapping file {po_io_mapping_file}")
        return
    if 'Program Outcome' not in po_io_df.columns:
        print(f"Error: 'Program Outcome' column missing in {po_io_mapping_file}")
        st.error(f"Error: 'Program Outcome' column missing in {po_io_mapping_file}")
        return
    io_columns = [col for col in po_io_df.columns if col.startswith('IO')]
    if not io_columns:
        print(f"Error: No IO columns found in {po_io_mapping_file}")
        st.error(f"Error: No IO columns found in {po_io_mapping_file}")
        return
    student_io_scores = {sid: {io: 0.0 for io in io_columns} for sid in student_po_scores.index}
    class_io_scores = {io: 0.0 for io in io_columns}
    po_counts = {io: 0 for io in io_columns}
    for _, row in po_io_df.iterrows():
        po = row['Program Outcome']
        if po not in student_po_scores.columns:
            print(f"Warning: PO {po} not found in PO scores for {course_name}")
            st.warning(f"Warning: PO {po} not found in PO scores for {course_name}")
            continue
        for io in io_columns:
            weight = row[io]
            if weight > 0:
                for sid in student_po_scores.index:
                    po_score = student_po_scores.at[sid, po]
                    if pd.notna(po_score):
                        student_io_scores[sid][io] += po_score * weight
                class_po_score = class_po_avg.get(po, 0)
                class_io_scores[io] += class_po_score * weight
                po_counts[io] += 1
    for io in io_columns:
        if po_counts[io] > 0:
            class_io_scores[io] /= po_counts[io]
            for sid in student_io_scores:
                student_io_scores[sid][io] /= po_counts[io]
    student_io_df = pd.DataFrame(student_io_scores).T.reset_index().rename(columns={'index': 'SIS User ID'})
    class_io_df = pd.DataFrame([class_io_scores], index=['Class Average'])
    output_df = pd.concat([student_io_df, class_io_df.reset_index().rename(columns={'index': 'SIS User ID'})])
    io_output_file = os.path.join(
        output_folder,
        f"{course_name}_{semester}_{section}_io_outcomes.xlsx"
    )
    try:
        output_df.to_excel(io_output_file, index=False)
        print(f"Saved IO outcomes to {io_output_file}")
        st.success(f"Saved IO outcomes to {io_output_file}")
    except Exception as e:
        print(f"Error saving IO outcomes to {io_output_file}: {e}")
        st.error(f"Error saving IO outcomes to {io_output_file}: {e}")
    return io_output_file

def compute_student_assessments(config, course_name, semester, section, co_excel_file, po_excel_file, io_excel_file, output_folder):
    co_df = safe_read_excel(co_excel_file)
    po_df = safe_read_excel(po_excel_file)
    io_df = safe_read_excel(io_excel_file)
    if co_df is None or po_df is None or io_df is None:
        print(f"Error: Could not read input files for student assessments in {course_name}_{semester}_{section}")
        st.error(f"Error: Could not read input files for student assessments in {course_name}_{semester}_{section}")
        return
    student_co_scores = co_df[co_df['SIS User ID'] != 'Class Average'].set_index('SIS User ID').filter(like='CO')
    student_po_scores = po_df[po_df['SIS User ID'] != 'Class Average'].set_index('SIS User ID').filter(like='PO')
    student_io_scores = io_df[io_df['SIS User ID'] != 'Class Average'].set_index('SIS User ID').filter(like='IO')
    student_ids = student_co_scores.index.intersection(student_po_scores.index).intersection(student_io_scores.index)
    if student_ids.empty:
        print(f"Error: No common student IDs found for {course_name}_{semester}_{section}")
        st.error(f"Error: No common student IDs found for {course_name}_{semester}_{section}")
        return
    course_outcome_agent = Agent(
        role='Course Outcome Assessment Agent',
        goal='Analyze student performance at the course outcome level and identify strengths and weaknesses.',
        backstory='Expert in evaluating course-level student performance data.'
    )
    program_outcome_agent = Agent(
        role='Program Outcome Assessment Agent',
        goal='Assess student capabilities at the program outcome level.',
        backstory='Specialist in program-level educational assessment.'
    )
    institutional_outcome_agent = Agent(
        role='Institutional Outcome Assessment Agent',
        goal='Evaluate student attainment of institutional goals based on institutional outcome data.',
        backstory='Experienced in institutional-level outcome analysis with a focus on broad educational goals.'
    )
    overall_assessment_agent = Agent(
        role='Student Learning Overall Assessment Agent',
        goal='Combine CO, PO, and IO data to provide comprehensive student capability insights.',
        backstory='Expert in synthesizing multi-level educational data for holistic student assessment.'
    )
    assessments = []
    for sid in student_ids:
        co_data = student_co_scores.loc[sid].to_dict()
        po_data = student_po_scores.loc[sid].to_dict()
        io_data = student_io_scores.loc[sid].to_dict()
        co_task = Task(
            description=f"Analyze course outcome data for student {sid}: {co_data}",
            agent=course_outcome_agent,
            expected_output=f"Textual summary of student {sid}'s strengths and weaknesses in course outcomes."
        )
        po_task = Task(
            description=f"Analyze program outcome data for student {sid}: {po_data}",
            agent=program_outcome_agent,
            expected_output=f"Textual summary of student {sid}'s program-level capabilities."
        )
        io_task = Task(
            description=f"Analyze institutional outcome data for student {sid}: {io_data}",
            agent=institutional_outcome_agent,
            expected_output=f"Textual summary of student {sid}'s attainment of institutional goals."
        )
        overall_task = Task(
            description=f"Combine CO ({co_data}), PO ({po_data}), and IO ({io_data}) data for student {sid} to provide overall capability insights.",
            agent=overall_assessment_agent,
            expected_output=f"Comprehensive textual summary of student {sid}'s overall learning capabilities."
        )
        crew = Crew(
            agents=[course_outcome_agent, program_outcome_agent, institutional_outcome_agent, overall_assessment_agent],
            tasks=[co_task, po_task, io_task, overall_task],
            verbose=False
        )
        results = crew.kickoff()
        assessment_summary = {
            'SIS User ID': sid,
            'Course Outcome Assessment': results[0] if results else 'No assessment generated',
            'Program Outcome Assessment': results[1] if len(results) > 1 else 'No assessment generated',
            'Institutional Outcome Assessment': results[2] if len(results) > 2 else 'No assessment generated',
            'Overall Assessment': results[3] if len(results) > 3 else 'No assessment generated'
        }
        assessments.append(assessment_summary)
    assessment_df = pd.DataFrame(assessments)
    output_file = os.path.join(
        output_folder,
        f"{course_name}_{semester}_{section}_student_assessment.xlsx"
    )
    try:
        assessment_df.to_excel(output_file, index=False)
        print(f"Saved student assessments to {output_file}")
        st.success(f"Saved student assessments to {output_file}")
    except Exception as e:
        print(f"Error saving student assessments to {output_file}: {e}")
        st.error(f"Error saving student assessments to {output_file}: {e}")

def create_zip_file(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            if os.path.exists(file):
                zip_file.write(file, os.path.basename(file))
    buffer.seek(0)
    return buffer

def streamlit_app():
    st.title("Program and Institutional Outcomes Assessment System")
    with st.container():
        st.subheader("Upload Configuration and Input Files")
        config_file = st.file_uploader("Upload acat_config.json", type=["json"])
        uploaded_files = st.file_uploader("Upload Excel Files (outcomes, assignments, grades)", type=["xlsx"], accept_multiple_files=True)
        st.subheader("Processing Log")
        log_container = st.container()
        if st.button("Process Files"):
            if config_file and uploaded_files:
                with st.spinner("Processing files..."):
                    config_path = "temp_config.json"
                    with open(config_path, "wb") as f:
                        f.write(config_file.getvalue())
                    config = load_config(config_path)
                    if not config or 'courses' not in config:
                        log_container.error("Invalid or empty configuration file.")
                        return
                    excel_output_folder = config.get('output', {}).get('excel_folder', 'output')
                    os.makedirs(excel_output_folder, exist_ok=True)
                    for course in config['courses']:
                        course_name = course.get('course_name')
                        semester = course.get('semester')
                        outcomes_file = course.get('outcomes_file')
                        if not course_name or not semester or not outcomes_file:
                            log_container.warning(f"Skipping course due to missing info: {course}")
                            continue
                        outcomes = read_outcomes(outcomes_file)
                        if not outcomes:
                            log_container.warning(f"No outcomes found for course {course_name}, skipping.")
                            continue
                        log_container.info(f"Processing course: {course_name}")
                        log_container.write(f"Outcomes: {outcomes}")
                        for section_data in course.get('sections', []):
                            section = section_data.get('section')
                            if not section:
                                log_container.warning("Skipping section with missing section name.")
                                continue
                            log_container.info(f"Section: {section}")
                            assignments_mapping = read_assignments(section_data.get('assignments_file', ''), outcomes)
                            log_container.write(f"Assignments Mappings: {assignments_mapping}")
                            final_outcomes = {outcome: assignments_mapping.get(outcome, []) for outcome in outcomes}
                            log_container.write(f"Final Outcomes: {final_outcomes}")
                            required_columns = set(assignment for criteria in final_outcomes.values() for assignment in criteria)
                            grades_file = section_data.get('grades_file')
                            if not grades_file:
                                log_container.warning(f"Grades file missing for section {section} of course {course_name}, skipping.")
                                continue
                            student_data = read_grades(grades_file, required_columns=required_columns)
                            if not student_data:
                                log_container.warning(f"No student data found for section {section} of course {course_name}, skipping.")
                                continue
                            log_container.write(f"Student Data: {student_data}")
                            try:
                                acat = ACAT(course_name, semester, section, final_outcomes, student_data)
                                student_outcomes = acat.compute_course_outcomes()
                                acat.summarize_course_outcomes(student_outcomes)
                                excel_output = os.path.join(excel_output_folder, f"{course_name}_{semester}_{section}_outcomes.xlsx")
                                db_output = os.path.join(config.get('output', {}).get('database_folder', 'db'), f"{course_name}_{semester}_{section}_outcomes.db")
                                os.makedirs(os.path.dirname(db_output), exist_ok=True)
                                acat.save_to_excel(student_outcomes, excel_output)
                                acat.save_to_sqlite(db_output, student_outcomes)
                                po_output_file = compute_program_outcomes(config, course_name, semester, section, excel_output, excel_output_folder)
                                if po_output_file:
                                    io_output_file = compute_institutional_outcomes(config, course_name, semester, section, po_output_file, excel_output_folder)
                                    if io_output_file:
                                        compute_student_assessments(config, course_name, semester, section, excel_output, po_output_file, io_output_file, excel_output_folder)
                                log_container.success(f"Processed {course_name} {semester} {section}")
                            except Exception as e:
                                log_container.error(f"Error processing {course_name} section {section}: {e}")
            else:
                log_container.error("Please upload both config file and Excel files.")
    output_folder = config.get('output', {}).get('excel_folder', 'output') if 'config' in locals() else 'output'
    excel_files = glob.glob(os.path.join(output_folder, "*.xlsx"))
    if excel_files:
        st.subheader("Download All Output Files")
        courses = list(set(f.split('_')[0] for f in excel_files))
        course_filter = st.selectbox("Select Course", ["All"] + courses, key="course_filter")
        sections = list(set(f.split('_')[2].replace('_outcomes.xlsx', '').replace('_student_assessment.xlsx', '') for f in excel_files if course_filter == "All" or f.startswith(course_filter)))
        section_filter = st.selectbox("Select Section", ["All"] + sections, key="section_filter")
        filtered_files = [f for f in excel_files if (course_filter == "All" or f.startswith(course_filter)) and (section_filter == "All" or section_filter in f)]
        if filtered_files:
            zip_buffer = create_zip_file(filtered_files)
            st.download_button(
                label="Download All Files as ZIP",
                data=zip_buffer,
                file_name="output_files.zip",
                mime="application/zip"
            )
        tabs = st.tabs(["Course Outcomes", "Program Outcomes", "Institutional Outcomes", "Student Assessments"])
        for i, tab_name in enumerate(["co", "po", "io", "student_assessment"]):
            with tabs[i]:
                filtered_files = [f for f in excel_files if tab_name in f.lower() and (course_filter == "All" or f.startswith(course_filter)) and (section_filter == "All" or section_filter in f)]
                if filtered_files:
                    for file in filtered_files:
                        df = safe_read_excel(file)
                        if df is not None:
                            st.subheader(f"Data from {os.path.basename(file)}")
                            st.dataframe(df)
                            if tab_name != "student_assessment":
                                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                                if not numeric_cols.empty:
                                    avg_data = df[df['SIS User ID'] == 'Class Average'][numeric_cols].melt()
                                    fig = px.bar(avg_data, x="variable", y="value", title=f"{tab_name.upper()} Averages")
                                    st.plotly_chart(fig)
                                    dist_data = df[numeric_cols].melt()
                                    fig_dist = px.histogram(dist_data, x="value", nbins=20, title=f"{tab_name.upper()} Score Distribution")
                                    st.plotly_chart(fig_dist)
                                    box_data = df[numeric_cols].melt()
                                    fig_box = px.box(box_data, x="variable", y="value", title=f"{tab_name.upper()} Score Distribution (Box Plot)")
                                    st.plotly_chart(fig_box)
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                                df.to_excel(writer, index=False)
                            st.download_button(
                                label=f"Download {os.path.basename(file)}",
                                data=buffer,
                                file_name=os.path.basename(file),
                                mime="application/vnd.ms-excel"
                            )
                else:
                    st.write("No data available for this tab.")
    else:
        st.write("No output files found. Please process files first.")

def main():
    generate_mappings()
    streamlit_app()

if __name__ == "__main__":
    main()
