from setuptools import find_packages, setup


def get_version() -> str:
    rel_path = "src/cog_hf_template/__init__.py"
    with open(rel_path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

extras = {}

extras["dev"] = [
    "black",
    "ruff",
]
extras["gcp"] = [
    "google-cloud-storage",
]
extras["cli"] = [
    "fire",
]
extras["all"] = extras["dev"] + extras["gcp"] + extras["cli"]


setup(
    name="cog_hf_template",
    version=get_version(),
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description="Cog template for Hugging Face.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Apache",
    install_requires=requirements,
    extras_require=extras,
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["cog-hf-template=cog_hf_template.cli:main"]},
)
