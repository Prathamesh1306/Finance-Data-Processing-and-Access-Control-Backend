-- Plain-text passwords:
-- admin@finance.com   -> Admin1234!
-- analyst@finance.com -> Analyst1234!
-- viewer@finance.com  -> Viewer1234!

CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO users (id, email, full_name, hashed_password, role, is_active) VALUES
('11111111-1111-1111-1111-111111111111', 'admin@zorvyn.com', 'Admin User', crypt('Admin1234!', gen_salt('bf', 12)), 'ADMIN', true),
('22222222-2222-2222-2222-222222222222', 'analyst@zorvyn.com', 'Analyst User', crypt('Analyst1234!', gen_salt('bf', 12)), 'ANALYST', true),
('33333333-3333-3333-3333-333333333333', 'viewer@zorvyn.com', 'Viewer User', crypt('Viewer1234!', gen_salt('bf', 12)), 'VIEWER', true);

INSERT INTO transactions (id, amount, type, category, date, description, is_deleted, created_by) VALUES
(gen_random_uuid(), 5000.00, 'INCOME', 'SALARY', CURRENT_DATE - INTERVAL '60 days', 'Salary for Feb', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 1500.00, 'EXPENSE', 'RENT', CURRENT_DATE - INTERVAL '58 days', 'Feb Rent', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 100.00, 'EXPENSE', 'UTILITIES', CURRENT_DATE - INTERVAL '57 days', 'Water bill', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 400.00, 'EXPENSE', 'FOOD', CURRENT_DATE - INTERVAL '55 days', 'Groceries', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 50.00, 'EXPENSE', 'TRANSPORT', CURRENT_DATE - INTERVAL '54 days', 'Gas', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 200.00, 'EXPENSE', 'ENTERTAINMENT', CURRENT_DATE - INTERVAL '50 days', 'Concert', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 150.00, 'EXPENSE', 'HEALTH', CURRENT_DATE - INTERVAL '48 days', 'Pharmacy', false, '11111111-1111-1111-1111-111111111111'),

(gen_random_uuid(), 5000.00, 'INCOME', 'SALARY', CURRENT_DATE - INTERVAL '30 days', 'Salary for March', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 1500.00, 'EXPENSE', 'RENT', CURRENT_DATE - INTERVAL '28 days', 'March Rent', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 120.00, 'EXPENSE', 'UTILITIES', CURRENT_DATE - INTERVAL '26 days', 'Electricity', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 300.00, 'EXPENSE', 'FOOD', CURRENT_DATE - INTERVAL '25 days', 'Groceries', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 80.00, 'EXPENSE', 'TRANSPORT', CURRENT_DATE - INTERVAL '24 days', 'Train pass', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 1000.00, 'INCOME', 'OTHER', CURRENT_DATE - INTERVAL '20 days', 'Dividend', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 250.00, 'EXPENSE', 'OTHER', CURRENT_DATE - INTERVAL '18 days', 'Misc', false, '11111111-1111-1111-1111-111111111111'),

(gen_random_uuid(), 5000.00, 'INCOME', 'SALARY', CURRENT_DATE - INTERVAL '1 days', 'Salary for April', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 1500.00, 'EXPENSE', 'RENT', CURRENT_DATE, 'April Rent', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 450.00, 'EXPENSE', 'FOOD', CURRENT_DATE, 'Groceries', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 60.00, 'EXPENSE', 'TRANSPORT', CURRENT_DATE, 'Gas', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 120.00, 'EXPENSE', 'ENTERTAINMENT', CURRENT_DATE, 'Movies', false, '11111111-1111-1111-1111-111111111111'),
(gen_random_uuid(), 800.00, 'INCOME', 'FREELANCE', CURRENT_DATE, 'Consulting', false, '11111111-1111-1111-1111-111111111111');
