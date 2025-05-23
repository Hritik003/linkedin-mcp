# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
COPY src ./src

RUN pip install --no-cache-dir .

# Copy dotenv example if exists
# Runtime environment variables LINKEDIN_EMAIL and LINKEDIN_PASSWORD should be provided

# Start the MCP server
CMD ["python", "-u", "src/linkedin.py"]
