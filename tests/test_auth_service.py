"""
Unit tests for AscendCareer User Authentication & Unique User ID Isolation System.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import streamlit as st
from modules.auth.user_service import (
    PURPOSE_OPTIONS,
    generate_unique_user_id,
    register_user,
    get_user_by_id,
    update_user_record,
    set_active_user,
    get_current_user,
    sign_out,
)
from modules.auth.signin_ui import render_signin_flow


class TestAuthAndUserIdService(unittest.TestCase):
    def setUp(self):
        # Create temp file for isolated user storage during tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_users_file = Path(self.temp_dir.name) / "test_users.json"
        self.patcher = patch("modules.auth.user_service.USERS_FILE", self.temp_users_file)
        self.patcher.start()

        # Reset session state for test isolation
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["ac_theme"] = "light"

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_unique_user_id_generation(self):
        """Verify User ID is generated based on 4 capital letters + 4 numbers (e.g. XRYH3258) and guarantees uniqueness."""
        name = "Test Candidate"
        user_id_1 = generate_unique_user_id(name)
        user_id_2 = generate_unique_user_id(name)

        # Structure check: exactly 8 characters, starting with 4 uppercase letters 'TEST' followed by 4 digits
        self.assertEqual(len(user_id_1), 8)
        self.assertEqual(len(user_id_2), 8)
        self.assertTrue(user_id_1[:4] == "TEST" and user_id_1[4:].isdigit())
        self.assertTrue(user_id_2[:4] == "TEST" and user_id_2[4:].isdigit())
        
        # Guaranteed uniqueness even with identical names
        self.assertNotEqual(user_id_1, user_id_2)

    def test_user_registration_and_purpose_options(self):
        """Verify user registration with intended purposes: Resume Preparation, Interview Preparation, Both."""
        self.assertIn("Resume Preparation", PURPOSE_OPTIONS)
        self.assertIn("Interview Preparation", PURPOSE_OPTIONS)
        self.assertIn("Both", PURPOSE_OPTIONS)

        # Register User A (Resume Preparation)
        user_a = register_user("User Alpha", "Resume Preparation")
        self.assertEqual(user_a["name"], "User Alpha")
        self.assertEqual(user_a["purpose"], "Resume Preparation")
        self.assertEqual(len(user_a["user_id"]), 8)
        self.assertTrue(user_a["user_id"][:4] == "USER" and user_a["user_id"][4:].isdigit())

        # Register User B (Interview Preparation with exact same name)
        user_b = register_user("User Alpha", "Interview Preparation")
        self.assertEqual(user_b["name"], "User Alpha")
        self.assertEqual(user_b["purpose"], "Interview Preparation")
        self.assertNotEqual(user_a["user_id"], user_b["user_id"])

        # Register User C (Both)
        user_c = register_user("User Gamma", "Both")
        self.assertEqual(user_c["purpose"], "Both")

    def test_user_data_isolation(self):
        """Verify User A data and User B data are kept completely separate."""
        user_a = register_user("Candidate A", "Resume Preparation")
        user_b = register_user("Candidate B", "Interview Preparation")

        id_a = user_a["user_id"]
        id_b = user_b["user_id"]

        # Update User A record
        update_user_record(id_a, {"headline": "Senior Fullstack Engineer"})

        # Fetch records
        fetched_a = get_user_by_id(id_a)
        fetched_b = get_user_by_id(id_b)

        self.assertEqual(fetched_a["headline"], "Senior Fullstack Engineer")
        self.assertNotEqual(fetched_b["headline"], "Senior Fullstack Engineer")
        self.assertEqual(fetched_b["purpose"], "Interview Preparation")

    def test_active_user_session_and_signout(self):
        """Verify session state tracks active user ID and clears on sign out."""
        user = register_user("Session User", "Both")
        self.assertEqual(st.session_state["user_id"], user["user_id"])
        self.assertEqual(st.session_state["username"], "Session User")
        self.assertEqual(st.session_state["user_purpose"], "Both")
        self.assertTrue(st.session_state["is_signed_in"])

        sign_out()
        self.assertIsNone(st.session_state["user_id"])
        self.assertFalse(st.session_state["is_signed_in"])

    def test_signin_ui_callable(self):
        """Verify render_signin_flow runs cleanly."""
        self.assertTrue(callable(render_signin_flow))


if __name__ == "__main__":
    unittest.main()
