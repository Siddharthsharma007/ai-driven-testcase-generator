import re
import json
import openai
import os


def _create_client():
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _strip_code_fences(content: str) -> str:
    content = re.sub(r"```(?:json)?", "", content, flags=re.IGNORECASE)
    return content.replace("```", "").strip()


def generate_test_cases(requirements_text):
    client = _create_client()
    prompt = f"""
You are an expert QA engineer. Generate comprehensive test cases for the following requirements.

REQUIREMENTS:
{requirements_text}

INSTRUCTIONS:
Generate 30-50 detailed test cases covering:
- Positive test cases (happy path)
- Negative test cases (error conditions) 
- Boundary test cases (min/max values)
- Edge cases (unusual inputs)
- Security test cases
- Performance test cases

For each test case include: Test ID, Title, Preconditions, Steps, Expected Result, Priority (High/Medium/Low), Type (Positive/Negative/Boundary/Edge/Security/Performance)

IMPORTANT: Return ONLY a valid JSON array. Example format:
[
  {{"Test ID": "TC-001", "Title": "Test Title", "Preconditions": "Preconditions", "Steps": "Steps", "Expected Result": "Expected Result", "Priority": "High", "Type": "Positive"}}
]

Return the JSON array now:
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,  # Reduced to ensure we get a response
        temperature=0.1,   # Lower temperature for more consistent output
    )
    content = response.choices[0].message.content
    print("OpenAI raw content (requirements):", content)

    # Remove code fences if present
    content = _strip_code_fences(content)

    # Find the first JSON array in the text (non-greedy)
    match = re.search(r"\[.*?\]", content, re.DOTALL)
    if match:
        json_str = match.group(0)
        print("Extracted JSON string (requirements):", json_str)
    else:
        print("No JSON array found in response.")
        json_str = None

    try:
        cases = json.loads(json_str) if json_str else []
    except Exception as e:
        print("JSON decode error (requirements):", e)
        cases = []
    print("Final parsed cases (requirements):", cases)
    return cases


def generate_ui_test_suite(ui_description: str):
    """
    Generate a rich UI-based test suite from a textual description of a screen (e.g. OCR output).
    Returns a Python dict with:
      - ui_elements
      - test_cases
      - locators
      - automation_examples
      - coverage_summary
      - risk_areas
      - smoke_suite
      - regression_suite
    """
    client = _create_client()
    prompt = f"""
You are a Senior QA Architect with 15+ years of experience in software testing, automation architecture, and quality engineering.

You are given the textual description of a UI screen (labels, button names, field names, etc.).
Carefully infer the UI elements, user flows, and business logic, then design a production-grade test suite.

UI DESCRIPTION (from OCR or user notes):
{ui_description}

STEP 1 – Analyze the UI
- Identify all elements such as:
  - Input fields
  - Buttons
  - Dropdowns
  - Links
  - Checkboxes
  - Navigation items
  - Error messages
  - Tooltips (assume reasonable ones if not explicitly mentioned)

STEP 2 – Identify user flows and business logic
- Derive possible user journeys and actions the user can take on this screen and related flows.

STEP 3 – Generate test scenarios and detailed test cases

Create AT LEAST 50 meaningful test cases that ensure maximum coverage, across:
- Functional Test Cases  
- UI Test Cases  
- Validation Test Cases  
- Negative Test Cases  
- Boundary Test Cases  
- Security Test Cases  
- Accessibility Test Cases  
- Edge Cases  
- Cross Browser Tests  
- Mobile Responsiveness Tests  

Each test case MUST include:
- Test Case ID  
- Test Scenario  
- Preconditions  
- Test Steps  
- Expected Result  
- Priority (High/Medium/Low)  
- Severity (Critical/High/Medium/Low)  
- Test Data  
- Category (Functional/UI/Validation/Negative/Boundary/Security/Accessibility/Edge/CrossBrowser/Mobile)

Include advanced real-world scenarios like:
- Session expiry
- Concurrent users / simultaneous updates
- Network interruption / slow network
- Large input values and large payloads
- Security attacks (SQL injection, XSS, brute force, CSRF where applicable)
- Invalid formats and encodings
- Accessibility testing (screen readers, keyboard navigation, color contrast, focus order)

STEP 4 – Automation-ready output

Also produce:
- Suggested locators for major UI elements:
  - CSS selectors
  - XPath
  - Playwright selectors
- Example automation snippets for:
  - Playwright + TypeScript (Page Object Model, clean structure, robust locators)
  - Selenium + Java (Page Object Model, reusable methods, robust locators)

STEP 5 – Test strategy outputs

Provide:
- Test coverage summary (1–2 paragraphs)
- Key risk areas (list)
- Recommended smoke test suite (list of Test Case IDs + brief titles)
- Recommended regression suite (list of Test Case IDs + brief titles)

RESPONSE FORMAT (VERY IMPORTANT):
Return ONLY a single valid JSON object with the following shape:
{{
  "ui_elements": [
    {{"name": "...", "type": "input/button/dropdown/checkbox/link/other", "description": "..."}}
  ],
  "test_cases": [
    {{
      "Test Case ID": "TC_UI_001",
      "Test Scenario": "...",
      "Preconditions": "...",
      "Test Steps": "...",
      "Expected Result": "...",
      "Priority": "High/Medium/Low",
      "Severity": "Critical/High/Medium/Low",
      "Test Data": "...",
      "Category": "Functional/UI/Validation/Negative/Boundary/Security/Accessibility/Edge/CrossBrowser/Mobile"
    }}
  ],
  "locators": [
    {{
      "element_name": "...",
      "css": "...",
      "xpath": "...",
      "playwright": "locator(...) string"
    }}
  ],
  "automation_examples": {{
    "playwright_typescript": "```typescript\\n// example code here\\n```",
    "selenium_java": "```java\\n// example code here\\n```"
  }},
  "coverage_summary": "...",
  "risk_areas": ["...", "..."],
  "smoke_suite": [
    {{"Test Case ID": "TC_UI_001", "Title": "..."}}
  ],
  "regression_suite": [
    {{"Test Case ID": "TC_UI_010", "Title": "..."}}
  ]
}}

Return ONLY this JSON object. Do not include any explanation outside of JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.1,
    )
    content = response.choices[0].message.content
    print("OpenAI raw content (UI suite):", content)

    # Strip any code fences that might still be present
    content = _strip_code_fences(content)

    try:
        suite = json.loads(content)
    except Exception as e:
        print("JSON decode error (UI suite):", e)
        # Best-effort fallback
        try:
            # Try to locate the first JSON object
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                suite = json.loads(match.group(0))
            else:
                suite = {}
        except Exception as e2:
            print("Second JSON decode failure (UI suite):", e2)
            suite = {}

    return suite
