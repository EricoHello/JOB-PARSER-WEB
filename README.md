# Job Parser Web

This project automatically reads job alert emails sent from [Distill.io](https://distill.io/) and extracts the number of available jobs from multiple job boards. It stores the results in a local SQLite database and runs daily via a cron job.

## How It Works

* **Distill.io** monitors job search result pages and sends you an email when the result count changes.
* **This script** connects to your Gmail inbox via IMAP, finds recent Distill alerts, and extracts job counts from:

  * LinkedIn
  * Indeed
  * ZipRecruiter
* It logs the counts, search parameters, and timestamp into a SQLite database (`jobs_data.db`).
* The script is intended to run automatically using cron.

## Requirements

* Python 3.8+
* A Gmail account with [App Passwords](https://support.google.com/accounts/answer/185833) enabled.
* Distill.io set up to send email alerts for job search result changes.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/job-parser-web.git
   cd job-parser-web
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with:

   ```
   GMAIL_USER=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   ```

## Usage

Run manually:

```bash
python parse_email.py
```

Or set up a daily cron job:

```bash
58 21 * * * /path/to/.venv/bin/python /path/to/parse_email.py >> /path/to/cron.log 2>&1
```

## Database

The script creates a table `job_counts` in `jobs_data.db` with:

* Timestamp
* Counts for LinkedIn, Indeed, ZipRecruiter
* Total job count
* Search parameters (keywords, location, radius, remote setting)

## Viewing History

To view all stored entries:

```bash
python parse_email.py  # also calls read_history() at the end
```