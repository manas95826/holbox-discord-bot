from setuptools import setup, find_packages

setup(
    name="community-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.3.2",
        "python-dotenv>=1.0.0",
        "supabase>=2.0.0",
        "openai>=1.0.0",
        "empire-chain>=0.1.0",
        "python-dateutil>=2.8.2"
    ],
    python_requires=">=3.7",
) 