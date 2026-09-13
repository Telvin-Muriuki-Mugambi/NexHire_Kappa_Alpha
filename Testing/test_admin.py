"""Test administrator models, persistence, permissions, and dashboard routing."""

import json
import sys
import types

import pytest
from Models.Admin import Admin, AdminManager, BaseManager
from Models.Auth import Auth
from Models.User import User

@pytest.fixture
def admin_manager(tmp_path, monkeypatch):
    """Create an admin manager using temporary JSON files."""
    u, j = tmp_path / "users.json", tmp_path / "jobs.json"
    u.write_text("[]"); j.write_text("[]")
    monkeypatch.setattr(AdminManager, "USERS_FILE", str(u))
    monkeypatch.setattr(AdminManager, "JOBS_FILE", str(j))
    return AdminManager()

@pytest.fixture
def admin_user():
    """Provide a minimal authenticated admin record for manager tests."""
    return {"user_id": "admin-001", "role": "ADMIN"}

@pytest.fixture
def normal_user():
    """Provide a non-admin record for permission-denial tests."""
    return {"user_id": "user-001", "role": "USER"}


def _install_email_validator_stub(monkeypatch):
    """Provide a minimal email_validator module so flow imports can run in tests."""
    module = types.ModuleType("email_validator")

    class FakeEmailNotValidError(ValueError):
        pass

    def fake_validate_email(email, check_deliverability=True):
        if "@" not in email:
            raise FakeEmailNotValidError("invalid email")
        return types.SimpleNamespace(normalized=email)

    module.validate_email = fake_validate_email
    module.EmailNotValidError = FakeEmailNotValidError
    monkeypatch.setitem(sys.modules, "email_validator", module)


def test_admin_manager_inherits_from_base_manager():
    admin = AdminManager()
    assert isinstance(admin, AdminManager) and isinstance(admin, BaseManager)

def test_base_manager_protected_methods_exist():
    manager = AdminManager()
    assert hasattr(manager, "_ensure_file_exists") and hasattr(manager, "_load_data") and hasattr(manager, "_save_data")

def test_load_and_save_data_are_encapsulated(admin_manager):
    test_data = [{"name": "Test User"}]
    admin_manager._save_data(admin_manager.USERS_FILE, test_data)
    assert admin_manager._load_data(admin_manager.USERS_FILE) == test_data

def test_admin_manager_overrides_parent_description():
    assert BaseManager().get_manager_description() == "Base Data Manager System"
    assert AdminManager().get_manager_description() == "Admin-Level Security and Opportunity Manager"

def test_admin_class_properties():
    assert hasattr(AdminManager, "USERS_FILE") and hasattr(AdminManager, "JOBS_FILE")


def test_admin_inherits_user_and_preserves_role_data():
    admin = Admin("Admin User", "admin@example.com", "0712345678", "secret")
    assert isinstance(admin, User)
    assert isinstance(admin, Admin)
    assert admin.role == "ADMIN"
    assert admin.user_id is not None


def test_admin_menu_uses_authenticated_admin_user(monkeypatch):
    from CLI_commands.Admin_CLI import main as admin_cli_main

    auth = Auth()
    admin = auth.register("Admin User", "admin@example.com", "0712345678", "secret", "ADMIN")
    auth.current_user = admin

    monkeypatch.setattr("CLI_commands.Admin_CLI.create_auth", lambda data_dir=None: auth)
    monkeypatch.setattr("CLI_commands.Admin_CLI.login", lambda auth_obj: auth_obj.current_user)

    def fake_show_admin_menu(auth_obj):
        assert auth_obj is auth
        return 0

    monkeypatch.setattr("CLI_commands.Admin_CLI.show_admin_menu", fake_show_admin_menu)

    assert admin_cli_main(["interactive"]) == 0


def test_landing_passes_authenticated_admin_to_admin_cli(monkeypatch):
    _install_email_validator_stub(monkeypatch)

    import flow.Landing as landing_module

    auth = Auth()
    auth.current_user = auth.register("Admin User", "admin@example.com", "0712345678", "secret", "ADMIN")
    called = {}

    def fake_admin_menu(auth_obj=None):
        called["auth"] = auth_obj
        return 0

    monkeypatch.setattr(landing_module, "admin_menu", fake_admin_menu)

    assert landing_module.landing(auth) == 0
    assert called["auth"] is auth


def test_landing_passes_authenticated_job_seeker_to_jobseeker_dashboard(monkeypatch):
    _install_email_validator_stub(monkeypatch)

    import flow.Landing as landing_module

    auth = Auth()
    auth.current_user = auth.register("Jane Doe", "jane@example.com", "0712345678", "secret", "JOB_SEEKER")
    called = {}

    def fake_jobseeker_menu(auth_obj=None):
        called["auth"] = auth_obj
        return 0

    monkeypatch.setattr(landing_module, "jobseeker_menu", fake_jobseeker_menu)

    assert landing_module.landing(auth) == 0
    assert called["auth"] is auth


def test_get_default_paths_is_class_method():
    paths = AdminManager.get_default_paths()
    assert isinstance(paths, dict) and "users_path" in paths and "jobs_path" in paths

def test_post_opportunity_creates_pending_job(admin_manager, admin_user):
    job = admin_manager.post_opportunity("Dev", "Python", "Tech", admin_user["user_id"])
    assert job["job_id"] and job["status"] == "PENDING"

def test_post_opportunity_persists_to_json(admin_manager, admin_user):
    job = admin_manager.post_opportunity("Backend", "APIs", "ABC", admin_user["user_id"])
    with open(admin_manager.JOBS_FILE, "r") as f:
        assert len(json.load(f)) == 1

def test_review_opportunity_returns_pending_jobs(admin_manager, admin_user):
    admin_manager.post_opportunity("Frontend", "React", "A", admin_user["user_id"])
    assert len(admin_manager.review_opportunity(admin_user)) == 1

def test_admin_can_approve_pending_job(admin_manager, admin_user, monkeypatch):
    job = admin_manager.post_opportunity("Python", "Dev", "Tech", admin_user["user_id"])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert admin_manager.approve_job(job["job_id"], admin_user) is True

def test_approved_status_persists_to_json(admin_manager, admin_user, monkeypatch):
    job = admin_manager.post_opportunity("SE", "Dev", "Ltd", admin_user["user_id"])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    admin_manager.approve_job(job["job_id"], admin_user)
    with open(admin_manager.JOBS_FILE, "r") as f:
        assert json.load(f)[0]["status"] == "APPROVED"

def test_approved_job_remains_approved(admin_manager, admin_user, monkeypatch):
    job = admin_manager.post_opportunity("Fake", "Desc", "Unknown", admin_user["user_id"])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert admin_manager.approve_job(job["job_id"], admin_user) is True

def test_only_admin_can_review_jobs(admin_manager, normal_user):
    with pytest.raises(PermissionError):
        admin_manager.review_opportunity(normal_user)

def test_invalid_job_id_returns_false(admin_manager, admin_user):
    assert admin_manager.approve_job("INVALID-ID", admin_user) is False

def test_already_approved_job_cannot_be_approved_again(admin_manager, admin_user, monkeypatch):
    job = admin_manager.post_opportunity("Dev", "Code", "Co", admin_user["user_id"])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert admin_manager.approve_job(job["job_id"], admin_user) is True
    assert admin_manager.approve_job(job["job_id"], admin_user) is False
