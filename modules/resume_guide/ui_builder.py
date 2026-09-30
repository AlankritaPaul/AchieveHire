"""
Page-wise UI flow for 'Create Resume' in AscendCareer Resume Guide.
Provides complete wizard with user data collection, privacy controls, custom sections,
photo upload, mandatory declaration with date and signature, 6 visual templates,
and comprehensive preview/edit/download controls.
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
        "1. Target Position",
        "2. Personal & Photo",
        "3. Education",
        "4. Skills",
        "5. Experience",
        "6. Projects",
        "7. Additional Info",
        "8. Declaration & Signature",
        "9. Template Selection",
        "10. Preview & Review",
        "11. Final Resume & Download"
    ]

    current_step = st.session_state.builder_step
    
    st.markdown("""
        <div style="background-color: #EDF2F7; border-radius: 8px; padding: 10px 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <div><strong style="color: #2B6CB0;">Path:</strong> Create Resume</div>
            <div style="font-size: 0.9rem; color: #4A5568;">Step %d of 11: <strong>%s</strong></div>
        </div>
    """ % (current_step, steps_labels[current_step - 1]), unsafe_allow_html=True)

    # -------------------------------------------------------------
    # STEP 1: TARGET POSITION & COMPANY
    # -------------------------------------------------------------
    if current_step == 1:
        st.markdown("### Step 1: Target Position & Company")
        st.caption("Tell us what role and organization you are preparing for so your resume can be professionally tailored.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Target Job Role")
            role_choice = st.radio(
                "How would you like to set your Job Role?",
                options=["Select a Job Role", "Write Your Job Role"],
                key="builder_role_mode"
            )
            if role_choice == "Select a Job Role":
                selected_role = st.selectbox(
                    "Suggested Job Roles (Searchable):",
                    options=SUGGESTED_JOB_ROLES,
                    index=0,
                    key="builder_suggested_role"
                )
                data["job_role"] = selected_role
            else:
                custom_role = st.text_input(
                    "Write Your Job Role:",
                    value=data.get("job_role", ""),
                    placeholder="e.g. Machine Learning Systems Engineer",
                    key="builder_custom_role"
                )
                data["job_role"] = custom_role.strip() if custom_role.strip() else "Software Developer"
            st.info(f"Target Role: **{data['job_role']}**")

        with col2:
            st.markdown("#### Target Company")
            comp_choice = st.radio(
                "How would you like to set your Target Company?",
                options=["Select a Company", "Write Your Company"],
                key="builder_comp_mode"
            )
            if comp_choice == "Select a Company":
                selected_comp = st.selectbox(
                    "Suggested Companies / Types (Searchable):",
                    options=SUGGESTED_COMPANIES,
                    index=0,
                    key="builder_suggested_comp"
                )
                data["company"] = selected_comp
            else:
                custom_comp = st.text_input(
                    "Write Your Company:",
                    value=data.get("company", ""),
                    placeholder="e.g. Microsoft, Razorpay, Tech Innovators Ltd",
                    key="builder_custom_comp"
                )
                data["company"] = custom_comp.strip() if custom_comp.strip() else "General Tech Company"
            st.info(f"Target Company: **{data['company']}**")

        st.markdown("#### Job Description (Optional / Recommended)")
        jd_val = st.text_area(
            "Paste Target Job Description (if available):",
            value=data.get("job_description", ""),
            height=120,
            placeholder="Paste responsibilities and tech stack requirements from the job ad to tailor terminology...",
            key="builder_jd_input"
        )
        data["job_description"] = jd_val.strip()

        st.markdown("")
        if st.button("Continue to Personal Information →", type="primary", use_container_width=True):
            st.session_state.builder_step = 2
            st.rerun()

    # -------------------------------------------------------------
    # STEP 2: PERSONAL DETAILS & PHOTO
    # -------------------------------------------------------------
    elif current_step == 2:
        st.markdown("### Step 2: Personal Details & Photo")
        st.caption("Provide your contact information. You are free to skip any personal fields you prefer not to include.")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            data["full_name"] = st.text_input("Full Name:", value=data.get("full_name", ""), placeholder="e.g. Alex Morgan")
            data["email"] = st.text_input("Email Address:", value=data.get("email", ""), placeholder="e.g. alex.morgan@email.com")
            data["phone"] = st.text_input("Phone Number:", value=data.get("phone", ""), placeholder="e.g. +1 (555) 019-2834")
            data["location"] = st.text_input("Location / City, Country:", value=data.get("location", ""), placeholder="e.g. San Francisco, CA")

        with col_p2:
            st.markdown("#### Photo Section (Optional)")
            st.caption("Upload a professional headshot if desired for your template. Never forced.")
            
            photo_file = st.file_uploader("Upload Photo (PNG/JPG):", type=["png", "jpg", "jpeg"], key="builder_photo_upload")
            if photo_file:
                b64 = base64.b64encode(photo_file.read()).decode("utf-8")
                st.session_state.builder_photo_b64 = b64
                data["photo_b64"] = b64
                st.success("Photo uploaded successfully!")

            if st.session_state.builder_photo_b64:
                st.image(f"data:image/jpeg;base64,{st.session_state.builder_photo_b64}", width=100)
                if st.button("Remove Photo", key="btn_remove_photo"):
                    st.session_state.builder_photo_b64 = ""
                    data["photo_b64"] = ""
                    st.rerun()

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Step 1", use_container_width=True):
                st.session_state.builder_step = 1
                st.rerun()
        with col_n:
            if st.button("Continue to Education →", type="primary", use_container_width=True):
                st.session_state.builder_step = 3
                st.rerun()

    # -------------------------------------------------------------
    # STEP 3: EDUCATION
    # -------------------------------------------------------------
    elif current_step == 3:
        st.markdown("### Step 3: Education & Academic Qualifications")
        st.caption("List your degrees, institutions, and graduation years. You may skip if not applicable.")

        data["education"] = st.text_area(
            "Education Details (one institution per line or bullet):",
            value=data.get("education", ""),
            height=150,
            placeholder="• B.S. in Computer Science | University of California, Berkeley | 2020 - 2024 (GPA: 3.8/4.0)\n• High School Diploma | Central High School | 2018 - 2020",
            key="builder_edu_input"
        )

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Personal Details", use_container_width=True):
                st.session_state.builder_step = 2
                st.rerun()
        with col_n:
            if st.button("Continue to Skills →", type="primary", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()

    # -------------------------------------------------------------
    # STEP 4: SKILLS & CORE COMPETENCIES
    # -------------------------------------------------------------
    elif current_step == 4:
        st.markdown("### Step 4: Skills & Core Competencies")
        st.caption("Enter your actual technical, software, and functional skills. The system will never fabricate or assume skills you do not have.")

        data["skills"] = st.text_area(
            "List your skills (comma separated or bullet points):",
            value=data.get("skills", ""),
            height=150,
            placeholder="Python, Java, React, PostgreSQL, Docker, Git, REST APIs, Problem Solving, Data Structures",
            key="builder_skills_input"
        )

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Education", use_container_width=True):
                st.session_state.builder_step = 3
                st.rerun()
        with col_n:
            if st.button("Continue to Work Experience →", type="primary", use_container_width=True):
                st.session_state.builder_step = 5
                st.rerun()

    # -------------------------------------------------------------
    # STEP 5: WORK EXPERIENCE & INTERNSHIPS
    # -------------------------------------------------------------
    elif current_step == 5:
        st.markdown("### Step 5: Work Experience & Internships")
        st.caption("List your professional work history, internships, or freelancing. If you are a fresher or entry-level candidate, you can leave this blank.")

        data["experience"] = st.text_area(
            "Work Experience (Titles, Companies, Dates, Bullet points):",
            value=data.get("experience", ""),
            height=200,
            placeholder="Software Engineering Intern | TechCorp Inc. | Jun 2023 - Aug 2023\n• Built automated data pipelines using Python and SQL.\n• Collaborated with frontend team to integrate REST APIs.",
            key="builder_exp_input"
        )

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Skills", use_container_width=True):
                st.session_state.builder_step = 4
                st.rerun()
        with col_n:
            if st.button("Continue to Projects →", type="primary", use_container_width=True):
                st.session_state.builder_step = 6
                st.rerun()

    # -------------------------------------------------------------
    # STEP 6: PROJECTS
    # -------------------------------------------------------------
    elif current_step == 6:
        st.markdown("### Step 6: Projects")
        st.caption("Highlight academic, open-source, or personal projects that showcase your practical abilities.")

        data["projects"] = st.text_area(
            "Project Details (Title, Tech Stack, What you built):",
            value=data.get("projects", ""),
            height=180,
            placeholder="E-Commerce Microservices Platform | Python, FastAPI, Docker, PostgreSQL\n• Designed scalable RESTful services supporting customer authentication and payment processing.\n• Deployed live demo at github.com/username/project.",
            key="builder_proj_input"
        )

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Experience", use_container_width=True):
                st.session_state.builder_step = 5
                st.rerun()
        with col_n:
            if st.button("Continue to Additional Information →", type="primary", use_container_width=True):
                st.session_state.builder_step = 7
                st.rerun()

    # -------------------------------------------------------------
    # STEP 7: ADDITIONAL SECTIONS & CUSTOM INFORMATION
    # -------------------------------------------------------------
    elif current_step == 7:
        st.markdown("### Step 7: Certifications & Additional Information")
        st.caption("Add certifications, leadership roles, languages, or any custom information relevant to your profile.")

        data["certifications"] = st.text_area(
            "Certifications & Courses (Optional):",
            value=data.get("certifications", ""),
            height=100,
            placeholder="• AWS Certified Cloud Practitioner (2023)\n• Meta Front-End Developer Professional Certificate (Coursera)",
            key="builder_cert_input"
        )

        st.markdown("#### Add Other Information")
        st.caption("You are not restricted to predefined sections. Add any custom section with your own title.")

        with st.expander("➕ Add New Custom Section", expanded=False):
            new_title = st.text_input("Custom Section Title:", placeholder="e.g. Leadership & Volunteering, Publications, Languages")
            new_content = st.text_area("Custom Section Content:", placeholder="Enter details for this section...")
            if st.button("Save Custom Section"):
                if new_title.strip() and new_content.strip():
                    data["custom_sections"].append({
                        "title": new_title.strip(),
                        "content": new_content.strip()
                    })
                    st.success(f"Added section: {new_title}")
                    st.rerun()

        # Display existing custom sections
        if data.get("custom_sections"):
            st.markdown("**Your Custom Sections:**")
            for idx, sec in enumerate(data["custom_sections"]):
                c_title, c_del = st.columns([4, 1])
                with c_title:
                    st.markdown(f"**{sec['title']}**\n{sec['content']}")
                with c_del:
                    if st.button(f"🗑️ Remove", key=f"del_custom_{idx}"):
                        data["custom_sections"].pop(idx)
                        st.rerun()

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Projects", use_container_width=True):
                st.session_state.builder_step = 6
                st.rerun()
        with col_n:
            if st.button("Continue to Declaration & Signature →", type="primary", use_container_width=True):
                st.session_state.builder_step = 8
                st.rerun()

    # -------------------------------------------------------------
    # STEP 8: DECLARATION, DATE & SIGNATURE
    # -------------------------------------------------------------
    elif current_step == 8:
        st.markdown("### Step 8: Declaration, Date & Signature")
        st.caption("The declaration is a mandatory section verifying the authenticity of your resume details.")

        st.markdown("#### Declaration")
        data["declaration"] = st.text_area(
            "Declaration Statement (Editable):",
            value=data.get("declaration", DEFAULT_DECLARATION),
            height=100,
            key="builder_dec_input"
        )

        col_d, col_s = st.columns(2)
        with col_d:
            st.markdown("#### Date")
            data["date_val"] = st.text_input("Date (or leave blank for underline):", value=data.get("date_val", ""), placeholder="e.g. October 15, 2026")
            if not data["date_val"]:
                st.caption("Will render as placeholder line: `Date: ____________________`")

        with col_s:
            st.markdown("#### Signature")
            data["sig_val"] = st.text_input("Signature Name (or leave blank for underline):", value=data.get("sig_val", ""), placeholder="e.g. Alex Morgan")
            if not data["sig_val"]:
                st.caption("Will render as placeholder line: `Signature: ____________________`")

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Additional Info", use_container_width=True):
                st.session_state.builder_step = 7
                st.rerun()
        with col_n:
            if st.button("Continue to Template Selection →", type="primary", use_container_width=True):
                st.session_state.builder_step = 9
                st.rerun()

    # -------------------------------------------------------------
    # STEP 9: TEMPLATE SELECTION (VISUAL PREVIEWS)
    # -------------------------------------------------------------
    elif current_step == 9:
        st.markdown("### Step 9: Choose Your Resume Template")
        st.caption("Select the visual style for your resume. Each template provides a unique typography, color palette, and layout.")

        current_tpl = data.get("template_name", "Modern")

        tpl_cols = st.columns(3)
        for i, (tpl_key, tpl_info) in enumerate(TEMPLATES_INFO.items()):
            col_target = tpl_cols[i % 3]
            with col_target:
                st.markdown(f"#### {tpl_info['name']}")
                # Render visual SVG/HTML preview picture
                st.markdown(tpl_info["preview_svg"], unsafe_allow_html=True)
                st.caption(tpl_info["description"])

                is_selected = (current_tpl == tpl_key)
                btn_label = "✅ Selected" if is_selected else f"Select {tpl_info['name']}"
                if st.button(btn_label, key=f"sel_tpl_{tpl_key}", use_container_width=True):
                    data["template_name"] = tpl_key
                    st.rerun()

        st.markdown("---")
        st.info(f"Active Selected Template: **{data.get('template_name', 'Modern')}**")

        col_b, col_n = st.columns(2)
        with col_b:
            if st.button("← Back to Declaration & Signature", use_container_width=True):
                st.session_state.builder_step = 8
                st.rerun()
        with col_n:
            if st.button("Generate & Preview Resume →", type="primary", use_container_width=True):
                # Tailor content without inventing facts
                tailored = ResumeBuilderModel.tailor_content(data)
                st.session_state.builder_data.update(tailored)
                st.session_state.builder_step = 10
                st.rerun()

    # -------------------------------------------------------------
    # STEP 10: COMPLETE RESUME PREVIEW & REVIEW CONTROLS
    # -------------------------------------------------------------
    elif current_step == 10:
        st.markdown("### Step 10: Complete Resume Preview & Review")
        st.caption("Review your complete resume rendered in the " + data.get("template_name", "Modern") + " template. You have full editing rights.")

        # Action Buttons row: Edit Resume, Change Template, Accept Resume
        col_act1, col_act2, col_act3 = st.columns(3)
        with col_act1:
            if st.button("✎ Edit Resume", use_container_width=True):
                st.session_state.builder_step = 2
                st.rerun()
        with col_act2:
            if st.button("🎨 Change Template", use_container_width=True):
                st.session_state.builder_step = 9
                st.rerun()
        with col_act3:
            if st.button("✅ Accept Resume", type="primary", use_container_width=True):
                st.session_state.builder_accepted = True
                st.session_state.builder_step = 11
                st.rerun()

        st.markdown("")
        # Render HTML Resume Preview in exact template
        html_preview = render_resume_html(
            data=data,
            template_name=data.get("template_name", "Modern"),
            photo_b64=st.session_state.builder_photo_b64
        )
        st.markdown(html_preview, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # STEP 11: FINAL RESUME & DOWNLOADS
    # -------------------------------------------------------------
    elif current_step == 11:
        st.markdown("### Step 11: Final Resume & Downloads")
        if data.get("job_description"):
            st.success("### “Your resume has been created and tailored based on your selected job role, company, and job description.”")
        else:
            st.success("### “Your resume has been created and tailored based on your selected job role and company.”")

        st.caption("You maintain ongoing control over your resume. You can edit any details or switch templates anytime.")

        # Download Buttons
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
                label="📥 Download Text (.txt)",
                data=plain_text,
                file_name=f"{data.get('full_name', 'Resume').replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown("---")
        # Final Controls: Edit Resume or Change Template
        col_end1, col_end2 = st.columns(2)
        with col_end1:
            if st.button("✎ Edit Resume Details", use_container_width=True):
                st.session_state.builder_step = 2
                st.rerun()
        with col_end2:
            if st.button("🎨 Switch to Another Template", use_container_width=True):
                st.session_state.builder_step = 9
                st.rerun()

        st.markdown("")
        with st.expander("👁️ View Full Resume Preview", expanded=True):
            html_preview = render_resume_html(
                data=data,
                template_name=data.get("template_name", "Modern"),
                photo_b64=st.session_state.builder_photo_b64
            )
            st.markdown(html_preview, unsafe_allow_html=True)
