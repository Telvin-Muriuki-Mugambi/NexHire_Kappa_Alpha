from Models.Auth import Auth, AuthenticationError, AuthorizationError


def main():
	auth = Auth()

	user = auth.register(
		"Telvin",
		"telvin@gmail.com",
		"2345432",
		"dcdceee",
		role="job_seeker",
	)

	print(f"Registered {user.email} as {user.role}")

	try:
		logged_in_user = auth.login("telvin@gmail.com", "dcdceee")
		print(f"Logged in as {logged_in_user.name}")
		auth.require_role("JOB_SEEKER")
		print("Job seeker access granted")
	except (AuthenticationError, AuthorizationError) as error:
		print(error)
	finally:
		auth.logout()
		print("Logged out")


if __name__ == "__main__":
	main()