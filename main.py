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
text = "Find me a Software Engineer with two years of experience, also skilled in Python, Spring, JavaScript having experience in Health Care and located in Karachi, Pakistan."
# text = "Find me a healthcare it specialist with five years of experience, also skilled in Express.js, VHDL, CI/CD Pipelines, SVG Animations having experience in e-commerce and located in France."

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

import json

def build_crust_filters(extracted_experience, extracted_industry, extracted_job_title,
                        extracted_location, extracted_skills):
    """
    Build CrustData screener/persondb/search filters JSON
    from extracted fields.
    """

    conditions = []

    # --- Experience ---
    if extracted_experience:
        exp_conditions = []
        for num, op in extracted_experience:  # e.g., [(2, '=')]
            # map operator
            if op == '=':
                operator = '='
            elif op == '=>':
                operator = '=>'
            elif op == '=<':
                operator = '=<'
            elif op == '>':
                operator = '>'
            elif op == '<':
                operator = '<'
            else:
                continue

            exp_conditions.append({
                "column": "years_of_experience_raw",
                "type": operator,
                "value": num
            })
        if exp_conditions:
            conditions.append({"op": "or", "conditions": exp_conditions})

    # --- Industry ---
    if extracted_industry:
        ind_conditions = []
        for ind in extracted_industry:
            ind_conditions.append({
                "column": "all_employers.company_industries",
                "type": "(.)",
                "value": ind
            })
        if ind_conditions:
            conditions.append({"op": "or", "conditions": ind_conditions})

    # --- Job Title ---
    if extracted_job_title:
        jt_conditions = []
        for jt in extracted_job_title:
            jt_conditions.append({
                "column": "current_employers.title",
                "type": "(.)",
                "value": jt
            })
        if jt_conditions:
            conditions.append({"op": "or", "conditions": jt_conditions})

    # --- Location ---
    if extracted_location:
        loc_conditions = []
        for loc in extracted_location:
            loc_conditions.append({
                "column": "region",
                "type": "(.)",
                "value": loc
            })
        if loc_conditions:
            conditions.append({"op": "or", "conditions": loc_conditions})

    # --- Skills ---
    if extracted_skills:
        skill_conditions = []
        for skill in extracted_skills:
            skill_conditions.append({
                "column": "skills",
                "type": "(.)",
                "value": skill
            })
        if skill_conditions:
            conditions.append({"op": "or", "conditions": skill_conditions})

    # Final filter structure
    filters = {
        "filters": {
            "op": "and",
            "conditions": conditions
        },
        "limit": 3,
        "preview": True
    }

    return json.dumps(filters, indent=4)



filters_json = build_crust_filters(
    extracted_experience,
    extracted_industry,
    extracted_job_title,
    extracted_location,
    extracted_skills
)

print(filters_json)
