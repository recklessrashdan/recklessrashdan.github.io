create extension if not exists pgcrypto;

create table if not exists public.contact_messages (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text not null,
  message text not null,
  created_at timestamptz not null default now()
);

alter table public.contact_messages enable row level security;

drop policy if exists "Allow anon insert contact messages" on public.contact_messages;
create policy "Allow anon insert contact messages"
on public.contact_messages
for insert
to anon
with check (true);

drop policy if exists "Allow service role read contact messages" on public.contact_messages;
create policy "Allow service role read contact messages"
on public.contact_messages
for select
to service_role
using (true);
