/**
 * Rule type matching backend model.
 */
export interface Rule {
    id?: number;
    field: 'amount' | 'category';
    operator: '<' | '<=' | '>' | '==';
    value: string;
    decision: 'APPROVE' | 'REJECT' | 'REVIEW';
    priority: number;
}
