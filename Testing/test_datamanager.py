import json

import pytest

from Models.DataManager import DataManager
from Models.JobListing import JobListing
from Models.User import User


class TestDataManager:
	@pytest.fixture
	def manager(self, tmp_path):
		return DataManager(tmp_path)

	@pytest.fixture
	def user(self):
		return User("Ada", "ada@example.com", "0712345678", "secret")

	@pytest.fixture
	def job(self):
		return JobListing(
			"Python Developer",
			"Build APIs",
			"Nairobi",
			["Python"],
			5000,
			"mid",
			"FULL_TIME",
		)

	def test_initialization_creates_json_files(self, manager):
		assert manager.users_file.exists()
		assert manager.jobs_file.exists()
		assert json.loads(manager.users_file.read_text()) == []
		assert json.loads(manager.jobs_file.read_text()) == []

	def test_save_user_writes_structured_payload(self, manager, user):
		manager.save_user(user)

		payload = json.loads(manager.users_file.read_text())[0]
		assert payload["user_id"] == user.user_id
		assert payload["email"] == user.email
		assert payload["password_hash"] == user._password_hash

	def test_save_job_writes_structured_payload(self, manager, job):
		manager.save_job(job)

		assert json.loads(manager.jobs_file.read_text())[0] == job.to_dict()

	def test_load_users_recreates_user_instance(self, manager, user):
		manager.save_user(user)

		loaded = manager.load_users()
		assert isinstance(loaded[0], User)
		assert loaded[0].to_dict() == user.to_dict()
		assert loaded[0].verify_password("secret")

	def test_load_jobs_recreates_job_instance(self, manager, job):
		manager.save_job(job)

		loaded = manager.load_jobs()
		assert isinstance(loaded[0], JobListing)
		assert loaded[0].to_dict() == job.to_dict()

	def test_save_updates_existing_record(self, manager, job):
		manager.save_job(job)
		job.status = "APPROVED"
		manager.save_job(job)

		records = json.loads(manager.jobs_file.read_text())
		assert len(records) == 1
		assert records[0]["status"] == "APPROVED"

	def test_save_appends_new_records(self, manager, job):
		manager.save_job(job)
		second_job = JobListing(
			"Data Analyst",
			"Analyze reports",
			"Mombasa",
			["SQL"],
			4000,
			"entry",
			"PART_TIME",
		)
		manager.save_job(second_job)

		assert len(json.loads(manager.jobs_file.read_text())) == 2

	def test_empty_and_corrupt_files_load_as_empty(self, manager):
		manager.users_file.write_text("")
		manager.jobs_file.write_text("{not valid json")

		assert manager.load_users() == []
		assert manager.load_jobs() == []

	def test_missing_file_is_handled_cleanly(self, manager):
		manager.users_file.unlink()

		assert manager.load_users() == []

	def test_get_job_by_id_returns_job_or_none(self, manager, job):
		manager.save_job(job)

		assert manager.get_job_by_id(job.job_id).job_id == job.job_id
		assert manager.get_job_by_id(999999) is None
