import os
import shutil
import tkinter as tk
from tkinter import filedialog
class job_seeker:
    # dummy data

    job_postings = [
        {"id": 1, "title": "Senior Python Developer", "location": "Remote", "type": "Full-time", "skills": ["Python", "Django", "SQL"]},
        {"id": 2, "title": "Data Analyst", "location": "New York, NY", "type": "Full-time", "skills": ["Python", "Excel", "Tableau"]},
        {"id": 3, "title": "Frontend Engineer", "location": "Remote", "type": "Contract", "skills": ["JavaScript", "React", "CSS"]},
        {"id": 4, "title": "Junior Python Developer", "location": "Austin, TX", "type": "Full-time", "skills": ["Python", "Flask"]},
        {"id": 5, "title": "DevOps Engineer", "location": "Remote", "type": "Part-time", "skills": ["AWS", "Docker", "Linux"]},
    ]

    cv_file_path = "Models/jobseekers_cv's"

    

    def search_job(self):
        print ("\n 1. Filter by any Keyword")
        print("\n 2. Filter by Job title")
        print("\n 3. Filter by Location")
        print("\n 4. Filter by job type eg hybrid")
        print("\n 5. Filter by skills")
        # initialize filter variables to avoid NameError
        any_keyword = title = location = job_type = skill = None

        while True:
            options = input("Choose one of the options from 1 to 5:")

            if options == "1":
                any_keyword = input("Enter search keyword: ").strip() or None
                break
            elif options == "2":
                title = input("Enter job title: ").strip() or None
                break
            elif options == "3":
                location = input("Enter location: ").strip() or None
                break
            elif options == "4":
                job_type = input("Enter job type (Full-time/Part-time/Contract): ").strip() or None
                break
            elif options == "5":
                skill = input("Enter skill: ").strip() or None
                break
            else:
                print("Invalid choice. Please pick a number from 1 to 5:")

        filtered_list = []
        for job in self.job_postings:
         
            if any_keyword:
                combined_text = f"{job['title']} {job['location']} {job['type']} {' '.join(job['skills'])}".lower()
                if any_keyword.lower() not in combined_text:
                    continue

            if title and title.lower() not in job.get("title", "").lower():
                continue
                        
            if job_type and job_type.lower() not in job.get("type", "").lower():
                continue
            if skill:
                skills = [s.lower() for s in job.get("skills", [])]
                if skill.lower() not in skills:
                    continue

            filtered_list.append(job)

        return print(filtered_list)
    def upload_file(self, target_directory=None):
        """Opens native OS file chooser and copies selected CV to predetermined destination directory."""
        save_directory = target_directory or self.cv_file_path

        print("\nOpening file selection window...")

        # Setup hidden Tkinter root window
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected_file_path = filedialog.askopenfilename(
            title="Select CV / Resume to Upload",
            filetypes=[
                ("Supported CV Formats", "*.pdf *.docx *.txt"),
                ("All Files", "*.*")
            ]
        )

        if not selected_file_path:
            print("❌ Upload cancelled: No file selected.")
            return None

        # Automatically create output folder if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)

        # Build path and copy file
        file_name = os.path.basename(selected_file_path)
        destination_path = os.path.join(save_directory, file_name)
        shutil.copy(selected_file_path, destination_path)

        print("✅ Success! CV copied to target directory:")
        print(f"   {os.path.abspath(destination_path)}")
        return destination_path
    def run(self):
        """Launches the interactive menu system loop in the terminal."""
        while True:
            print("\n==============================")
            print("   JOB SEEKER CLI APP")
            print("==============================")
            print("1. Search Jobs")
            print("2. Upload CV")
            print("3. Exit Application")

            choice = input("\nChoose an option (1-3): ").strip()

            if choice == "1":
                self.search_job()
            elif choice == "2":
                self.upload_file()
            elif choice == "3":
                print("\nExiting application. Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1, 2, or 3.")



if __name__ == "__main__":
    job_seeker().run()
        
               


    

    


    
    