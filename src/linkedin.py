from linkedin_api import Linkedin
from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import logging
from typing import List, Dict
from datetime import datetime, timedelta
from PyPDF2 import PdfReader

load_dotenv()

mcp = FastMCP("LinkedIn-MCP")
logger = logging.getLogger(__name__)
pdf_path = "Resume.pdf"

def get_creds():
    return Linkedin(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"), debug=True)

@mcp.tool()
def get_profile():
    """
    Retrieves the User Profile
    """
    linkedin = get_creds()
    profile = linkedin.get_profile()
    return profile

@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieve LinkedIn feed posts.

    :return: List of feed post details
    """
    linkedin = get_creds()
    try:
        post_urns = linkedin.get_feed_posts(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"
    
    posts = ""
    for urn in post_urns:
        posts += f"Post by {urn["author_name"]}: {urn["content"]}\n"

    return posts

@mcp.tool()
def search_jobs(
    keywords: str = "Software Engineer",
    location: str = "United States",
    experience: List[str] = ["2", "3", "4"],  # 1=Intern, 2=Entry, 3=Mid, 4=Senior
    job_type: str = "F",  # F=Full-time, C=Contract, P=Part-time
    remote: bool = True,
    date_posted: str = "past-week",
    skills: List[str] = ["Python", "AWS"],
    limit: int = 10
) -> List[Dict]:
    """
    Search LinkedIn jobs with advanced filters
    """
    linkedin = get_creds()

    date_map = {
        "past-24h": (datetime.now() - timedelta(days=1)).timestamp() * 1000,
        "past-week": (datetime.now() - timedelta(weeks=1)).timestamp() * 1000,
        "past-month": (datetime.now() - timedelta(days=30)).timestamp() * 1000
    }
    
    try:
        results = linkedin.search_jobs(
            keywords=" ".join([keywords] + skills),
            location_name=location,
            listed_at=date_map.get(date_posted),
            experience=experience,
            job_type=job_type,
            remote=remote,
            limit=limit
        )
        
        return [parse_job(job) for job in results]
    
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return {"error": "Job search failed - check auth or parameters"}

def parse_job(job_data: Dict) -> Dict:
    """Normalize LinkedIn job structure to MCP standard"""
    return {
        "title": job_data.get("title"),
        "company": job_data.get("companyName"),
        "location": job_data.get("formattedLocation"),
        "posted": datetime.fromtimestamp(job_data.get("listedAt")/1000).strftime('%Y-%m-%d'),
        "apply_url": job_data.get("applyMethod", {}).get("easyApplyUrl"),
        "skills": extract_skills(job_data.get("description", "")),
        "experience": job_data.get("formattedExperienceLevel"),
        "remote": "Remote" in job_data.get("formattedLocation", "")
    }

def extract_skills(description: str) -> List[str]:
    """Simple skill extraction from description (enhance with NLP)"""
    SKILLS_DB = ["Python", "AWS", "React", "SQL"]
    return [skill for skill in SKILLS_DB if skill.lower() in description.lower()]

@mcp.tool()
def save_search_preferences(
    name: str,
    params: Dict
):
    """Save common search configurations"""
    mcp.state[name] = params
    return f"Saved search '{name}'"

@mcp.tool() 
def load_search_preferences(name: str):
    """Retrieve saved search parameters"""
    return mcp.state.get(name)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file
    
    param pdf_path: Path to PDF file
    return: Extracted text
    """
    
    try:
        reader = PdfReader(pdf_path)
        text=""
        for page in reader.pages:
            text+=page.extract_text()
        
        return text
    except Exception as e:
        return f"Error Extracting Text: {str(e)}"


    

def parsed_resume(resume:str):
    
# list all the specs based on resume?
# and search automatically?


if __name__ == "__main__":
    mcp.run(transport='stdio')
    # get_feed_posts()