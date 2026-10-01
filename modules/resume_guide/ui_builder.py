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
import plotly.graph_objects as go

def render_builder_section_breakdown_pie_chart(data: Dict[str, Any]):
    """
    Render an interactive Plotly donut/pie chart summarizing section completeness
    and content breakdown for the created resume in Resume Builder.
    """
    from modules.resume_guide.builder_templates import get_resume_headline

    # Evaluate sections in builder
    sections_status = []

    # 1. Contact / Personal Details
    has_contact = bool(data.get("full_name") and (data.get("email") or data.get("phone")))
    sections_status.append(("Personal Details & Contact", has_contact, "Essential contact credentials provided." if has_contact else "Missing name or contact info."))

    # 2. Professional Headline
    hl = get_resume_headline(data)
    sections_status.append(("Professional Headline", bool(hl), f"Headline: '{hl}'" if hl else "Clean layout without headline."))

    # 3. Education & Qualifications
    has_edu = bool(data.get("education", "").strip() or data.get("education_entries"))
    sections_status.append(("Education & Qualifications", has_edu, "Academic qualifications provided." if has_edu else "No education provided."))

    # 4. Technical Skills
    has_tech_skills = bool(data.get("skills", "").strip() or data.get("tech_skills_raw", "").strip())
    sections_status.append(("Technical Skills", has_tech_skills, "Technical competencies added." if has_tech_skills else "No technical skills entered."))

    # 5. Non-Technical Skills
    has_non_tech = bool("Non-Technical" in data.get("skills", "") or data.get("non_tech_skills_raw", "").strip())
    sections_status.append(("Non-Technical Skills", has_non_tech, "Interpersonal & soft skills included." if has_non_tech else "Optional non-technical skills skipped."))

    # 6. Work Experience
    has_exp = bool(data.get("experience", "").strip() or [e for e in data.get("experience_entries", []) if any(e.values())])
    sections_status.append(("Work Experience", has_exp, "Professional experience included." if has_exp else "Fresher / Entry-Level (No prior employment)."))

    # 7. Technical Projects
    has_proj = bool(data.get("projects", "").strip() or [p for p in data.get("project_entries", []) if any(p.values())])
    sections_status.append(("Technical Projects", has_proj, "Technical projects detailed." if has_proj else "No technical projects (Skipped)."))

    # 8. Certifications / Courses
    has_cert = bool(data.get("certifications", "").strip())
    sections_status.append(("Certifications & Courses", has_cert, "Professional credentials included." if has_cert else "Optional certifications skipped."))

    # 9. Declaration & Signature
    has_decl = bool(data.get("declaration", "").strip() and (data.get("sig_val") or data.get("signature_img_b64") or data.get("signature_mode") == "blank"))
    sections_status.append(("Declaration & Signature", has_decl, "Formal verification completed." if has_decl else "Pending signature."))

    completed_sections = [s for s in sections_status if s[1]]
    optional_skipped = [s for s in sections_status if not s[1]]

    labels = ["Completed Sections", "Optional / Skipped Sections"]
    values = [len(completed_sections), len(optional_skipped)]
    colors_palette = ["#10B981", "#94A3B8"]

    hover_completed = "<br>• ".join([s[0] for s in completed_sections])
    hover_skipped = "<br>• ".join([s[0] for s in optional_skipped])
    hover_texts = [f"<b>Included:</b><br>• {hover_completed}", f"<b>Skipped / Omitted:</b><br>• {hover_skipped}" if hover_skipped else "None skipped"]

    col_chart, col_summary = st.columns([1.1, 1])
    with col_chart:
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.52,
            marker=dict(colors=colors_palette, line=dict(color='#FFFFFF', width=2.5)),
            textinfo='percent+label',
            textposition='inside',
            hovertext=hover_texts,
            hovertemplate='<b>%{label}</b><br>%{hovertext}<br><b>Count:</b> %{value} of ' + str(len(sections_status)) + ' sections (%{percent})<extra></extra>',
            pull=[0.02, 0.02]
        )])

        pct_complete = int((len(completed_sections) / len(sections_status)) * 100)
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
            margin=dict(t=15, b=65, l=15, r=15),
            height=320,
            annotations=[dict(text=f'<b>{pct_complete}%</b><br><span style="font-size:11px;color:#64748B;">Complete</span>', x=0.5, y=0.5, font_size=18, showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_summary:
        st.markdown("##### Resume Content & Completeness Summary")
        for name, active, note in completed_sections:
            st.markdown(f"🟢 **{name}**: *Included* — {note}")
        for name, active, note in optional_skipped:
            st.markdown(f"⚪ **{name}**: *Omitted* — {note}")

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
    if "experience_entries" not in st.session_state.builder_data or not isinstance(st.session_state.builder_data.get("experience_entries"), list):
        st.session_state.builder_data["experience_entries"] = []
    if "professional_headline" not in st.session_state.builder_data:
        st.session_state.builder_data["professional_headline"] = ""
    if "place_val" not in st.session_state.builder_data:
        st.session_state.builder_data["place_val"] = ""
    if "project_entries" not in st.session_state.builder_data or not isinstance(st.session_state.builder_data.get("project_entries"), list):
        st.session_state.builder_data["project_entries"] = []
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
        "4. Personal Details & Photo",
        "5. Professional Headline",
        "6. Education and Qualifications",
        "7. Skills",
        "8. Work Experience",
        "9. Technical Project",
        "10. Additional Information",
        "11. Declaration, Date and Signature",
        "12. Template Selection",
        "13. Resume Preview",
        "14. Final Resume & Download"
    ]

    current_step = st.session_state.builder_step
    
    st.markdown("""
        <div style="background-color: #EDF2F7; border-radius: 8px; padding: 10px 16px; margin-bottom: 20px;">
            <span style="font-size: 0.95rem; color: #2D3748; font-weight: 600;">Create Resume — Step %d of 14: %s</span>
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
    # STEP 5: PROFESSIONAL HEADLINE
    # -------------------------------------------------------------
    elif current_step == 5:
        col_hl_head, col_hl_btn = st.columns([3, 1])
        with col_hl_head:
            st.markdown("### Professional Headline")
            st.caption("Provide a professional headline that defines your expertise or specialization. This field is completely user-controlled.")
        with col_hl_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_headline", use_container_width=True, help="Convert basic headline or skills into a professional, structured resume headline"):
                current_hl = st.session_state.get("builder_prof_headline_input", data.get("professional_headline", "")).strip()
                if current_hl:
                    enhanced_hl = ResumeBuilderModel.enhance_headline(current_hl)
                    st.session_state["builder_prof_headline_input"] = enhanced_hl
                    data["professional_headline"] = enhanced_hl
                    st.success("✅ Professional headline enhanced!")
                    st.rerun()
                else:
                    st.warning("Please enter your basic headline or role/skills first before enhancing.")

        data["professional_headline"] = st.text_input(
            "Professional Headline (Optional):",
            value=st.session_state.get("builder_prof_headline_input", data.get("professional_headline", "")),
            placeholder="e.g. Full-Stack Developer | Python & Cloud Solutions",
            key="builder_prof_headline_input"
        )

        st.markdown(
            """
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #3B82F6; padding: 14px 16px; border-radius: 6px; margin-top: 14px; font-size: 0.88rem; color: #334155; line-height: 1.6;">
                <strong>📌 Headline Placement & Header Logic:</strong>
                <ul style="margin: 6px 0 0 16px; padding: 0;">
                    <li><strong>Entered Headline:</strong> If provided, this exact headline appears directly below your name on your final resume.</li>
                    <li><strong>Ongoing Experience Fallback:</strong> If left empty, the builder will look at your <em>Work Experience</em>. If you have an entry marked as <em>Currently Ongoing</em>, its job position title will be displayed.</li>
                    <li><strong>Clean & Empty:</strong> If there is no headline and no ongoing experience, the space below your name remains completely clean and empty.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_5", use_container_width=True):
                data["professional_headline"] = st.session_state.get("builder_prof_headline_input", data.get("professional_headline", "")).strip()
                st.session_state.builder_step = 4
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_5", use_container_width=True):
                data["professional_headline"] = st.session_state.get("builder_prof_headline_input", data.get("professional_headline", "")).strip()
                st.session_state.builder_step = 6
                st.rerun()

    # -------------------------------------------------------------
    # STEP 6: EDUCATION AND QUALIFICATIONS
    # -------------------------------------------------------------
    elif current_step == 6:
        col_e_head, col_e_btn = st.columns([3, 1])
        with col_e_head:
            st.markdown("### Education and Qualifications")
            st.caption("Provide your formal education and any additional professional qualifications.")
        with col_e_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_edu_top", use_container_width=True, help="Standardize degrees, specializations, and qualifications professionally without altering facts"):
                for idx, entry in enumerate(data.get("education_entries", [])):
                    if f"edu_deg_{idx}" in st.session_state:
                        entry["degree"] = st.session_state[f"edu_deg_{idx}"]
                    if f"edu_field_{idx}" in st.session_state:
                        entry["field_of_study"] = st.session_state[f"edu_field_{idx}"]
                        entry["stream"] = st.session_state[f"edu_field_{idx}"]
                    if f"edu_inst_{idx}" in st.session_state:
                        entry["institution"] = st.session_state[f"edu_inst_{idx}"]
                    if f"edu_board_{idx}" in st.session_state:
                        entry["board_univ"] = st.session_state[f"edu_board_{idx}"]
                    if f"edu_loc_{idx}" in st.session_state:
                        entry["location"] = st.session_state[f"edu_loc_{idx}"]
                    if f"edu_syr_{idx}" in st.session_state:
                        entry["start_year"] = st.session_state[f"edu_syr_{idx}"]
                    if f"edu_eyr_{idx}" in st.session_state:
                        entry["end_year"] = st.session_state[f"edu_eyr_{idx}"]
                    if f"edu_expyr_{idx}" in st.session_state:
                        entry["expected_grad_year"] = st.session_state[f"edu_expyr_{idx}"]
                    if f"edu_cgpa_{idx}" in st.session_state:
                        entry["cgpa"] = st.session_state[f"edu_cgpa_{idx}"]
                    if f"edu_pct_{idx}" in st.session_state:
                        entry["percentage"] = st.session_state[f"edu_pct_{idx}"]
                    if f"edu_grd_{idx}" in st.session_state:
                        entry["grade"] = st.session_state[f"edu_grd_{idx}"]

                if data.get("education_entries"):
                    data["education_entries"] = ResumeBuilderModel.enhance_education_entries(data["education_entries"])
                    for idx, entry in enumerate(data["education_entries"]):
                        st.session_state[f"edu_deg_{idx}"] = entry.get("degree", "")
                        st.session_state[f"edu_field_{idx}"] = entry.get("field_of_study", "")
                        st.session_state[f"edu_inst_{idx}"] = entry.get("institution", "")
                        st.session_state[f"edu_board_{idx}"] = entry.get("board_univ", "")
                        st.session_state[f"edu_loc_{idx}"] = entry.get("location", "")
                        st.session_state[f"edu_syr_{idx}"] = entry.get("start_year", "")
                        st.session_state[f"edu_eyr_{idx}"] = entry.get("end_year", "")
                        st.session_state[f"edu_expyr_{idx}"] = entry.get("expected_grad_year", "")
                        st.session_state[f"edu_cgpa_{idx}"] = entry.get("cgpa", "")
                        st.session_state[f"edu_pct_{idx}"] = entry.get("percentage", "")
                        st.session_state[f"edu_grd_{idx}"] = entry.get("grade", "")

                for q_idx, q_ent in enumerate(data.get("qualification_entries", [])):
                    if f"qual_title_{q_idx}" in st.session_state:
                        q_ent["title"] = st.session_state[f"qual_title_{q_idx}"]
                    if f"qual_org_{q_idx}" in st.session_state:
                        q_ent["organization"] = st.session_state[f"qual_org_{q_idx}"]
                    if f"qual_yr_{q_idx}" in st.session_state:
                        q_ent["year"] = st.session_state[f"qual_yr_{q_idx}"]
                    if f"qual_det_{q_idx}" in st.session_state:
                        q_ent["details"] = st.session_state[f"qual_det_{q_idx}"]

                if data.get("qualification_entries"):
                    data["qualification_entries"] = ResumeBuilderModel.enhance_qualification_entries(data["qualification_entries"])
                    for q_idx, q_ent in enumerate(data["qualification_entries"]):
                        st.session_state[f"qual_title_{q_idx}"] = q_ent.get("title", "")
                        st.session_state[f"qual_org_{q_idx}"] = q_ent.get("organization", "")
                        st.session_state[f"qual_yr_{q_idx}"] = q_ent.get("year", "")
                        st.session_state[f"qual_det_{q_idx}"] = q_ent.get("details", "")

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
                        value=st.session_state.get(f"edu_deg_{idx}", entry.get("degree", "")),
                        placeholder="e.g. Bachelor of Technology / Class XII",
                        key=f"edu_deg_{idx}"
                    )
                    entry["field_of_study"] = st.text_input(
                        "Field of Study or Specialization:",
                        value=st.session_state.get(f"edu_field_{idx}", entry.get("field_of_study", entry.get("stream", ""))),
                        placeholder="e.g. Computer Science & Engineering / Science",
                        key=f"edu_field_{idx}"
                    )
                    entry["institution"] = st.text_input(
                        "Institution Name:",
                        value=st.session_state.get(f"edu_inst_{idx}", entry.get("institution", "")),
                        placeholder="e.g. Delhi Technological University / High School",
                        key=f"edu_inst_{idx}"
                    )
                with c2:
                    entry["board_univ"] = st.text_input(
                        "University or Board (Optional):",
                        value=st.session_state.get(f"edu_board_{idx}", entry.get("board_univ", "")),
                        placeholder="e.g. CBSE / State Board / University Name",
                        key=f"edu_board_{idx}"
                    )
                    entry["location"] = st.text_input(
                        "Location (Optional):",
                        value=st.session_state.get(f"edu_loc_{idx}", entry.get("location", "")),
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
                        value=st.session_state.get(f"edu_syr_{idx}", entry.get("start_year", "")),
                        placeholder="e.g. 2020",
                        key=f"edu_syr_{idx}"
                    )
                with cd2:
                    if entry["status"] == "Completed":
                        entry["end_year"] = st.text_input(
                            "End Year:",
                            value=st.session_state.get(f"edu_eyr_{idx}", entry.get("end_year", "")),
                            placeholder="e.g. 2024",
                            key=f"edu_eyr_{idx}"
                        )
                        entry["expected_grad_year"] = ""
                    else:  # Currently Pursuing
                        entry["expected_grad_year"] = st.text_input(
                            "Expected Graduation Year:",
                            value=st.session_state.get(f"edu_expyr_{idx}", entry.get("expected_grad_year", "")),
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
                        value=st.session_state.get(f"edu_cgpa_{idx}", entry.get("cgpa", "")),
                        placeholder="e.g. 8.7",
                        key=f"edu_cgpa_{idx}"
                    )
                with ca2:
                    entry["percentage"] = st.text_input(
                        "Percentage (Optional):",
                        value=st.session_state.get(f"edu_pct_{idx}", entry.get("percentage", "")),
                        placeholder="e.g. 88.5%",
                        key=f"edu_pct_{idx}"
                    )
                with ca3:
                    entry["grade"] = st.text_input(
                        "Grade (Optional):",
                        value=st.session_state.get(f"edu_grd_{idx}", entry.get("grade", "")),
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

        # Automatically compile structured education and qualifications for the resume
        compiled_edu = ResumeBuilderModel.compile_education_and_qualifications(
            data.get("education_entries", []),
            data.get("qualification_entries", [])
        )
        if compiled_edu:
            data["education"] = compiled_edu

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_6", use_container_width=True):
                st.session_state.builder_step = 5
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_6", use_container_width=True):
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
                st.session_state.builder_step = 7
                st.rerun()

    # -------------------------------------------------------------
    # STEP 7: SKILLS
    # -------------------------------------------------------------
    elif current_step == 7:
        col_s_head, col_s_btn = st.columns([3, 1])
        with col_s_head:
            st.markdown("### Skills")
            st.caption("List your technical and non-technical skills. Press Enter to write skills on each new line.")
        with col_s_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_skills", use_container_width=True, help="Group skills into industry categories and capitalize technologies properly"):
                cur_tech = st.session_state.get("builder_tech_skills_input", data.get("tech_skills_raw", "")).strip()
                cur_non_tech = st.session_state.get("builder_non_tech_skills_input", data.get("non_tech_skills_raw", "")).strip()
                if cur_tech or cur_non_tech:
                    enhanced_skills = ResumeBuilderModel.enhance_technical_and_non_technical(cur_tech, cur_non_tech)
                    data["skills"] = enhanced_skills
                    st.success("✅ Skills organized into professional categories and standardized!")
                    st.rerun()
                else:
                    st.warning("Please enter your skills first before enhancing.")

        # Multi-line input 1: Technical Skills
        data["tech_skills_raw"] = st.text_area(
            "Technical Skills (Languages, Frameworks, Databases, Tools):",
            value=st.session_state.get("builder_tech_skills_input", data.get("tech_skills_raw", "")),
            height=120,
            placeholder="Type or press Enter to add each skill on a new line:\nPython\nC++\nSQL\nReact\nDocker\nGit",
            key="builder_tech_skills_input",
            help="Press Enter to write skills on each new line"
        )

        # Multi-line input 2: Non-Technical Skills
        data["non_tech_skills_raw"] = st.text_area(
            "Non-Technical Skills (Soft Skills, Leadership, Communication):",
            value=st.session_state.get("builder_non_tech_skills_input", data.get("non_tech_skills_raw", "")),
            height=90,
            placeholder="Type or press Enter to add each skill on a new line:\nPublic Speaking\nProblem Solving\nTeam Leadership\nCritical Thinking",
            key="builder_non_tech_skills_input",
            help="Press Enter to write skills on each new line"
        )

        st.markdown(
            """
            <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; color: #166534; margin-top: 8px;">
                <strong>💡 Multi-line Skills Entry:</strong> You can press <strong>Enter</strong> to write each skill line-by-line or separate skills with commas. Technical skills and non-technical skills (such as Public Speaking) are formatted cleanly under their own separate sections on your final resume.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_7", use_container_width=True):
                cur_tech = st.session_state.get("builder_tech_skills_input", data.get("tech_skills_raw", "")).strip()
                cur_non_tech = st.session_state.get("builder_non_tech_skills_input", data.get("non_tech_skills_raw", "")).strip()
                data["tech_skills_raw"] = cur_tech
                data["non_tech_skills_raw"] = cur_non_tech
                if cur_tech or cur_non_tech:
                    data["skills"] = ResumeBuilderModel.enhance_technical_and_non_technical(cur_tech, cur_non_tech)
                st.session_state.builder_step = 6
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_7", use_container_width=True):
                cur_tech = st.session_state.get("builder_tech_skills_input", data.get("tech_skills_raw", "")).strip()
                cur_non_tech = st.session_state.get("builder_non_tech_skills_input", data.get("non_tech_skills_raw", "")).strip()
                data["tech_skills_raw"] = cur_tech
                data["non_tech_skills_raw"] = cur_non_tech
                if cur_tech or cur_non_tech:
                    data["skills"] = ResumeBuilderModel.enhance_technical_and_non_technical(cur_tech, cur_non_tech)
                else:
                    data["skills"] = ""
                st.session_state.builder_step = 8
                st.rerun()

    # -------------------------------------------------------------
    # STEP 8: WORK EXPERIENCE
    # -------------------------------------------------------------
    elif current_step == 8:
        col_exp_head, col_exp_btn = st.columns([3, 1])
        with col_exp_head:
            st.markdown("### Work Experience")
            st.caption("Provide your professional work experience. This section is optional; if you do not have work experience, you can leave it empty and proceed.")
        with col_exp_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_exp", use_container_width=True, help="Upgrade action verbs in descriptions and responsibilities without altering facts"):
                for idx, exp_ent in enumerate(data.get("experience_entries", [])):
                    if f"exp_pos_{idx}" in st.session_state:
                        exp_ent["position"] = st.session_state[f"exp_pos_{idx}"]
                    if f"exp_comp_{idx}" in st.session_state:
                        exp_ent["company"] = st.session_state[f"exp_comp_{idx}"]
                    if f"exp_loc_{idx}" in st.session_state:
                        exp_ent["location"] = st.session_state[f"exp_loc_{idx}"]
                    if f"exp_desc_{idx}" in st.session_state:
                        exp_ent["description"] = st.session_state[f"exp_desc_{idx}"]
                    if f"exp_resp_{idx}" in st.session_state:
                        exp_ent["responsibilities"] = st.session_state[f"exp_resp_{idx}"]
                    if f"exp_sdate_{idx}" in st.session_state:
                        exp_ent["start_date"] = st.session_state[f"exp_sdate_{idx}"]
                    if f"exp_edate_{idx}" in st.session_state:
                        exp_ent["end_date"] = st.session_state[f"exp_edate_{idx}"]

                if data.get("experience_entries"):
                    data["experience_entries"] = ResumeBuilderModel.enhance_experience_entries(data["experience_entries"])
                    for idx, exp_ent in enumerate(data["experience_entries"]):
                        st.session_state[f"exp_pos_{idx}"] = exp_ent.get("position", "")
                        st.session_state[f"exp_desc_{idx}"] = exp_ent.get("description", "")
                        st.session_state[f"exp_resp_{idx}"] = exp_ent.get("responsibilities", "")
                    compiled_exp = ResumeBuilderModel.compile_experience_entries(data["experience_entries"])
                    if compiled_exp:
                        data["experience"] = compiled_exp
                    st.success("✅ Work experience enhanced with powerful action verbs!")
                    st.rerun()
                elif data.get("experience", "").strip():
                    data["experience"] = ResumeBuilderModel.enhance_experience(data["experience"])
                    st.success("✅ Work experience enhanced with powerful action verbs!")
                    st.rerun()
                else:
                    st.info("No work experience entries to enhance yet.")

        if "experience_entries" not in data or not isinstance(data.get("experience_entries"), list):
            data["experience_entries"] = []

        exp_type_options = [
            "Internship",
            "Placement",
            "Full-Time",
            "Part-Time",
            "Contract",
            "Freelance",
            "Apprenticeship",
            "Write Your Own"
        ]

        if not data["experience_entries"]:
            st.info("ℹ️ No work experience added yet. If you have internships, placements, or jobs to include, click **'+ Add Work Experience'** below. Otherwise, you can leave this section empty and click **'Next →'**.")
            if st.button("➕ Add Work Experience", key="btn_add_first_exp", type="primary"):
                data["experience_entries"].append({
                    "experience_type": "Full-Time",
                    "custom_experience_type": "",
                    "work_arrangement": "On-site",
                    "custom_work_arrangement": "",
                    "company": "",
                    "position": "",
                    "location": "",
                    "status": "Completed",
                    "start_date": "",
                    "end_date": "",
                    "description": "",
                    "responsibilities": ""
                })
                st.rerun()
        else:
            del_exp_indices = []

            for idx, exp_ent in enumerate(data["experience_entries"]):
                exp_pos_disp = exp_ent.get("position", "").strip() or "Work Experience Entry"
                with st.container():
                    col_h, col_del = st.columns([5, 1])
                    with col_h:
                        st.markdown(f"**💼 {exp_pos_disp}**")
                    with col_del:
                        if st.button("🗑️ Remove", key=f"btn_del_exp_{idx}"):
                            del_exp_indices.append(idx)

                    c1, c2 = st.columns(2)
                    with c1:
                        exp_ent["position"] = st.text_input(
                            "Position or Job Title:",
                            value=st.session_state.get(f"exp_pos_{idx}", exp_ent.get("position", "")),
                            placeholder="e.g. Software Engineer, Data Analyst",
                            key=f"exp_pos_{idx}"
                        )

                        current_type = exp_ent.get("experience_type", "Full-Time")
                        if current_type not in exp_type_options:
                            type_idx = exp_type_options.index("Write Your Own")
                            if not exp_ent.get("custom_experience_type"):
                                exp_ent["custom_experience_type"] = current_type
                        else:
                            type_idx = exp_type_options.index(current_type)

                        selected_type = st.selectbox(
                            "Experience Type:",
                            options=exp_type_options,
                            index=type_idx,
                            key=f"exp_type_sel_{idx}",
                            help="Employment nature (Internship, Full-Time, Part-Time, Contract, Placement, etc.)"
                        )
                        exp_ent["experience_type"] = selected_type

                        if selected_type == "Write Your Own":
                            exp_ent["custom_experience_type"] = st.text_input(
                                "Write Your Own Experience Type:",
                                value=exp_ent.get("custom_experience_type", ""),
                                placeholder="e.g. Research Fellow, Volunteer, Trainee",
                                key=f"exp_custom_type_{idx}"
                            )
                        else:
                            exp_ent["custom_experience_type"] = ""

                    with c2:
                        exp_ent["company"] = st.text_input(
                            "Company Name:",
                            value=st.session_state.get(f"exp_comp_{idx}", exp_ent.get("company", "")),
                            placeholder="e.g. Google, Microsoft, TechCorp Solutions",
                            key=f"exp_comp_{idx}"
                        )
                        exp_ent["location"] = st.text_input(
                            "Location (Where work was based, optional):",
                            value=st.session_state.get(f"exp_loc_{idx}", exp_ent.get("location", "")),
                            placeholder="e.g. Bengaluru, India / San Francisco, CA",
                            key=f"exp_loc_{idx}"
                        )

                        # Work Arrangement: single field with suggested options (On-site, Remote, Hybrid) and custom writing allowance
                        arr_suggested = ["On-site", "Remote", "Hybrid"]
                        state_key = f"exp_arr_sel_{idx}"
                        curr_arr = exp_ent.get("work_arrangement", "")
                        if curr_arr == "Write Your Own":
                            curr_arr = exp_ent.get("custom_work_arrangement", "")
                        if not curr_arr:
                            curr_arr = "On-site"

                        if state_key in st.session_state and st.session_state[state_key]:
                            curr_arr = str(st.session_state[state_key])

                        arr_options = list(arr_suggested)
                        if curr_arr not in arr_options:
                            arr_options.append(curr_arr)
                        arr_idx = arr_options.index(curr_arr)

                        selected_arr = st.selectbox(
                            "Work Arrangement:",
                            options=arr_options,
                            index=arr_idx,
                            accept_new_options=True,
                            key=state_key,
                            help="Suggested options: On-site, Remote, Hybrid. You can also write your own directly in this field if required."
                        )
                        exp_ent["work_arrangement"] = selected_arr or ""
                        exp_ent["custom_work_arrangement"] = selected_arr or ""

                    # Status and Dynamic Date Fields
                    st.markdown("<span style='font-size: 0.88rem; font-weight: 600; color: #4A5568;'>Status & Dates:</span>", unsafe_allow_html=True)
                    status_val = exp_ent.get("status", "Completed")
                    status_idx = 0 if status_val == "Completed" else 1
                    exp_ent["status"] = st.radio(
                        "Status:",
                        options=["Completed", "Currently Ongoing"],
                        index=status_idx,
                        key=f"exp_status_{idx}",
                        horizontal=True
                    )

                    if exp_ent["status"] == "Completed":
                        cd1, cd2 = st.columns(2)
                        with cd1:
                            exp_ent["start_date"] = st.text_input(
                                "Start Date:",
                                value=exp_ent.get("start_date", ""),
                                placeholder="e.g. Jun 2022",
                                key=f"exp_sdate_{idx}"
                            )
                        with cd2:
                            exp_ent["end_date"] = st.text_input(
                                "End Date:",
                                value=exp_ent.get("end_date", ""),
                                placeholder="e.g. May 2024",
                                key=f"exp_edate_{idx}"
                            )
                    else:  # Currently Ongoing
                        exp_ent["start_date"] = st.text_input(
                            "Start Date:",
                            value=exp_ent.get("start_date", ""),
                            placeholder="e.g. Jun 2023",
                            key=f"exp_sdate_{idx}"
                        )
                        exp_ent["end_date"] = ""

                    # Description & Responsibilities
                    exp_ent["description"] = st.text_area(
                        "Description (Overview of role or team, optional):",
                        value=st.session_state.get(f"exp_desc_{idx}", exp_ent.get("description", "")),
                        height=75,
                        placeholder="e.g. Part of the core engineering team building microservices and customer APIs.",
                        key=f"exp_desc_{idx}"
                    )
                    exp_ent["responsibilities"] = st.text_area(
                        "Key Responsibilities or Achievements (Bullet points):",
                        value=st.session_state.get(f"exp_resp_{idx}", exp_ent.get("responsibilities", "")),
                        height=110,
                        placeholder="• Architected REST APIs handling 5M+ daily requests with 99.9% uptime.\n• Optimized database queries cutting page load time by 30%.\n• Collaborated with product designers to ship 4 customer-facing features.",
                        key=f"exp_resp_{idx}"
                    )
                    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px dashed #CBD5E0;'/>", unsafe_allow_html=True)

            if del_exp_indices:
                for di in sorted(del_exp_indices, reverse=True):
                    data["experience_entries"].pop(di)
                st.rerun()

            if st.button("➕ Add Another Experience", key="btn_add_another_exp"):
                data["experience_entries"].append({
                    "experience_type": "Full-Time",
                    "custom_experience_type": "",
                    "work_arrangement": "On-site",
                    "custom_work_arrangement": "",
                    "company": "",
                    "position": "",
                    "location": "",
                    "status": "Completed",
                    "start_date": "",
                    "end_date": "",
                    "description": "",
                    "responsibilities": ""
                })
                st.rerun()

        # Compile in background into data["experience"]
        compiled_exp = ResumeBuilderModel.compile_experience_entries(data.get("experience_entries", []))
        data["experience"] = compiled_exp

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_8", use_container_width=True):
                st.session_state.builder_step = 7
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_8", use_container_width=True):
                valid_entries = [
                    e for e in data.get("experience_entries", [])
                    if any([
                        e.get("company", "").strip(),
                        e.get("position", "").strip(),
                        e.get("description", "").strip(),
                        e.get("responsibilities", "").strip()
                    ])
                ]
                data["experience_entries"] = valid_entries
                if valid_entries:
                    data["experience_entries"] = ResumeBuilderModel.enhance_experience_entries(valid_entries)
                    data["experience"] = ResumeBuilderModel.compile_experience_entries(data["experience_entries"])
                else:
                    data["experience"] = ""
                st.session_state.builder_step = 9
                st.rerun()

    # -------------------------------------------------------------
    # STEP 9: TECHNICAL PROJECT
    # -------------------------------------------------------------
    elif current_step == 9:
        col_proj_head, col_proj_btn = st.columns([3, 1])
        with col_proj_head:
            st.markdown("### Technical Project")
            st.caption("Provide technical projects that showcase your hands-on engineering, architecture, and problem-solving abilities.")
        with col_proj_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_proj", use_container_width=True, help="Upgrade project descriptions to strong technical phrasing"):
                for p_idx, proj in enumerate(data.get("project_entries", [])):
                    if f"proj_name_{p_idx}" in st.session_state:
                        proj["name"] = st.session_state[f"proj_name_{p_idx}"]
                    if f"proj_stack_{p_idx}" in st.session_state:
                        proj["tech_stack"] = st.session_state[f"proj_stack_{p_idx}"]
                    if f"proj_desc_{p_idx}" in st.session_state:
                        proj["description"] = st.session_state[f"proj_desc_{p_idx}"]

                if data.get("project_entries"):
                    data["project_entries"] = ResumeBuilderModel.enhance_project_entries(data["project_entries"])
                    for p_idx, proj in enumerate(data["project_entries"]):
                        st.session_state[f"proj_name_{p_idx}"] = proj.get("name", "")
                        st.session_state[f"proj_stack_{p_idx}"] = proj.get("tech_stack", "")
                        st.session_state[f"proj_desc_{p_idx}"] = proj.get("description", "")
                    data["projects"] = ResumeBuilderModel.compile_project_entries(data["project_entries"])
                    st.success("✅ Technical project descriptions enhanced with strong technical phrasing!")
                    st.rerun()
                elif data.get("projects", "").strip():
                    data["projects"] = ResumeBuilderModel.enhance_projects(data["projects"])
                    st.success("✅ Project descriptions enhanced with strong technical phrasing!")
                    st.rerun()
                else:
                    st.warning("Please enter your project details first before enhancing.")

        # User Choice: Add or Skip Technical Projects
        has_proj_choice = st.radio(
            "Do you have any technical projects to include on your resume?",
            options=["Yes, Add Technical Projects", "No Technical Projects (Skip this section)"],
            index=0 if data.get("has_projects", True) and not data.get("skip_projects", False) else 1,
            key="builder_has_projects_radio",
            horizontal=True
        )

        if has_proj_choice == "No Technical Projects (Skip this section)":
            data["has_projects"] = False
            data["skip_projects"] = True
            data["projects"] = ""
            st.info("ℹ️ You have chosen to skip the Technical Project section. Your final resume will cleanly omit this section without leaving any empty space or placeholder.")
        else:
            data["has_projects"] = True
            data["skip_projects"] = False

            if "project_entries" not in data or not isinstance(data.get("project_entries"), list) or not data["project_entries"]:
                data["project_entries"] = [
                    {"name": "", "tech_stack": "", "description": ""}
                ]

            del_proj_indices = []
            for p_idx, proj in enumerate(data["project_entries"]):
                proj_title = proj.get("name", "").strip() or f"Technical Project #{p_idx + 1}"
                with st.container():
                    cp_head, cp_del = st.columns([5, 1])
                    with cp_head:
                        st.markdown(f"**💻 {proj_title}**")
                    with cp_del:
                        if len(data["project_entries"]) > 1:
                            if st.button("🗑️ Remove", key=f"btn_del_proj_{p_idx}"):
                                del_proj_indices.append(p_idx)

                    c1, c2 = st.columns(2)
                    with c1:
                        proj["name"] = st.text_input(
                            "Project Name:",
                            value=st.session_state.get(f"proj_name_{p_idx}", proj.get("name", "")),
                            placeholder="e.g. Distributed Task Queue",
                            key=f"proj_name_{p_idx}"
                        )
                    with c2:
                        proj["tech_stack"] = st.text_input(
                            "Technologies Used (Languages, Frameworks, Tools):",
                            value=st.session_state.get(f"proj_stack_{p_idx}", proj.get("tech_stack", "")),
                            placeholder="e.g. Python, Redis, Docker, FastAPI",
                            key=f"proj_stack_{p_idx}"
                        )

                    proj["description"] = st.text_area(
                        "Project Description (Explain what the project is, what it does, and your technical role):",
                        value=st.session_state.get(f"proj_desc_{p_idx}", proj.get("description", "")),
                        height=95,
                        placeholder="Describe what the project does, key features, and your technical implementation. It will appear as a clean normal paragraph below the project name.",
                        key=f"proj_desc_{p_idx}"
                    )
                    st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px dashed #CBD5E0;'/>", unsafe_allow_html=True)

            if del_proj_indices:
                for di in sorted(del_proj_indices, reverse=True):
                    data["project_entries"].pop(di)
                st.rerun()

            if st.button("➕ Add Another Project", key="btn_add_another_proj"):
                data["project_entries"].append({
                    "name": "",
                    "tech_stack": "",
                    "description": ""
                })
                st.rerun()

            # Compile project entries into data["projects"]
            compiled_proj = ResumeBuilderModel.compile_project_entries(data.get("project_entries", []))
            if compiled_proj:
                data["projects"] = compiled_proj

            st.markdown(
                """
                <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; color: #166534; margin-top: 8px;">
                    <strong>💡 Professional Formatting:</strong> On the final resume paper, each Project Name appears as a bullet-point-style heading (<code>• Project Name | Technologies Used: ...</code>). The project description appears as a clean normal paragraph directly below the project name.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_9", use_container_width=True):
                st.session_state.builder_step = 8
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_9", use_container_width=True):
                if data.get("skip_projects", False):
                    data["projects"] = ""
                    data["project_entries"] = []
                else:
                    valid_projs = [
                        p for p in data.get("project_entries", [])
                        if any([p.get("name", "").strip(), p.get("tech_stack", "").strip(), p.get("description", "").strip()])
                    ]
                    data["project_entries"] = valid_projs
                    if valid_projs:
                        data["project_entries"] = ResumeBuilderModel.enhance_project_entries(valid_projs)
                        data["projects"] = ResumeBuilderModel.compile_project_entries(data["project_entries"])
                    else:
                        data["projects"] = ""
                st.session_state.builder_step = 10
                st.rerun()

    # -------------------------------------------------------------
    # STEP 10: ADDITIONAL INFORMATION & CUSTOM SECTIONS
    # -------------------------------------------------------------
    elif current_step == 10:
        col_cert_head, col_cert_btn = st.columns([3, 1])
        with col_cert_head:
            st.markdown("### Additional Information")
            st.caption("Add certifications, leadership roles, or custom sections.")
        with col_cert_btn:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Enhance Writing", key="btn_enhance_cert", use_container_width=True, help="Polish certifications formatting"):
                current_cert = st.session_state.get("builder_cert_input", data.get("certifications", "")).strip()
                if current_cert:
                    enhanced_cert = ResumeBuilderModel.enhance_custom_section(current_cert)
                    st.session_state["builder_cert_input"] = enhanced_cert
                    data["certifications"] = enhanced_cert
                    st.success("✅ Certifications formatted professionally!")
                    st.rerun()
                else:
                    st.warning("Please enter certifications first before enhancing.")

        data["certifications"] = st.text_area(
            "Certifications & Courses (Optional):",
            value=st.session_state.get("builder_cert_input", data.get("certifications", "")),
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
                            value=st.session_state.get(f"cs_title_{idx}", sec.get("title", "")),
                            placeholder="e.g. Leadership, Languages, Publications",
                            key=f"cs_title_{idx}"
                        )
                        sec["title"] = sec_title
                    with col_enh_s:
                        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("✨ Enhance Writing", key=f"btn_cs_enh_{idx}", use_container_width=True):
                            current_cs = st.session_state.get(f"cs_content_{idx}", sec.get("content", "")).strip()
                            if current_cs:
                                enhanced_cs = ResumeBuilderModel.enhance_custom_section(current_cs)
                                st.session_state[f"cs_content_{idx}"] = enhanced_cs
                                sec["content"] = enhanced_cs
                                st.success(f"✅ Enhanced '{sec_title or 'Section'}'!")
                                st.rerun()
                    with col_del:
                        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Remove", key=f"cs_del_{idx}", use_container_width=True):
                            indices_to_remove.append(idx)

                    sec_content = st.text_area(
                        f"Section Content #{idx + 1}:",
                        value=st.session_state.get(f"cs_content_{idx}", sec.get("content", "")),
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
            if st.button("← Back", key="btn_bld_back_10", use_container_width=True):
                st.session_state.builder_step = 9
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_10", use_container_width=True):
                st.session_state.builder_step = 11
                st.rerun()

    # -------------------------------------------------------------
    # STEP 11: DECLARATION, DATE & SIGNATURE
    # -------------------------------------------------------------
    elif current_step == 11:
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
            st.markdown("#### Date & Place")
            data["date_val"] = st.text_input("Date:", value=data.get("date_val", ""), placeholder="e.g. October 15, 2026", key="bld_date_input")
            if not data["date_val"]:
                st.caption("Will render as: `Date: ____________________`")

            data["place_val"] = st.text_input("Place / City:", value=data.get("place_val", data.get("location", "")), placeholder="e.g. San Francisco, CA / New Delhi", key="bld_place_input")
            if not data["place_val"]:
                st.caption("Will render as: `Place: ____________________`")

        with col_s:
            st.markdown("#### Signature & Name")
            
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
                st.info("A clean single signature line (`Signature: ____________________`) will be included for physical hand signing after printing.")

            # Full Name Display
            st.markdown(f"<div style='margin-top: 10px; font-size: 0.9rem; color: #4A5568;'><strong>Candidate Name:</strong> {data.get('full_name', 'Not provided')}</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_11", use_container_width=True):
                st.session_state.builder_step = 10
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_11", use_container_width=True):
                st.session_state.builder_step = 12
                st.rerun()

    # -------------------------------------------------------------
    # STEP 12: TEMPLATE SELECTION (10 ATS-FRIENDLY TEMPLATES)
    # -------------------------------------------------------------
    elif current_step == 12:
        st.markdown("### Template Selection")
        st.caption("Select from 10 professionally designed templates. Each template displays its picture preview and name directly below.")

        current_tpl = data.get("template_name", "Modern")

        tpl_cols = st.columns(3)
        for i, (tpl_key, tpl_info) in enumerate(TEMPLATES_INFO.items()):
            col_target = tpl_cols[i % 3]
            with col_target:
                st.markdown(f"#### {tpl_info['name']}")
                st.markdown(tpl_info["preview_svg"], unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: #2D3748; margin-top: 6px; margin-bottom: 2px;'>{tpl_info['name']} Template</div>", unsafe_allow_html=True)
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
            if st.button("← Back", key="btn_bld_back_12", use_container_width=True):
                st.session_state.builder_step = 11
                st.rerun()
        with col_next:
            if st.button("Next: Create & Preview Resume →", type="primary", key="btn_bld_next_12", use_container_width=True):
                tailored = ResumeBuilderModel.tailor_content(data)
                st.session_state.builder_data.update(tailored)
                st.session_state.builder_step = 13
                st.rerun()

    # -------------------------------------------------------------
    # STEP 13: RESUME PREVIEW & REVIEW CONTROLS
    # -------------------------------------------------------------
    elif current_step == 13:
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
                st.session_state.builder_step = 12
                st.rerun()
        with col_act3:
            if st.button("✅ Accept Resume", type="primary", use_container_width=True):
                st.session_state.builder_accepted = True
                st.session_state.builder_step = 14
                st.rerun()

        # Visual Pie Graph: Resume Section Breakdown & Completeness
        st.markdown("---")
        st.markdown("### 📊 Resume Section Breakdown & Completeness")
        st.caption("Visual pie graph showing your completed resume sections and structure summary.")
        render_builder_section_breakdown_pie_chart(data)

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
            if st.button("← Back", key="btn_bld_back_13", use_container_width=True):
                st.session_state.builder_step = 12
                st.rerun()
        with col_next:
            if st.button("Next: Finalize & Download →", type="primary", key="btn_bld_next_13", use_container_width=True):
                st.session_state.builder_accepted = True
                st.session_state.builder_step = 14
                st.rerun()

    # -------------------------------------------------------------
    # STEP 14: FINAL RESUME & DOWNLOADS
    # -------------------------------------------------------------
    elif current_step == 14:
        st.markdown("### Final Resume")
        if data.get("job_description"):
            st.success("### “Your resume has been updated based on your selected job role, company, and job description.”")
        else:
            st.success("### “Your resume has been updated based on your selected job role and company.”")

        st.caption("You have complete control over your resume. You can edit any details or change the template at any time.")

        # Visual Pie Graph: Resume Section Breakdown & Completeness
        st.markdown("---")
        st.markdown("### 📊 Resume Section Breakdown & Completeness")
        st.caption("Visual pie graph summarizing all sections included in your final resume.")
        render_builder_section_breakdown_pie_chart(data)
        st.markdown("---")

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
            if st.button("← Back to Edit", key="btn_bld_back_14", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()
        with col_next:
            if st.button("Switch Template", key="btn_bld_next_14", use_container_width=True):
                st.session_state.builder_step = 12
                st.rerun()

        st.markdown("")
        with st.expander("Preview Resume", expanded=True):
            html_preview = render_resume_html(
                data=data,
                template_name=data.get("template_name", "Modern"),
                photo_b64=st.session_state.builder_photo_b64
            )
            components.html(html_preview, height=950, scrolling=True)
