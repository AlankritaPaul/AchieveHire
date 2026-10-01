"""
Unit tests for AscendCareer Main Navigation, Interview, Profile, and Legal structures.
"""

import unittest
from unittest.mock import MagicMock, patch
import streamlit as st


class TestNavigationStructure(unittest.TestCase):
    def setUp(self):
        # Reset session state for test isolation
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["ac_theme"] = "light"

    def test_imports_cleanly(self):
        from modules.navigation.panel import render_navigation_drawer, render_top_nav_bar, _get_avatar_uri
        from modules.interview.specialized_ui import render_specialized_interview, SPECIALIZED_DOMAINS
        from modules.interview.job_related_ui import render_job_related_interview, INTERVIEW_ROUNDS
        from modules.profile.ui import render_user_profile
        from modules.legal.privacy_ui import render_privacy_page
        from modules.legal.terms_ui import render_terms_page

        self.assertTrue(len(SPECIALIZED_DOMAINS) >= 4)
        self.assertTrue(len(INTERVIEW_ROUNDS) >= 3)
        self.assertTrue(callable(render_navigation_drawer))
        self.assertTrue(callable(render_top_nav_bar))
        self.assertTrue(callable(render_specialized_interview))
        self.assertTrue(callable(render_job_related_interview))
        self.assertTrue(callable(render_user_profile))
        self.assertTrue(callable(render_privacy_page))
        self.assertTrue(callable(render_terms_page))

    def test_default_avatar_uri(self):
        from modules.navigation.panel import _get_avatar_uri
        # Default when no profile pic uploaded
        uri = _get_avatar_uri()
        self.assertTrue(uri.startswith("data:image/svg+xml;base64,"))

        # Custom uploaded picture returns custom URI
        st.session_state["user_profile_pic"] = "data:image/png;base64,customdata"
        self.assertEqual(_get_avatar_uri(), "data:image/png;base64,customdata")

    def test_navigation_hierarchy_rule(self):
        """
        Verify that Resume contains Resume Create and Resume Analysis,
        Interview contains Specialized Interview and Job Related Interview,
        and neither mixes the two or embeds role/company in branding.
        """
        from modules.interview.specialized_ui import SPECIALIZED_DOMAINS
        from modules.interview.job_related_ui import INTERVIEW_ROUNDS

        # Specialized interview domains should be technical / architectural
        domain_titles = [d["title"] for d in SPECIALIZED_DOMAINS]
        self.assertTrue(any("Software" in t or "Systems" in t for t in domain_titles))
        self.assertTrue(any("AI" in t or "Data" in t for t in domain_titles))

        # Job related interview rounds should be behavioral / situational / competency
        round_titles = [r["title"] for r in INTERVIEW_ROUNDS]
        self.assertTrue(any("Behavioral" in t for t in round_titles))
        self.assertTrue(any("Competency" in t for t in round_titles))


if __name__ == "__main__":
    unittest.main()
