#Test file for the admin
import pytest
from Models.Admin import AdminManager

# Test the CRUD operations on users
def test_crud_on_users(tmp_path, monkeypatch):
    # An object of the AdminManager class
    admin_instance = AdminManager()
    monkeypatch.setattr(AdminManager, "USERS_FILE", (tmp_path / "users.json"))
    #Test Create User via manage_user
    user = admin_instance.manage_user("create", username="admin_boss", email="boss@example.com", password="secure123", role="admin")
    assert user["username"] == "admin_boss"
    assert user["role"] == "admin"
    #Test Get Users via manage_user
    users = admin_instance.manage_user("get")
    assert len(users) == 1
    #Test Update User Role via manage_user
    success = admin_instance.manage_user("update", user_id=user["user_id"], new_role="applicant")
    assert success is True
    #Test Delete User via manage_user
    deleted = admin_instance.manage_user("delete", user_id=user["user_id"])
    assert deleted is True
    #Test handling of non-existent/invalid user deletion
    failed_delete = admin_instance.manage_user("delete", user_id="non_existent_id")
    assert failed_delete is False
    
#Test the Verify of Opportunity Posted
def test_verify_opportunity_posted(tmp_path, monkeypatch):
    monkeypatch.setattr(AdminManager, "JOBS_FILE", (tmp_path / "jobs.json"))
    #Test Post Opportunity via for applicants
    job = admin_instance.post_opportunity("Python Developer", "Develop and maintain Python applications.", "TechCorp", "admin_01", "status=pending")
    assert job["title"] == "Python Developer"
    assert job["status"] == "pending"
    #Test review Opportunity via review_opportunity
    pending_jobs = admin_instance.review_opportunity()
    assert len(pending_jobs) == 1
    assert pending_jobs[0]["title"] == "Python Developer"

    #Test Approving job (moving from pending to verified)
    approved = admin_instance.approve_job(job["job_id"], status="verified")
    assert approved is True
    assert len(admin_instance.review_opportunity()) == 0  # No pending jobs after approval
    


    



    
   