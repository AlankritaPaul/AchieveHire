"""
AscendCareer — Authentication & User Identity Modules
"""
from modules.auth.user_service import (
    PURPOSE_OPTIONS,
    generate_unique_user_id,
    register_user,
    get_user_by_id,
    update_user_record,
    set_active_user,
    get_current_user,
    sign_out,
    delete_user_account,
)
from modules.auth.signin_ui import render_signin_flow

__all__ = [
    "PURPOSE_OPTIONS",
    "generate_unique_user_id",
    "register_user",
    "get_user_by_id",
    "update_user_record",
    "set_active_user",
    "get_current_user",
    "sign_out",
    "delete_user_account",
    "render_signin_flow",
]
