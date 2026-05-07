# GenMedia — BMM601 Assignment Website

A static website introducing Generative AI technologies and their applications in multimedia systems.

---

## Project Information

- **Course:** Multimedia Systems — BMM601 + ISE_MM
- **Semester:** Spring 2026 (S25)
- **Supervisor:** Eng. Talal M. W. Antakieli
- **University:** Syrian Virtual University
- **Submission Deadline:** 2026-05-10

---

## Project Structure

```
bmm601-website/
├── public/                 ← Files to deploy to hosting
│   ├── index.html          ← Home page
│   ├── images.html         ← (to be created)
│   ├── audio-video.html    ← (to be created)
│   ├── how-it-works.html   ← (to be created)
│   ├── about.html          ← (to be created)
│   │
│   ├── assets/
│   │   ├── images/         ← Static images (WEBP/AVIF only)
│   │   ├── videos/         ← Video files + .vtt subtitles
│   │   ├── audio/          ← Audio files
│   │   └── logo/           ← Logo (SVG)
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── main.js
│
├── report/                 ← Final PDF report
├── students.txt            ← List of all 7 team members
├── CLAUDE.md               ← Guide for Claude Code sessions
└── README.md
```

---

## Color Palette

| Color | Hex | Usage |
|---|---|---|
| Deep Blue | `#1E3A8A` | Header, primary buttons |
| Orange | `#F59E0B` | Accents, highlights |
| Light Gray | `#F8F9FA` | Background |
| Soft Black | `#212529` | Body text |

---

## Typography

- **Inter** (Google Fonts) — used for all text

---

## Local Preview

```powershell
cd D:\bmm601-website\public
python -m http.server 8000
# Open browser at http://localhost:8000
```

---

## Hosting

The site will be deployed on **Cloudflare Pages** once complete.

---

## Notes for the Team

- Static (non-animated) images **must** be in WEBP or AVIF format only — this is a hard requirement (10 points).
- Videos must include audio + synchronized subtitles (`.vtt` file).
- AI-generated content must be disclosed in the report (tool, prompt, location on site).
