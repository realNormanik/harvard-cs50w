-- ============================================================
-- EXAMPLE DATA - PostgreSQL
-- ============================================================


-- ============================================================
-- USER
-- username: user
-- password: password
-- ============================================================

INSERT INTO auth_user (
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
VALUES (
    1,
    'pbkdf2_sha256$600000$example$NM3mC9boABgLTl2uIwgt0x5awBSmVkt0hdsdqcbt1cY=',
    NULL,
    FALSE,
    'user',
    'John',
    'Smith',
    'user@example.com',
    FALSE,
    TRUE,
    '2026-08-30 12:00:00'
)
ON CONFLICT DO NOTHING;


-- ============================================================
-- PIPELINE STAGES
-- ============================================================

INSERT INTO crm_pipelinestage (
    id,
    name,
    "order",
    owner_id,
    is_final
)
VALUES
    (1, 'New Lead',        1, 1, FALSE),
    (2, 'Contacted',       2, 1, FALSE),
    (3, 'Proposal Sent',   3, 1, FALSE),
    (4, 'Negotiation',     4, 1, FALSE),
    (5, 'Won',             5, 1, TRUE),
    (6, 'Lost',            6, 1, TRUE)
ON CONFLICT DO NOTHING;


-- ============================================================
-- CLIENTS
-- ============================================================

INSERT INTO crm_client (
    id,
    owner_id,
    first_name,
    last_name,
    company,
    email,
    phone,
    notes,
    created_at
)
VALUES
    (
        1,
        1,
        'James',
        'Anderson',
        'TechVision Inc.',
        'james.anderson@techvision.com',
        '+1 202-555-0101',
        'Interested in implementing a CRM system.',
        '2026-08-20 09:15:00'
    ),
    (
        2,
        1,
        'Emily',
        'Johnson',
        'Green Solutions',
        'emily.johnson@greensolutions.com',
        '+1 202-555-0102',
        'Interested in a long-term marketing partnership.',
        '2026-08-21 10:30:00'
    ),
    (
        3,
        1,
        'Michael',
        'Williams',
        'Digital Factory',
        'michael.williams@digitalfactory.com',
        '+1 202-555-0103',
        'Potential B2B customer interested in process automation.',
        '2026-08-22 11:00:00'
    ),
    (
        4,
        1,
        'Sarah',
        'Brown',
        'Nova Marketing',
        'sarah.brown@novamarketing.com',
        '+1 202-555-0104',
        'Interested in the premium service package.',
        '2026-08-23 13:20:00'
    ),
    (
        5,
        1,
        'David',
        'Miller',
        'Smart Office',
        'david.miller@smartoffice.com',
        '+1 202-555-0105',
        'Initial contact made at an industry conference.',
        '2026-08-24 14:45:00'
    )
ON CONFLICT DO NOTHING;


-- ============================================================
-- DEALS
-- ============================================================

INSERT INTO crm_deal (
    id,
    owner_id,
    title,
    description,
    client_id,
    stage_id,
    value,
    priority,
    due_date,
    "order",
    created_at,
    updated_at,
    is_closed
)
VALUES
    (
        1,
        1,
        'CRM Implementation',
        'Implementation of a CRM system for the sales department.',
        1,
        3,
        25000,
        'high',
        '2026-09-10',
        1,
        '2026-08-20 10:00:00',
        '2026-08-28 15:30:00',
        FALSE
    ),
    (
        2,
        1,
        'Marketing Package',
        'Comprehensive marketing campaign management.',
        2,
        2,
        12000,
        'medium',
        '2026-09-15',
        2,
        '2026-08-21 11:30:00',
        '2026-08-27 12:00:00',
        FALSE
    ),
    (
        3,
        1,
        'Process Automation',
        'Automation of sales processes and business reporting.',
        3,
        4,
        18500,
        'high',
        '2026-09-05',
        3,
        '2026-08-22 12:00:00',
        '2026-08-29 09:00:00',
        FALSE
    ),
    (
        4,
        1,
        'Website Development',
        'Development of a modern corporate website.',
        4,
        5,
        15000,
        'medium',
        '2026-08-25',
        4,
        '2026-08-10 09:00:00',
        '2026-08-25 16:00:00',
        TRUE
    ),
    (
        5,
        1,
        'Office Management System',
        'Delivery and configuration of an office management system.',
        5,
        6,
        8500,
        'low',
        '2026-08-18',
        5,
        '2026-08-05 14:00:00',
        '2026-08-18 10:00:00',
        TRUE
    )
ON CONFLICT DO NOTHING;


-- ============================================================
-- ACTIVITIES
-- ============================================================

INSERT INTO crm_activity (
    id,
    owner_id,
    client_id,
    deal_id,
    activity_type,
    content,
    created_at
)
VALUES
    (
        1,
        1,
        1,
        1,
        'call',
        'Phone call regarding the CRM implementation scope.',
        '2026-08-25 09:30:00'
    ),
    (
        2,
        1,
        1,
        1,
        'email',
        'Sent the proposal and detailed project scope.',
        '2026-08-26 13:15:00'
    ),
    (
        3,
        1,
        2,
        2,
        'meeting',
        'Online meeting with the client regarding the marketing campaign.',
        '2026-08-27 10:00:00'
    ),
    (
        4,
        1,
        3,
        3,
        'call',
        'The client confirmed their interest in process automation.',
        '2026-08-28 14:20:00'
    ),
    (
        5,
        1,
        4,
        4,
        'email',
        'Confirmed that the project has been completed.',
        '2026-08-25 15:45:00'
    ),
    (
        6,
        1,
        5,
        5,
        'note',
        'Project closed without implementation.',
        '2026-08-18 11:30:00'
    )
ON CONFLICT DO NOTHING;


-- ============================================================
-- TASKS
-- ============================================================

INSERT INTO crm_task (
    id,
    owner_id,
    client_id,
    deal_id,
    title,
    due_date,
    is_done,
    created_at
)
VALUES
    (
        1,
        1,
        1,
        1,
        'Prepare final proposal',
        '2026-09-01',
        FALSE,
        '2026-08-28 09:00:00'
    ),
    (
        2,
        1,
        2,
        2,
        'Contact the client',
        '2026-09-02',
        FALSE,
        '2026-08-28 10:30:00'
    ),
    (
        3,
        1,
        3,
        3,
        'Prepare the contract',
        '2026-09-03',
        FALSE,
        '2026-08-29 08:45:00'
    ),
    (
        4,
        1,
        4,
        4,
        'Archive project files',
        '2026-08-30',
        TRUE,
        '2026-08-25 17:00:00'
    ),
    (
        5,
        1,
        5,
        5,
        'Complete documentation',
        '2026-08-20',
        TRUE,
        '2026-08-18 12:00:00'
    ),
    (
        6,
        1,
        NULL,
        NULL,
        'Prepare sales report',
        '2026-09-05',
        FALSE,
        '2026-08-30 09:00:00'
    )
ON CONFLICT DO NOTHING;