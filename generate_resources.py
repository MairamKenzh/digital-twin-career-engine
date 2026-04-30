def get_resources(skill):
    return [
        f"YouTube tutorials for {skill}",
        f"GitHub repositories for {skill}",
        f"Best online course for {skill}"
    ]

skills_to_learn = ["Unity", "Prompt Engineering", "Figma"]

print("Suggested learning resources:\n")

for skill in skills_to_learn:
    print(f"{skill}:")
    for item in get_resources(skill):
        print(" -", item)
    print()