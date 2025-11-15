from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import re

# Full list of links from your file
links = [
    "https://www.codechef.com/viewsolution/1205844261",
    "https://www.codechef.com/viewsolution/1205854419",
    "https://www.codechef.com/viewsolution/1205857588",
    "https://www.codechef.com/viewsolution/1205865134",
    "https://www.codechef.com/viewsolution/1205830191",
    "https://www.codechef.com/viewsolution/1205859218",
    "https://www.codechef.com/viewsolution/1205862035",
    "https://www.codechef.com/viewsolution/1205838780",
    "https://www.codechef.com/viewsolution/1205816564",
    "https://www.codechef.com/viewsolution/1205839051",
    "https://www.codechef.com/viewsolution/1205847157",
    "https://www.codechef.com/viewsolution/1205836811",
    "https://www.codechef.com/viewsolution/1205854462",
    "https://www.codechef.com/viewsolution/1205839453",
    "https://www.codechef.com/viewsolution/1205847301",
    "https://www.codechef.com/viewsolution/1205854988",
    "https://www.codechef.com/viewsolution/1205842050",
    "https://www.codechef.com/viewsolution/1205831288",
    "https://www.codechef.com/viewsolution/1205839205",
    "https://www.codechef.com/viewsolution/1205844512",
    "https://www.codechef.com/viewsolution/1205852132",
    "https://www.codechef.com/viewsolution/1205827758",
    "https://www.codechef.com/viewsolution/1205849779",
    "https://www.codechef.com/viewsolution/1205857066",
    "https://www.codechef.com/viewsolution/1205859697",
    "https://www.codechef.com/viewsolution/1205810331",
    "https://www.codechef.com/viewsolution/1205809004",
    "https://www.codechef.com/viewsolution/1205800958",
    "https://www.codechef.com/viewsolution/1205800245",
    "https://www.codechef.com/viewsolution/1205812427",
    "https://www.codechef.com/viewsolution/1205800450",
    "https://www.codechef.com/viewsolution/1205838041",
    "https://www.codechef.com/viewsolution/1205818619",
    "https://www.codechef.com/viewsolution/1205824489",
    "https://www.codechef.com/viewsolution/1205832443",
    "https://www.codechef.com/viewsolution/1205824801",
    "https://www.codechef.com/viewsolution/1205812925",
    "https://www.codechef.com/viewsolution/1205813278",
    "https://www.codechef.com/viewsolution/1205819018",
    "https://www.codechef.com/viewsolution/1205852048",
    "https://www.codechef.com/viewsolution/1205814251",
    "https://www.codechef.com/viewsolution/1205832586",
    "https://www.codechef.com/viewsolution/1205813503",
    "https://www.codechef.com/viewsolution/1205815922",
    "https://www.codechef.com/viewsolution/1205853310",
    "https://www.codechef.com/viewsolution/1205831635",
    "https://www.codechef.com/viewsolution/1205848932",
    "https://www.codechef.com/viewsolution/1205806660",
    "https://www.codechef.com/viewsolution/1205809362",
    "https://www.codechef.com/viewsolution/1205803898",
    "https://www.codechef.com/viewsolution/1205809362"
]

output_file = "submission_info.csv"
results = []

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in background
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Initialize driver
print("Initializing browser...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(10)

total_links = len(links)
print(f"Processing {total_links} links...\n")

def extract_field(text, label):
    """Extract field value after a label"""
    pattern = rf"{re.escape(label)}:\s*(.+?)(?:\s+[A-Z][a-z]+:|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

for idx, link in enumerate(links, 1):
    try:
        print(f"[{idx}/{total_links}] Processing: {link}")
        driver.get(link)
        
        # Wait for page to load
        time.sleep(3)
        
        # Get page text
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Initialize result dictionary
        result = {
            "Link": link,
            "Status": "Not Found",
            "Submission by": "Not Found",
            "Submitted": "Not Found",
            "Problem": "Not Found",
            "Contest": "Not Found"
        }
        
        # Extract Status
        try:
            # Look for status indicators
            status_patterns = [
                r"Status:\s*([^\n]+)",
                r"Correct Answer",
                r"Wrong Answer",
                r"Time Limit Exceeded",
                r"Runtime Error",
                r"Compilation Error"
            ]
            for pattern in status_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    result["Status"] = match.group(1) if match.groups() else pattern
                    break
        except:
            pass
        
        # Extract Submission by - get parent element text
        try:
            # Find element containing "Submission by:" and get parent's text
            try:
                sub_by_elem = driver.find_element(By.XPATH, "//*[contains(text(), 'Submission by:')]")
                # Get the parent element
                parent = sub_by_elem.find_element(By.XPATH, "./..")
                parent_text = parent.text
                # Extract everything after "Submission by:" - it may span multiple lines
                # Pattern: "Submission by:" followed by content until "Submitted:" or end
                match = re.search(r"Submission by:\s*(.+?)(?:\s+Submitted:|\s+Problem:|\s+Contest:|$)", parent_text, re.IGNORECASE | re.DOTALL)
                if match:
                    sub_by_text = match.group(1).strip()
                    # Replace newlines with spaces and clean up
                    sub_by_text = re.sub(r'\s+', ' ', sub_by_text)
                    result["Submission by"] = sub_by_text
            except:
                # Fallback: try regex on full page text
                sub_by_match = re.search(r"Submission by:\s*([^\n]+?)(?:\s+Submitted:|\s+Problem:|\s+Contest:|$)", page_text, re.IGNORECASE | re.DOTALL)
                if sub_by_match:
                    sub_by_text = sub_by_match.group(1).strip()
                    sub_by_text = re.sub(r'\s+', ' ', sub_by_text)
                    result["Submission by"] = sub_by_text
        except:
            pass
        
        # Extract Submitted
        try:
            submitted_match = re.search(r"Submitted:\s*([^\n]+)", page_text, re.IGNORECASE)
            if submitted_match:
                result["Submitted"] = submitted_match.group(1).strip()
        except:
            pass
        
        # Extract Problem
        try:
            problem_match = re.search(r"Problem:\s*([^\n]+)", page_text, re.IGNORECASE)
            if problem_match:
                result["Problem"] = problem_match.group(1).strip()
        except:
            pass
        
        # Extract Contest
        try:
            contest_match = re.search(r"Contest:\s*([^\n]+)", page_text, re.IGNORECASE)
            if contest_match:
                result["Contest"] = contest_match.group(1).strip()
        except:
            pass
        
        # Try alternative method: look for elements by text content
        try:
            # Find all text elements and search for patterns
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Status:') or contains(text(), 'Submission by:') or contains(text(), 'Submitted:') or contains(text(), 'Problem:') or contains(text(), 'Contest:')]")
            for elem in elements:
                text = elem.text
                if "Status:" in text and result["Status"] == "Not Found":
                    parts = text.split("Status:", 1)
                    if len(parts) > 1:
                        result["Status"] = parts[1].split("\n")[0].strip()
                if "Submission by:" in text and result["Submission by"] == "Not Found":
                    parts = text.split("Submission by:", 1)
                    if len(parts) > 1:
                        result["Submission by"] = parts[1].split("\n")[0].strip()
                if "Submitted:" in text and result["Submitted"] == "Not Found":
                    parts = text.split("Submitted:", 1)
                    if len(parts) > 1:
                        result["Submitted"] = parts[1].split("\n")[0].strip()
                if "Problem:" in text and result["Problem"] == "Not Found":
                    parts = text.split("Problem:", 1)
                    if len(parts) > 1:
                        result["Problem"] = parts[1].split("\n")[0].strip()
                if "Contest:" in text and result["Contest"] == "Not Found":
                    parts = text.split("Contest:", 1)
                    if len(parts) > 1:
                        result["Contest"] = parts[1].split("\n")[0].strip()
        except:
            pass
        
        results.append(result)
        print(f"  ✓ Status: {result['Status']}")
        print(f"  ✓ Submission by: {result['Submission by']}")
        print(f"  ✓ Submitted: {result['Submitted']}")
        print(f"  ✓ Problem: {result['Problem']}")
        print(f"  ✓ Contest: {result['Contest']}\n")
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        results.append({
            "Link": link,
            "Status": f"Error: {str(e)}",
            "Submission by": "Error",
            "Submitted": "Error",
            "Problem": "Error",
            "Contest": "Error"
        })
    
    # Add delay between requests
    if idx < total_links:
        time.sleep(2)  # 2 second delay between requests

# Close browser
driver.quit()

# Save to CSV
print(f"\nSaving results to {output_file}...")
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Link", "Status", "Submission by", "Submitted", "Problem", "Contest"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

successful = sum(1 for r in results if r["Status"] != "Not Found" and not r["Status"].startswith("Error"))
print(f"\n✓ Data saved to {output_file}")
print(f"✓ Successfully processed: {successful}/{total_links} links")
