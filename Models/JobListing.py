import random

class JobListing:
   def __init__(
       self,
       title,
       description,
       location,
       skills,
       pay_rate,
       experience_level,
       availability,
       job_id=None,
       status="PENDING",
   ):
       if pay_rate < 0:
           raise ValueError("pay_rate cannot be negative")
       if experience_level.lower() not in {"entry", "mid", "senior"}:
           raise ValueError("invalid experience level")
       self.job_id = job_id if job_id is not None else random.randint(1000, 9999)
       self.title = title
       self.description = description
       self.location = location
       self.skills = skills
       self.pay_rate = pay_rate
       self.experience_level = experience_level
       self.availability = availability
       self.status = status


   def approve(self):
       self.status = "APPROVED"


   def reject(self):
       self.status = "REJECTED"


   def matches_criteria(self, filters):
       if "location" in filters and filters["location"].lower() not in self.location.lower():
           return False
       if "skills" in filters:
           listing_skills = {skill.lower() for skill in self.skills}
           if not all(skill.lower() in listing_skills for skill in filters["skills"]):
               return False
       if "min_pay" in filters and self.pay_rate < filters["min_pay"]:
           return False
       if "availability" in filters and self.availability.lower() != filters["availability"].lower():
           return False
       return True


   def to_dict(self):
       return {
           "job_id": self.job_id,
           "title": self.title,
           "description": self.description,
           "location": self.location,
           "skills": self.skills,
           "pay_rate": self.pay_rate,
           "experience_level": self.experience_level,
           "availability": self.availability,
           "status": self.status,
       }


   @classmethod
   def from_dict(cls, record):
       return cls(
           record["title"],
           record["description"],
           record["location"],
           record["skills"],
           record["pay_rate"],
           record["experience_level"],
           record["availability"],
           job_id=record["job_id"],
           status=record.get("status", "PENDING"),
       )




