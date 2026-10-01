"""
Constants, taxonomy, and suggested datasets for AscendCareer Resume Guide.
"""

SUGGESTED_JOB_ROLES = [
    "Software Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Engineer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "Cloud Solutions Architect",
    "Cybersecurity Analyst",
    "Product Manager",
    "QA / Test Automation Engineer",
    "Mobile App Developer (iOS/Android)",
    "Database Administrator",
    "Systems Engineer",
    "Embedded Systems Engineer",
    "AI Research Scientist",
    "Site Reliability Engineer (SRE)",
    "Blockchain Developer",
    "UI/UX Designer",
    "Business Intelligence Analyst",
]

SUGGESTED_COMPANIES = [
    "Google",
    "Microsoft",
    "Amazon",
    "Meta",
    "Apple",
    "Netflix",
    "MNC (Multinational Corporation)",
    "Startup (Early Stage)",
    "Startup (Growth / Series B+)",
    "General Tech Company",
    "FinTech (e.g. Stripe, PayPal, Goldman Sachs)",
    "Consulting Firm (e.g. Deloitte, McKinsey, Accenture)",
    "Enterprise SaaS Company",
    "Healthcare Tech",
    "E-Commerce Platform",
]

# Skills map for reference & gap analysis
ROLE_SKILL_DATABASE = {
    "software developer": [
        "python", "java", "c++", "data structures", "algorithms", "git",
        "object-oriented programming", "rest api", "sql", "problem solving",
        "unit testing", "system design"
    ],
    "frontend developer": [
        "javascript", "typescript", "react", "html5", "css3", "tailwind css",
        "redux", "next.js", "responsive design", "web performance", "rest api", "git"
    ],
    "backend developer": [
        "python", "node.js", "fastapi", "django", "java", "spring boot",
        "rest api", "postgresql", "mongodb", "redis", "docker", "microservices", "git"
    ],
    "full stack engineer": [
        "javascript", "typescript", "react", "node.js", "python", "sql",
        "rest api", "docker", "git", "cloud computing", "mongodb", "postgresql"
    ],
    "data analyst": [
        "sql", "python", "excel", "power bi", "tableau", "data visualization",
        "statistical analysis", "pandas", "numpy", "data cleaning", "reporting", "etl"
    ],
    "data scientist": [
        "python", "r", "machine learning", "scikit-learn", "pandas", "numpy",
        "statistical modeling", "deep learning", "sql", "tensorflow", "pytorch", "data visualization"
    ],
    "machine learning engineer": [
        "python", "pytorch", "tensorflow", "scikit-learn", "mlops", "docker",
        "deep learning", "nlp", "computer vision", "kubernetes", "data pipelines", "git"
    ],
    "devops engineer": [
        "docker", "kubernetes", "ci/cd", "aws", "terraform", "linux",
        "jenkins", "github actions", "bash", "prometheus", "ansible", "cloud computing"
    ],
    "cloud solutions architect": [
        "aws", "azure", "gcp", "cloud architecture", "terraform", "microservices",
        "networking", "security", "docker", "kubernetes", "high availability", "disaster recovery"
    ],
    "cybersecurity analyst": [
        "network security", "siem", "vulnerability assessment", "incident response",
        "penetration testing", "firewalls", "wireshark", "compliance", "threat intelligence", "linux"
    ],
    "product manager": [
        "product strategy", "agile", "scrum", "roadmap planning", "user research",
        "kpis", "jira", "wireframing", "a/b testing", "cross-functional leadership", "data analytics"
    ],
    "qa / test automation engineer": [
        "selenium", "cypress", "python", "java", "test automation", "api testing",
        "junit", "pytest", "ci/cd", "bug tracking", "test planning", "performance testing"
    ],
    "mobile app developer (ios/android)": [
        "flutter", "react native", "swift", "kotlin", "mobile ui",
        "rest api", "app store deployment", "git", "sqlite", "state management"
    ],
    "ui/ux designer": [
        "figma", "wireframing", "prototyping", "user research", "usability testing",
        "design systems", "information architecture", "interaction design", "adobe xd"
    ]
}

# Weak phrasing to strong action verbs mapping
WEAK_VERBS_MAP = {
    "worked on": ["architected", "engineered", "spearheaded", "developed", "built"],
    "worked with": ["collaborated with", "partnered with", "utilized", "leveraged"],
    "helped in": ["engineered", "streamlined", "optimized", "collaborated on"],
    "helped with": ["collaborated to deliver", "partnered across teams to accelerate", "co-authored", "facilitated"],
    "helped": ["collaborated to deliver", "accelerated", "facilitated", "partnered on"],
    "contributed to": ["spearheaded", "engineered", "collaborated on", "developed"],
    "contributed in": ["spearheaded", "engineered", "collaborated on"],
    "contributed": ["spearheaded", "engineered", "collaborated on"],
    "responsible for": ["drove", "led", "directed", "managed", "orchestrated"],
    "handled": ["resolved", "executed", "streamlined", "administered", "optimized"],
    "did": ["implemented", "executed", "delivered", "performed", "established"],
    "made": ["designed", "constructed", "formulated", "created", "generated"],
    "assisted": ["partnered with", "supported the delivery of", "contributed to", "enabled"],
    "used": ["leveraged", "utilized", "harnessed", "deployed", "integrated"],
    "tried": ["piloted", "initiated", "researched and benchmarked"]
}

# Unnecessary details patterns to flag
UNNECESSARY_DETAILS_KEYWORDS = [
    "marital status", "married", "single", "date of birth", "dob",
    "father's name", "mother's name", "religion", "caste", "nationality",
    "passport number", "gender", "photo attached", "hobbies: watching tv",
    "salary expectations", "references available upon request"
]
