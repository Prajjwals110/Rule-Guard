/**
 * Decision type matching backend model.
 */
export interface Decision {
    id?: number;
    request_id: number;
    decision: 'APPROVED' | 'REJECTED' | 'NEEDS_REVIEW';
    explanation: string;
    rule_id?: number | null;
    created_at?: string;
}
