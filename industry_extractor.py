industry_type = [
    "Agriculture","Automotive","Aerospace","Banking","Biotechnology","Chemical","Construction","Consulting","Consumer Goods",
    "Defense","E-Commerce","Education","Electronics","Energy","Entertainment","Environmental Services","Fashion","Fintech",
    "Food & Beverage","Gaming","Government","Healthcare","Hospitality","Information Technology","Insurance","Legal Services",
    "Logistics","Manufacturing","Marine","Media & Broadcasting","Mining & Metals","Non-Profit","Oil & Gas","Pharmaceuticals",
    "Publishing","Real Estate","Renewable Energy","Research & Development","Retail","Robotics","Software Development","Sports",
    "Telecommunications","Textiles","Tourism","Transportation","Utilities","Venture Capital","Waste Management","Wholesale",
    "Software Development","Web Development","Mobile App Development","Artificial Intelligence","Machine Learning","Deep Learning",
    "Natural Language Processing","Computer Vision","Data Science","Big Data Analytics","Cloud Computing","Cybersecurity",
    "Blockchain","Cryptocurrency","Fintech","HealthTech","EdTech","AgriTech","LegalTech","E-Commerce","Gaming","Game Development",
    "Virtual Reality","Augmented Reality","Mixed Reality","Robotics","Internet of Things","Embedded Systems","Computer Networks",
    "Telecommunications","DevOps","Database Management","Business Intelligence","SaaS (Software as a Service)",
    "PaaS (Platform as a Service)","IaaS (Infrastructure as a Service)","Cloud Security","Digital Marketing Technology",
    "AdTech","InsurTech","Automotive Software","Smart Cities","Industrial Automation","Quantum Computing","5G Technology",
    "Wearable Technology","IT Consulting","UI/UX Design","Open Source Software", "Health Care", "IT" 
]

industry_type_expansion = {
    "technology": [
        "information technology", "software development", "web development", "mobile app development",
        "it consulting", "tech", "technology", "software", "computer technology", "digital technology"
    ],
    "artificial intelligence": [
        "artificial intelligence", "machine learning", "deep learning", "ai", "ml", "neural networks",
        "cognitive computing", "intelligent systems", "ai research", "machine intelligence"
    ],
    "data science": [
        "data science", "big data analytics", "data analytics", "business intelligence", "data mining",
        "predictive analytics", "statistical analysis", "data engineering", "analytics"
    ],
    "computer vision": [
        "computer vision", "image processing", "visual recognition", "image analysis",
        "pattern recognition", "visual ai", "computer graphics", "image ai"
    ],
    "natural language processing": [
        "natural language processing", "nlp", "text processing", "language ai",
        "computational linguistics", "speech processing", "text analytics"
    ],
    "cloud computing": [
        "cloud computing", "saas (software as a service)", "paas (platform as a service)",
        "iaas (infrastructure as a service)", "cloud services", "cloud infrastructure",
        "cloud solutions", "aws", "azure", "google cloud", "cloud security"
    ],
    "cybersecurity": [
        "cybersecurity", "information security", "cyber security", "network security",
        "data security", "security services", "infosec", "cyber defense", "digital security"
    ],
    "blockchain": [
        "blockchain", "cryptocurrency", "crypto", "distributed ledger", "bitcoin",
        "ethereum", "defi", "web3", "digital currency", "cryptography"
    ],
    "fintech": [
        "fintech", "financial technology", "digital finance", "payment technology",
        "insurtech", "regtech", "wealthtech", "digital banking", "financial services technology"
    ],
    "healthtech": [
        "healthtech", "health technology", "medical technology", "digital health",
        "telemedicine", "health informatics", "medical devices", "biotech", "medtech", "Health Care"
    ],
    "edtech": [
        "edtech", "educational technology", "e-learning", "online learning",
        "learning management systems", "digital education", "education technology"
    ],
    "agritech": [
        "agritech", "agricultural technology", "precision agriculture", "smart farming",
        "farm technology", "agricultural innovation", "agtech"
    ],
    "legaltech": [
        "legaltech", "legal technology", "lawtech", "legal software", "legal services technology",
        "legal innovation", "legal automation"
    ],
    "e-commerce": [
        "e-commerce", "ecommerce", "online retail", "digital commerce", "electronic commerce",
        "online marketplace", "retail technology", "digital retail"
    ],
    "gaming": [
        "gaming", "game development", "video games", "mobile gaming", "console gaming",
        "pc gaming", "game industry", "interactive entertainment", "esports"
    ],
    "virtual reality": [
        "virtual reality", "vr", "immersive technology", "virtual worlds", "vr development"
    ],
    "augmented reality": [
        "augmented reality", "ar", "mixed reality", "mr", "extended reality", "xr",
        "immersive media", "spatial computing"
    ],
    "robotics": [
        "robotics", "automation", "robotic systems", "industrial automation",
        "robotic process automation", "rpa", "autonomous systems"
    ],
    "internet of things": [
        "internet of things", "iot", "connected devices", "smart devices",
        "sensor networks", "embedded systems", "wearable technology"
    ],
    "telecommunications": [
        "telecommunications", "telecom", "5g technology", "wireless technology",
        "network infrastructure", "communications technology", "mobile networks"
    ],
    "devops": [
        "devops", "continuous integration", "continuous deployment", "ci/cd",
        "infrastructure as code", "site reliability engineering"
    ],
    "database management": [
        "database management", "database systems", "data storage", "database administration",
        "sql", "nosql", "data warehousing"
    ],
    "digital marketing technology": [
        "digital marketing technology", "adtech", "advertising technology", "martech",
        "marketing automation", "digital advertising", "programmatic advertising"
    ],
    "automotive": [
        "automotive", "automobile", "car manufacturing", "automotive software",
        "autonomous vehicles", "electric vehicles", "automotive technology"
    ],
    "aerospace": [
        "aerospace", "aviation", "space technology", "aircraft manufacturing",
        "defense aerospace", "commercial aviation", "space exploration"
    ],
    "banking": [
        "banking", "financial services", "commercial banking", "investment banking",
        "retail banking", "digital banking", "financial institutions"
    ],
    "biotechnology": [
        "biotechnology", "biotech", "life sciences", "biopharmaceuticals",
        "genetic engineering", "molecular biology", "biomedical research"
    ],
    "chemical": [
        "chemical", "chemicals", "petrochemicals", "specialty chemicals",
        "chemical manufacturing", "chemical processing", "materials science"
    ],
    "construction": [
        "construction", "building", "real estate development", "infrastructure",
        "civil engineering", "architecture", "smart cities", "construction technology"
    ],
    "consulting": [
        "consulting", "management consulting", "business consulting", "strategy consulting",
        "technology consulting", "professional services", "advisory services"
    ],
    "consumer goods": [
        "consumer goods", "retail", "consumer products", "fmcg", "fast moving consumer goods",
        "wholesale", "consumer electronics", "household products"
    ],
    "defense": [
        "defense", "military", "government", "public sector", "defense technology",
        "homeland security", "government services"
    ],
    "education": [
        "education", "academic", "university", "schools", "higher education",
        "k-12 education", "educational services", "research institutions"
    ],
    "electronics": [
        "electronics", "semiconductor", "computer hardware", "electronic devices",
        "consumer electronics", "embedded systems", "microelectronics"
    ],
    "energy": [
        "energy", "oil & gas", "renewable energy", "utilities", "power generation",
        "clean energy", "solar energy", "wind energy", "nuclear energy"
    ],
    "entertainment": [
        "entertainment", "media & broadcasting", "film", "television", "music",
        "publishing", "digital media", "content creation", "streaming"
    ],
    "environmental services": [
        "environmental services", "waste management", "sustainability", "green technology",
        "environmental consulting", "renewable resources", "clean technology"
    ],
    "fashion": [
        "fashion", "apparel", "textiles", "clothing", "luxury goods",
        "fashion technology", "retail fashion", "fashion design"
    ],
    "food & beverage": [
        "food & beverage", "food processing", "agriculture", "food technology",
        "beverage industry", "food manufacturing", "nutrition"
    ],
    "healthcare": [
        "healthcare", "medical", "pharmaceuticals", "hospital", "clinical",
        "medical devices", "health services", "biomedical", "life sciences"
    ],
    "hospitality": [
        "hospitality", "tourism", "travel", "hotels", "restaurants",
        "leisure", "hospitality technology", "travel technology"
    ],
    "insurance": [
        "insurance", "insurtech", "risk management", "actuarial", "underwriting",
        "insurance technology", "reinsurance", "financial protection"
    ],
    "legal services": [
        "legal services", "law", "legal", "law firms", "legal consulting",
        "compliance", "regulatory", "legal technology"
    ],
    "logistics": [
        "logistics", "transportation", "supply chain", "shipping", "freight",
        "distribution", "warehouse management", "delivery services"
    ],
    "manufacturing": [
        "manufacturing", "industrial", "production", "factory automation",
        "industrial automation", "smart manufacturing", "industry 4.0"
    ],
    "marine": [
        "marine", "maritime", "shipping", "offshore", "naval",
        "marine technology", "ocean engineering", "port operations"
    ],
    "mining & metals": [
        "mining & metals", "mining", "metals", "extraction", "mineral processing",
        "metallurgy", "mining technology", "resources"
    ],
    "non-profit": [
        "non-profit", "nonprofit", "ngo", "charity", "social sector",
        "humanitarian", "public interest", "social impact"
    ],
    "pharmaceuticals": [
        "pharmaceuticals", "pharma", "drug development", "clinical research",
        "medical research", "pharmaceutical manufacturing", "biopharma"
    ],
    "real estate": [
        "real estate", "property", "real estate development", "property management",
        "commercial real estate", "residential real estate", "proptech"
    ],
    "research & development": [
        "research & development", "r&d", "research", "scientific research",
        "innovation", "product development", "technology research"
    ],
    "sports": [
        "sports", "athletics", "sports technology", "fitness", "recreation",
        "sports entertainment", "sports analytics", "esports"
    ],
    "venture capital": [
        "venture capital", "private equity", "investment", "funding", "startups",
        "angel investing", "venture funding", "capital markets"
    ],
    "quantum computing": [
        "quantum computing", "quantum technology", "quantum research", "quantum systems",
        "quantum information", "quantum algorithms", "quantum hardware"
    ],
    "smart cities": [
        "smart cities", "urban technology", "city planning", "municipal technology",
        "civic technology", "urban innovation", "digital cities"
    ],
    "ui/ux design": [
        "ui/ux design", "user experience", "user interface", "design", "product design",
        "interaction design", "visual design", "digital design"
    ],
    "open source software": [
        "open source software", "open source", "oss", "free software",
        "community software", "collaborative development", "open source technology"
    ]
}

import spacy
from spacy.matcher import PhraseMatcher

class IndustryExtractor:
    def __init__(self, industries, industry_expansions=None):
        """
        Initialize the extractor with industries and their expansions.
        :param industries: list of canonical industries
        :param industry_expansions: dict mapping canonical industries -> list of expansions
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.industry_expansions = industry_expansions or {}

        self._build_matcher(industries)

    def _build_matcher(self, industries):
        """Build PhraseMatcher with industries and their expansions."""
        for industry in industries:
            expansions = self.industry_expansions.get(industry, [industry])
            patterns = [self.nlp.make_doc(term) for term in expansions]
            self.matcher.add(industry, patterns)

    def extract(self, text):
        """
        Extract canonical industries from text.
        :param text: input string
        :return: list of canonical industries found
        """
        doc = self.nlp(text)
        found_industries = {
            self.nlp.vocab.strings[match_id] for match_id, start, end in self.matcher(doc)
        }
        return list(found_industries)


# extractor = IndustryExtractor(industry_type, industry_type_expansion)

# text = "The integration of agriculture, automotive, aerospace, banking, biotechnology, chemical, construction, consulting, consumer goods, defense, and e-commerce sectors has accelerated innovation across industries, driving global economic growth and technological advancements."
# print(extractor.extract(text))


