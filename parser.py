import json

from location_extractor import LocationExtractor
from experience_extractor import NumberExtractor
from skill_extractor import SkillExtractor, skills_expansions, skills_list
from industry_extractor import IndustryExtractor, industry_type_expansion, industry_type
from job_extractor import JobTitleExtractor, job_title_expansion, job_titles

def build_crust_filters_from_text(text):
    """
    Extracts experience, industry, job title, location, and skills from text
    and builds a CrustData /screener/persondb/search filters JSON.
    """

    # --- Run all extractors ---
    extractor_experience = NumberExtractor()
    extracted_experience = extractor_experience.extract(text)

    extractor_industry = IndustryExtractor(industry_type, industry_type_expansion)
    extracted_industry = extractor_industry.extract(text)

    extractor_job_title = JobTitleExtractor(job_titles, job_title_expansion)
    extracted_job_title = extractor_job_title.extract(text)

    extractor_location = LocationExtractor()
    extracted_location = extractor_location.extract(text)

    extractor_skills = SkillExtractor(skills_list, skills_expansions)
    extracted_skills = extractor_skills.extract(text)

    # --- Build filter JSON ---
    conditions = []

    # Experience
    if extracted_experience:
        exp_conditions = []
        for num, op in extracted_experience:
            if op in ['=', '=>', '=<', '>', '<']:
                exp_conditions.append({
                    "column": "years_of_experience_raw",
                    "type": op,
                    "value": num
                })
        if exp_conditions:
            conditions.append({"op": "or", "conditions": exp_conditions})

    # Industry
    if extracted_industry:
        ind_conditions = [
            {"column": "all_employers.company_industries", "type": "(.)", "value": ind}
            for ind in extracted_industry
        ]
        conditions.append({"op": "or", "conditions": ind_conditions})

    # Job Title
    if extracted_job_title:
        jt_conditions = [
            {"column": "current_employers.title", "type": "(.)", "value": jt}
            for jt in extracted_job_title
        ]
        conditions.append({"op": "or", "conditions": jt_conditions})

    # Location
    if extracted_location:
        loc_conditions = [
            {"column": "region", "type": "(.)", "value": loc}
            for loc in extracted_location
        ]
        conditions.append({"op": "or", "conditions": loc_conditions})

    # Skills
    if extracted_skills:
        skill_conditions = [
            {"column": "skills", "type": "(.)", "value": skill}
            for skill in extracted_skills
        ]
        conditions.append({"op": "or", "conditions": skill_conditions})

    filters = {
        "filters": {
            "op": "and",
            "conditions": conditions
        },
        "limit": 3,
        "preview": True
    }

    return json.dumps(filters, indent=4)


# ---------------- Example usage ----------------
if __name__ == "__main__":
    text = "I have around five years of experience as a Software Engineer in Health Care industry at Karachi, Pakistan, with skills in Python, JavaScript, and Spring."

    filters_json = build_crust_filters_from_text(text)
    print(filters_json)
