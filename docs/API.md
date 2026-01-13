# AIRR Transcript Parser - API Documentation

Version: 1.0  
Last Updated: January 13, 2026

## Overview

The AIRR Transcript Parser exposes a form-based webhook API for uploading and processing student transcript images. The system uses Gemini 2.0 Flash Vision API for intelligent extraction with self-learning template capabilities.

## Base URL

```
http://localhost:5678
```

For production deployments, replace with your N8N instance URL.

## Authentication

Currently, authentication is disabled for ease of use. For production:

1. Enable N8N Basic Auth:
   ```bash
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=your_username
   N8N_BASIC_AUTH_PASSWORD=your_password
   ```

2. Or implement custom authentication in the workflow

## Endpoints

### 1. Upload Transcript (Form)

**Endpoint:** `GET /form/airr-upload`

**Description:** Web form interface for uploading transcript images

**Method:** GET

**Parameters:** None

**Response:** HTML form

**Usage:**
```bash
# Open in browser
http://localhost:5678/form/airr-upload
```

**Form Fields:**
- `Transcript Image` (required) - File upload (.png, .jpg, .jpeg, .webp)

---

### 2. Process Transcript (Webhook)

**Endpoint:** `POST /webhook/airr-upload`

**Description:** Programmatic API for transcript processing

**Method:** POST

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Transcript image (PNG, JPG, JPEG, WEBP) |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:5678/webhook/airr-upload \
  -F "file=@/path/to/transcript.png"
```

**Example Request (Python):**

```python
import requests

url = "http://localhost:5678/webhook/airr-upload"
files = {"file": open("transcript.png", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

**Example Request (JavaScript/Fetch):**

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5678/webhook/airr-upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response Format:**

```json
{
  "studentinfo": {
    "SPRIDEN ID": {
      "value": "A12345678",
      "label": "SPRIDEN ID",
      "rule": "mixed",
      "length": 25,
      "previewJson": true
    },
    "STUDENT NAME": {
      "label": "STUDENT NAME",
      "value": "John Doe",
      "length": 25,
      "rule": "mixed"
    },
    "major": {
      "value": "Computer Science",
      "label": "Major",
      "rule": "mixed",
      "length": 40
    },
    "Start Date": {
      "value": "2020-08-15",
      "label": "Start Date",
      "rule": "mixed",
      "length": 20
    },
    "End Date": {
      "value": "2024-05-20",
      "label": "End Date",
      "rule": "mixed",
      "length": 20
    }
  },
  "collegeInfo": {
    "INSTITUTION NAME": {
      "label": "INSTITUTION NAME",
      "value": "Massachusetts Institute of Technology",
      "length": 25,
      "rule": "mixed",
      "previewJson": true
    },
    "ADDRESS": {
      "label": "ADDRESS",
      "value": "77 Massachusetts Ave",
      "length": 25,
      "rule": "mixed"
    },
    "CITY": {
      "label": "CITY",
      "value": "Cambridge",
      "length": 25,
      "rule": "mixed"
    },
    "STATE": {
      "label": "STATE",
      "value": "MA",
      "length": 25,
      "rule": "mixed"
    },
    "ZIP CODE": {
      "label": "ZIP CODE",
      "value": "02139",
      "length": 25,
      "rule": "mixed"
    }
  },
  "gpaSummary": {
    "Total Credit Earned": {
      "value": 120,
      "label": "Total Credit Earned",
      "rule": "mixed",
      "length": 25,
      "previewJson": true
    },
    "calculated_col_gpa": {
      "label": "calculated_col_gpa",
      "value": "3.85",
      "length": 25,
      "rule": "mixed",
      "previewJson": true
    }
  },
  "totalSummary": [
    {
      "overall_earned_hours": {
        "label": "overall_earned_hours",
        "value": "120",
        "length": 25,
        "rule": "mixed"
      },
      "overall_gpa": {
        "label": "overall_gpa",
        "value": "3.85",
        "length": 25,
        "rule": "mixed"
      },
      "total_credit_earned": {
        "label": "total_credit_earned",
        "value": 120,
        "length": 25,
        "rule": "mixed"
      }
    }
  ],
  "academicrecord": [
    {
      "termDetails": [
        {
          "monthYear": {
            "value": "Fall 2020",
            "label": "monthYear",
            "rule": "mixed",
            "length": 25,
            "index": 0
          }
        }
      ],
      "courseDetails": [
        {
          "course_id": {
            "value": "6.0001",
            "label": "course_id",
            "rule": "mixed",
            "length": 25,
            "index": 0
          },
          "course_name": {
            "value": "Introduction to Computer Science",
            "label": "course_name",
            "rule": "mixed",
            "length": 25,
            "index": 1
          },
          "credits_earned": {
            "value": "3",
            "label": "credits_earned",
            "rule": "mixed",
            "length": 25,
            "index": 2,
            "key": "credits_attempted"
          },
          "grades": {
            "value": "A",
            "label": "grades",
            "rule": "mixed",
            "length": 25,
            "index": 3
          },
          "points": {
            "index": 4,
            "value": "12.0",
            "label": "points"
          },
          "year_term": {
            "index": 5,
            "value": "Fall 2020",
            "label": "year_term"
          }
        }
      ]
    },
    {
      "termDetails": [
        {
          "monthYear": {
            "value": "Spring 2021",
            "label": "monthYear",
            "rule": "mixed",
            "length": 25,
            "index": 0
          }
        }
      ],
      "courseDetails": [
        {
          "course_id": {
            "value": "6.0002",
            "label": "course_id",
            "rule": "mixed",
            "length": 25,
            "index": 0
          },
          "course_name": {
            "value": "Introduction to Computational Thinking",
            "label": "course_name",
            "rule": "mixed",
            "length": 25,
            "index": 1
          },
          "credits_earned": {
            "value": "3",
            "label": "credits_earned",
            "rule": "mixed",
            "length": 25,
            "index": 2,
            "key": "credits_attempted"
          },
          "grades": {
            "value": "A-",
            "label": "grades",
            "rule": "mixed",
            "length": 25,
            "index": 3
          },
          "points": {
            "index": 4,
            "value": "11.1",
            "label": "points"
          },
          "year_term": {
            "index": 5,
            "value": "Spring 2021",
            "label": "year_term"
          }
        }
      ]
    }
  ],
  "academicrecordLLM": [],
  "pagewise_academic_records": "",
  "errors": [],
  "transformed": true
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `studentinfo` | Object | Student personal information |
| `studentinfo.STUDENT NAME.value` | String | Full name of the student |
| `studentinfo.major.value` | String | Major/program of study |
| `studentinfo.Start Date.value` | String | Program start date |
| `studentinfo.End Date.value` | String | Program end date |
| `collegeInfo` | Object | University/college information |
| `collegeInfo.INSTITUTION NAME.value` | String | Full university name |
| `collegeInfo.ADDRESS.value` | String | Institution address |
| `collegeInfo.CITY.value` | String | City |
| `collegeInfo.STATE.value` | String | State/province |
| `gpaSummary` | Object | GPA and credit summary |
| `gpaSummary.calculated_col_gpa.value` | String | Overall GPA |
| `gpaSummary.Total Credit Earned.value` | Number | Total credits earned |
| `totalSummary` | Array | Overall academic summary |
| `totalSummary[].overall_gpa.value` | String | Cumulative GPA |
| `totalSummary[].overall_earned_hours.value` | String | Total credit hours |
| `academicrecord` | Array | Semester-by-semester course records |
| `academicrecord[].termDetails` | Array | Term/semester information |
| `academicrecord[].termDetails[].monthYear.value` | String | Semester name (e.g., "Fall 2020") |
| `academicrecord[].courseDetails` | Array | Courses taken in this term |
| `academicrecord[].courseDetails[].course_id.value` | String | Course code |
| `academicrecord[].courseDetails[].course_name.value` | String | Course title |
| `academicrecord[].courseDetails[].credits_earned.value` | String | Credits for this course |
| `academicrecord[].courseDetails[].grades.value` | String | Letter or numeric grade |
| `academicrecord[].courseDetails[].points.value` | String | Grade points earned |
| `transformed` | Boolean | Always `true` when successful |
| `errors` | Array | Empty array if no errors |

**HTTP Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success - transcript processed |
| 400 | Bad Request - invalid file format |
| 500 | Server Error - processing failed |

---

## Internal APIs (Supabase)

These endpoints are used internally by the workflow.

### 3. Find Matching Template

**Endpoint:** `POST /rest/v1/rpc/find_matching_template`

**Description:** Search for learned templates matching university and layout

**Authentication:** Supabase API key required

**Request Body:**

```json
{
  "p_university": "Massachusetts Institute of Technology",
  "p_layout_type": "tabular"
}
```

**Response:**

```json
[
  {
    "id": "uuid-here",
    "university_name": "Massachusetts Institute of Technology",
    "layout_type": "tabular",
    "parsing_prompt": "Extract data from this MIT transcript...",
    "output_schema": {},
    "times_used": 15,
    "match_score": 100
  }
]
```

**Match Score Logic:**
- 100: Exact university name + layout type match
- 80: University name match only
- 70: University alias match
- 60: Layout type match only
- 0: No match

---

### 4. Save Learned Template

**Endpoint:** `POST /rest/v1/learned_templates`

**Description:** Save a new learned template to the database

**Authentication:** Supabase service role key required

**Request Headers:**

```
apikey: your-supabase-anon-key
Authorization: Bearer your-supabase-service-key
Content-Type: application/json
Prefer: return=representation
```

**Request Body:**

```json
{
  "university_name": "Massachusetts Institute of Technology",
  "university_aliases": ["MIT"],
  "layout_type": "tabular",
  "layout_fingerprint": {
    "university_full_name": "MIT",
    "grades": {
      "structure": "single-table",
      "columns": ["Course ID", "Title", "Credits", "Grade"],
      "grade_format": "letter"
    }
  },
  "parsing_prompt": "Extract data from this MIT transcript...",
  "output_schema": {
    "studentinfo": "object",
    "collegeInfo": "object",
    "academicrecord": "object"
  },
  "times_used": 1,
  "success_count": 1
}
```

**Response:**

```json
[
  {
    "id": "new-uuid",
    "university_name": "Massachusetts Institute of Technology",
    "university_aliases": ["MIT"],
    "layout_type": "tabular",
    "created_at": "2026-01-13T18:30:00Z",
    "updated_at": "2026-01-13T18:30:00Z",
    "times_used": 1,
    "success_count": 1
  }
]
```

---

## Rate Limits

### N8N Workflow
- No built-in rate limiting
- Recommended: Add rate limiting in production (nginx, API gateway)

### Gemini API
- Free tier: 15 requests per minute
- Paid tier: Higher limits based on plan
- Implement exponential backoff for rate limit errors

### Supabase
- Free tier: 500k requests/month
- API rate limits based on plan

---

## Error Handling

### Common Errors

**1. Invalid File Format**

```json
{
  "error": "No file uploaded"
}
```

**2. Processing Failed**

```json
{
  "success": false,
  "data": {
    "_error": "JSON parse failed: Unexpected token",
    "_raw": "raw gemini response"
  },
  "validation": {
    "is_valid": false,
    "errors": ["Missing: student_name", "Missing: semesters"]
  }
}
```

**3. Template Lookup Failed**

Returns empty array `[]` - workflow continues with dynamic analysis

---

## Webhooks & Callbacks

Currently not implemented. Future versions may include:

- Completion webhooks
- Progress callbacks
- Error notifications

---

## SDKs & Client Libraries

### Python Client Example

```python
import requests
import json

class AIRRClient:
    def __init__(self, base_url="http://localhost:5678"):
        self.base_url = base_url

    def process_transcript(self, image_path):
        url = f"{self.base_url}/webhook/airr-upload"

        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)

        return response.json()

    def extract_student_info(self, result):
        return {
            'name': result['studentinfo']['STUDENT NAME']['value'],
            'major': result['studentinfo']['major']['value'],
            'gpa': result['gpaSummary']['calculated_col_gpa']['value']
        }

# Usage
client = AIRRClient()
result = client.process_transcript('transcript.png')
student = client.extract_student_info(result)
print(f"Student: {student['name']}, GPA: {student['gpa']}")
```

### Node.js Client Example

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class AIRRClient {
  constructor(baseURL = 'http://localhost:5678') {
    this.baseURL = baseURL;
  }

  async processTranscript(imagePath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(imagePath));

    const response = await axios.post(
      `${this.baseURL}/webhook/airr-upload`,
      form,
      { headers: form.getHeaders() }
    );

    return response.data;
  }

  extractStudentInfo(result) {
    return {
      name: result.studentinfo['STUDENT NAME'].value,
      major: result.studentinfo.major.value,
      gpa: result.gpaSummary.calculated_col_gpa.value
    };
  }
}

// Usage
(async () => {
  const client = new AIRRClient();
  const result = await client.processTranscript('transcript.png');
  const student = client.extractStudentInfo(result);
  console.log(`Student: ${student.name}, GPA: ${student.gpa}`);
})();
```

---

## Performance

### Typical Processing Times

| Scenario | Time Range |
|----------|-----------|
| First upload (no template) | 8-15 seconds |
| With learned template | 3-6 seconds |
| Layout analysis only | 2-4 seconds |
| Data extraction only | 3-5 seconds |

### Optimization Tips

1. Use learned templates when possible (70%+ match score)
2. Cache Supabase template lookups
3. Implement connection pooling for Supabase
4. Use CDN for static assets in production

---

## Security Best Practices

1. **Enable Authentication**
   - Use N8N Basic Auth or custom auth
   - Validate API keys in production

2. **Input Validation**
   - Check file size limits (max 10MB recommended)
   - Validate file types server-side
   - Scan for malicious content

3. **API Key Protection**
   - Store keys in environment variables
   - Rotate keys regularly
   - Use service role keys only server-side

4. **CORS Configuration**
   ```javascript
   // If exposing to web apps
   Access-Control-Allow-Origin: your-domain.com
   ```

5. **HTTPS Required**
   - Always use HTTPS in production
   - Encrypt data in transit

---

## Changelog

### v1.0 (2026-01-13)
- Initial API release
- Form-based upload endpoint
- Webhook API for programmatic access
- Supabase template storage
- Self-learning template system

---

## Support

- GitHub Issues: https://github.com/yourusername/airr-transcript-parser/issues
- Documentation: https://github.com/yourusername/airr-transcript-parser
- Email: support@example.com

---

## License

MIT License - See LICENSE file for details