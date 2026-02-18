/**
 * Request type matching backend model.
 */
export interface Request {
    id?: number;
    amount: number;
    category: string;
    description?: string;
    created_at?: string;
}
