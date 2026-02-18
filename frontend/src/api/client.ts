/**
 * API client for RuleGuard backend.
 */
import { Request } from '../types/Request';
import { Decision } from '../types/Decision';
import { Rule } from '../types/Rule';

const API_BASE_URL = 'http://localhost:5000/api';
const REQUEST_TIMEOUT = 10000; // 10 seconds

/**
 * Parse error from API response.
 */
async function parseError(response: Response, defaultMessage: string): Promise<string> {
    try {
        const error = await response.json();
        return error.details || error.error || defaultMessage;
    } catch {
        return defaultMessage;
    }
}

/**
 * Fetch with timeout.
 */
async function fetchWithTimeout(url: string, options?: RequestInit): Promise<Response> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
        });
        return response;
    } finally {
        clearTimeout(timeout);
    }
}

export interface SubmitRequestResponse {
    request: Request;
    decision: Decision;
}

/**
 * Submit a new request for evaluation.
 */
export async function submitRequest(
    amount: number,
    category: string,
    description?: string
): Promise<SubmitRequestResponse> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/requests`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount, category, description }),
    });

    if (!response.ok) {
        const errorMessage = await parseError(response, 'Failed to submit request');
        throw new Error(errorMessage);
    }

    return response.json();
}

/**
 * Get all rules ordered by priority.
 */
export async function getRules(): Promise<Rule[]> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/rules`);

    if (!response.ok) {
        throw new Error('Failed to fetch rules');
    }

    return response.json();
}

/**
 * Create a new rule.
 */
export async function createRule(rule: Omit<Rule, 'id'>): Promise<Rule> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/rules`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(rule),
    });

    if (!response.ok) {
        const errorMessage = await parseError(response, 'Failed to create rule');
        throw new Error(errorMessage);
    }

    return response.json();
}

/**
 * Delete a rule by ID.
 */
export async function deleteRule(ruleId: number): Promise<void> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/rules/${ruleId}`, {
        method: 'DELETE',
    });

    if (!response.ok) {
        throw new Error('Failed to delete rule');
    }
}
