"""
AscendCareer — Legal, Compliance & FAQ Modules
"""
from modules.legal.faq_ui import render_faq_page, FAQ_ITEMS
from modules.legal.privacy_ui import render_privacy_page
from modules.legal.terms_ui import render_terms_page

__all__ = ["render_faq_page", "render_privacy_page", "render_terms_page", "FAQ_ITEMS"]
