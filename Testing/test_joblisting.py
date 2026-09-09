import pytest

from Models.JobListing import JobListing


@pytest.fixture
def listing():
	return JobListing(
		"Python Developer",
		"Build backend services",
		"Nairobi",
		["Python", "SQL"],
		5000,
		"mid",
		"FULL_TIME",
	)