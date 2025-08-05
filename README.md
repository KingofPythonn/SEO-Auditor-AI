# SEO Auditor AI 🧠🌐

A powerful Python command-line tool for auditing SEO performance of websites. It analyzes page structure, meta tags, broken links, and more — and provides **AI-powered SEO suggestions** using OpenRouter's GPT models.

---

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-CLI-lightgrey)

---

## 🚀 Features

- ✅ Analyze a single web page or crawl an entire website
- 🔍 Inspects title, meta tags, H1 tags, image alt attributes, and broken links
- 📄 Outputs clean and human-readable **HTML** and **JSON** reports
- 🤖 Generates actionable SEO suggestions using AI (OpenRouter + GPT)
- 🧠 Includes built-in local analysis rules for fast feedback
- 💻 Simple and user-friendly command-line interface using [Typer](https://typer.tiangolo.com)

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/seo-auditor-ai.git
cd seo-auditor-ai
pip install -r requirements.txt
```

---

## 🔑 Setup OpenRouter API Key

This tool uses OpenRouter to generate AI-powered SEO suggestions.  
To enable this feature:

### Step 1: Get Your API Key

- Visit [https://openrouter.ai](https://openrouter.ai)
- Create an account
- Go to [https://openrouter.ai/keys](https://openrouter.ai/keys) and create an API key

### Step 2: Add API Key to `.env`

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and replace `your_api_key_here` with your real API key:

```env
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: You're Done ✅

The project will automatically read the key from `.env`.  
If the key is missing or invalid, the AI feature will be skipped or raise an error.

---

## 🧪 Usage

Run everything using `main.py` from the project root.

### Analyze a single page:

```bash
python main.py check "https://example.com"
```

### Analyze with custom output file names:

```bash
python main.py check "https://example.com" --output-json result.json --output-html result.html
```

### Skip AI suggestions:

```bash
python main.py check "https://example.com" --no-ai
```

### Crawl an entire site (up to N pages):

```bash
python main.py crawl "https://example.com" --max-pages 10
```

---

## 📁 Output Files

- `report.json`: Raw SEO data
- `report.html`: Visually structured, human-readable report

Includes:

- Title, description, meta tag data
- H1 and image alt tag analysis
- Broken link detection
- Local analysis suggestions
- Optional AI-generated SEO suggestions

---

## 🧠 How AI Suggestions Work

When AI mode is enabled, the tool sends a summary of the page's SEO issues to a GPT-based model through OpenRouter.

The model returns a clear and detailed list of SEO recommendations tailored to your website, including:

- Missing or poor meta descriptions
- Issues with title length
- Alt text warnings
- Mobile optimization tips
- Overall best practices

---

## 📂 Project Structure

```
seo-auditor-ai/
├── dnz_seochecker/
│   ├── ai_suggester.py
│   ├── cli.py
│   ├── crawler.py
│   ├── link_checker.py
│   ├── meta_checker.py
│   ├── report_generator.py
│   ├── seo_analyzer.py
│   └── site_checker.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── LICENSE
```

---

## 🛡 License

This project is licensed under the MIT License.  
Feel free to use, modify, and share it.

---

## 🙌 Credits

- [Typer](https://typer.tiangolo.com) – CLI framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – HTML parser
- [OpenRouter](https://openrouter.ai) – AI integration platform

---

## 📬 Contact

Created by [Your Name] — feel free to reach out or contribute!
