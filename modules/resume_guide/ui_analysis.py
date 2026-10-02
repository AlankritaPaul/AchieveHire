"""
Page-wise UI flow for Resume Analysis.
Each selection has its own dedicated page.
Bottom navigation consistently provides:
- Left side below: Back clickable option
- Right side below: Next clickable option
"""

import streamlit as st
import plotly.graph_objects as go
from modules.constants import SUGGESTED_JOB_ROLES, SUGGESTED_COMPANIES
from modules.resume_guide.parser import extract_text_from_file, parse_resume_sections
from modules.resume_guide.analyzer import ResumeAnalyzer
from modules.resume_guide.optimizer import ResumeOptimizer
from modules.resume_guide.exporter import export_resume_to_pdf, export_resume_to_docx

def render_section_improvement_pie_chart(res):
    """
    Renders an interactive visual pie/donut graph summarizing the improvement status
    of what is written in each evaluated resume section.
    """
    already_correct = res.get("already_correct", [])
    needs_imp = res.get("needs_improvement_sections", [])
    missing_info = res.get("missing_info_sections", [])

    labels = []
    values = []
    colors = []
    hover_texts = []

    if already_correct:
        labels.append("Well-Structured & Retain")
        values.append(len(already_correct))
        colors.append("#10B981")  # Emerald Green
        sec_names = "<br>• ".join([s["title"] for s in already_correct])
        hover_texts.append(f"Sections:<br>• {sec_names}")

    if needs_imp:
        labels.append("Can Be Improved Directly")
        values.append(len(needs_imp))
        colors.append("#F59E0B")  # Amber / Warm Gold
        sec_names = "<br>• ".join([s["title"] for s in needs_imp])
        hover_texts.append(f"Sections:<br>• {sec_names}")

    if missing_info:
        labels.append("Information Missing (Action Required)")
        values.append(len(missing_info))
        colors.append("#EF4444")  # Crimson Red
        sec_names = "<br>• ".join([s["title"] for s in missing_info])
        hover_texts.append(f"Sections:<br>• {sec_names}")

    if not values:
        return

    col_chart, col_summary = st.columns([1.1, 1])

    with col_chart:
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.48,
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2.5)),
            textinfo='percent+label',
            textposition='inside',
            hovertext=hover_texts,
            hovertemplate='<b>%{label}</b><br>%{hovertext}<br><b>Count:</b> %{value} of ' + str(sum(values)) + ' sections (%{percent})<extra></extra>',
            pull=[0.02] * len(values)
        )])

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.28, xanchor='center', x=0.5),
            margin=dict(t=15, b=65, l=15, r=15),
            height=340,
            annotations=[dict(text=f'<b>{sum(values)}</b><br><span style="font-size:11px;color:#718096;">Sections</span>', x=0.5, y=0.5, font_size=17, showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_summary:
        st.markdown("##### Written Section Status Summary")
        for sec in already_correct:
            st.markdown(f"🟢 **{sec['title']}**: *Well-Structured* — No changes needed.")
        for sec in needs_imp:
            st.markdown(f"🟡 **{sec['title']}**: *Needs Polish* — {sec['action']}")
        for sec in missing_info:
            opt_tag = "*(Optional for Freshers)*" if sec.get("is_optional") else "*(Action Required)*"
            st.markdown(f"🔴 **{sec['title']}**: *Information Missing* {opt_tag} — Details needed.")

def render_resume_analysis_flow():
    """Render the step-by-step page-wise flow for Resume Analysis."""
    if "analysis_step" not in st.session_state:
        st.session_state.analysis_step = 1

    steps = [
        "1. Select Job Role",
        "2. Select Company",
        "3. Job Description",
        "4. Upload Resume",
        "5. Resume Match Analysis"
    ]
    
    current_step = st.session_state.analysis_step
    from modules.landing.ui import THEMES
    t = THEMES[st.session_state.get("ac_theme", "light")]

    st.markdown(f"""
        <div style="background-color: {t['surface2']}; border: 1px solid {t['border']}; border-radius: 8px; padding: 12px 18px; margin-bottom: 20px;">
            <span style="font-size: 1.05rem; color: {t['text_primary']}; font-weight: 700;">Resume Analysis — Step {current_step} of 5: {steps[current_step - 1]}</span>
        </div>
    """, unsafe_allow_html=True)

    # PAGE 1: SELECT JOB ROLE
    if current_step == 1:
        st.markdown("### Select Job Role")
        st.caption("Choose from the suggested job roles or enter your own.")

        role_choice = st.radio(
            "Select option:",
            options=["Select a Job Role", "Write Your Job Role"],
            key="analysis_role_mode"
        )
        if role_choice == "Select a Job Role":
            selected_role = st.selectbox(
                "Suggested Job Roles (Searchable):",
                options=SUGGESTED_JOB_ROLES,
                key="analysis_role_select"
            )
            st.session_state.selected_job_role = selected_role
        else:
            custom_role = st.text_input(
                "Write Your Job Role:",
                value=st.session_state.get("selected_job_role", ""),
                placeholder="e.g. Distributed Systems Engineer",
                key="analysis_role_custom"
            )
            st.session_state.selected_job_role = custom_role.strip() if custom_role.strip() else "Software Developer"

        st.info(f"Selected Job Role: **{st.session_state.selected_job_role}**")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_nav_back_step1", use_container_width=True):
                st.session_state.resume_guide_mode = None
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_nav_next_step1", use_container_width=True):
                st.session_state.analysis_step = 2
                st.rerun()

    # PAGE 2: SELECT COMPANY
    elif current_step == 2:
        st.markdown("### Select Company")
        st.caption("Choose from the suggested companies or enter your own.")

        comp_choice = st.radio(
            "Select option:",
            options=["Select a Company", "Write Your Company"],
            key="analysis_comp_mode"
        )
        if comp_choice == "Select a Company":
            selected_comp = st.selectbox(
                "Suggested Companies / Types (Searchable):",
                options=SUGGESTED_COMPANIES,
                key="analysis_comp_select"
            )
            st.session_state.selected_company = selected_comp
        else:
            custom_comp = st.text_input(
                "Write Your Company:",
                value=st.session_state.get("selected_company", ""),
                placeholder="e.g. Google, Microsoft, Local Tech Corp",
                key="analysis_comp_custom"
            )
            st.session_state.selected_company = custom_comp.strip() if custom_comp.strip() else "General Tech Company"

        st.info(f"Selected Company: **{st.session_state.selected_company}**")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_nav_back_step2", use_container_width=True):
                st.session_state.analysis_step = 1
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_nav_next_step2", use_container_width=True):
                st.session_state.analysis_step = 3
                st.rerun()

    # PAGE 3: JOB DESCRIPTION
    elif current_step == 3:
        st.markdown("### Job Description (Optional / Recommended)")
        st.caption("Provide a specific job description if you have one. If provided, the resume will be analyzed against it. If not provided, no job description analysis will be claimed.")

        current_jd = st.session_state.get("selected_jd", "") or ""
        jd_input = st.text_area(
            "Job Description (Optional):",
            value=current_jd,
            height=200,
            placeholder="Paste responsibilities, required qualifications, and key technologies from the job posting...",
            key="analysis_jd_textarea"
        )
        st.session_state.selected_jd = jd_input.strip() if jd_input.strip() else None

        if st.session_state.selected_jd:
            st.success("Job Description provided. The resume will be analyzed against this job description.")
        else:
            st.info(f"No Job Description provided. The resume will be analyzed based on the selected job role ({st.session_state.get('selected_job_role', 'Software Developer')}) and company ({st.session_state.get('selected_company', 'General Tech Company')}).")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_nav_back_step3", use_container_width=True):
                st.session_state.analysis_step = 2
                st.rerun()
        with col_next:
            if st.button("Next →", type="primary", key="btn_nav_next_step3", use_container_width=True):
                st.session_state.analysis_step = 4
                st.rerun()

    # PAGE 4: UPLOAD RESUME
    elif current_step == 4:
        st.markdown("### Upload Resume")
        st.caption("Upload your resume file (.pdf, .docx, or .txt) to begin the review.")

        uploaded_file = st.file_uploader(
            "Upload your resume:",
            type=["pdf", "docx", "txt", "md"],
            key="analysis_uploader_page"
        )

        st.markdown(f"""
            <div style="background: #F7FAFC; padding: 12px; border-radius: 6px; border: 1px solid #E2E8F0; margin: 15px 0;">
                <strong>Review Configuration:</strong><br>
                • <strong>Selected Job Role:</strong> {st.session_state.get('selected_job_role', 'Software Developer')}<br>
                • <strong>Selected Company:</strong> {st.session_state.get('selected_company', 'General Tech Company')}<br>
                • <strong>Job Description:</strong> {'Provided' if st.session_state.get('selected_jd') else 'None provided'}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back", key="btn_nav_back_step4", use_container_width=True):
                st.session_state.analysis_step = 3
                st.rerun()

        with col_next:
            submit_btn = st.button("Next: Submit Resume for Review →", type="primary", key="btn_nav_next_step4", use_container_width=True)

        if submit_btn:
            if not uploaded_file:
                st.error("Please upload a resume file before submitting.")
                return

            with st.spinner("Analyzing resume against selected criteria..."):
                raw_text = extract_text_from_file(uploaded_file)
                if not raw_text.strip():
                    st.error("Could not extract readable text from document. Please ensure it is not password protected.")
                    return

                # CLEAN SLATE: Purge previous inputs, decisions, and cached improvements
                # to guarantee absolute isolation between different resumes, users, or review cycles.
                stale_keys = [
                    "ui_p_name", "ui_p_desc", "ui_p_tools", "ui_p_outcome",
                    "ui_e_comp", "ui_e_role", "ui_e_dates", "ui_e_bullets",
                    "ui_s_tech", "ui_s_non_tech", "ui_ed_deg", "ui_ed_inst", "ui_ed_year", "ui_ed_details", "ui_s_text",
                    "missing_proj_choice", "missing_exp_choice", "missing_skills_choice", "missing_edu_choice", "missing_sum_choice",
                    "final_resume_text", "final_resume_generated", "improvements_list", "user_decisions", "show_improvements", "show_suggestions"
                ]
                for k in stale_keys:
                    st.session_state.pop(k, None)

                sections = parse_resume_sections(raw_text)
                analyzer = ResumeAnalyzer(
                    job_role=st.session_state.selected_job_role,
                    company=st.session_state.selected_company,
                    job_description=st.session_state.selected_jd
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
                st.session_state.analysis_step = 5
                st.rerun()

    # PAGE 5: RESUME MATCH ANALYSIS
    elif current_step == 5:
        if not st.session_state.get("analysis_result"):
            st.session_state.analysis_step = 4
            st.rerun()
            return

        res = st.session_state.analysis_result
        st.markdown("## Resume Match Analysis")
        st.caption(f"Evaluated for **{res['job_role']}** at **{res['company']}**" + (" with Job Description" if res['has_jd'] else " (No Job Description provided)"))

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
            if res["project_relevance"]["has_projects"]:
                st.markdown(f"**Project Relevance:** ({res['project_relevance']['score']}/100)")
            else:
                st.markdown("**Project Relevance:** 0/100 *(Section Not Present)*")
            st.write(res["project_relevance"]["summary"])
        with col_r2:
            if res["experience_relevance"]["has_experience"]:
                st.markdown(f"**Experience Relevance:** ({res['experience_relevance']['score']}/100)")
            else:
                st.markdown("**Experience Relevance:** 0/100 *(Section Not Present)*")
            st.write(res["experience_relevance"]["summary"])

        # Step 2: What is Already Well-Structured & Correct
        st.markdown("---")
        st.markdown("### ✅ What is Already Well-Structured & Correct")
        st.caption("These sections meet professional standards and require no modification. All authentic content is strictly preserved.")
        already_correct_list = res.get("already_correct", [])
        if already_correct_list:
            for sec in already_correct_list:
                st.markdown(f"• **{sec['title']}**: {sec['observation']}")
        else:
            st.markdown("_No sections were identified as completely optimal yet._")

        # Outcome Branching
        st.markdown("---")
        if res["is_well_aligned"]:
            st.success("### “Your resume is well-aligned with this job role and effectively highlights the skills and experience required.”")
            st.info("No unnecessary improvement message is shown because the resume does not require meaningful changes.")
            
            # Visual Pie Graph: Section Improvement Summary
            st.markdown("---")
            st.markdown("### 📊 Section Improvement Summary")
            st.caption("Visual pie graph summarizing the written analysis across all evaluated resume sections.")
            render_section_improvement_pie_chart(res)
        else:
            st.warning("### “Your resume needs some improvements to better match this job role.”")
            
            # Step 3: Areas Requiring Attention (Distinguishing Needs Improvement vs Missing Information)
            st.markdown("### 🔍 Areas Requiring Attention")
            
            needs_imp = res.get("needs_improvement_sections", [])
            if needs_imp:
                st.markdown("#### Sections That Can Be Improved Directly (Existing Information)")
                st.caption("These sections contain usable information and can be refined directly without inventing new data.")
                for sec in needs_imp:
                    st.markdown(f"• **{sec['title']}**: {sec['observation']} *(Action: {sec['action']})*")

            missing_info = res.get("missing_info_sections", [])
            if missing_info:
                st.markdown("#### Information Missing (Action Required)")
                st.caption("These sections lack essential data. The system pauses improvement for these sections until you provide the details or choose to decline/skip.")
                for sec in missing_info:
                    opt_note = " *(Optional - can be skipped)*" if sec.get("is_optional") else " *(Recommended / Essential)*"
                    st.markdown(f"• **{sec['title']}**{opt_note}: {sec['observation']}")

            # Visual Pie Graph: Section Improvement Summary
            st.markdown("---")
            st.markdown("### 📊 Section Improvement Summary")
            st.caption("Visual pie graph summarizing the written analysis across all evaluated resume sections.")
            render_section_improvement_pie_chart(res)

            # Step 4, 6, 10: Interactive Missing Information Form (User Remains in Control)
            user_provided_info: Dict[str, Any] = {"declined_sections": []}
            if missing_info:
                st.markdown("---")
                st.markdown("### 📝 Provide Missing Information")
                st.caption("Strict Accuracy Rule: We never generate placeholder, assumed, or fictional content. Provide the required information below, or choose to decline/skip if you do not have it.")

                for sec in missing_info:
                    sec_k = sec["key"]
                    sec_t = sec["title"]

                    if sec_k == "projects":
                        with st.expander(f"📌 {sec_t} (Action Required)", expanded=True):
                            st.write(sec["observation"])
                            st.caption(f"Why needed: {sec['action']}")
                            p_choice = st.radio(
                                f"Choose option for {sec_t}:",
                                options=["Provide Project Details", "Decline / I don't have projects (Skip)"],
                                key="missing_proj_choice",
                                horizontal=True
                            )
                            if p_choice == "Provide Project Details":
                                p_name = st.text_input("Project Name *", key="ui_p_name", placeholder="e.g. Distributed Task Orchestrator")
                                p_desc = st.text_area("Project Description *", key="ui_p_desc", placeholder="Describe what the project does, key features, and your role...")
                                p_tools = st.text_area(
                                    "Technologies Used (Languages, Frameworks, Tools)",
                                    key="ui_p_tools",
                                    height=68,
                                    placeholder="e.g. Python\nDocker\nRedis\nREST APIs",
                                    help="Press Enter to write technologies on each line or separate by commas"
                                )
                                p_outcome = st.text_area(
                                    "Key Contribution or Outcome (Optional/Measurable)",
                                    key="ui_p_outcome",
                                    height=68,
                                    placeholder="e.g. Handled 5,000 requests/sec with p99 latency < 20ms\nReduced query latency by 35%",
                                    help="Press Enter to write contributions on each line"
                                )
                                if p_name or p_desc:
                                    user_provided_info["projects"] = {
                                        "name": p_name,
                                        "description": p_desc,
                                        "tools": p_tools,
                                        "outcome": p_outcome
                                    }
                            else:
                                user_provided_info["declined_sections"].append("projects")

                    elif sec_k == "experience":
                        with st.expander(f"📌 {sec_t} (Optional for Freshers)", expanded=True):
                            st.write(sec["observation"])
                            st.info("💡 **Students & Freshers:** Work experience is optional. Choose **'Decline / Skip'** below if you have no prior professional employment. You will not be penalized.")
                            e_choice = st.radio(
                                f"Choose option for {sec_t}:",
                                options=["Decline / Skip (Entry-Level / Fresher)", "Provide Experience Details"],
                                key="missing_exp_choice",
                                horizontal=True
                            )
                            if e_choice == "Provide Experience Details":
                                e_comp = st.text_input("Company / Organization Name *", key="ui_e_comp", placeholder="e.g. TechCorp Solutions")
                                e_role = st.text_input("Job Title / Role *", key="ui_e_role", placeholder="e.g. Software Engineer Intern")
                                e_dates = st.text_input("Duration / Dates", key="ui_e_dates", placeholder="e.g. Jun 2023 - Aug 2023")
                                e_bullets = st.text_area("Key Responsibilities & Achievements (one per line)", key="ui_e_bullets", placeholder="• Developed backend REST APIs using Python\n• Optimized database queries")
                                if e_comp or e_role:
                                    user_provided_info["experience"] = {
                                        "company": e_comp,
                                        "role": e_role,
                                        "dates": e_dates,
                                        "bullets": e_bullets
                                    }
                            else:
                                user_provided_info["declined_sections"].append("experience")

                    elif sec_k == "skills":
                        with st.expander(f"📌 {sec_t} (Action Required)", expanded=True):
                            st.write(sec["observation"])
                            st.caption(f"Why needed: {sec['action']}")
                            s_choice = st.radio(
                                f"Choose option for {sec_t}:",
                                options=["Provide Skills Details", "Decline / Skip"],
                                key="missing_skills_choice",
                                horizontal=True
                            )
                            if s_choice == "Provide Skills Details":
                                s_tech = st.text_area(
                                    "Technical Skills (Languages, Frameworks, Tools) *",
                                    key="ui_s_tech",
                                    height=95,
                                    placeholder="Enter technical skills line-by-line (Press Enter) or comma-separated:\nPython\nC++\nSQL\nGit\nDocker",
                                    help="Press Enter to add skills on each new line"
                                )
                                s_non_tech = st.text_area(
                                    "Non-Technical / Functional Skills",
                                    key="ui_s_non_tech",
                                    height=85,
                                    placeholder="Enter non-technical skills line-by-line (Press Enter) or comma-separated:\nPublic Speaking\nProblem Solving\nTeam Leadership",
                                    help="Press Enter to add skills on each new line"
                                )
                                if s_tech or s_non_tech:
                                    user_provided_info["skills"] = {
                                        "technical": s_tech,
                                        "non_technical": s_non_tech
                                    }
                            else:
                                user_provided_info["declined_sections"].append("skills")

                    elif sec_k == "education":
                        with st.expander(f"📌 {sec_t} (Action Required)", expanded=True):
                            st.write(sec["observation"])
                            ed_choice = st.radio(
                                f"Choose option for {sec_t}:",
                                options=["Provide Education Details", "Decline / Skip"],
                                key="missing_edu_choice",
                                horizontal=True
                            )
                            if ed_choice == "Provide Education Details":
                                ed_deg = st.text_input("Degree / Qualification *", key="ui_ed_deg", placeholder="e.g. B.S. in Computer Science")
                                ed_inst = st.text_input("Institution / University *", key="ui_ed_inst", placeholder="e.g. State University")
                                ed_year = st.text_input("Graduation Year / Dates", key="ui_ed_year", placeholder="e.g. 2024")
                                ed_details = st.text_area(
                                    "Specialization / Coursework / Highlights (Optional):",
                                    key="ui_ed_details",
                                    height=68,
                                    placeholder="e.g. Specialization in Distributed Systems\nRelevant Coursework: Data Structures, Operating Systems",
                                    help="Press Enter to write details on each line"
                                )
                                if ed_deg or ed_inst:
                                    user_provided_info["education"] = {
                                        "degree": ed_deg,
                                        "institution": ed_inst,
                                        "year": ed_year,
                                        "details": ed_details
                                    }
                            else:
                                user_provided_info["declined_sections"].append("education")

                    elif sec_k == "summary":
                        with st.expander(f"📌 {sec_t} (Optional)", expanded=False):
                            st.write(sec["observation"])
                            sum_choice = st.radio(
                                f"Choose option for {sec_t}:",
                                options=["Decline / Skip", "Provide Summary"],
                                key="missing_sum_choice",
                                horizontal=True
                            )
                            if sum_choice == "Provide Summary":
                                s_text = st.text_area("Write a brief 2-3 sentence summary:", key="ui_s_text", placeholder="Briefly describe your background, technical focus, and goals for this role...")
                                if s_text.strip():
                                    user_provided_info["summary"] = s_text.strip()
                            else:
                                user_provided_info["declined_sections"].append("summary")

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("View Suggestions", use_container_width=True):
                    st.session_state.show_suggestions = True
            with col_b2:
                if st.button("Improve Resume", type="primary", use_container_width=True):
                    optimizer = ResumeOptimizer(
                        job_role=res["job_role"],
                        company=res["company"],
                        job_description=st.session_state.selected_jd
                    )
                    improvements = optimizer.generate_improvements(
                        sections=st.session_state.parsed_sections,
                        analysis_result=res,
                        user_provided_info=user_provided_info
                    )
                    st.session_state.improvements_list = improvements
                    st.session_state.show_improvements = True

        # View Suggestions
        if st.session_state.get("show_suggestions") and res["suggestions"]:
            st.markdown("---")
            st.markdown("### Suggestions")
            for idx, sugg in enumerate(res["suggestions"], 1):
                with st.container():
                    st.markdown(f"**{idx}. {sugg['title']}** `[{sugg['category']}]`")
                    st.markdown(f"**Observation:** {sugg['observation']}")
                    st.markdown(f"**Recommendation:** {sugg['recommendation']}")

        # Improve Resume Before / After
        if st.session_state.get("show_improvements") and st.session_state.get("improvements_list"):
            st.markdown("---")
            st.markdown("### Before / After Improvement")
            st.caption("For each changed section, review the changes. Choose Accept, Edit, or Keep Original.")

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
                        f"Choose option for {sec_title}:",
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
            if st.session_state.selected_jd:
                st.success("### “Your resume has been updated based on your selected job role, company, and job description.”")
            else:
                st.success("### “Your resume has been updated based on your selected job role and company.”")

            prev_tab, raw_tab = st.tabs(["Preview Updated Resume", "Raw Formatted Text"])
            with prev_tab:
                st.markdown(f"""
                    <div style="background-color: #FFFFFF; border: 2px solid #E2E8F0; padding: 2rem; border-radius: 8px;">
                        <pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.95rem; color: #2D3748;">{st.session_state.final_resume_text}</pre>
                    </div>
                """, unsafe_allow_html=True)
            with raw_tab:
                st.text_area("Updated Content:", value=st.session_state.final_resume_text, height=300)

            st.markdown("#### Download Resume")
            pdf_bytes = export_resume_to_pdf(st.session_state.final_resume_text, f"{st.session_state.selected_job_role} Resume")
            docx_bytes = export_resume_to_docx(st.session_state.final_resume_text)

            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                st.download_button("📥 Download PDF Resume", data=pdf_bytes, file_name="AscendCareer_Updated_Resume.pdf", mime="application/pdf", use_container_width=True)
            with col_d2:
                st.download_button("📥 Download Word (.docx)", data=docx_bytes, file_name="AscendCareer_Updated_Resume.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            with col_d3:
                st.download_button("📥 Download Plain Text (.txt)", data=st.session_state.final_resume_text, file_name="AscendCareer_Updated_Resume.txt", mime="text/plain", use_container_width=True)

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col_back, col_space, col_next = st.columns([1, 2, 1])
        with col_back:
            if st.button("← Back to Upload", key="btn_nav_back_step5", use_container_width=True):
                st.session_state.analysis_step = 4
                st.rerun()
        with col_next:
            if st.button("Start Over", key="btn_nav_next_step5", use_container_width=True):
                # Clean slate for next user/session: purge all analysis, inputs, and selections
                keys_to_purge = [
                    "analysis_result", "raw_resume_text", "parsed_sections", "show_suggestions",
                    "show_improvements", "improvements_list", "user_decisions", "final_resume_generated",
                    "final_resume_text", "selected_job_role", "selected_company", "selected_jd",
                    "analysis_role_mode", "analysis_comp_mode", "analysis_role_custom", "analysis_comp_custom",
                    "analysis_role_select", "analysis_comp_select", "analysis_jd_textarea", "analysis_uploader_page",
                    "missing_proj_choice", "missing_exp_choice", "missing_skills_choice", "missing_edu_choice", "missing_sum_choice",
                    "ui_p_name", "ui_p_desc", "ui_p_tools", "ui_p_outcome",
                    "ui_e_comp", "ui_e_role", "ui_e_dates", "ui_e_bullets",
                    "ui_s_tech", "ui_s_non_tech", "ui_ed_deg", "ui_ed_inst", "ui_ed_year", "ui_ed_details", "ui_s_text"
                ]
                for k in keys_to_purge:
                    st.session_state.pop(k, None)
                st.session_state.analysis_step = 1
                st.session_state.analysis_complete = False
                st.rerun()
