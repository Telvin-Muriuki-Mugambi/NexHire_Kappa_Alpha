#Test file for the admin
import json
import pytest
from Models.Admin import AdminManager, BaseManager

@pytest.fixture
def admin_manager(tmp_path, monkeypatch):
    u, j = tmp_path / "users.json", tmp_path / "jobs.json"
    u.write_text("[]"); j.write_text("[]")
    monkeypatch.setattr(AdminManager, "USERS_FILE", str(u))
    monkeypatch.setattr(AdminManager, "JOBS_FILE", str(j))
    return AdminManager()

@pytest.fixture
def admin_user():
    return {"user_id": "admin-001", "role": "ADMIN"}

@pytest.fixture
def normal_user():
    return {"user_id": "user-001", "role": "USER"}

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