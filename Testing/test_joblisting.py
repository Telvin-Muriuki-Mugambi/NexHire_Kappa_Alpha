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

#Test to approve of Job Listing and changing status from PENDING to APPROVE
def test_approve_changes_status(listing):
	listing.approve()

	assert listing.status == "APPROVED"

#Test to REJECT of Job Listing and changing status from PENDING to REJECTED
def test_reject_changes_status(listing):
	listing.reject()

	assert listing.status == "REJECTED"

#Test to ensure filtering function works. Filters using location, skills, expected minimum pay, and job availability
def test_matches_location_skills_pay_and_availability(listing):
	filters = {
		"location": "nai",
		"skills": ["python"],
		"min_pay": 4000,
		"availability": "full_time",
	}

	assert listing.matches_criteria(filters)

@pytest.mark.parametrize(
	"filters",
	[
		{"location": "Mombasa"},
		{"skills": ["Java"]},
		{"min_pay": 6000},
		{"availability": "PART_TIME"},
	],
)

#Test to check when criteria is not met
def test_does_not_match_when_a_filter_fails(listing, filters):
	assert not listing.matches_criteria(filters)

#Test to empty the filters
def test_empty_filters_match_every_listing(listing):
	assert listing.matches_criteria({})

#Test to ensure no negative amount is inserted
def test_negative_pay_rate_is_rejected():
	with pytest.raises(ValueError):
		JobListing("Role", "Description", "Nairobi", [], -1, "ENTRY", "FULL_TIME")

#Test to reject invalid experience level
@pytest.mark.parametrize("experience_level", ["intern", "expert", ""])
def test_invalid_experience_level_is_rejected(experience_level):
	with pytest.raises(ValueError):
		JobListing("Role", "Description", "Nairobi", [], 1000, experience_level, "FULL_TIME")
