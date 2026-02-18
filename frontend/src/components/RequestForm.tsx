/**
 * RequestForm component - form for submitting requests.
 */
import { useState, FormEvent, useCallback } from 'react';
import { submitRequest } from '../api/client';
import { Decision } from '../types/Decision';
import { DecisionResult } from './DecisionResult';
import './RequestForm.css';

export function RequestForm() {
    const [amount, setAmount] = useState('');
    const [category, setCategory] = useState('');
    const [description, setDescription] = useState('');
    const [decision, setDecision] = useState<Decision | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = useCallback(async (e: FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setDecision(null);

        try {
            const amountNum = parseFloat(amount);
            const response = await submitRequest(amountNum, category, description || undefined);
            setDecision(response.decision);

            // Clear form on success
            setAmount('');
            setCategory('');
            setDescription('');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to submit request');
        } finally {
            setLoading(false);
        }
    }, [amount, category, description]);

    return (
        <div className="request-form-container">
            <form onSubmit={handleSubmit} className="request-form">
                <div className="form-group">
                    <label htmlFor="amount">Amount *</label>
                    <input
                        id="amount"
                        type="number"
                        step="0.01"
                        min="0.01"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        required
                        placeholder="Enter amount"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="category">Category *</label>
                    <input
                        id="category"
                        type="text"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        required
                        placeholder="e.g., travel, office, equipment"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="description">Description (optional)</label>
                    <textarea
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Additional details about the request"
                        rows={3}
                    />
                </div>

                {error && (
                    <div className="error-message">
                        <strong>Error:</strong> {error}
                    </div>
                )}

                <button type="submit" disabled={loading} className="submit-button">
                    {loading ? 'Submitting...' : 'Submit Request'}
                </button>
            </form>

            {decision && <DecisionResult decision={decision} />}
        </div>
    );
}
