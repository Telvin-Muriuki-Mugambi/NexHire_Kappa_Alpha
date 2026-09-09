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

#Test to ensure all the job listings created result to a pending status
def test_new_listing_defaults_to_pending(listing):
	assert listing.status == "PENDING"