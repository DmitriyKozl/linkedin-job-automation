class Job:
    def __init__(self, name, skills, job_type, company, location, url,recruiter_link):
        self.name = name
        self.skills = skills
        self.job_type = job_type
        self.company = company
        self.location = location
        self.url = url
        self.recruiter_link = recruiter_link

    def to_dict(self):
        return {
            self.name: {
                "skills": self.skills,
                "job_type": self.job_type,
                "company": self.company,
                "location": self.location,
                "url": self.url,
                "recruiter_link": self.recruiter_link
            }
        }

    def __str__(self):
        return str(self.to_dict())

