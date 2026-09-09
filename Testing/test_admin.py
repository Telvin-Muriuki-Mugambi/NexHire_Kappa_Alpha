#Test file for the admin
import pytest
from Models.Admin import AdminManager

# Test the CRUD operations on users
def test_crud_on_users(tmp_path, monkeypatch):
    monkeypatch.setattr(AdminManager, "USERS_FILE", (tmp_path / "users.json"))
    #Test Create User via manage_user
    user = AdminManager.manage_user("create", username="admin_boss", email="boss@example.com", password="secure123", role="admin")
    assert user["username"] == "admin_boss"
    assert user["role"] == "admin"
    #Test Get Users via manage_user
    users = AdminManager.manage_user("get")
    assert len(users) == 1
    #Test Update User Role via manage_user
    success = AdminManager.manage_user("update", user_id=user["user_id"], new_role="applicant")
    assert success is True
    #Test Delete User via manage_user
    deleted = AdminManager.manage_user("delete", user_id=user["user_id"])
    assert deleted is True
    assert len(AdminManager.manage_user("get")) == 0


    #Test the Verify of Opportunity Posted
def test_verify_opportunity_posted(tmp_path, monkeypatch):
    monkeypatch.setattr(AdminManager, "JOBS_FILE", (tmp_path / "jobs.json"))
    #Test Post Opportunity via for applicants
    job = AdminManager.post_opportunity("Python Developer", "Develop and maintain Python applications.", "TechCorp", "admin_01", "status=pending")
    assert job["title"] == "Python Developer"
    assert job["status"] == "pending"
    #Test review Opportunity via review_opportunity
    pending_jobs = AdminManager.review_opportunity()
    assert len(pending_jobs) == 1
    assert pending_jobs[0]["title"] == "Python Developer"

    #Test Approving job (moving from pending to verified)
    approved = AdminManager.approve_job(job["job_id"], status="verified")
    assert approved is True
    assert len(AdminManager.review_opportunity()) == 0  # No pending jobs after approval
    


    



    
   