from groq import Groq
from typing import Generator
import re
from app.config import settings

REVIEW_PROMPT = """You are an expert senior software engineer doing a thorough code review.
Analyze the following {language} code and provide a structured review covering:

1. **Bugs & Logic Errors** — label each as [CRITICAL] / [WARNING] / [INFO]
2. **Security Issues** — injection risks, exposed secrets, vulnerabilities
3. **Performance** — inefficiencies, memory leaks, slow operations
4. **Code Quality** — naming, readability, SOLID principles
5. **Best Practices** — language-specific idioms and patterns
6. **Overall Score** — rate the code quality from 0 to 100

For each issue provide:
- Severity: [CRITICAL] / [WARNING] / [INFO]
- Line reference if applicable
- Clear explanation
- Suggested fix with a code example

End your review with this exact format on its own line: SCORE: XX

Code to review:
````{language}
{code}
```"""

def stream_code_review(code: str, language: str) -> Generator[str, None, None]:
    """Stream Groq's code review token by token using synchronous generator."""
    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = REVIEW_PROMPT.format(language=language, code=code)

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=2000
    )

    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text:
            yield text

def detect_language(code: str, hint: str = "") -> str:
    """Detect programming language from code patterns."""
    if hint:
        return hint
    if "def " in code or "import " in code or "print(" in code:
        return "python"
    if "const " in code or "=>" in code or "function " in code:
        return "javascript"
    if "public class" in code or "System.out" in code:
        return "java"
    if "func " in code or "fmt." in code:
        return "go"
    if "fn " in code or "let mut" in code:
        return "rust"
    if "#include" in code:
        return "cpp"
    return "code"

def extract_score(review_text: str) -> int:
    """Extract numeric score from review text using regex."""
    match = re.search(r'SCORE:\s*(\d+)', review_text, re.IGNORECASE)
    return int(match.group(1)) if match else 50

def extract_issues(review_text: str) -> list[dict]:
    """Parse review text and extract structured issue list."""
    issues = []
    for line in review_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        for severity in ['CRITICAL', 'WARNING', 'INFO']:
            if f'[{severity}]' in line:
                issues.append({
                    "severity": severity,
                    "description": line
                })
                break
    return issues
