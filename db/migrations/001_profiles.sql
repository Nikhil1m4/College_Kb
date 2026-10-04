-- 1. Create profiles table
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  role text not null default 'member' check (role in ('member','admin')),
  created_at timestamptz default now()
);

-- 2. Trigger function to create profile on user signup
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, role)
  values (new.id, new.email, 'member');
  return new;
end;
$$;

-- 3. Trigger on auth.users
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- 4. Row-level security on profiles
alter table public.profiles enable row level security;

create policy "Users can view their own profile"
  on public.profiles
  for select
  using ( auth.uid() = id );

-- No insert/update/delete policies for normal users, so a user can never change their own role.

-- EXAMPLE: Promoting a user to admin (run this manually in SQL Editor)
-- update public.profiles set role = 'admin' where email = 'your.email@example.com';

-- 5. Explicit Data API Grants (Required because 'Automatically expose new tables' is DISABLED)
-- The anon role should NOT have access to read profiles to prevent data leaks.
-- (We simply don't grant anything to anon).

-- The authenticated role needs SELECT access to read their own profile row.
-- (This is restricted by the RLS policy defined above).
-- They get NO insert/update/delete privileges here.
GRANT SELECT ON TABLE public.profiles TO authenticated;

-- The service_role needs full SELECT access so the FastAPI backend can fetch any user's role.
-- (The service_role bypasses RLS).
GRANT SELECT ON TABLE public.profiles TO service_role;

-- Note on Insert: The `handle_new_user` trigger function runs as `SECURITY DEFINER` (the owner/superuser),
-- meaning it automatically has permission to insert into `public.profiles` during signup,
-- even without an explicit INSERT grant to users.

/*
-- VERIFICATION BLOCK (Run in SQL Editor after signing up a user):
select * from public.profiles;
-- You should see the user's row with role 'member'.
*/
