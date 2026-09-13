"""Test the actual job-seeker behaviors implemented in Models/jobseeker.py."""

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Models.DataManager import DataManager
from Models.JobListing import JobListing
from Models.jobseeker import JobSeeker


@pytest.fixture
def seeded_manager(tmp_path):
    """Create a data manager with one approved job and one pending job."""
    manager = DataManager(tmp_path)

    approved = JobListing(
        title="Python Developer",
        description="Build APIs",
        location="Nairobi",
        skills=["Python", "Flask"],
        pay_rate=120000,
        experience_level="mid",
        availability="FULL_TIME",
        job_id="job-approve-1",
        status="APPROVED",
        employer_id="employer-1",
        company_name="NexHire",
    )
    pending = JobListing(
        title="Java Developer",
        description="Legacy system work",
        location="Remote",
        skills=["Java", "Spring"],
        pay_rate=100000,
        experience_level="mid",
        availability="PART_TIME",
        job_id="job-pending-1",
        status="PENDING",
        employer_id="employer-2",
        company_name="CodeWorks",
    )

    manager.save_job(approved)
    manager.save_job(pending)
    return manager


def test_available_jobs_returns_only_approved_listings(seeded_manager):
    """Only approved jobs should be visible to a seeker."""
    seeker = JobSeeker(data_manager=seeded_manager, user_id="user-1", name="Jane Doe")

    jobs = seeker.available_jobs()

    assert [job.job_id for job in jobs] == ["job-approve-1"]
    assert all(str(job.status).upper() == "APPROVED" for job in jobs)


def test_search_jobs_filters_by_keyword_and_skill(seeded_manager):
    """Search should match approved jobs by a keyword and the skill filter."""
    seeker = JobSeeker(data_manager=seeded_manager, user_id="user-1", name="Jane Doe")

    keyword_results = seeker.search_jobs("python")
    skill_results = seeker.filter_jobs(skill="flask")

    assert [job["job_id"] for job in keyword_results] == ["job-approve-1"]
    assert [job["job_id"] for job in skill_results] == ["job-approve-1"]
    assert all("python" in job["title"].lower() for job in keyword_results)


def test_apply_job_persists_application_for_approved_listing(seeded_manager):
    """Applying to an approved job should save the application and record the job ID."""
    seeker = JobSeeker(
        data_manager=seeded_manager,
        user_id="user-1",
        name="Jane Doe",
        cv="/tmp/jane_cv.pdf",
    )

    result = seeker.apply_job("job-approve-1")
    applications = seeded_manager.load_applicants("job-approve-1")

    assert result == "job-approve-1"
    assert "job-approve-1" in seeker.applied_jobs
    assert applications[0]["user_id"] == "user-1"
    assert applications[0]["cv"] == "/tmp/jane_cv.pdf"


def test_apply_job_rejects_unknown_or_pending_job(seeded_manager):
    """Only approved jobs with a valid identifier can be applied for."""
    seeker = JobSeeker(data_manager=seeded_manager, user_id="user-1", name="Jane Doe")

    with pytest.raises(ValueError):
        seeker.apply_job("missing-job")

    with pytest.raises(ValueError):
        seeker.apply_job("job-pending-1")


def test_upload_cv_sets_path_without_copying(seeded_manager):
    """The helper should just record a provided CV path and return it."""
    seeker = JobSeeker(data_manager=seeded_manager, user_id="user-1", name="Jane Doe")
    cv_path = str(Path("/tmp/example_cv.pdf"))

    result = seeker.upload_cv(cv_path)

    assert result == cv_path
    assert seeker.cv_path == cv_path


def test_cv_filename_requires_user_id():
    """A seeker cannot generate a CV filename without a user id."""
    seeker = JobSeeker(name="Jane Doe")

    with pytest.raises(ValueError, match="user ID"):
        seeker.cv_filename("resume.pdf")


def test_upload_file_copies_cv_to_target_directory(tmp_path):
    """upload_file should copy the selected file into the destination directory and set cv_path."""
    source = tmp_path / "source.pdf"
    source.write_text("CV content", encoding="utf-8")
    destination = tmp_path / "target_cvs"

    seeker = JobSeeker(user_id="42", name="Jane Doe")
    result = seeker.upload_file(target_directory=str(destination), file_path=str(source))

    assert result == str(destination / "42_Jane_Doe.pdf")
    assert seeker.cv_path == str(destination / "42_Jane_Doe.pdf")
    assert os.path.exists(seeker.cv_path)


def test_upload_registration_cv_uses_default_upload_logic(tmp_path, monkeypatch):
    """The registration helper should delegate to upload_file with the configured directory."""
    seeker = JobSeeker(user_id="42", name="Jane Doe")
    captured = {}

    def fake_upload_file(target_directory=None, file_path=None):
        captured["target_directory"] = target_directory
        captured["file_path"] = file_path
        return "uploaded-path"

    monkeypatch.setattr(seeker, "upload_file", fake_upload_file)

    result = seeker.upload_registration_cv(target_directory=str(tmp_path))

    assert result == "uploaded-path"
    assert captured == {"target_directory": str(tmp_path), "file_path": None}
