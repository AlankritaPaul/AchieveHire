"""
Page-wise UI flow for 'Create Resume' in AscendCareer Resume Guide.
Each selection has its own dedicated page.
Bottom navigation consistently provides:
- Left side below: Back clickable option
- Right side below: Next clickable option
"""

import streamlit as st
import streamlit.components.v1 as components
import base64
from typing import Dict, Any, List
from modules.constants import SUGGESTED_JOB_ROLES, SUGGESTED_COMPANIES
from modules.resume_guide.builder import ResumeBuilderModel, DEFAULT_DECLARATION
from modules.resume_guide.builder_templates import (
    TEMPLATES_INFO,
    render_resume_html,
    export_builder_resume_to_pdf
)
from modules.resume_guide.exporter import export_resume_to_docx

def init_builder_state():
    """Ensure all required builder session keys exist."""
    if "builder_step" not in st.session_state:
        st.session_state.builder_step = 1
    if "builder_data" not in st.session_state:
        model = ResumeBuilderModel()
        st.session_state.builder_data = model.data
    if "builder_custom_sections" not in st.session_state:
        st.session_state.builder_custom_sections = []
    if "builder_photo_b64" not in st.session_state:
        st.session_state.builder_photo_b64 = ""
    if "builder_sig_b64" not in st.session_state:
        st.session_state.builder_sig_b64 = ""
    if (
        "education_entries" not in st.session_state.builder_data
        or not st.session_state.builder_data.get("education_entries")
        or "status" not in st.session_state.builder_data["education_entries"][0]
    ):
        st.session_state.builder_data["education_entries"] = [
            {
                "degree": "",
                "field_of_study": "",
                "institution": "",
                "board_univ": "",
                "location": "",
                "status": "Completed",
                "start_year": "",
                "end_year": "",
                "expected_grad_year": "",
                "cgpa": "",
                "percentage": "",
                "grade": ""
            }
        ]
    if "qualification_entries" not in st.session_state.builder_data or not isinstance(st.session_state.builder_data.get("qualification_entries"), list):
        st.session_state.builder_data["qualification_entries"] = []
    if "builder_accepted" not in st.session_state:
        st.session_state.builder_accepted = False

def render_create_resume_flow():
    """Render the step-by-step page-wise flow for creating a new resume."""
    init_builder_state()
    data = st.session_state.builder_data

    steps_labels = [
        "1. Select Job Role",
        "2. Select Company",
        "3. Job Description",
        "4. Personal & Photo",
        "5. Education and Qualifications",
        "6. Skills",
        "7. Work Experience",
        "8. Projects",
        "9. Additional Information",
        "10. Declaration & Signature",
        "11. Template Selection",
        "12. Resume Preview",
        "13. Final Resume & Download"
    ]

    current_step = st.session_state.builder_step
    
    st.markdown("""
        <div style="background-color: #EDF2F7; border-radius: 8px; padding: 10px 16px; margin-bottom: 20px;">
            <span style="font-size: 0.95rem; color: #2D3748; font-weight: 600;">Create Resume — Step %d of 13: %s</span>
        </div>
    """ % (current_step, steps_labels[current_step - 1]), unsafe_allow_html=True)

    # -------------------------------------------------------------
    # STEP 1: SELECT JOB ROLE
    # -------------------------------------------------------------
    if current_step == 1:
        st.markdown("### Select Job Role")
        st.caption("Provide the job role for this resume.")

        role_choice = st.radio(
            "Select option:",
            options=["Select a Job Role", "Write Your Job Role"],
            key="builder_role_mode"
        )
        if role_choice == "Select a Job Role":
            selected_role = st.selectbox(
                "Suggested Job Roles (Searchable):",
                options=SUGGESTED_JOB_ROLES,
                key="builder_suggested_role"
            )
            data["job_role"] = selected_role
        else:
            custom_role = st.text_input(
                "Write Your Job Role:",
                value=data.get("job_role", ""),
                placeholder="e.g. Distributed Systems Engineer",
                key="builder_custom_role"
            )
            data["job_role"] = custom_role.strip() if custom_role.strip() else "Software Developer"

        st.info(f"Selected Job Role: **{data['job_role']}**")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_1", use_container_width=True):
                st.session_state.resume_guide_mode = None
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_1", use_container_width=True):
                st.session_state.builder_step = 2
                st.rerun()

    # -------------------------------------------------------------
    # STEP 2: SELECT COMPANY
    # -------------------------------------------------------------
    elif current_step == 2:
        st.markdown("### Select Company")
        st.caption("Provide the company for this resume.")

        comp_choice = st.radio(
            "Select option:",
            options=["Select a Company", "Write Your Company"],
            key="builder_comp_mode"
        )
        if comp_choice == "Select a Company":
            selected_comp = st.selectbox(
                "Suggested Companies / Types (Searchable):",
                options=SUGGESTED_COMPANIES,
                key="builder_suggested_comp"
            )
            data["company"] = selected_comp
        else:
            custom_comp = st.text_input(
                "Write Your Company:",
                value=data.get("company", ""),
                placeholder="e.g. Google, Microsoft, Local Tech Firm",
                key="builder_custom_comp"
            )
            data["company"] = custom_comp.strip() if custom_comp.strip() else "General Tech Company"

        st.info(f"Selected Company: **{data['company']}**")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_2", use_container_width=True):
                st.session_state.builder_step = 1
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_2", use_container_width=True):
                st.session_state.builder_step = 3
                st.rerun()

    # -------------------------------------------------------------
    # STEP 3: JOB DESCRIPTION
    # -------------------------------------------------------------
    elif current_step == 3:
        st.markdown("### Job Description (Optional / Recommended)")
        st.caption("Provide a specific job description if you have one. If provided, the resume will be tailored to it. If not provided, it will be tailored according to the selected job role and company.")

        jd_val = st.text_area(
            "Job Description (Optional):",
            value=data.get("job_description", ""),
            height=160,
            placeholder="Paste job posting details here if available...",
            key="builder_jd_input"
        )
        data["job_description"] = jd_val.strip()

        if data["job_description"]:
            st.success("Job Description provided. The resume will be tailored to reflect requirements from this job description.")
        else:
            st.info(f"No Job Description provided. The resume will be tailored according to the selected job role ({data.get('job_role', 'Software Developer')}) and company ({data.get('company', 'General Tech Company')}).")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_3", use_container_width=True):
                st.session_state.builder_step = 2
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_3", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()

    # -------------------------------------------------------------
    # STEP 4: PERSONAL DETAILS & PHOTO
    # -------------------------------------------------------------
    elif current_step == 4:
        st.markdown("### Personal Details & Photo")
        st.caption("Provide your contact information. Any field can be skipped if you do not want to provide it.")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            data["full_name"] = st.text_input("Full Name:", value=data.get("full_name", ""), placeholder="e.g. Alex Morgan")
            data["email"] = st.text_input("Email Address:", value=data.get("email", ""), placeholder="e.g. alex.morgan@email.com")
            data["phone"] = st.text_input("Phone Number:", value=data.get("phone", ""), placeholder="e.g. +1 (555) 019-2834")
            data["location"] = st.text_input("Location / City, Country:", value=data.get("location", ""), placeholder="e.g. San Francisco, CA")

        with col_p2:
            st.markdown("#### Photo Section (Optional)")
            st.caption("Choose whether to upload a digital photo, keep a designated space for a physical photo, or omit photo entirely.")
            
            photo_options = [
                "Upload digital photo (JPG or PNG from your device)",
                "Keep space for passport-size photo (To paste a physical photo later)",
                "Do not include a photo or photo space"
            ]
            current_photo_mode = data.get("photo_mode", "none")
            initial_idx = 0 if current_photo_mode == "upload" else (1 if current_photo_mode == "box" else 2)
            
            selected_photo_option = st.radio(
                "Photo Preference:",
                options=photo_options,
                index=initial_idx,
                key="builder_photo_mode_radio"
            )

            if selected_photo_option == photo_options[0]:
                data["photo_mode"] = "upload"
                photo_file = st.file_uploader(
                    "Upload Photograph (JPG, JPEG, PNG):",
                    type=["png", "jpg", "jpeg"],
                    key="builder_photo_upload"
                )
                if photo_file:
                    b64 = base64.b64encode(photo_file.read()).decode("utf-8")
                    st.session_state.builder_photo_b64 = b64
                    data["photo_b64"] = b64
                    st.success("Photo uploaded successfully.")

                if st.session_state.get("builder_photo_b64"):
                    st.image(f"data:image/jpeg;base64,{st.session_state.builder_photo_b64}", width=100)
                    if st.button("🗑️ Remove Photo", key="btn_remove_photo"):
                        st.session_state.builder_photo_b64 = ""
                        data["photo_b64"] = ""
                        st.rerun()

            elif selected_photo_option == photo_options[1]:
                data["photo_mode"] = "box"
                data["photo_b64"] = ""
                st.session_state.builder_photo_b64 = ""
                st.markdown(
                    """
                    <div style="border: 2px dashed #718096; background: #F8FAFC; border-radius: 6px; padding: 14px 18px; text-align: center; max-width: 160px; margin: 10px 0;">
                        <div style="font-size: 26px; color: #4A5568;">📷</div>
                        <div style="font-size: 11px; font-weight: 600; color: #2D3748; margin-top: 4px;">Affix Passport Size Photo</div>
                        <div style="font-size: 9px; color: #718096; margin-top: 2px;">(Standard 3.5cm x 4.5cm)</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.info("A designated passport-size photo box will be placed on your resume so you can affix a printed physical photo after printing.")

            else:
                data["photo_mode"] = "none"
                data["photo_b64"] = ""
                st.session_state.builder_photo_b64 = ""
                st.caption("No photo or photo box will be added to your resume.")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_4", use_container_width=True):
                st.session_state.builder_step = 3
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_4", use_container_width=True):
                st.session_state.builder_step = 5
                st.rerun()

    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # STEP 5: EDUCATION AND QUALIFICATIONS
    # -------------------------------------------------------------
    elif current_step == 5:
        col_e_head, col_e_btn = st.columns([3, 1])
        with col_e_head:
            st.markdown("### Education and Qualifications")
            st.caption("Provide your formal education and any additional professional qualifications.")
        with col_e_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_edu_top", use_container_width=True, help="Standardize degrees, specializations, and qualifications professionally without altering facts"):
                if data.get("education_entries"):
                    data["education_entries"] = ResumeBuilderModel.enhance_education_entries(data["education_entries"])
                if data.get("qualification_entries"):
                    data["qualification_entries"] = ResumeBuilderModel.enhance_qualification_entries(data["qualification_entries"])
                compiled = ResumeBuilderModel.compile_education_and_qualifications(
                    data.get("education_entries", []),
                    data.get("qualification_entries", [])
                )
                if compiled:
                    data["education"] = compiled
                st.success("✅ Enhanced all education and qualifications with professional keywords!")
                st.rerun()

        # Subsection 1: Education
        st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid #E2E8F0;'/>", unsafe_allow_html=True)
        st.markdown("#### Education")
        st.caption("Add your formal educational qualifications. Each entry supports independent status, dates, and academic details.")

        if "education_entries" not in data or not isinstance(data.get("education_entries"), list) or not data["education_entries"]:
            data["education_entries"] = [
                {
                    "degree": "",
                    "field_of_study": "",
                    "institution": "",
                    "board_univ": "",
                    "location": "",
                    "status": "Completed",
                    "start_year": "",
                    "end_year": "",
                    "expected_grad_year": "",
                    "cgpa": "",
                    "percentage": "",
                    "grade": ""
                }
            ]

        del_edu_indices = []
        for idx, entry in enumerate(data["education_entries"]):
            entry_title = entry.get("degree", "").strip() or "Education Entry"
            with st.container():
                col_eh, col_ed = st.columns([5, 1])
                with col_eh:
                    st.markdown(f"**🎓 {entry_title}**")
                with col_ed:
                    if len(data["education_entries"]) > 1:
                        if st.button("🗑️ Remove", key=f"btn_del_edu_{idx}"):
                            del_edu_indices.append(idx)

                c1, c2 = st.columns(2)
                with c1:
                    entry["degree"] = st.text_input(
                        "Degree or Qualification:",
                        value=entry.get("degree", ""),
                        placeholder="e.g. Bachelor of Technology / Class XII",
                        key=f"edu_deg_{idx}"
                    )
                    entry["field_of_study"] = st.text_input(
                        "Field of Study or Specialization:",
                        value=entry.get("field_of_study", entry.get("stream", "")),
                        placeholder="e.g. Computer Science & Engineering / Science",
                        key=f"edu_field_{idx}"
                    )
                    entry["institution"] = st.text_input(
                        "Institution Name:",
                        value=entry.get("institution", ""),
                        placeholder="e.g. Delhi Technological University / High School",
                        key=f"edu_inst_{idx}"
                    )
                with c2:
                    entry["board_univ"] = st.text_input(
                        "University or Board (Optional):",
                        value=entry.get("board_univ", ""),
                        placeholder="e.g. CBSE / State Board / University Name",
                        key=f"edu_board_{idx}"
                    )
                    entry["location"] = st.text_input(
                        "Location (Optional):",
                        value=entry.get("location", ""),
                        placeholder="e.g. New Delhi, India",
                        key=f"edu_loc_{idx}"
                    )
                    
                    status_val = entry.get("status", "Completed")
                    status_idx = 0 if status_val == "Completed" else 1
                    entry["status"] = st.radio(
                        "Status:",
                        options=["Completed", "Currently Pursuing"],
                        index=status_idx,
                        key=f"edu_status_{idx}",
                        horizontal=True
                    )

                # Dynamic Date Fields based on Status
                cd1, cd2 = st.columns(2)
                with cd1:
                    entry["start_year"] = st.text_input(
                        "Start Year:",
                        value=entry.get("start_year", ""),
                        placeholder="e.g. 2020",
                        key=f"edu_syr_{idx}"
                    )
                with cd2:
                    if entry["status"] == "Completed":
                        entry["end_year"] = st.text_input(
                            "End Year:",
                            value=entry.get("end_year", ""),
                            placeholder="e.g. 2024",
                            key=f"edu_eyr_{idx}"
                        )
                        entry["expected_grad_year"] = ""
                    else:  # Currently Pursuing
                        entry["expected_grad_year"] = st.text_input(
                            "Expected Graduation Year:",
                            value=entry.get("expected_grad_year", ""),
                            placeholder="e.g. 2026",
                            key=f"edu_expyr_{idx}"
                        )
                        entry["end_year"] = ""

                # Academic Results
                st.markdown("<span style='font-size: 0.85rem; font-weight: 600; color: #4A5568;'>Academic Results:</span>", unsafe_allow_html=True)
                ca1, ca2, ca3 = st.columns(3)
                with ca1:
                    entry["cgpa"] = st.text_input(
                        "CGPA (if applicable):",
                        value=entry.get("cgpa", ""),
                        placeholder="e.g. 8.7",
                        key=f"edu_cgpa_{idx}"
                    )
                with ca2:
                    entry["percentage"] = st.text_input(
                        "Percentage (Optional):",
                        value=entry.get("percentage", ""),
                        placeholder="e.g. 88.5%",
                        key=f"edu_pct_{idx}"
                    )
                with ca3:
                    entry["grade"] = st.text_input(
                        "Grade (Optional):",
                        value=entry.get("grade", ""),
                        placeholder="e.g. A+",
                        key=f"edu_grd_{idx}"
                    )

                st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px dashed #E2E8F0;'/>", unsafe_allow_html=True)

        if del_edu_indices:
            for di in sorted(del_edu_indices, reverse=True):
                data["education_entries"].pop(di)
            st.rerun()

        if st.button("➕ Add Another Education", key="btn_add_another_edu"):
            data["education_entries"].append({
                "degree": "",
                "field_of_study": "",
                "institution": "",
                "board_univ": "",
                "location": "",
                "status": "Completed",
                "start_year": "",
                "end_year": "",
                "expected_grad_year": "",
                "cgpa": "",
                "percentage": "",
                "grade": ""
            })
            st.rerun()

        # Subsection 2: Qualifications (Optional)
        st.markdown("<hr style='margin: 22px 0; border: none; border-top: 2px solid #CBD5E0;'/>", unsafe_allow_html=True)
        st.markdown("#### Qualifications (Optional)")
        st.caption("Include any additional relevant qualifications, diplomas, or credentials separate from your formal education entries.")

        if "qualification_entries" not in data or not isinstance(data.get("qualification_entries"), list):
            data["qualification_entries"] = []

        del_qual_indices = []
        if data["qualification_entries"]:
            for q_idx, qual in enumerate(data["qualification_entries"]):
                q_title = qual.get("title", "").strip() or "Qualification Entry"
                with st.container():
                    col_qh, col_qd = st.columns([5, 1])
                    with col_qh:
                        st.markdown(f"**📜 {q_title}**")
                    with col_qd:
                        if st.button("🗑️ Remove", key=f"btn_del_qual_{q_idx}"):
                            del_qual_indices.append(q_idx)

                    cq1, cq2 = st.columns(2)
                    with cq1:
                        qual["title"] = st.text_input(
                            "Qualification Title:",
                            value=qual.get("title", ""),
                            placeholder="e.g. Certified Cloud Practitioner / Diploma in Project Management",
                            key=f"qual_title_{q_idx}"
                        )
                        qual["organization"] = st.text_input(
                            "Issuing Body / Organization:",
                            value=qual.get("organization", ""),
                            placeholder="e.g. AWS / PMI / University Name",
                            key=f"qual_org_{q_idx}"
                        )
                    with cq2:
                        qual["year"] = st.text_input(
                            "Year / Period:",
                            value=qual.get("year", ""),
                            placeholder="e.g. 2023",
                            key=f"qual_yr_{q_idx}"
                        )
                        qual["details"] = st.text_input(
                            "Details / Score (Optional):",
                            value=qual.get("details", ""),
                            placeholder="e.g. Credential ID: 12345 / Score: 92%",
                            key=f"qual_det_{q_idx}"
                        )
                    st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px dashed #CBD5E0;'/>", unsafe_allow_html=True)

        if del_qual_indices:
            for dqi in sorted(del_qual_indices, reverse=True):
                data["qualification_entries"].pop(dqi)
            st.rerun()

        if st.button("➕ Add Qualification", key="btn_add_qual"):
            data["qualification_entries"].append({
                "title": "",
                "organization": "",
                "year": "",
                "details": ""
            })
            st.rerun()

        # Compile into realistic preview
        compiled_edu = ResumeBuilderModel.compile_education_and_qualifications(
            data.get("education_entries", []),
            data.get("qualification_entries", [])
        )
        if compiled_edu and (not data.get("education") or data.get("education") != compiled_edu):
            data["education"] = compiled_edu

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📄 Formatted Education and Qualifications Preview (As it will appear on your resume):")
        data["education"] = st.text_area(
            "Live Compiled Education and Qualifications Preview (Editable):",
            value=data.get("education", ""),
            height=160,
            key="builder_edu_preview_input"
        )

        st.markdown(
            """
            <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; color: #166534; margin-top: 8px;">
                <strong>💡 Realistic Resume Structure:</strong> Information is organized under the main heading 'Education and Qualifications' with separate subsections for Education and Qualifications. Status-based dates, CGPA, and optional grades are displayed only when provided. No internal form labels appear on your resume.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_5", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_5", use_container_width=True):
                if data.get("education_entries"):
                    data["education_entries"] = ResumeBuilderModel.enhance_education_entries(data["education_entries"])
                if data.get("qualification_entries"):
                    data["qualification_entries"] = ResumeBuilderModel.enhance_qualification_entries(data["qualification_entries"])
                compiled = ResumeBuilderModel.compile_education_and_qualifications(
                    data.get("education_entries", []),
                    data.get("qualification_entries", [])
                )
                if compiled:
                    data["education"] = compiled
                elif data.get("education", "").strip():
                    data["education"] = ResumeBuilderModel.enhance_qualifications(data["education"])
                st.session_state.builder_step = 6
                st.rerun()

    # -------------------------------------------------------------
    # STEP 6: SKILLS
    # -------------------------------------------------------------
    elif current_step == 6:
        col_s_head, col_s_btn = st.columns([3, 1])
        with col_s_head:
            st.markdown("### Skills")
            st.caption("List your skills. The system will categorize and format them professionally without inventing any unprovided skills.")
        with col_s_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_skills", use_container_width=True, help="Group skills into industry categories and capitalize technologies properly"):
                if data.get("skills", "").strip():
                    data["skills"] = ResumeBuilderModel.enhance_skills(data["skills"])
                    st.success("✅ Skills organized into professional categories and standardized!")
                    st.rerun()
                else:
                    st.warning("Please enter your skills first before enhancing.")

        data["skills"] = st.text_area(
            "List your skills (comma-separated or lines):",
            value=data.get("skills", ""),
            height=150,
            placeholder="Python, Java, React, SQL, Docker, Git, REST APIs, Problem Solving, PostgreSQL, AWS",
            key="builder_skills_input"
        )

        st.markdown(
            """
            <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; color: #166534; margin-top: 8px;">
                <strong>💡 Smart Skill Categorization:</strong> Enter raw technologies or competencies. Clicking <strong>'✨ Enhance Writing'</strong> automatically groups them into standard professional categories (e.g. Programming Languages, Frameworks, Databases, Cloud & Tools, Core Competencies) while strictly keeping only what you have entered.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_6", use_container_width=True):
                st.session_state.builder_step = 5
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_6", use_container_width=True):
                if data.get("skills", "").strip():
                    data["skills"] = ResumeBuilderModel.enhance_skills(data["skills"])
                st.session_state.builder_step = 7
                st.rerun()

    # -------------------------------------------------------------
    # STEP 7: WORK EXPERIENCE
    # -------------------------------------------------------------
    elif current_step == 7:
        col_exp_head, col_exp_btn = st.columns([3, 1])
        with col_exp_head:
            st.markdown("### Work Experience & Internships")
            st.caption("List your work experience or internships. You may skip this if you do not have work experience.")
        with col_exp_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_exp", use_container_width=True, help="Upgrade weak verbs to strong action verbs and format bullet points professionally"):
                if data.get("experience", "").strip():
                    data["experience"] = ResumeBuilderModel.enhance_experience(data["experience"])
                    st.success("✅ Work experience enhanced with powerful action verbs!")
                    st.rerun()
                else:
                    st.warning("Please enter your work experience first before enhancing.")

        data["experience"] = st.text_area(
            "Work Experience:",
            value=data.get("experience", ""),
            height=200,
            placeholder="Junior Developer | TechCorp Solutions | Jun 2023 - Present\n• Developed backend services in Python and SQL.\n• Maintained REST APIs and server logging.",
            key="builder_exp_input"
        )

        st.markdown(
            """
            <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; color: #166534; margin-top: 8px;">
                <strong>💡 Action-Oriented Phrasing:</strong> Clicking <strong>'✨ Enhance Writing'</strong> upgrades passive language (like <em>worked on</em> or <em>helped with</em>) into assertive action verbs (<em>Architected, Engineered, Spearheaded, Implemented</em>) while preserving all your real companies, dates, and achievements.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_7", use_container_width=True):
                st.session_state.builder_step = 6
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_7", use_container_width=True):
                if data.get("experience", "").strip():
                    data["experience"] = ResumeBuilderModel.enhance_experience(data["experience"])
                st.session_state.builder_step = 8
                st.rerun()

    # -------------------------------------------------------------
    # STEP 8: PROJECTS
    # -------------------------------------------------------------
    elif current_step == 8:
        col_proj_head, col_proj_btn = st.columns([3, 1])
        with col_proj_head:
            st.markdown("### Projects")
            st.caption("Provide projects that showcase your hands-on ability and problem-solving skills.")
        with col_proj_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_proj", use_container_width=True, help="Upgrade project descriptions to strong technical phrasing"):
                if data.get("projects", "").strip():
                    data["projects"] = ResumeBuilderModel.enhance_projects(data["projects"])
                    st.success("✅ Project descriptions enhanced with strong technical phrasing!")
                    st.rerun()
                else:
                    st.warning("Please enter your project details first before enhancing.")

        data["projects"] = st.text_area(
            "Project Details:",
            value=data.get("projects", ""),
            height=180,
            placeholder="• E-Commerce Web App | Tech Stack: Python, FastAPI, SQLite\n  - Built an online store with product catalog and checkout cart.\n  - Deployed live demo at github.com/username/project.",
            key="builder_proj_input"
        )

        st.markdown(
            """
            <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; color: #166534; margin-top: 8px;">
                <strong>💡 Impactful Technical Bullet Points:</strong> Clicking <strong>'✨ Enhance Writing'</strong> refines project descriptions to highlight design, engineering, and architecture without inventing false technologies or metrics.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_8", use_container_width=True):
                st.session_state.builder_step = 7
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_8", use_container_width=True):
                if data.get("projects", "").strip():
                    data["projects"] = ResumeBuilderModel.enhance_projects(data["projects"])
                st.session_state.builder_step = 9
                st.rerun()

    # -------------------------------------------------------------
    # STEP 9: ADDITIONAL INFORMATION & CUSTOM SECTIONS
    # -------------------------------------------------------------
    elif current_step == 9:
        col_cert_head, col_cert_btn = st.columns([3, 1])
        with col_cert_head:
            st.markdown("### Additional Information")
            st.caption("Add certifications, leadership roles, or custom sections.")
        with col_cert_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_cert", use_container_width=True, help="Polish certifications formatting"):
                if data.get("certifications", "").strip():
                    data["certifications"] = ResumeBuilderModel.enhance_custom_section(data["certifications"])
                    st.success("✅ Certifications formatted professionally!")
                    st.rerun()
                else:
                    st.warning("Please enter certifications first before enhancing.")

        data["certifications"] = st.text_area(
            "Certifications & Courses (Optional):",
            value=data.get("certifications", ""),
            height=100,
            placeholder="• AWS Certified Cloud Practitioner\n• Meta Frontend Developer Certificate",
            key="builder_cert_input"
        )

        st.markdown("#### Add Other Information")
        st.caption("You are not restricted to predefined sections. You can add as many custom sections as you want.")

        if "custom_sections" not in data or not isinstance(data["custom_sections"], list):
            data["custom_sections"] = []

        # Render all active custom sections with directly editable inputs
        indices_to_remove = []
        if data["custom_sections"]:
            st.markdown("##### Your Custom Sections:")
            for idx, sec in enumerate(data["custom_sections"]):
                with st.container():
                    col_t, col_enh_s, col_del = st.columns([4, 2, 1])
                    with col_t:
                        sec_title = st.text_input(
                            f"Section Title #{idx + 1}:",
                            value=sec.get("title", ""),
                            placeholder="e.g. Leadership, Languages, Publications",
                            key=f"cs_title_{idx}"
                        )
                    with col_enh_s:
                        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("✨ Enhance Writing", key=f"btn_cs_enh_{idx}", use_container_width=True):
                            if sec.get("content", "").strip():
                                sec["content"] = ResumeBuilderModel.enhance_custom_section(sec["content"])
                                st.success(f"✅ Enhanced '{sec_title or 'Section'}'!")
                                st.rerun()
                    with col_del:
                        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Remove", key=f"cs_del_{idx}", use_container_width=True):
                            indices_to_remove.append(idx)

                    sec_content = st.text_area(
                        f"Section Content #{idx + 1}:",
                        value=sec.get("content", ""),
                        placeholder="Enter description, bullet points, or details...",
                        height=100,
                        key=f"cs_content_{idx}"
                    )
                    sec["title"] = sec_title
                    sec["content"] = sec_content
                    st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px dashed #E2E8F0;'/>", unsafe_allow_html=True)

        if indices_to_remove:
            for idx in sorted(indices_to_remove, reverse=True):
                data["custom_sections"].pop(idx)
            st.rerun()

        # Dynamic Add Section Controls (Allows adding multiple sections easily)
        st.markdown("##### ➕ Add Another Section:")
        col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)
        with col_a1:
            if st.button("➕ Custom Section", key="btn_add_blank_sec", use_container_width=True):
                data["custom_sections"].append({"title": "", "content": ""})
                st.rerun()
        with col_a2:
            if st.button("+ Leadership", key="btn_add_lead_sec", use_container_width=True):
                data["custom_sections"].append({"title": "Leadership & Positions of Responsibility", "content": ""})
                st.rerun()
        with col_a3:
            if st.button("+ Languages", key="btn_add_lang_sec", use_container_width=True):
                data["custom_sections"].append({"title": "Languages", "content": ""})
                st.rerun()
        with col_a4:
            if st.button("+ Hobbies", key="btn_add_hobb_sec", use_container_width=True):
                data["custom_sections"].append({"title": "Hobbies & Interests", "content": ""})
                st.rerun()
        with col_a5:
            if st.button("+ Volunteering", key="btn_add_vol_sec", use_container_width=True):
                data["custom_sections"].append({"title": "Volunteer Experience", "content": ""})
                st.rerun()

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_9", use_container_width=True):
                st.session_state.builder_step = 8
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_9", use_container_width=True):
                st.session_state.builder_step = 10
                st.rerun()

    # -------------------------------------------------------------
    # STEP 10: DECLARATION, DATE & SIGNATURE
    # -------------------------------------------------------------
    elif current_step == 10:
        st.markdown("### Declaration, Date and Signature")
        st.caption("Every generated resume includes a professional declaration section.")

        st.markdown("#### Declaration")
        data["declaration"] = st.text_area(
            "Declaration Statement (Editable):",
            value=data.get("declaration", DEFAULT_DECLARATION),
            height=90,
            key="builder_dec_input"
        )

        col_d, col_s = st.columns([1, 1])
        with col_d:
            st.markdown("#### Date")
            data["date_val"] = st.text_input("Date:", value=data.get("date_val", ""), placeholder="e.g. October 15, 2026")
            if not data["date_val"]:
                st.caption("Will render as: `Date: ____________________`")

        with col_s:
            st.markdown("#### Signature")
            
            sig_choices = [
                "Write the signature",
                "Upload the signature",
                "Leave blank line"
            ]
            cur_sig_mode = data.get("signature_mode", "write")
            sig_idx = 0 if cur_sig_mode == "write" else (1 if cur_sig_mode == "upload" else 2)

            selected_sig = st.radio(
                "Select Signature Type:",
                options=sig_choices,
                index=sig_idx,
                key="builder_sig_mode_radio"
            )

            if selected_sig == sig_choices[0]:
                data["signature_mode"] = "write"
                data["sig_val"] = st.text_input(
                    "Write Your Signature (Type your name):",
                    value=data.get("sig_val", data.get("full_name", "")),
                    placeholder="e.g. Alex Morgan",
                    key="builder_sig_write_input"
                )
                if data["sig_val"]:
                    st.markdown(
                        f"""
                        <div style="padding: 10px 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; margin-top: 6px;">
                            <div style="font-size: 11px; color: #718096; margin-bottom: 2px;">Live Signature Preview:</div>
                            <div style="font-family: 'Brush Script MT', 'Dancing Script', 'Caveat', cursive, sans-serif; font-size: 1.6rem; color: #1E3A8A; line-height: 1.2;">
                                {data["sig_val"]}
                            </div>
                            <div style="border-top: 1px solid #A0AEC0; width: 170px; margin-top: 4px;"></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.caption("Will render as: `Signature: ____________________`")

            elif selected_sig == sig_choices[1]:
                data["signature_mode"] = "upload"
                st.markdown(
                    """
                    <div style="background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 10px 12px; border-radius: 4px; font-size: 0.88rem; color: #92400E; margin-bottom: 8px;">
                        <strong>Requirement:</strong> The signature file must be in <strong>JPEG, JPG, or PNG</strong> format with a <strong>maximum file size of 100 KB</strong>.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                sig_file = st.file_uploader(
                    "Upload Signature Image (JPEG, JPG, PNG — Max 100 KB):",
                    type=["jpg", "jpeg", "png"],
                    key="builder_sig_file_uploader"
                )
                if sig_file:
                    if sig_file.size > 100 * 1024:
                        st.error(f"❌ File size exceeds 100 KB ({sig_file.size / 1024:.1f} KB). Please upload a signature file smaller than 100 KB.")
                    else:
                        sig_bytes = sig_file.read()
                        b64_sig = base64.b64encode(sig_bytes).decode("utf-8")
                        st.session_state.builder_sig_b64 = b64_sig
                        data["signature_img_b64"] = b64_sig
                        st.success(f"✅ Signature uploaded successfully ({sig_file.size / 1024:.1f} KB).")

                if data.get("signature_img_b64"):
                    st.markdown("##### Uploaded Signature Preview:")
                    st.markdown(
                        f"""
                        <div style="padding: 8px 12px; background: white; border: 1px solid #CBD5E0; border-radius: 6px; display: inline-block;">
                            <img src="data:image/png;base64,{data['signature_img_b64']}" style="max-height: 48px; max-width: 170px; object-fit: contain; display: block;" />
                            <div style="border-top: 1px solid #718096; width: 170px; margin-top: 4px;"></div>
                            <div style="font-size: 11px; color: #718096; margin-top: 2px;">Signature</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("🗑️ Remove Signature Image", key="btn_remove_sig_img"):
                        data["signature_img_b64"] = ""
                        st.session_state.builder_sig_b64 = ""
                        st.rerun()

            else:
                data["signature_mode"] = "blank"
                data["sig_val"] = ""
                st.info("A blank signature line (`Signature: ____________________`) will be included for physical hand signing after printing.")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_10", use_container_width=True):
                st.session_state.builder_step = 9
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_10", use_container_width=True):
                st.session_state.builder_step = 11
                st.rerun()

    # -------------------------------------------------------------
    # STEP 11: TEMPLATE SELECTION
    # -------------------------------------------------------------
    elif current_step == 11:
        st.markdown("### Template Selection")
        st.caption("Select your preferred resume template. Each template displays its picture preview and name.")

        current_tpl = data.get("template_name", "Modern")

        tpl_cols = st.columns(3)
        for i, (tpl_key, tpl_info) in enumerate(TEMPLATES_INFO.items()):
            col_target = tpl_cols[i % 3]
            with col_target:
                st.markdown(f"#### {tpl_info['name']}")
                st.markdown(tpl_info["preview_svg"], unsafe_allow_html=True)
                st.caption(tpl_info["description"])

                is_selected = (current_tpl == tpl_key)
                btn_label = "✅ Selected" if is_selected else f"Select {tpl_info['name']}"
                if st.button(btn_label, key=f"sel_tpl_{tpl_key}", use_container_width=True):
                    data["template_name"] = tpl_key
                    st.rerun()

        st.markdown("---")
        st.info(f"Selected Template: **{data.get('template_name', 'Modern')}**")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_11", use_container_width=True):
                st.session_state.builder_step = 10
                st.rerun()
        with col_next:
            if st.button("Next: Create & Preview Resume →", type="primary", key="btn_bld_next_11", use_container_width=True):
                tailored = ResumeBuilderModel.tailor_content(data)
                st.session_state.builder_data.update(tailored)
                st.session_state.builder_step = 12
                st.rerun()

    # -------------------------------------------------------------
    # STEP 12: RESUME PREVIEW & REVIEW CONTROLS
    # -------------------------------------------------------------
    elif current_step == 12:
        st.markdown("### Resume Preview")
        st.caption(f"Previewing resume using the {data.get('template_name', 'Modern')} template.")

        # Controls: Edit Resume, Change Template, Accept Resume
        col_act1, col_act2, col_act3 = st.columns(3)
        with col_act1:
            if st.button("✎ Edit Resume", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()
        with col_act2:
            if st.button("🎨 Change Template", use_container_width=True):
                st.session_state.builder_step = 11
                st.rerun()
        with col_act3:
            if st.button("✅ Accept Resume", type="primary", use_container_width=True):
                st.session_state.builder_accepted = True
                st.session_state.builder_step = 13
                st.rerun()

        st.markdown("")
        html_preview = render_resume_html(
            data=data,
            template_name=data.get("template_name", "Modern"),
            photo_b64=st.session_state.builder_photo_b64
        )
        components.html(html_preview, height=950, scrolling=True)

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_12", use_container_width=True):
                st.session_state.builder_step = 11
                st.rerun()
        with col_next:
            if st.button("Next: Finalize & Download →", type="primary", key="btn_bld_next_12", use_container_width=True):
                st.session_state.builder_accepted = True
                st.session_state.builder_step = 13
                st.rerun()

    # -------------------------------------------------------------
    # STEP 13: FINAL RESUME & DOWNLOADS
    # -------------------------------------------------------------
    elif current_step == 13:
        st.markdown("### Final Resume")
        if data.get("job_description"):
            st.success("### “Your resume has been updated based on your selected job role, company, and job description.”")
        else:
            st.success("### “Your resume has been updated based on your selected job role and company.”")

        st.caption("You have complete control over your resume. You can edit any details or change the template at any time.")

        pdf_bytes = export_builder_resume_to_pdf(data, data.get("template_name", "Modern"))
        plain_text = ResumeBuilderModel.to_plain_text(data)
        docx_bytes = export_resume_to_docx(plain_text)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                label=f"📥 Download PDF ({data.get('template_name', 'Modern')})",
                data=pdf_bytes,
                file_name=f"{data.get('full_name', 'Resume').replace(' ', '_')}_{data.get('template_name', 'Template')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label="📥 Download Word (.docx)",
                data=docx_bytes,
                file_name=f"{data.get('full_name', 'Resume').replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with col_d3:
            st.download_button(
                label="📥 Download Plain Text (.txt)",
                data=plain_text,
                file_name=f"{data.get('full_name', 'Resume').replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back to Edit", key="btn_bld_back_13", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()
        with col_next:
            if st.button("Switch Template", key="btn_bld_next_13", use_container_width=True):
                st.session_state.builder_step = 11
                st.rerun()

        st.markdown("")
        with st.expander("Preview Resume", expanded=True):
            html_preview = render_resume_html(
                data=data,
                template_name=data.get("template_name", "Modern"),
                photo_b64=st.session_state.builder_photo_b64
            )
            components.html(html_preview, height=950, scrolling=True)
