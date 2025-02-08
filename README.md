
# UNHChatbot

This project is designed for web scraping, fine-tuning, and Retrieval-Augmented Generation (RAG) to enhance chatbot functionality for the University of New Haven.

## Web Scraping

Navigate to the appropriate directory before executing commands:

```bash
cd UNHChatbot/web_scraping/myfirst/myfirst/spiders
```

### Commands:
- **Scrape a specific webpage**:
  ```bash
  scrapy runspider newhavenadmission.py -o filename.json
  ```
  Replace `filename.json` with your desired output file name.

- **Scrape all URLs from a webpage**:
  ```bash
  scrapy crawl newhavencrawler -o filename.json
  ```
  Replace `filename.json` with your desired output file name.

## Fine-Tuning

To perform fine-tuning for the chatbot:

```bash
python chatbot.py
```

## Retrieval-Augmented Generation (RAG)

To implement RAG for the chatbot:

```bash
python RAG.py
```

## Additional Notes

- Ensure all dependencies are installed and configured before running the commands.
- Replace placeholders (e.g., `filename.json`) with appropriate file names based on your use case.
