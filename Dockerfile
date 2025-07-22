FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY tock_checker_playwright.py .

CMD ["python", "-u", "tock_checker_playwright.py"]
