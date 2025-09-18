# import spacy
# import re

# # Load NLP model
# nlp = spacy.load("en_core_web_sm")

# # -----------------------
# # Dictionaries
# # -----------------------

# # ~200+ skills (extendable)
# skills_dict = [
#     # Frontend
#     "html", "css", "javascript", "typescript", "react", "next.js", "vue", "nuxt.js",
#     "angular", "svelte", "bootstrap", "tailwind", "jquery",
#     # Backend
#     "node", "express", "nestjs", "django", "flask", "spring", "dotnet", "php", "laravel", "ruby", "rails",
#     "golang", "c", "c++", "c#", "rust", "perl", "scala",
#     # Mobile
#     "react native", "flutter", "swift", "kotlin", "ios", "android",
#     # Cloud
#     "aws", "gcp", "azure", "firebase", "heroku", "digitalocean",
#     # Databases
#     "mysql", "postgresql", "sqlite", "mongodb", "dynamodb", "redis", "cassandra", "oracle", "mariadb",
#     # DevOps / Infra
#     "docker", "kubernetes", "terraform", "ansible", "jenkins", "git", "github", "gitlab", "bitbucket",
#     "linux", "bash", "shell", "powershell",
#     # Data / ML
#     "pandas", "numpy", "scipy", "tensorflow", "pytorch", "sklearn", "matlab", "sas", "r", "julia",
#     "hadoop", "spark", "hive", "kafka", "airflow",
#     # Other tools
#     "graphql", "rest", "grpc", "soap", "openapi",
#     "jira", "confluence", "notion", "figma", "tableau", "powerbi"
# ]

# # Normalize synonyms
# synonyms = {
#     "js": "JavaScript",
#     "node": "Node.js",
#     "express": "Express.js",
#     "gcp": "Google Cloud Platform",
#     "aws": "Amazon Web Services",
#     "azure": "Microsoft Azure",
#     "ml": "Machine Learning",
#     "ai": "Artificial Intelligence",
#     "db": "Database"
# }

# # Job titles dictionary
# job_titles = [
#     "software engineer", "fullstack developer", "frontend developer", "backend developer",
#     "web developer", "mobile developer", "ios developer", "android developer",
#     "cloud engineer", "devops engineer", "data engineer", "data scientist",
#     "machine learning engineer", "ai engineer", "ml engineer", "site reliability engineer",
#     "product manager", "project manager", "qa engineer", "test engineer",
#     "security engineer", "systems engineer", "network engineer", "solution architect",
#     "technical lead", "engineering manager", "cto", "cio"
# ]

# # -----------------------
# # Parsing function
# # -----------------------
# def parse_prompt(text: str):
#     doc = nlp(text)

#     # --- Experience ---
#     exp_match = re.search(r"(less than \d+\s+years|\d+\s+years)", text, re.I)
#     experience = exp_match.group(0) if exp_match else None

#     # --- Location ---
#     location = None
#     loc_match = re.search(r"(location\s+(is|should be)?\s*)([A-Za-z\s,]+)", text, re.I)
#     if loc_match:
#         location = loc_match.group(3).strip()
#     else:
#         # fallback: use NER
#         for ent in doc.ents:
#             if ent.label_ in ["GPE", "LOC"]:
#                 location = ent.text

#     # --- Job Title ---
#     job_title = None
#     for jt in job_titles:
#         if re.search(rf"\b{jt}\b", text.lower()):
#             job_title = jt
#             break

#     # --- Skills ---
#     found_skills = []
#     for skill in skills_dict:
#         if re.search(rf"\b{skill}\b", text.lower()):
#             normalized = synonyms.get(skill.lower(), skill.capitalize())
#             if normalized not in found_skills:
#                 found_skills.append(normalized)

#     return {
#         "experience": experience,
#         "location": location,
#         "job_title": job_title,
#         "skills": found_skills
#     }

# # -----------------------
# # Example
# # -----------------------
# if __name__ == "__main__":
#     text = "Find software engineer for less than 7 years experience in vue and node and gcp, location should be Fulda Germany"
#     result = parse_prompt(text)
#     print(result)

import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")

# -----------------------
# Dictionaries
# -----------------------




# -----------------------
# Helpers
# -----------------------
def expand_location(location: str):
    """
    Expand location into variants: city, city+country, full form etc.
    Example: 'Fulda Germany' -> ['Fulda', 'Germany', 'Fulda, Germany']
    """
    parts = [p.strip() for p in re.split(r"[,\s]+", location) if p.strip()]
    variants = set()

    # Add simple combinations
    for i in range(len(parts)):
        variants.add(parts[i])
    if len(parts) > 1:
        variants.add(", ".join(parts))          # full
        variants.add(parts[0] + ", " + parts[-1])  # city + country/state

    return list(variants)

# -----------------------
# Filter builder
# -----------------------
def build_filter(text: str):
    doc = nlp(text)

    filters = {"filters": {"op": "and", "conditions": []}}

    # --- Job Title ---
    for jt, expansions in job_titles.items():
        if jt in text.lower():
            jt_conditions = []
            for title in expansions:
                jt_conditions.append({
                    "column": "current_employers.title",
                    "type": "(.)",
                    "value": title
                })
            filters["filters"]["conditions"].append({
                "op": "or",
                "conditions": jt_conditions
            })
            break

    # --- Skills ---
    skill_conditions = []
    for skill in skills_dict:
        if re.search(rf"\b{re.escape(skill)}\b", text.lower()):
            variations = skill_expansions.get(skill, [skill])
            skill_group = []
            for v in variations:
                skill_group.append({
                    "column": "skills",
                    "type": "(.)",
                    "value": v
                })
            skill_conditions.append({"op": "or", "conditions": skill_group})

    if skill_conditions:
        filters["filters"]["conditions"].extend(skill_conditions)

    # --- Experience ---
    exp_match = re.search(r"(less than \d+|\d+)\s+years", text, re.I)
    if exp_match:
        exp_str = exp_match.group(0).lower()
        years = int(re.search(r"\d+", exp_str).group())
        if "less than" in exp_str:
            filters["filters"]["conditions"].append({
                "column": "years_of_experience_raw",
                "type": "=<",
                "value": years
            })
        else:
            filters["filters"]["conditions"].append({
                "column": "years_of_experience_raw",
                "type": "=",
                "value": years
            })

    # --- Location (modified) ---
    loc_match = re.search(r"(location\s+(is|should be)?\s*)([A-Za-z\s,]+)", text, re.I)
    if loc_match:
        location = loc_match.group(3).strip()
        variants = expand_location(location)
        filters["filters"]["conditions"].append({
            "op": "or",
            "conditions": [
                {
                    "column": "region",
                    "type": "(.)",
                    "value": v
                } for v in variants
            ]
        })

    return filters


# -----------------------
# Example
# -----------------------
if __name__ == "__main__":
    text = """Senior Software Engineer (Python, Node.js, React.js)
Location: Onsite (Preferred: Pakistan, U.S. Time Zone Overlap)
 Experience: 5+ years
About ConnectDevs
ConnectDevs is an AI-powered talent-matching platform helping U.S. companies discover, evaluate, and hire top-tier software engineers worldwide. We’re not just another recruiter—we understand intent, parse context, and deliver real-time matches powered by AI.
We’re looking for a Senior Software Engineer who thrives on problem-solving, building scalable systems, and translating technical complexity into client-friendly solutions.
Key Responsibilities
Design, build, and maintain scalable applications using Python, Node.js, and React.js.
Collaborate with cross-functional teams (Product, Design, AI/ML) to ship features with impact.
Write clean, maintainable, and testable code while mentoring junior engineers.
Translate technical concepts into business-friendly language for clients and stakeholders.
Troubleshoot and debug complex issues across the stack.
Contribute to architectural decisions and long-term technical strategy.
Stay up-to-date with emerging technologies, frameworks, and industry trends.
Requirements
Bachelor’s degree in Computer Science or equivalent.
5+ years of hands-on experience with Python, Node.js, and React.js.
Strong expertise in designing and scaling web applications.
Excellent problem-solving skills with the ability to think outside the box.
Clear and effective communication skills—able to simplify technical ideas for clients.
Experience working in agile environments and collaborating across distributed teams.
Familiarity with cloud platforms (AWS, GCP, or Azure) is a plus.
Exposure to AI/ML-driven products or recruiting platforms is a bonus."""
    result = build_filter(text)
    
    print(json.dumps(result, indent=2))
