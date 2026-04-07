-- Create custom ENUM types
CREATE TYPE role_enum AS ENUM ('VIEWER', 'ANALYST', 'ADMIN');
CREATE TYPE type_enum AS ENUM ('INCOME', 'EXPENSE');
CREATE TYPE category_enum AS ENUM ('SALARY', 'FREELANCE', 'FOOD', 'TRANSPORT', 'UTILITIES', 'ENTERTAINMENT', 'HEALTH', 'EDUCATION', 'RENT', 'OTHER');

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    role role_enum NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX ix_users_email ON users(email);

-- Create transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    amount NUMERIC(15,2) NOT NULL,
    type type_enum NOT NULL,
    category category_enum NOT NULL,
    date DATE NOT NULL,
    description VARCHAR,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX ix_transactions_date ON transactions(date);
CREATE INDEX ix_transactions_type ON transactions(type);
CREATE INDEX ix_transactions_category ON transactions(category);
