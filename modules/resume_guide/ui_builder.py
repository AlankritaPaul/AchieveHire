"""
Page-wise UI flow for 'Create Resume' in AscendCareer Resume Guide.
Each selection has its own dedicated page.
Bottom navigation consistently provides:
- Left side below: Back clickable option
- Right side below: Next clickable option
"""

import streamlit as st
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
        "5. Education",
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
            st.caption("Upload a photograph if desired for your template. You are never forced to upload one.")
            
            photo_file = st.file_uploader("Upload Photo (PNG/JPG):", type=["png", "jpg", "jpeg"], key="builder_photo_upload")
            if photo_file:
                b64 = base64.b64encode(photo_file.read()).decode("utf-8")
                st.session_state.builder_photo_b64 = b64
                data["photo_b64"] = b64
                st.success("Photo uploaded.")

            if st.session_state.builder_photo_b64:
                st.image(f"data:image/jpeg;base64,{st.session_state.builder_photo_b64}", width=100)
                if st.button("Remove Photo", key="btn_remove_photo"):
                    st.session_state.builder_photo_b64 = ""
                    data["photo_b64"] = ""
                    st.rerun()

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
    # STEP 5: EDUCATION
    # -------------------------------------------------------------
    elif current_step == 5:
        st.markdown("### Education")
        st.caption("Provide your education details. Skip if not applicable.")

        data["education"] = st.text_area(
            "Education Details:",
            value=data.get("education", ""),
            height=150,
            placeholder="• B.S. in Computer Science | State University | 2020 - 2024\n• High School Diploma | City High | 2018 - 2020",
            key="builder_edu_input"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_5", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_5", use_container_width=True):
                st.session_state.builder_step = 6
                st.rerun()

    # -------------------------------------------------------------
    # STEP 6: SKILLS
    # -------------------------------------------------------------
    elif current_step == 6:
        st.markdown("### Skills")
        st.caption("List your skills. The system will only include skills you provide and will not invent any.")

        data["skills"] = st.text_area(
            "List your skills:",
            value=data.get("skills", ""),
            height=150,
            placeholder="Python, Java, React, SQL, Docker, Git, REST APIs, Problem Solving",
            key="builder_skills_input"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_6", use_container_width=True):
                st.session_state.builder_step = 5
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_6", use_container_width=True):
                st.session_state.builder_step = 7
                st.rerun()

    # -------------------------------------------------------------
    # STEP 7: WORK EXPERIENCE
    # -------------------------------------------------------------
    elif current_step == 7:
        st.markdown("### Work Experience & Internships")
        st.caption("List your work experience or internships. You may skip this if you do not have work experience.")

        data["experience"] = st.text_area(
            "Work Experience:",
            value=data.get("experience", ""),
            height=200,
            placeholder="Junior Developer | TechCorp Solutions | Jun 2023 - Present\n• Developed backend services in Python and SQL.\n• Maintained REST APIs and server logging.",
            key="builder_exp_input"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_7", use_container_width=True):
                st.session_state.builder_step = 6
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_7", use_container_width=True):
                st.session_state.builder_step = 8
                st.rerun()

    # -------------------------------------------------------------
    # STEP 8: PROJECTS
    # -------------------------------------------------------------
    elif current_step == 8:
        st.markdown("### Projects")
        st.caption("Provide projects that showcase your hands-on ability.")

        data["projects"] = st.text_area(
            "Project Details:",
            value=data.get("projects", ""),
            height=180,
            placeholder="E-Commerce Web App | Python, FastAPI, SQLite\n• Built an online store with product catalog and checkout cart.\n• Deployed live demo at github.com/username/project.",
            key="builder_proj_input"
        )

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_bld_back_8", use_container_width=True):
                st.session_state.builder_step = 7
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_bld_next_8", use_container_width=True):
                st.session_state.builder_step = 9
                st.rerun()

    # -------------------------------------------------------------
    # STEP 9: ADDITIONAL INFORMATION & CUSTOM SECTIONS
    # -------------------------------------------------------------
    elif current_step == 9:
        st.markdown("### Additional Information")
        st.caption("Add certifications, leadership roles, or custom sections.")

        data["certifications"] = st.text_area(
            "Certifications & Courses (Optional):",
            value=data.get("certifications", ""),
            height=100,
            placeholder="• AWS Certified Cloud Practitioner\n• Meta Frontend Developer Certificate",
            key="builder_cert_input"
        )

        st.markdown("#### Add Other Information")
        st.caption("Add any other section with your own appropriate section title.")

        with st.expander("➕ Add Other Information Section", expanded=False):
            new_title = st.text_input("Section Title:", placeholder="e.g. Leadership / Positions of Responsibility, Languages, Hobbies")
            new_content = st.text_area("Section Content:", placeholder="Enter details...")
            if st.button("Add Section"):
                if new_title.strip() and new_content.strip():
                    data["custom_sections"].append({
                        "title": new_title.strip(),
                        "content": new_content.strip()
                    })
                    st.success(f"Added section: {new_title}")
                    st.rerun()

        if data.get("custom_sections"):
            st.markdown("**Added Custom Sections:**")
            for idx, sec in enumerate(data["custom_sections"]):
                c_title, c_del = st.columns([4, 1])
                with c_title:
                    st.markdown(f"**{sec['title']}**\n{sec['content']}")
                with c_del:
                    if st.button(f"🗑️ Remove", key=f"del_custom_{idx}"):
                        data["custom_sections"].pop(idx)
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
        st.caption("Every generated resume includes a declaration section.")

        st.markdown("#### Declaration")
        data["declaration"] = st.text_area(
            "Declaration (Editable):",
            value=data.get("declaration", DEFAULT_DECLARATION),
            height=100,
            key="builder_dec_input"
        )

        col_d, col_s = st.columns(2)
        with col_d:
            st.markdown("#### Date")
            data["date_val"] = st.text_input("Date:", value=data.get("date_val", ""), placeholder="e.g. October 15, 2026")
            if not data["date_val"]:
                st.caption("Will render as: `Date: ____________________`")

        with col_s:
            st.markdown("#### Signature")
            data["sig_val"] = st.text_input("Signature:", value=data.get("sig_val", ""), placeholder="e.g. Alex Morgan")
            if not data["sig_val"]:
                st.caption("Will render as: `Signature: ____________________`")

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
        st.markdown(html_preview, unsafe_allow_html=True)

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
            st.markdown(html_preview, unsafe_allow_html=True)
