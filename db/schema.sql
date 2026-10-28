CREATE TABLE IF NOT EXISTS institutions (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  registration_reference TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS financial_instruments (
  id UUID PRIMARY KEY,
  institution_id UUID NOT NULL REFERENCES institutions(id),
  reference_number TEXT NOT NULL,
  issuing_bank TEXT NOT NULL,
  amount_minor BIGINT NOT NULL CHECK (amount_minor > 0),
  currency CHAR(3) NOT NULL DEFAULT 'INR',
  issue_date DATE NOT NULL,
  maturity_date DATE NOT NULL CHECK (maturity_date > issue_date),
  status TEXT NOT NULL,
  original_instrument_id UUID REFERENCES financial_instruments(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (issuing_bank, reference_number)
);

CREATE TABLE IF NOT EXISTS audit_events (
  id UUID PRIMARY KEY,
  actor_id UUID NOT NULL,
  action TEXT NOT NULL,
  record_id UUID NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  previous_hash TEXT NOT NULL,
  event_hash TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS financial_instruments_maturity_idx
  ON financial_instruments (maturity_date, status);
