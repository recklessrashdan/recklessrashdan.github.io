# recklessrashdan.github.io

Hi, welcome to my website!  
I'm a beginner and created this site to share my projects, interests, and a bit about myself. The site is built and hosted using GitHub Pages. All the files you see here are what make the website work.

## What’s Here

- Updates on things I’m learning or building
- My coding projects and experiments
- A place for me to practice web development

## How It Works

- Visit the website: https://recklessrashdan.github.io/
- If you want to see how it works, clone the repository:
  ```bash
  git clone https://github.com/recklessrashdan/recklessrashdan.github.io.git
  ```
- Any changes I push show up on the site right away!

Thanks for visiting!

## Weekly site check (email report)

A GitHub Action runs every **Monday at 09:00 UTC** and emails a short health report to your Gmail. You can also run it manually from the **Actions** tab → **Weekly website check** → **Run workflow**.

### One-time Gmail setup

1. Turn on [2-Step Verification](https://myaccount.google.com/signinoptions/two-step-verification) for your Google account.
2. Create an [App Password](https://myaccount.google.com/apppasswords) (choose “Mail” and your device).
3. In this repo on GitHub: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:
   - `GMAIL_USER` — your Gmail address (e.g. `rashdanrishan69@gmail.com`)
   - `GMAIL_APP_PASSWORD` — the 16-character app password (not your normal Gmail password)

4. Push this repo (including `.github/workflows/weekly-site-check.yml`) to GitHub.

After secrets are set, use **Run workflow** once to confirm you receive the email.
