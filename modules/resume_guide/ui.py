"""
Streamlit UI implementation for the AscendCareer Resume Guide.
Faithfully implements the complete user flow requested with state management and exact messaging.
"""

import streamlit as st
from typing import Dict, Any, Optional
from modules.constants import SUGGESTED_JOB_ROLES, SUGGESTED_COMPANIES
from modules.resume_guide.parser import extract_text_from_file, parse_resume_sections
from modules.resume_guide.analyzer import ResumeAnalyzer
from modules.resume_guide.optimizer import ResumeOptimizer
from modules.resume_guide.exporter import export_resume_to_pdf, export_resume_to_docx

def render_resume_guide():
    """Render the complete Resume Guide section."""
    st.markdown("""
        <style>
        .module-header {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1A365D;
            margin-bottom: 0.2rem;
        }
        .module-sub {
            font-size: 1.05rem;
            color: #4A5568;
            margin-bottom: 1.5rem;
        }
        .custom-card {
            background-color: #F7FAFC;
            border-radius: 10px;
            padding: 1.25rem;
            border: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }
        .metric-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .badge-green { background-color: #C6F6D5; color: #22543D; }
        .badge-amber { background-color: #FEEBC8; color: #7B341E; }
        .badge-blue { background-color: #BEE3F8; color: #2B6CB0; }
        .diff-before {
            background-color: #FFF5F5;
            border-left: 4px solid #E53E3E;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
        }
        .diff-after {
            background-color: #F0FFF4;
            border-left: 4px solid #38A169;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="module-header">📄 Resume Guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-sub">Analyze your resume, identify gaps against your target role & company, and optimize content while maintaining 100% factual accuracy.</div>', unsafe_allow_html=True)

    # Initialize session state keys
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "raw_resume_text" not in st.session_state:
        st.session_state.raw_resume_text = ""
    if "parsed_sections" not in st.session_state:
        st.session_state.parsed_sections = {}
    if "show_suggestions" not in st.session_state:
        st.session_state.show_suggestions = False
    if "show_improvements" not in st.session_state:
        st.session_state.show_improvements = False
    if "improvements_list" not in st.session_state:
        st.session_state.improvements_list = []
    if "user_decisions" not in st.session_state:
        st.session_state.user_decisions = {}
    if "final_resume_generated" not in st.session_state:
        st.session_state.final_resume_generated = False
    if "final_resume_text" not in st.session_state:
        st.session_state.final_resume_text = ""

    # ==========================================
    # STEP 1: INPUT FORM
    # ==========================================
    with st.container():
        st.markdown("### 1. Resume Analysis")
        st.caption("Provide your target details and upload your resume to begin.")

        col_role, col_comp = st.columns(2)

        # A. Job Role (Both options remain available)
        with col_role:
            st.markdown("#### A. Job Role")
            role_mode = st.radio(
                "How would you like to set your Job Role?",
                options=["Select a Job Role", "Write Your Job Role"],
                key="role_mode_choice"
            )

            if role_mode == "Select a Job Role":
                selected_role = st.selectbox(
                    "Suggested Job Roles (Searchable):",
                    options=SUGGESTED_JOB_ROLES,
                    index=0,
                    key="suggested_role_select"
                )
                active_job_role = selected_role
            else:
                custom_role = st.text_input(
                    "Write Your Job Role:",
                    placeholder="e.g. Senior Distributed Systems Engineer",
                    key="custom_role_input"
                )
                active_job_role = custom_role.strip() if custom_role.strip() else "Software Developer"

            st.info(f"Target Role: **{active_job_role}**")

        # B. Company (Both options remain available)
        with col_comp:
            st.markdown("#### B. Company")
            company_mode = st.radio(
                "How would you like to set your Target Company?",
                options=["Select a Company", "Write Your Company"],
                key="company_mode_choice"
            )

            if company_mode == "Select a Company":
                selected_company = st.selectbox(
                    "Suggested Companies / Types (Searchable):",
                    options=SUGGESTED_COMPANIES,
                    index=0,
                    key="suggested_company_select"
                )
                active_company = selected_company
            else:
                custom_company = st.text_input(
                    "Write Your Company:",
                    placeholder="e.g. Stripe, OpenAI, My Local Tech Firm",
                    key="custom_company_input"
                )
                active_company = custom_company.strip() if custom_company.strip() else "General Tech Company"

            st.info(f"Target Company: **{active_company}**")

        # C. Job Description (Optional / Recommended)
        st.markdown("#### C. Job Description (Optional / Recommended)")
        jd_input = st.text_area(
            "Paste the target Job Description below if available. (If provided, your resume will be analyzed against it):",
            height=120,
            placeholder="Paste responsibilities, required qualifications, and key technologies from the job posting...",
            key="jd_text_area"
        )
        has_jd = bool(jd_input.strip())

        # D. Upload Resume
        st.markdown("#### D. Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload your current resume (PDF, DOCX, or TXT):",
            type=["pdf", "docx", "txt", "md"],
            key="resume_file_uploader"
        )

        submit_btn = st.button("Submit Resume for Review", type="primary", use_container_width=True)

        if submit_btn:
            if uploaded_file is None:
                st.error("Please upload a resume file before submitting.")
                return

            with st.spinner("Extracting text and analyzing resume alignment..."):
                raw_text = extract_text_from_file(uploaded_file)
                if not raw_text.strip():
                    st.error("Could not extract any readable text from the uploaded file. Please ensure it is not an empty or password-protected document.")
                    return

                sections = parse_resume_sections(raw_text)
                analyzer = ResumeAnalyzer(
                    job_role=active_job_role,
                    company=active_company,
                    job_description=jd_input.strip() if has_jd else None
                )
                analysis = analyzer.analyze(raw_text, sections)

                # Save into session state
                st.session_state.analysis_complete = True
                st.session_state.analysis_result = analysis
                st.session_state.raw_resume_text = raw_text
                st.session_state.parsed_sections = sections
                st.session_state.active_job_role = active_job_role
                st.session_state.active_company = active_company
                st.session_state.active_jd = jd_input.strip() if has_jd else None
                st.session_state.show_suggestions = False
                st.session_state.show_improvements = False
                st.session_state.improvements_list = []
                st.session_state.user_decisions = {}
                st.session_state.final_resume_generated = False
                st.success("Analysis complete! Review the results below.")

    # ==========================================
    # STEP 2: RESUME MATCH ANALYSIS DISPLAY
    # ==========================================
    if st.session_state.analysis_complete and st.session_state.analysis_result:
        res = st.session_state.analysis_result
        st.markdown("---")
        st.markdown("## Resume Match Analysis")
        st.caption(f"Evaluated against **{res['job_role']}** at **{res['company']}**" + (" with Job Description" if res['has_jd'] else " (No JD provided)"))

        # Top metric tiles
        if res["has_jd"]:
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Role Alignment", f"{res['role_alignment_score']}%")
            with col_m2:
                st.metric("JD Alignment", f"{res['jd_alignment_score']}%")
            with col_m3:
                st.metric("Skills Matched", f"{len(res['matched_skills'])}")
        else:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Role Alignment", f"{res['role_alignment_score']}%")
            with col_m2:
                st.metric("Skills Matched", f"{len(res['matched_skills'])}")

        # Skills Match Breakdown
        st.markdown("#### 🎯 Skills Match")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("**Identified in Resume:**")
            if res["matched_skills"]:
                matched_html = " ".join([f'<span class="metric-badge badge-green">{s}</span>' for s in res["matched_skills"]])
                st.markdown(matched_html, unsafe_allow_html=True)
            else:
                st.markdown("_No core technical skills for this role were identified in the resume text._")

        with col_s2:
            st.markdown("**Missing Keywords / Skills:**")
            if res["missing_skills"]:
                missing_html = " ".join([f'<span class="metric-badge badge-amber">{s}</span>' for s in res["missing_skills"]])
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.markdown("✅ _All major core competencies for this role are represented._")

        # Project & Experience Relevance
        st.markdown("#### 💼 Relevance Assessment")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"**Project Relevance:** ({res['project_relevance']['score']}/100)")
            st.write(res["project_relevance"]["summary"])
        with col_r2:
            st.markdown(f"**Experience Relevance:** ({res['experience_relevance']['score']}/100)")
            st.write(res["experience_relevance"]["summary"])

        # Section-wise Feedback
        st.markdown("#### 📋 Section-wise Feedback")
        for sec_name, fb_text in res["section_feedback"].items():
            with st.expander(f"Section: {sec_name}", expanded=True):
                st.write(fb_text)

        # ==========================================
        # STEP 3: OUTCOME BRANCHING
        # ==========================================
        st.markdown("---")
        if res["is_well_aligned"]:
            st.success("### “Your resume is well-aligned with this job role and effectively highlights the skills and experience required.”")
            st.info("No unnecessary improvements are required. Your resume meets the criteria for this position.")
        else:
            st.warning("### “Your resume needs some improvements to better match this job role.”")

            # High-level relevant areas (only when relevant!)
            if res["high_level_areas"]:
                st.markdown("**Recommended Improvement Focus Areas:**")
                for area in res["high_level_areas"]:
                    st.markdown(f"- **{area}**")

            # Two Options: View Suggestions and Improve Resume
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🔍 View Suggestions", use_container_width=True):
                    st.session_state.show_suggestions = True

            with col_b2:
                if st.button("✨ Improve Resume", type="primary", use_container_width=True):
                    optimizer = ResumeOptimizer(
                        job_role=res["job_role"],
                        company=res["company"],
                        job_description=st.session_state.active_jd
                    )
                    improvements = optimizer.generate_improvements(
                        st.session_state.parsed_sections,
                        res
                    )
                    st.session_state.improvements_list = improvements
                    st.session_state.show_improvements = True

    # ==========================================
    # VIEW SUGGESTIONS ACCORDION / VIEW
    # ==========================================
    if st.session_state.show_suggestions and st.session_state.analysis_result:
        res = st.session_state.analysis_result
        st.markdown("---")
        st.markdown("### 💡 Tailored Resume Suggestions")
        st.caption("Personalized findings based strictly on your specific resume content and target criteria.")

        if not res["suggestions"]:
            st.info("No specific critical weaknesses were found for your resume.")
        else:
            for idx, sugg in enumerate(res["suggestions"], 1):
                with st.container():
                    st.markdown(f"**{idx}. {sugg['title']}** `[{sugg['category']}]`")
                    st.markdown(f"**Observation:** {sugg['observation']}")
                    st.markdown(f"**Recommendation:** {sugg['recommendation']}")
                    st.markdown("")

    # ==========================================
    # IMPROVE RESUME: BEFORE / AFTER & DECISIONS
    # ==========================================
    if st.session_state.show_improvements and st.session_state.improvements_list:
        st.markdown("---")
        st.markdown("### ⚡ Resume Improvement Review")
        st.markdown("""
        Review each improved section below. In accordance with the **Accuracy Rule**, all factual data (skills, jobs, degrees, accomplishments) remains strictly truthful to your original resume.
        Choose whether to **Accept**, **Edit**, or **Keep Original** for each section.
        """)

        improvements = st.session_state.improvements_list

        for item in improvements:
            sec_key = item["section_key"]
            sec_title = item["section_title"]
            
            # Initialize decision state if not present
            if sec_key not in st.session_state.user_decisions:
                st.session_state.user_decisions[sec_key] = {
                    "decision": "accept",
                    "original": item["before"],
                    "improved": item["after"],
                    "edited": item["after"]
                }

            with st.container():
                st.markdown(f"#### Section: {sec_title}")
                st.caption(f"Rationale: {item['rationale']}")

                col_before, col_after = st.columns(2)
                with col_before:
                    st.markdown("**Before Improvement**")
                    st.markdown(f'<div class="diff-before">{item["before"]}</div>', unsafe_allow_html=True)

                with col_after:
                    st.markdown("**After Improvement**")
                    st.markdown(f'<div class="diff-after">{item["after"]}</div>', unsafe_allow_html=True)

                # Decision Controls
                choice = st.radio(
                    f"Choose action for {sec_title}:",
                    options=["✅ Accept", "✎ Edit", "↩ Keep Original"],
                    key=f"decision_radio_{sec_key}",
                    horizontal=True
                )

                if choice == "✅ Accept":
                    st.session_state.user_decisions[sec_key]["decision"] = "accept"
                elif choice == "↩ Keep Original":
                    st.session_state.user_decisions[sec_key]["decision"] = "keep_original"
                elif choice == "✎ Edit":
                    st.session_state.user_decisions[sec_key]["decision"] = "edit"
                    edited_val = st.text_area(
                        f"Modify the improved content for {sec_title}:",
                        value=st.session_state.user_decisions[sec_key]["edited"],
                        key=f"edit_area_{sec_key}",
                        height=140
                    )
                    st.session_state.user_decisions[sec_key]["edited"] = edited_val

                st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px dashed #CBD5E0;'/>", unsafe_allow_html=True)

        # Final generation trigger
        if st.button("Generate Final Updated Resume", type="primary", use_container_width=True):
            final_text = ResumeOptimizer.compile_final_resume(
                st.session_state.parsed_sections,
                st.session_state.user_decisions
            )
            st.session_state.final_resume_text = final_text
            st.session_state.final_resume_generated = True

    # ==========================================
    # STEP 4: FINAL UPDATED RESUME
    # ==========================================
    if st.session_state.final_resume_generated and st.session_state.final_resume_text:
        st.markdown("---")
        st.markdown("## Final Updated Resume")

        # Required confirmation message
        if st.session_state.active_jd:
            st.success("### “Your resume has been updated based on your selected job role, company, and job description.”")
        else:
            st.success("### “Your resume has been updated based on your selected job role and company.”")

        st.caption("Your original uploaded resume remains completely safe and untouched. You can preview and download the new version below.")

        preview_tab, text_tab = st.tabs(["Preview Updated Resume", "Raw Formatted Text"])

        with preview_tab:
            st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 2px solid #E2E8F0; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.95rem; color: #2D3748;">{st.session_state.final_resume_text}</pre>
                </div>
            """, unsafe_allow_html=True)

        with text_tab:
            st.text_area("Updated Resume Text:", value=st.session_state.final_resume_text, height=350)

        # Download options
        st.markdown("#### Download Resume")
        pdf_bytes = export_resume_to_pdf(st.session_state.final_resume_text, f"{st.session_state.active_job_role} Resume")
        docx_bytes = export_resume_to_docx(st.session_state.final_resume_text)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                label="📥 Download PDF Resume",
                data=pdf_bytes,
                file_name="AscendCareer_Updated_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label="📥 Download Word (.docx)",
                data=docx_bytes,
                file_name="AscendCareer_Updated_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with col_d3:
            st.download_button(
                label="📥 Download Plain Text (.txt)",
                data=st.session_state.final_resume_text,
                file_name="AscendCareer_Updated_Resume.txt",
                mime="text/plain",
                use_container_width=True
            )
