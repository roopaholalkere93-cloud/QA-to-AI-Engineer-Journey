import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


# ============================================================
# 1. PROJECT FOLDERS
# ============================================================

# This file is located inside the Outputs folder.
# Therefore, parent.parent = "Gen Testcase_Using Groq"

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_DIR / "Inputs"
OUTPUT_DIR = PROJECT_DIR / "Outputs"
SETUP_DIR = PROJECT_DIR / "Setup"


# ============================================================
# 2. FILE PATHS
# ============================================================

PRD_FILE = INPUT_DIR / "01_Input_PRD.txt"

RULES_FILE = INPUT_DIR / "02_Anti_Hallucination_Rules.txt"

PROMPT_FILE = INPUT_DIR / "03_Prompt_Template.txt"

ENV_FILE = SETUP_DIR / ".env"

OUTPUT_FILE = OUTPUT_DIR / "Output_Testcase.xlsx"


# ============================================================
# 3. CHECK REQUIRED FILES
# ============================================================

required_files = [
    PRD_FILE,
    RULES_FILE,
    PROMPT_FILE,
    ENV_FILE
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found:\n{file_path}"
        )


# ============================================================
# 4. LOAD API KEY
# ============================================================

load_dotenv(ENV_FILE)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found in Setup/.env"
    )


# ============================================================
# 5. CONNECT TO GROQ
# ============================================================

client = Groq(api_key=api_key)

model_name = os.getenv("GROQ_MODEL")

if not model_name:
    raise ValueError(
        "GROQ_MODEL was not found in Setup/.env"
    )

print(f"\nUsing Groq model: {model_name}")


# ============================================================
# 6. READ PRD
# ============================================================

with open(PRD_FILE, "r", encoding="utf-8") as file:
    prd = file.read()

if not prd.strip():
    raise ValueError(
        "01_Input_PRD.txt is empty."
    )


# ============================================================
# 7. READ ANTI-HALLUCINATION RULES
# ============================================================

with open(RULES_FILE, "r", encoding="utf-8") as file:
    anti_hallucination_rules = file.read()

if not anti_hallucination_rules.strip():
    raise ValueError(
        "02_Anti_Hallucination_Rules.txt is empty."
    )


# ============================================================
# 8. READ PROMPT TEMPLATE
# ============================================================

with open(PROMPT_FILE, "r", encoding="utf-8") as file:
    prompt_template = file.read()

if not prompt_template.strip():
    raise ValueError(
        "03_Prompt_Template.txt is empty."
    )


# ============================================================
# 9. INSERT PRD AND RULES INTO PROMPT
# ============================================================

prompt = prompt_template.replace(
    "{PRD}",
    prd
)

prompt = prompt.replace(
    "{ANTI_HALLUCINATION_RULES}",
    anti_hallucination_rules
)

print("\n========== DEBUG ==========")
print("PRD length:", len(prd))
print("PRD preview:")
print(prd[:500])

print("\nPrompt contains PRD placeholder:",
      "{PRD}" in prompt_template)

print("Prompt contains rules placeholder:",
      "{ANTI_HALLUCINATION_RULES}" in prompt_template)

print("\nFinal prompt preview:")
print(prompt[:1500])
print("===========================\n")


# ============================================================
# 10. SEND REQUEST TO GROQ
# ============================================================

print("\n============================================")
print("Starting Test Case Generation")
print("============================================")

print("\nReading PRD...")
print("Reading anti-hallucination rules...")
print("Reading prompt template...")

print("\nSending request to Groq LLM...")
print("Please wait...\n")


response = client.chat.completions.create(
    model=model_name,

    
    messages=[
        {
            "role": "system",
            "content": (
                "You are a Senior QA Engineer with 7+ years "
                "of manual testing experience. "
                "Follow the provided instructions strictly. "
                "Use only information provided in the PRD. "
                "Do not invent or assume requirements."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.2,

    max_completion_tokens=8192
)


# ============================================================
# 11. GET AI RESPONSE
# ============================================================

result = response.choices[0].message.content

print("\nGenerated Test Cases:")
print("--------------------------------------------")
print(result)
print("--------------------------------------------")


# ============================================================
# 12. CREATE EXCEL WORKBOOK
# ============================================================

workbook = Workbook()

sheet = workbook.active

sheet.title = "Test Cases"


# ============================================================
# 13. EXCEL HEADERS
# ============================================================

headers = [
    "Test ID",
    "Description",
    "Pre-conditions",
    "Steps",
    "Expected Result",
    "Priority"
]

sheet.append(headers)


# ============================================================
# 14. FORMAT HEADER
# ============================================================

for cell in sheet[1]:

    cell.font = Font(bold=True)

    cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )


# ============================================================
# 15. CONVERT AI RESPONSE INTO EXCEL ROWS
# ============================================================

for line in result.splitlines():

    line = line.strip()

    # Ignore blank lines
    if not line:
        continue

    # Ignore markdown separator
    if "---" in line:
        continue

    # Only process table rows
    if not line.startswith("|"):
        continue

    # Remove first and last pipe
    line = line.strip("|")

    # Split into columns
    parts = [
        part.strip()
        for part in line.split("|")
    ]

    # We expect 6 columns
    if len(parts) != 6:
        continue

    # Ignore header
    if parts[0].lower() == "test id":
        continue

    # Only accept TC IDs
    if not parts[0].upper().startswith("TC"):
        continue

    sheet.append(parts)


# ============================================================
# 16. FORMAT EXCEL
# ============================================================

for row in sheet.iter_rows():

    for cell in row:

        cell.alignment = Alignment(
            vertical="top",
            wrap_text=True
        )


# ============================================================
# 17. SET COLUMN WIDTHS
# ============================================================

column_widths = {
    "A": 12,
    "B": 40,
    "C": 30,
    "D": 60,
    "E": 60,
    "F": 15
}

for column, width in column_widths.items():

    sheet.column_dimensions[column].width = width


# ============================================================
# 18. FREEZE HEADER
# ============================================================

sheet.freeze_panes = "A2"


# ============================================================
# 19. SAVE EXCEL
# ============================================================

workbook.save(OUTPUT_FILE)


# ============================================================
# 20. COMPLETION MESSAGE
# ============================================================

print("\n============================================")
print("TEST CASE GENERATION COMPLETED")
print("============================================")

print(f"\nExcel file created at:")

print(OUTPUT_FILE)

print("\n============================================")