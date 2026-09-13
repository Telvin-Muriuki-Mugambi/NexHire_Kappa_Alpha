import os
import shutil
import tkinter as tk
from tkinter import filedialog

class JobSeeker:
    job_postings = [
        {"id": 1, "title": "Senior Python Developer", "location": "Remote", "type": "Full-time", "skills": ["Python", "Django", "SQL"]},
        {"id": 2, "title": "Data Analyst", "location": "New York, NY", "type": "Full-time", "skills": ["Python", "Excel", "Tableau"]},
        {"id": 3, "title": "Frontend Engineer", "location": "Remote", "type": "Contract", "skills": ["JavaScript", "React", "CSS"]},
        {"id": 4, "title": "Junior Python Developer", "location": "Austin, TX", "type": "Full-time", "skills": ["Python", "Flask"]},
        {"id": 5, "title": "DevOps Engineer", "location": "Remote", "type": "Part-time", "skills": ["AWS", "Docker", "Linux"]},
    ]

    cv_file_path = "Models/jobseekers_cv's"

    def filter_jobs(self, any_keyword=None, title=None, location=None, job_type=None, skill=None):
        """Filters job postings based on provided parameters."""
        filtered_list = []
        for job in self.job_postings:
            if any_keyword:
                combined_text = f"{job['title']} {job['location']} {job['type']} {' '.join(job['skills'])}".lower()
                if any_keyword.lower() not in combined_text:
                    continue

            if title and title.lower() not in job.get("title", "").lower():
                continue
                
            if location and location.lower() not in job.get("location", "").lower():
                continue
                        
            if job_type and job_type.lower() not in job.get("type", "").lower():
                continue
                
            if skill:
                skills = [s.lower() for s in job.get("skills", [])]
                if skill.lower() not in skills:
                    continue

            filtered_list.append(job)

        return filtered_list

    def upload_file(self, target_directory=None):
        """Opens native OS file chooser and copies selected CV to predetermined destination directory."""
        save_directory = target_directory or self.cv_file_path

        print("\n📂 Opening file selection window...")
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        file_path = filedialog.askopenfilename(
            title="Select CV / Resume to Upload",
            filetypes=[
                ("Supported CV Formats", "*.pdf *.docx *.txt"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            print("⚠️ Upload cancelled: No file selected.")
            return None

        os.makedirs(save_directory, exist_ok=True)
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(save_directory, file_name)
        shutil.copy(file_path, destination_path)

        print("✨ Success! CV copied to target directory:")
        print(f"   📁 {os.path.abspath(destination_path)}")
        return destination_path



if __name__ == "__main__":
    job_seeker()
        
               


    

    


