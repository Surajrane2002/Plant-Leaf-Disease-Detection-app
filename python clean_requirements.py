import re

input_file = "requirements.txt"
output_file = "requirements_cleaned.txt"

cleaned_lines = []

with open(input_file, "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if "@" in line and "file://" in line:
            # Extract just the package name and guess version if possible
            pkg = line.split("@")[0].strip()
            version_match = re.search(rf"{pkg}-(\d+\.\d+(?:\.\d+)?)", line)
            version = version_match.group(1) if version_match else "latest"
            cleaned_line = f"{pkg}=={version}" if version != "latest" else pkg
            cleaned_lines.append(cleaned_line)
        else:
            cleaned_lines.append(line)

with open(output_file, "w") as f:
    f.write("\n".join(cleaned_lines))

print("✅ Cleaned requirements saved to", output_file)
