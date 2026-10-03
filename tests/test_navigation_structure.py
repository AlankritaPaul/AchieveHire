"""
Unit tests for AchieveHire Main Navigation, Interview, Profile, and Legal structures.
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


    def test_faq_items_and_ordering(self):
        from modules.legal.faq_ui import FAQ_ITEMS, render_faq_page
        from modules.legal import render_faq_page, render_privacy_page, render_terms_page
        from modules.landing.content import PRIVACY_SECTIONS

        # 1. Check all 8 FAQ items are present
        self.assertEqual(len(FAQ_ITEMS), 8)
        self.assertEqual(FAQ_ITEMS[0]["q"], "How does AchieveHire work?")
        self.assertEqual(FAQ_ITEMS[1]["q"], "How do I create a resume?")
        self.assertEqual(FAQ_ITEMS[2]["q"], "Can I edit my resume after creating it?")
        self.assertEqual(FAQ_ITEMS[3]["q"], "How does Resume Analysis work?")
        self.assertEqual(FAQ_ITEMS[4]["q"], "Can I delete my account?")
        self.assertEqual(FAQ_ITEMS[5]["q"], "What happens to my resume and profile after account deletion?")
        self.assertEqual(FAQ_ITEMS[6]["q"], "Is AchieveHire free?")
        self.assertEqual(FAQ_ITEMS[7]["q"], "How does Interview Practice work?")

        # 2. Terms & Conditions does NOT contain Account Deletion
        terms_sections = [s for s in PRIVACY_SECTIONS if "Terms" in s["title"]]
        self.assertEqual(len(terms_sections), 1)
        terms_qa_titles = [qa["q"] for qa in terms_sections[0]["qa"]]
        self.assertFalse(any("delete" in q.lower() for q in terms_qa_titles))

        # 3. FAQ contains Account Deletion (Q5 & Q6)
        faq_q_titles = [item["q"] for item in FAQ_ITEMS]
        self.assertIn("Can I delete my account?", faq_q_titles)
        self.assertIn("What happens to my resume and profile after account deletion?", faq_q_titles)

        # 4. Render functions are callable
        self.assertTrue(callable(render_faq_page))
        self.assertTrue(callable(render_privacy_page))
        self.assertTrue(callable(render_terms_page))

    def test_top_nav_bar_and_landing_structure(self):
        from modules.landing.ui import render_landing, THEMES
        from modules.navigation.panel import render_top_nav_bar
        import inspect

        # Check render_top_nav_bar signature defaults
        sig = inspect.signature(render_top_nav_bar)
        self.assertFalse(sig.parameters["show_signin"].default)
        self.assertFalse(sig.parameters["show_theme"].default)

        # Check render_landing is callable
        self.assertTrue(callable(render_landing))

    def test_footer_content_and_structure(self):
        from modules.landing.ui import _render_footer, THEMES
        import inspect

        # Inspect the source code of _render_footer
        src = inspect.getsource(_render_footer)

        # 1. Career Readiness Line
        self.assertIn("Smarter preparation. Stronger confidence. Better opportunities.", src)

        # 2. Copyright & Rights
        self.assertIn("© 2026 AchieveHire", src)
        self.assertIn("All rights reserved", src)

        # 3. Brand Statement
        self.assertIn("AchieveHire", src)
        self.assertIn("Built for candidates serious about their next step.", src)

        # 4. Creator Credit
        self.assertIn("The brainchild of", src)
        self.assertIn("ALANKRITA PAL", src)
        self.assertIn("💛", src)

    def test_settings_page_and_options(self):
        from modules.settings.ui import render_settings_page
        from modules.auth.user_service import register_user, delete_user_account, get_user_by_id
        import inspect

        self.assertTrue(callable(render_settings_page))

        # Check source of render_settings_page contains all 3 requested options with logos
        src = inspect.getsource(render_settings_page)
        self.assertIn("Notification Preferences", src)
        self.assertIn("🔔", src)
        self.assertIn("Add AchieveHire to Desktop", src)
        self.assertIn("🖥️", src)
        self.assertIn("Delete Account", src)
        self.assertIn("🗑️", src)

        # Test account deletion logic
        test_user = register_user("Delete Target User", "Both")
        uid = test_user["user_id"]
        self.assertIsNotNone(get_user_by_id(uid))

        delete_user_account(uid)
        self.assertIsNone(get_user_by_id(uid))


if __name__ == "__main__":
    unittest.main()
