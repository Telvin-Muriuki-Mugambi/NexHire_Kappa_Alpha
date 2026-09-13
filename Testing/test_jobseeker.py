import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Models.jobseeker import job_seeker


def test_upload_cv_success(tmp_path):
    """Uploading a real CV should store the file path."""
    test_file = tmp_path / "cv.pdf"
    test_file.write_text("Candidate CV content")

    seeker = job_seeker()
    result = seeker.upload_cv(str(test_file))

    assert result == str(test_file)
    assert seeker.cv_path == str(test_file)


def test_apply_job_tracks_application():
    """Applying to a job should record the job ID for the seeker."""
    seeker = job_seeker()

    result = seeker.apply_job("JOB-101")

    assert result == "JOB-101"
    assert "JOB-101" in seeker.applied_jobs


def test_search_jobs_filters_by_keyword():
    """The search should return only relevant job matches."""
    seeker = job_seeker()

    matches = seeker.search_jobs("python")

    assert len(matches) >= 1
    assert any(job["title"] == "Python Developer" for job in matches)
    assert all("python" in " ".join([job["title"], job["company"], *job["skills"]]).lower() for job in matches)


def test_search_jobs_no_match_returns_empty_list():
    """Unknown filters should not return any jobs."""
    seeker = job_seeker()

    matches = seeker.search_jobs("nonexistent-role")

    assert matches == []
