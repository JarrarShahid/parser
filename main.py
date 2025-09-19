from location_extractor import LocationExtractor
from experience_extractor import NumberExtractor
from skill_extractor import SkillExtractor, skills_expansions, skills_list
from industry_extractor import IndustryExtractor, industry_type_expansion, industry_type
from job_extractor import JobTitleExtractor, job_title_expansion, job_titles

job_title_expansion = job_title_expansion
job_titles = job_titles
skills_expansions = skills_expansions
skills_list = skills_list
industry_type_expansion = industry_type_expansion
industry_type = industry_type
text = "Find me a Software Engineer with two years of experience, also skilled in Python, Spring, JavaScript having experience in Health Care and located in Pakistan."

# Experience
extractor_experience = NumberExtractor()
extracted_experience = extractor_experience.extract(text)

# Industry
extractor_industry = IndustryExtractor(industry_type, industry_type_expansion)
extracted_industry = extractor_industry.extract(text)

# Job Title
extractor_job_title = JobTitleExtractor(job_titles, job_title_expansion)
extracted_job_title = extractor_job_title.extract(text)

# Location
extractor_location = LocationExtractor()
extracted_location = locations = extractor_location.extract(text)

# Skills
extractor_skills = SkillExtractor(skills_list, skills_expansions)
extracted_skills = extractor_skills.extract(text)

print(text)
print(extracted_experience)
print(extracted_industry)
print(extracted_job_title)
print(extracted_location)
print(extracted_skills)

