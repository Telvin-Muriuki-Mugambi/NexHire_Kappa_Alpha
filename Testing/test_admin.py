#Test file for the admin
import pytest
from Models.Admin import AdminManager, BaseManager

# Test the CRUD operations on users
def test_crud_on_users(tmp_path, monkeypatch):
    temp_users = tmp_path / "users.json"
    monkeypatch.setattr(AdminManager, "USERS_FILE", str(temp_users))
    
    manager = AdminManager()
    
    # 1. Test Create
    new_user = manager.manage_user("create", username="testuser", email="test@mail.com", password="123", role="user")
    assert new_user["username"] == "testuser"
    assert "user_id" in new_user
    
    # 2. Test Get
    users = manager.manage_user("get")
    assert len(users) == 1
    assert users[0]["username"] == "testuser"
    
    # 3. Test Update
    user_id = new_user["user_id"]
    updated = manager.manage_user("update", user_id=user_id, new_role="admin")
    assert updated is True
    
    users_after_update = manager.manage_user("get")
    assert users_after_update[0]["role"] == "admin"
    
    # 4. Test Delete
    deleted = manager.manage_user("delete", user_id=user_id)
    assert deleted is True
    assert len(manager.manage_user("get")) == 0

def test_verify_opportunity_posted(tmp_path, monkeypatch):
    temp_jobs = tmp_path / "jobs.json"
    monkeypatch.setattr(AdminManager, "JOBS_FILE", str(temp_jobs))
    
    manager = AdminManager()
    
    # 1. Post a job opportunity
    job = manager.post_opportunity(
        title="Software Engineer", 
        description="Build scalable apps", 
        company="TechCorp", 
        admin_id="admin_123"
    )
    assert job["title"] == "Software Engineer"
    assert job["status"] == "pending"
    
    # 2. Review pending opportunities
    pending_jobs = manager.review_opportunity()
    assert len(pending_jobs) == 1
    
    # 3. Approve job
    job_id = job["job_id"]
    approved = manager.approve_job(job_id)
    assert approved is True
    
    # Verify no more pending jobs exist
    assert len(manager.review_opportunity()) == 0

def test_base_manager_inheritance(tmp_path):
    temp_file = tmp_path / "test_base.json"
    manager = AdminManager()
    
    manager._save_data(str(temp_file), [{"test": "data"}])
    data = manager._load_data(str(temp_file))
    
    assert data == [{"test": "data"}]

def test_polymorphic_description():
    base = BaseManager()
    admin = AdminManager()
    
    assert base.get_manager_description() == "Base Data Manager System"
    assert admin.get_manager_description() == "Admin-Level Security and Opportunity Manager"

def test_class_methods_and_edge_cases():
    paths = AdminManager.get_default_paths()
    assert "users_path" in paths
    assert "jobs_path" in paths
    
    manager = AdminManager()
    result = manager.manage_user("update", user_id="nonexistent_id", new_role="superuser")
    assert result is False