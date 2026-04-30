import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("user_profile.json", "r", encoding="utf-8") as f:
    profile = json.load(f)

jobs = pd.read_csv("jobs_dataset.csv")

user_text = " ".join(profile["hard_skills"] + profile["soft_skills"] + profile["interests"])
corpus = [user_text] + jobs["skills"].tolist()

vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(corpus)

similarities = cosine_similarity(vectors[0], vectors[1:]).flatten()

results = []

user_skills_lower = set(skill.lower() for skill in profile["hard_skills"])

for i, row in jobs.iterrows():
    job = row["job_title"]
    skills = row["skills"].split()

    missing = [skill for skill in skills if skill.lower() not in user_skills_lower]

    results.append({
        "job": job,
        "score": round(float(similarities[i]) * 100, 2),
        "missing_skills": missing[:5]
    })

results = sorted(results, key=lambda x: x["score"], reverse=True)

print("Top 3 career matches:\n")
for r in results[:3]:
    print(r)
    