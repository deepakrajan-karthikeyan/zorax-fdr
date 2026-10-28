export type InstrumentStatus =
  | "SUBMITTED"
  | "VALIDATED"
  | "PENDING_VERIFICATION"
  | "VERIFIED"
  | "DISCREPANCY"
  | "RENEWAL_PENDING"
  | "RELEASE_APPROVED"
  | "RELEASED";

export type UserRole =
  | "SYSTEM_ADMINISTRATOR"
  | "INSTITUTION_ADMINISTRATOR"
  | "BUREAU_REVIEWER"
  | "APPROVING_OFFICER"
  | "AUDITOR";

export interface FinancialInstrument {
  id: string;
  institutionId: string;
  referenceNumber: string;
  issuingBank: string;
  amountMinor: number;
  currency: "INR";
  issueDate: string;
  maturityDate: string;
  status: InstrumentStatus;
  confidence?: number;
  originalInstrumentId?: string;
}

export interface ExtractionResult {
  instrumentType: "FDR" | "SECURITY_DEPOSIT";
  referenceNumber: string;
  issuingBank: string;
  amountMinor: number;
  maturityDate: string;
  confidence: number;
  requiresHumanReview: boolean;
  modelMode: "DEMO" | "PRODUCTION";
}

export interface AuditEvent {
  id: string;
  actorId: string;
  action: string;
  recordId: string;
  occurredAt: string;
  previousHash: string;
  eventHash: string;
}
