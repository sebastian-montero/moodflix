from moodflix.text import ABOUT


if __name__ == "__main__":
    readme = f"""# Moodflix

{ABOUT.replace("# About", "").replace("## Extras", "")}"""
    
    with open("README.md", "w") as f:
        f.write(readme)

