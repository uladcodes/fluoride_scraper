# Fluoride Scraper — Web Automation with Selenium

A structured web scraping project built with production-level practices, including error handling, modular design, and automated data collection.

---

### Project Overview

This script (`colgate_final.py`) automates data extraction from the **Colgate US official website**, collecting product details from toothpaste pages.

It was designed to simulate a real-world web automation scenario —  
from browser interaction to error tolerance and data parsing.

---

### Features

- Navigates the full list of fluoride-based products
- Extracts key product data:
  - Product name  
  - Star rating  
  - Number of reviews  
  - Active ingredients (if available)
- Skips broken or missing elements gracefully using `try/except`
- Outputs the data in a clean, structured format

---

### Stack & Tools

| Tool        | Purpose                        |
|-------------|--------------------------------|
| `selenium`  | Automate web interaction       |
| `pandas`    | Store and structure data       |
| `datetime`  | Add timestamps to results      |
| `time`      | Sleep timers to avoid blocking |

---

### Example Output

```bash
Loading card 1...
Product: Colgate Total Whitening  
Rating: 4.7  
Reviews: 632  
Ingredients: Sodium Fluoride, Silica, Glycerin...

Loading card 2...
Product: Colgate Cavity Protection  
Rating: 4.5  
Reviews: 421  
Ingredients: Fluoride, Calcium Carbonate, Water...
```
### Quick Start

```bash
git clone https://github.com/uladcodes/fluoride_scraper.git
cd fluoride_scraper
pip install -r requirements.txt
python colgate_final.py
```
Project Structure
```
fluoride_scraper/
├── colgate_final.py     # Scraper logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
## About This Project

Inspired by a real-life moment  
(yes, a toothpaste in my bathroom) —  
this project was my hands-on way to deepen skills in Python automation and web data extraction.

It’s not just about Selenium — it’s about building logic that works.

---

Wanna see more? Let’s connect.  
I’m open to freelance, full-time, or collaborative work.
