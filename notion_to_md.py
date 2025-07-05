import requests
import os

# 🔐 Your Notion credentials
NOTION_TOKEN = "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"
DATABASE_ID = "2276ce8190b680b7a683fa3c85779458"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def fetch_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("results", [])

def get_prop(page, name):
    try:
        prop = page["properties"][name]
        if prop["type"] == "title":
            return prop["title"][0]["text"]["content"]
        elif prop["type"] == "rich_text":
            return prop["rich_text"][0]["text"]["content"]
        elif prop["type"] == "date":
            return prop["date"]["start"]
        elif prop["type"] == "number":
            return str(prop["number"])
    except (KeyError, IndexError, TypeError):
        return "N/A"

def save_markdown(page):
    title = get_prop(page, "Topic")
    notes = get_prop(page, "Notes")
    date = get_prop(page, "Date")
    duration = get_prop(page, "Duration")

    filename = f"{date} - {title}.md".replace(":", "-").replace("/", "-")
    filepath = os.path.join("logs", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Date:** {date}\n\n")
        f.write(f"**Duration:** {duration} mins\n\n")
        f.write(f"## Notes\n{notes}\n")

    print(f"✅ Saved: {filepath}")

def main():
    os.makedirs("logs", exist_ok=True)
    pages = fetch_pages()
    for page in pages:
        save_markdown(page)

if __name__ == "__main__":
    main()
