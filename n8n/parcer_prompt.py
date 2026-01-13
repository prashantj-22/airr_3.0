# AIRR Transcript Parser - Prompts Configuration
# This file contains all AI prompts used in the N8N workflow
# Version: 1.0

## 1. QUICK UNIVERSITY DETECTION PROMPT
# Node: Quick Detect University
# Purpose: Fast identification of university and layout type
# Temperature: 0.1 | Max Tokens: 500

QUICK_DETECT_PROMPT = '''
Identify this student transcript:
1. University name (exact)
2. Layout type: 'tabular' | 'semester-block' | 'multi-column' | 'single-page'
3. Country

Return ONLY JSON, no markdown:
{"university": "name", "layout_type": "type", "country": "country or null"}
'''

## 2. DEEP LAYOUT ANALYSIS PROMPT
# Node: Deep Layout Analysis
# Purpose: Detailed structural analysis of transcript format
# Temperature: 0.2 | Max Tokens: 2000

DEEP_LAYOUT_ANALYSIS_PROMPT = '''
Analyze this transcript image IN DETAIL:

1. HEADER: University name/logo position, student info fields
2. GRADES: Table structure, column headers, grade format (letter/number/percentage)
3. SEMESTERS: How separated, SGPA per semester?
4. SUMMARY: CGPA location, other fields

Return JSON:
{
  "university_full_name": "",
  "header": {"position": "", "student_fields": []},
  "grades": {"structure": "single-table|multi-table|semester-blocks", "columns": [], "grade_format": "letter|10-point|percentage"},
  "semesters": {"organization": "", "has_semester_gpa": true, "gpa_label": "SGPA"},
  "summary": {"has_cgpa": true, "cgpa_label": "CGPA", "other_fields": []},
  "extractable_fields": []
}
'''

## 3. DYNAMIC EXTRACTION PROMPT TEMPLATE
# Node: Build Dynamic Prompt (output)
# Purpose: Main extraction prompt built from layout analysis
# Temperature: 0.1 | Max Tokens: 4000

DYNAMIC_EXTRACTION_TEMPLATE = '''
You are a precise JSON extraction engine. Extract data from this {university_name} transcript image.

LAYOUT ANALYSIS CONTEXT:
- University: {university_full_name}
- Document Structure: {structure}
- Grade Format: {grade_format}
- Available Columns: {columns}
- Has Semester GPA: {has_semester_gpa}
- Has Overall CGPA: {has_cgpa}

OUTPUT REQUIREMENTS:
1. Return ONLY raw JSON - no markdown, no code blocks, no explanations
2. Do NOT wrap in ```json or ``` tags
3. Start with { and end with }
4. Use exactly this structure:

{
  "studentinfo": {
    "SPRIDEN ID": {"value": "", "label": "SPRIDEN ID", "rule": "mixed", "length": 25, "previewJson": true},
    "SPRIDEN_PIDM": {"value": "", "label": "SPRIDEN_PIDM", "rule": "mixed", "length": 25, "previewJson": true},
    "STUDENT NAME": {"label": "STUDENT NAME", "value": "", "length": 25, "rule": "mixed"},
    "MAILING ADDRESS": {"label": "MAILING ADDRESS", "value": "", "length": 25, "rule": "mixed"},
    "Start Date": {"value": "", "label": "Start Date", "rule": "mixed", "length": 20},
    "End Date": {"value": "", "label": "End Date", "rule": "mixed", "length": 20},
    "major": {"value": "", "label": "Major", "rule": "mixed", "length": 40}
  },
  "collegeInfo": {
    "INSTITUTION TYPE": {"value": "", "label": "INSTITUTION TYPE", "rule": "mixed", "length": 25, "previewJson": true},
    "INSTITUTION NAME": {"label": "INSTITUTION NAME", "value": "{university_full_name}", "length": 25, "rule": "mixed", "previewJson": true},
    "ADDRESS": {"label": "ADDRESS", "value": "", "length": 25, "rule": "mixed"},
    "CITY": {"label": "CITY", "value": "", "length": 25, "rule": "mixed"},
    "PHONE": {"label": "PHONE", "value": "", "length": 25, "rule": "mixed"},
    "STATE": {"label": "STATE", "value": "", "length": 25, "rule": "mixed"},
    "ZIP CODE": {"label": "ZIP CODE", "value": "", "length": 25, "rule": "mixed"},
    "COLLEGE CODE": {"value": "", "label": "COLLEGE CODE", "rule": "mixed", "length": 25, "previewJson": true}
  },
  "gpaSummary": {
    "TOTAL TRANSFERABLE CREDITS": {"value": "", "label": "TOTAL TRANSFERABLE CREDITS", "rule": "mixed", "length": 25, "previewJson": true},
    "TOTAL CTX CREDITS": {"value": "", "label": "TOTAL CTX CREDITS", "rule": "mixed", "length": 25, "previewJson": true},
    "Total Credit Earned": {"value": 0, "label": "Total Credit Earned", "rule": "mixed", "length": 25, "previewJson": true},
    "calculated_col_gpa": {"label": "calculated_col_gpa", "value": "0.000", "length": 25, "rule": "mixed", "previewJson": true}
  },
  "totalSummary": [{
    "overall_earned_hours": {"label": "overall_earned_hours", "value": "", "length": 25, "rule": "mixed"},
    "overall_gpa": {"label": "overall_gpa", "value": "", "length": 25, "rule": "mixed"},
    "total_institution_earned_hours": {"label": "total_institution_earned_hours", "value": "", "length": 25, "rule": "mixed"},
    "total_transfer_earned_hours": {"label": "total_transfer_earned_hours", "value": "", "length": 25, "rule": "mixed"},
    "total_credit_earned": {"label": "total_credit_earned", "value": 0, "length": 25, "rule": "mixed"},
    "total_qualilty_number": {"label": "total_quality_number", "value": 0, "length": 25, "rule": "mixed"}
  }],
  "academicrecord": [
    {
      "termDetails": [{"monthYear": {"value": "", "label": "monthYear", "rule": "mixed", "length": 25, "index": 0}}],
      "courseDetails": [
        {
          "course_id": {"value": "", "label": "course_id", "rule": "mixed", "length": 25, "index": 0},
          "course_name": {"value": "", "label": "course_name", "rule": "mixed", "length": 25, "index": 1},
          "credits_earned": {"value": "", "label": "credits_earned", "rule": "mixed", "length": 25, "index": 2, "key": "credits_attempted"},
          "grades": {"value": "", "label": "grades", "rule": "mixed", "length": 25, "index": 3},
          "points": {"index": 4, "value": "", "label": "points"},
          "year_term": {"index": 5, "value": "", "label": "year_term"}
        }
      ]
    }
  ],
  "academicrecordLLM": [],
  "pagewise_academic_records": "",
  "errors": [],
  "transformed": true
}

EXTRACTION RULES (Based on Layout Analysis):
- Student name → studentinfo.STUDENT NAME.value
- University → collegeInfo.INSTITUTION NAME.value (use "{university_full_name}")
- Major/Program → studentinfo.major.value  
- Each term/semester → new object in academicrecord array
- Term format → academicrecord[].termDetails[].monthYear.value (e.g., "Fall 2022")
- Course extraction follows detected columns: {columns}
- Grade format: {grade_format}
- Each course → object in courseDetails with: course_id, course_name, credits_earned, grades, points, year_term
- GPA mapping: {gpa_label} → per-term GPA, {cgpa_label} → overall GPA
- totalSummary[].overall_gpa.value gets the {cgpa_label} value
- Empty strings for missing text, 0 for missing numbers
- Keep ALL metadata fields (label, rule, length, index, previewJson) unchanged
- Extract ALL visible semesters/terms from the transcript

CRITICAL: Your response must start with { and end with }. No other text before or after.
'''

## 4. LEARNED TEMPLATE SUFFIX
# Node: Parse With Learned Template
# Purpose: Additional instruction appended to saved templates
# Temperature: 0.1 | Max Tokens: 4000

LEARNED_TEMPLATE_SUFFIX = '''

Return ONLY valid JSON.
'''

## CONFIGURATION NOTES

### Temperature Settings:
- Quick Detection: 0.1 (factual, deterministic)
- Layout Analysis: 0.2 (slightly creative for structure detection)
- Data Extraction: 0.1 (precise, consistent)

### Token Limits:
- Quick Detection: 500 (small JSON response)
- Layout Analysis: 2000 (detailed structure description)
- Data Extraction: 4000 (complete transcript with multiple semesters)

### Prompt Engineering Best Practices:
1. Always specify output format explicitly (JSON)
2. Use "Return ONLY" to prevent explanations
3. Provide exact schema structure as example
4. Include fallback values (empty strings, 0)
5. Add "CRITICAL" for emphasis on key requirements

### Variable Substitutions in Build Dynamic Prompt Node:
{university_name} - From detected.university or analysis.university_full_name
{university_full_name} - From analysis.university_full_name
{structure} - From analysis.grades.structure
{grade_format} - From analysis.grades.grade_format  
{columns} - From analysis.grades.columns (joined with commas)
{has_semester_gpa} - From analysis.semesters.has_semester_gpa
{has_cgpa} - From analysis.summary.has_cgpa
{gpa_label} - From analysis.semesters.gpa_label
{cgpa_label} - From analysis.summary.cgpa_label

### Customization Guide:
To modify prompts for different use cases:
1. Update OUTPUT_SCHEMA in DYNAMIC_EXTRACTION_TEMPLATE
2. Adjust EXTRACTION_RULES to match new schema
3. Update DEEP_LAYOUT_ANALYSIS_PROMPT to detect new fields
4. Keep temperature low (0.1-0.2) for consistency
5. Test with sample transcripts before deploying
