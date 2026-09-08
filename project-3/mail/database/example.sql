-- ============================================================
-- USERS
-- ============================================================
--
-- User 1 = user@example.com
-- User 2 = pepe@example.com
--
-- Password for both users: password
-- ============================================================

INSERT INTO mail_user (
    id,
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
)
VALUES
(
    1,
    'pbkdf2_sha256$600000$example$NM3mC9boABgLTl2uIwgt0x5awBSmVkt0hdsdqcbt1cY=',
    NULL,
    TRUE,
    'user@example.com',
    'Example',
    'User',
    'user@example.com',
    TRUE,
    TRUE,
    '2026-08-18 18:05:00'
),
(
    2,
    'pbkdf2_sha256$600000$example$NM3mC9boABgLTl2uIwgt0x5awBSmVkt0hdsdqcbt1cY=',
    NULL,
    FALSE,
    'pepe@example.com',
    'Pepe',
    'User',
    'pepe@example.com',
    FALSE,
    TRUE,
    '2026-08-18 18:06:00'
)
ON CONFLICT DO NOTHING;


-- ============================================================
-- EMAILS
-- ============================================================
--
-- Each logical email has two database records:
--
-- 1. Copy in sender's "Sent" folder
-- 2. Copy in recipient's "Inbox"
--
-- Email A:
-- pepe -> user
-- Subject: Working hard? :)
--
-- Email B:
-- user -> pepe
-- Subject: Re: Working hard? :)
--
-- Email C:
-- pepe -> user
-- Subject: Guess where I am
-- ============================================================

INSERT INTO mail_email (
    id,
    subject,
    body,
    timestamp,
    read,
    archived,
    user_id,
    sender_id
)
VALUES

-- ============================================================
-- EMAIL A
-- Copy in Pepe's Sent folder
-- ============================================================
(
    1,
    'Working hard? :)',
    'Hey,

Just saw your status is online during business hours again. Must be nice being chained to that desk while the rest of us are living our lives. Say hi to your inbox for me.

Pepe',
    '2026-08-18 18:10:00',
    TRUE,
    FALSE,
    2,
    2
),

-- ============================================================
-- EMAIL A
-- Copy in User's Inbox
-- ============================================================
(
    2,
    'Working hard? :)',
    'Hey,

Just saw your status is online during business hours again. Must be nice being chained to that desk while the rest of us are living our lives. Say hi to your inbox for me.

Pepe',
    '2026-08-18 18:10:00',
    FALSE,
    FALSE,
    1,
    2
),

-- ============================================================
-- EMAIL B
-- Copy in User's Sent folder
-- ============================================================
(
    3,
    'Re: Working hard? :)',
    'Ha ha, very funny. Some of us actually have deadlines. Enjoy your free time while it lasts.

user',
    '2026-08-18 18:20:00',
    TRUE,
    FALSE,
    1,
    1
),

-- ============================================================
-- EMAIL B
-- Copy in Pepe's Inbox
-- ============================================================
(
    4,
    'Re: Working hard? :)',
    'Ha ha, very funny. Some of us actually have deadlines. Enjoy your free time while it lasts.

user',
    '2026-08-18 18:20:00',
    FALSE,
    FALSE,
    2,
    1
),

-- ============================================================
-- EMAIL C
-- Copy in Pepe's Sent folder
-- ============================================================
(
    5,
    'Guess where I am',
    'Speaking of free time... guess who''s currently on vacation? Sun, sand, and zero deadlines. Check out the view:

<img src="https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/mail/uploads/IlGqDZY84G.webp">

Wish you were here (kind of).

Pepe',
    '2026-08-18 18:30:00',
    TRUE,
    FALSE,
    2,
    2
),

-- ============================================================
-- EMAIL C
-- Copy in User's Inbox
-- ============================================================
(
    6,
    'Guess where I am',
    'Speaking of free time... guess who''s currently on vacation? Sun, sand, and zero deadlines. Check out the view:

<img src="https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/mail/uploads/IlGqDZY84G.webp">

Wish you were here (kind of).

Pepe',
    '2026-08-18 18:30:00',
    FALSE,
    FALSE,
    1,
    2
)

ON CONFLICT DO NOTHING;


-- ============================================================
-- EMAIL RECIPIENTS
-- ============================================================
--
-- M2M table for mail_email.recipients
--
-- Email A:
-- records 1 and 2 -> recipient = user (id 1)
--
-- Email B:
-- records 3 and 4 -> recipient = pepe (id 2)
--
-- Email C:
-- records 5 and 6 -> recipient = user (id 1)
-- ============================================================

INSERT INTO mail_email_recipients (
    id,
    email_id,
    user_id
)
VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 2),
(4, 4, 2),
(5, 5, 1),
(6, 6, 1)
ON CONFLICT DO NOTHING;