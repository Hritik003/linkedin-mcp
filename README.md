# MCP Server for LinkedIn

[![smithery badge](https://smithery.ai/badge/@Hritik003/linkedin-mcp)](https://smithery.ai/server/@Hritik003/linkedin-mcp)

A Model Context Protocol (MCP) server for linkedin to apply Jobs and search through feed seamlessly. 

This uses Unoffical [Linkedin API Docs](https://linkedin-api.readthedocs.io/en/latest/api.html) for hitting at the clients Credentials.

## Features

1. **Profile Retrieval**

    Fetch user profiles using `get_profile()` function
    Extract key information such as `name`, `headline`, and `current position`

2. **Job Search**

  - Advanced job search functionality with multiple parameters:
      - Keywords
      - Location
      - Experience level
      - Job type (Full-time, Contract, Part-time)
      - Remote work options
      - Date posted
      - Required skills
  - Customizable search limit

3. **Feed Posts**

  - Retrieve LinkedIn feed posts using `get_feed_posts()`
  - Configurable limit and offset for pagination
  
4. **Resume Analysis**

  - Parse and extract information from `resumes (PDF format)`
  - Extracted data includes:
      - Name
      - Email
      - Phone number
      - Skills
      - Work experience
      - Education
      - Languages


---

# Configuration

After cloning the repo, adjust the `<LOCAL_PATH>` accordingly

```python
{
    "linkedin":{
        "command":"uv",
        "args": [
            "--directory",
            "<LOCAL_PATH>",
            "run",
            "linkedin.py"
        ]
    }   
}     

```

---

# Usage

I have been testing using [MCP-client](https://github.com/chrishayuk/mcp-cli) and found as the best one for testing your `MCP-Servers`.



