"""
Page-wise UI flow for Resume Analysis in AscendCareer Resume Guide.
Replaces single-page A,B,C,D headers with clean, dedicated page-by-page steps.
"""

import streamlit as st
from modules.constants import SUGGESTED_JOB_ROLES, SUGGESTED_COMPANIES
from modules.resume_guide.parser import extract_text_from_file, parse_resume_sections
from modules.resume_guide.analyzer import ResumeAnalyzer
from modules.resume_guide.optimizer import ResumeOptimizer
from modules.resume_guide.exporter import export_resume_to_pdf, export_resume_to_docx

def render_resume_analysis_flow():
    """Render the step-by-step page-wise flow for reviewing an existing resume."""
    if "analysis_step" not in st.session_state:
        st.session_state.analysis_step = 1

    # Breadcrumb / Step Indicator
    steps = [
        "1. Target Role & Company",
        "2. Job Description",
        "3. Upload & Review",
        "4. Analysis & Results"
    ]
    
    st.markdown("""
        <div style="background-color: #EDF2F7; border-radius: 8px; padding: 10px 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <div><strong style="color: #2B6CB0;">Path:</strong> Resume Analysis</div>
            <div style="font-size: 0.9rem; color: #4A5568;">Step %d of 4: <strong>%s</strong></div>
        </div>
    """ % (st.session_state.analysis_step, steps[st.session_state.analysis_step - 1]), unsafe_allow_html=True)

    # PAGE 1: TARGET ROLE & COMPANY
    if st.session_state.analysis_step == 1:
        st.markdown("### Step 1: Target Position & Company")
        st.caption("Specify your target job role and company so the analysis can evaluate alignment accurately.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Target Job Role")
            role_choice = st.radio(
                "Select method to specify Job Role:",
                options=["Select a Job Role", "Write Your Job Role"],
                key="analysis_role_mode"
            )
            if role_choice == "Select a Job Role":
                target_role = st.selectbox(
                    "Suggested Job Roles (Searchable):",
                    options=SUGGESTED_JOB_ROLES,
                    key="analysis_role_select"
                )
            else:
                target_role = st.text_input(
                    "Write Your Job Role:",
                    placeholder="e.g. Distributed Systems Engineer",
                    key="analysis_role_custom"
                )
            st.session_state.active_job_role = target_role.strip() if target_role and target_role.strip() else "Software Developer"
            st.info(f"Active Job Role: **{st.session_state.active_job_role}**")

        with col2:
            st.markdown("#### Target Company")
            comp_choice = st.radio(
                "Select method to specify Target Company:",
                options=["Select a Company", "Write Your Company"],
                key="analysis_comp_mode"
            )
            if comp_choice == "Select a Company":
                target_comp = st.selectbox(
                    "Suggested Companies / Types (Searchable):",
                    options=SUGGESTED_COMPANIES,
                    key="analysis_comp_select"
                )
            else:
                target_comp = st.text_input(
                    "Write Your Company:",
                    placeholder="e.g. Google, Microsoft, Local Tech Corp",
                    key="analysis_comp_custom"
                )
            st.session_state.active_company = target_comp.strip() if target_comp and target_comp.strip() else "General Tech Company"
            st.info(f"Active Target Company: **{st.session_state.active_company}**")

        st.markdown("")
        if st.button("Continue to Job Description →", type="primary", use_container_width=True):
            st.session_state.analysis_step = 2
            st.rerun()

    # PAGE 2: JOB DESCRIPTION
    elif st.session_state.analysis_step == 2:
        st.markdown("### Step 2: Job Description (Optional / Recommended)")
        st.caption("If you have the actual job description, paste it below. If you don't have one, you can proceed without it.")

        current_jd = st.session_state.get("active_jd", "") or ""
        jd_input = st.text_area(
            "Paste Target Job Description (Optional):",
            value=current_jd,
            height=200,
            placeholder="Paste responsibilities, required qualifications, and technologies here...",
            key="analysis_jd_textarea"
        )
        st.session_state.active_jd = jd_input.strip() if jd_input.strip() else None

        if st.session_state.active_jd:
            st.success("✅ Job Description provided. Resume will be analyzed against this specific posting.")
        else:
            st.info("ℹ️ No Job Description provided. Resume will be analyzed against general standards for " + st.session_state.get("active_job_role", "this role") + ".")

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back to Role & Company", use_container_width=True):
                st.session_state.analysis_step = 1
                st.rerun()
        with col_next:
            if st.button("Continue to Resume Upload →", type="primary", use_container_width=True):
                st.session_state.analysis_step = 3
                st.rerun()

    # PAGE 3: UPLOAD RESUME & REVIEW
    elif st.session_state.analysis_step == 3:
        st.markdown("### Step 3: Upload Resume")
        st.caption("Upload your current resume file to begin the match analysis.")

        uploaded_file = st.file_uploader(
            "Upload your resume file (.pdf, .docx, .txt):",
            type=["pdf", "docx", "txt", "md"],
            key="analysis_uploader_page"
        )

        st.markdown("""
            <div style="background: #F7FAFC; padding: 12px; border-radius: 6px; border: 1px solid #E2E8F0; margin: 15px 0;">
                <strong>Evaluation Summary:</strong><br>
                • <strong>Target Role:</strong> {role}<br>
                • <strong>Target Company:</strong> {comp}<br>
                • <strong>Job Description:</strong> {jd_status}
            </div>
        """.format(
            role=st.session_state.get("active_job_role", "Software Developer"),
            comp=st.session_state.get("active_company", "General Tech Company"),
            jd_status="Provided (" + str(len(st.session_state.active_jd.split())) + " words)" if st.session_state.get("active_jd") else "None provided"
        ), unsafe_allow_html=True)

        col_back, col_submit = st.columns(2)
        with col_back:
            if st.button("← Back to Job Description", use_container_width=True):
                st.session_state.analysis_step = 2
                st.rerun()

        with col_submit:
            submit_btn = st.button("Submit Resume for Review", type="primary", use_container_width=True)

        if submit_btn:
            if not uploaded_file:
                st.error("Please upload a resume file to proceed.")
                return

            with st.spinner("Analyzing resume against target criteria..."):
                raw_text = extract_text_from_file(uploaded_file)
                if not raw_text.strip():
                    st.error("Could not extract readable text from document. Please ensure it is not password protected.")
                    return

                sections = parse_resume_sections(raw_text)
                analyzer = ResumeAnalyzer(
                    job_role=st.session_state.active_job_role,
                    company=st.session_state.active_company,
                    job_description=st.session_state.active_jd
                )
                analysis = analyzer.analyze(raw_text, sections)

                st.session_state.analysis_complete = True
                st.session_state.analysis_result = analysis
                st.session_state.raw_resume_text = raw_text
                st.session_state.parsed_sections = sections
                st.session_state.show_suggestions = False
                st.session_state.show_improvements = False
                st.session_state.improvements_list = []
                st.session_state.user_decisions = {}
                st.session_state.final_resume_generated = False
                st.session_state.analysis_step = 4
                st.rerun()

    # PAGE 4: RESULTS, SUGGESTIONS & IMPROVEMENTS
    elif st.session_state.analysis_step == 4:
        if not st.session_state.get("analysis_result"):
            st.session_state.analysis_step = 3
            st.rerun()
            return

        res = st.session_state.analysis_result
        st.markdown("### Step 4: Resume Match Analysis")
        st.caption(f"Evaluated against **{res['job_role']}** at **{res['company']}**" + (" with Job Description" if res['has_jd'] else " (No JD provided)"))

        # Metrics row
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

        # Skills breakdown
        st.markdown("#### Skills Match")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("**Identified in Resume:**")
            if res["matched_skills"]:
                matched_html = " ".join([f'<span class="metric-badge badge-green">{s}</span>' for s in res["matched_skills"]])
                st.markdown(matched_html, unsafe_allow_html=True)
            else:
                st.markdown("_No core technical skills for this role were identified._")

        with col_s2:
            st.markdown("**Missing Keywords / Skills:**")
            if res["missing_skills"]:
                missing_html = " ".join([f'<span class="metric-badge badge-amber">{s}</span>' for s in res["missing_skills"]])
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.markdown("✅ _All major core competencies for this role are represented._")

        # Relevance
        st.markdown("#### Relevance Assessment")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"**Project Relevance:** ({res['project_relevance']['score']}/100)")
            st.write(res["project_relevance"]["summary"])
        with col_r2:
            st.markdown(f"**Experience Relevance:** ({res['experience_relevance']['score']}/100)")
            st.write(res["experience_relevance"]["summary"])

        # Section-wise feedback
        st.markdown("#### Section-wise Feedback")
        for sec_name, fb_text in res["section_feedback"].items():
            with st.expander(f"Section: {sec_name}", expanded=False):
                st.write(fb_text)

        # Outcome Branching
        st.markdown("---")
        if res["is_well_aligned"]:
            st.success("### “Your resume is well-aligned with this job role and effectively highlights the skills and experience required.”")
            st.info("No unnecessary improvements are required. Your resume meets the criteria for this position.")
        else:
            st.warning("### “Your resume needs some improvements to better match this job role.”")
            if res["high_level_areas"]:
                st.markdown("**Recommended Improvement Focus Areas:**")
                for area in res["high_level_areas"]:
                    st.markdown(f"- **{area}**")

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

        # View Suggestions
        if st.session_state.get("show_suggestions") and res["suggestions"]:
            st.markdown("---")
            st.markdown("### 💡 Tailored Resume Suggestions")
            for idx, sugg in enumerate(res["suggestions"], 1):
                with st.container():
                    st.markdown(f"**{idx}. {sugg['title']}** `[{sugg['category']}]`")
                    st.markdown(f"**Observation:** {sugg['observation']}")
                    st.markdown(f"**Recommendation:** {sugg['recommendation']}")

        # Improve Resume Before / After
        if st.session_state.get("show_improvements") and st.session_state.get("improvements_list"):
            st.markdown("---")
            st.markdown("### ⚡ Resume Improvement Review")
            st.caption("Choose whether to Accept, Edit, or Keep Original for each changed section. Factual accuracy is strictly preserved.")

            for item in st.session_state.improvements_list:
                sec_key = item["section_key"]
                sec_title = item["section_title"]

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

                    col_bef, col_aft = st.columns(2)
                    with col_bef:
                        st.markdown("**Before Improvement**")
                        st.markdown(f'<div class="diff-before">{item["before"]}</div>', unsafe_allow_html=True)
                    with col_aft:
                        st.markdown("**After Improvement**")
                        st.markdown(f'<div class="diff-after">{item["after"]}</div>', unsafe_allow_html=True)

                    choice = st.radio(
                        f"Action for {sec_title}:",
                        options=["✅ Accept", "✎ Edit", "↩ Keep Original"],
                        key=f"analysis_decision_{sec_key}",
                        horizontal=True
                    )

                    if choice == "✅ Accept":
                        st.session_state.user_decisions[sec_key]["decision"] = "accept"
                    elif choice == "↩ Keep Original":
                        st.session_state.user_decisions[sec_key]["decision"] = "keep_original"
                    elif choice == "✎ Edit":
                        st.session_state.user_decisions[sec_key]["decision"] = "edit"
                        ed_val = st.text_area(
                            f"Edit content for {sec_title}:",
                            value=st.session_state.user_decisions[sec_key]["edited"],
                            key=f"analysis_edit_{sec_key}",
                            height=120
                        )
                        st.session_state.user_decisions[sec_key]["edited"] = ed_val

                    st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px dashed #CBD5E0;'/>", unsafe_allow_html=True)

            if st.button("Generate Final Updated Resume", type="primary", use_container_width=True):
                final_text = ResumeOptimizer.compile_final_resume(
                    st.session_state.parsed_sections,
                    st.session_state.user_decisions
                )
                st.session_state.final_resume_text = final_text
                st.session_state.final_resume_generated = True

        # Final Updated Resume Display & Downloads
        if st.session_state.get("final_resume_generated") and st.session_state.get("final_resume_text"):
            st.markdown("---")
            st.markdown("## Final Updated Resume")
            if st.session_state.active_jd:
                st.success("### “Your resume has been updated based on your selected job role, company, and job description.”")
            else:
                st.success("### “Your resume has been updated based on your selected job role and company.”")

            prev_tab, raw_tab = st.tabs(["Preview Updated Resume", "Raw Plain Text"])
            with prev_tab:
                st.markdown(f"""
                    <div style="background-color: #FFFFFF; border: 2px solid #E2E8F0; padding: 2rem; border-radius: 8px;">
                        <pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.95rem; color: #2D3748;">{st.session_state.final_resume_text}</pre>
                    </div>
                """, unsafe_allow_html=True)
            with raw_tab:
                st.text_area("Updated Content:", value=st.session_state.final_resume_text, height=300)

            st.markdown("#### Download Resume")
            pdf_bytes = export_resume_to_pdf(st.session_state.final_resume_text, f"{st.session_state.active_job_role} Resume")
            docx_bytes = export_resume_to_docx(st.session_state.final_resume_text)

            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                st.download_button("📥 Download PDF", data=pdf_bytes, file_name="AscendCareer_Updated_Resume.pdf", mime="application/pdf", use_container_width=True)
            with col_d2:
                st.download_button("📥 Download Word (.docx)", data=docx_bytes, file_name="AscendCareer_Updated_Resume.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            with col_d3:
                st.download_button("📥 Download Text (.txt)", data=st.session_state.final_resume_text, file_name="AscendCareer_Updated_Resume.txt", mime="text/plain", use_container_width=True)

        st.markdown("")
        if st.button("← Upload Another Resume / Start Over", use_container_width=True):
            st.session_state.analysis_step = 1
            st.session_state.analysis_complete = False
            st.rerun()
