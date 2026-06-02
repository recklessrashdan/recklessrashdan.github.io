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

## Weekly site check (Discord notification)

A GitHub Action runs every **Monday at 09:00 UTC** and posts a short health report to your Discord server. You can also run it manually from the **Actions** tab → **Weekly website check** → **Run workflow**.

### One-time Discord setup

1. In Discord, open the server and channel where you want reports.
2. **Edit Channel** → **Integrations** → **Webhooks** → **New Webhook** (name it e.g. “Site check”).
3. Copy the webhook URL.
4. On GitHub, open this repo: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:
   - `DISCORD_WEBHOOK_URL` — paste the webhook URL (keep it private; anyone with the URL can post to that channel).

5. Push this repo (including `.github/workflows/weekly-site-check.yml`) to GitHub.

After the secret is set, use **Run workflow** once to confirm the message appears in Discord.
