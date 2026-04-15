# Supabase Contact Setup

## 1) Run SQL

In your Supabase project:

- Open SQL Editor
- Paste the contents of `supabase_setup.sql`
- Click Run

## 2) Copy project values

From Supabase Project Settings > API, copy:

- Project URL
- `anon` public key

## 3) Update local `.env`

Set:

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_TABLE=contact_messages
```

## 4) Start the website backend

Run:

```bash
python server.py
```

Open:

- http://127.0.0.1:8000

## 5) Test contact form

- Fill and submit your contact form
- In Supabase, open `Table Editor > contact_messages`
- Confirm the message row appears
