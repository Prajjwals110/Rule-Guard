/**
 * RuleList component - displays and manages rules.
 */
import { useState, useEffect, useCallback } from 'react';
import { Rule } from '../types/Rule';
import { getRules, deleteRule, createRule } from '../api/client';
import './RuleList.css';

export function RuleList() {
    const [rules, setRules] = useState<Rule[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showAddForm, setShowAddForm] = useState(false);

    // Form state
    const [field, setField] = useState<'amount' | 'category'>('amount');
    const [operator, setOperator] = useState<'<' | '<=' | '>' | '=='>('<');
    const [value, setValue] = useState('');
    const [decision, setDecision] = useState<'APPROVE' | 'REJECT' | 'REVIEW'>('APPROVE');
    const [priority, setPriority] = useState('');

    const loadRules = useCallback(async () => {
        try {
            setLoading(true);
            const data = await getRules();
            setRules(data);
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load rules');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadRules();
    }, [loadRules]);

    const handleDelete = useCallback(async (ruleId: number) => {
        if (!confirm('Are you sure you want to delete this rule?')) {
            return;
        }

        try {
            await deleteRule(ruleId);
            await loadRules();
        } catch (err) {
            alert(err instanceof Error ? err.message : 'Failed to delete rule');
        }
    }, [loadRules]);

    const handleAddRule = useCallback(async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            await createRule({
                field,
                operator,
                value,
                decision,
                priority: parseInt(priority),
            });

            // Reset form
            setValue('');
            setPriority('');
            setShowAddForm(false);

            // Reload rules
            await loadRules();
        } catch (err) {
            alert(err instanceof Error ? err.message : 'Failed to create rule');
        }
    }, [field, operator, value, decision, priority, loadRules]);

    if (loading) {
        return <div className="loading">Loading rules...</div>;
    }

    if (error) {
        return <div className="error-message">Error: {error}</div>;
    }

    return (
        <div className="rule-list-container">
            <div className="rule-list-header">
                <h2>Rules (evaluated by priority)</h2>
                <button onClick={() => setShowAddForm(!showAddForm)} className="add-rule-button">
                    {showAddForm ? 'Cancel' : '+ Add Rule'}
                </button>
            </div>

            {showAddForm && (
                <form onSubmit={handleAddRule} className="add-rule-form">
                    <div className="form-row">
                        <div className="form-group">
                            <label>Field</label>
                            <select value={field} onChange={(e) => setField(e.target.value as 'amount' | 'category')}>
                                <option value="amount">amount</option>
                                <option value="category">category</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Operator</label>
                            <select value={operator} onChange={(e) => setOperator(e.target.value as '<' | '<=' | '>' | '==')}>
                                <option value="<">&lt;</option>
                                <option value="<=">&lt;=</option>
                                <option value=">">&gt;</option>
                                <option value="==">==</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Value</label>
                            <input
                                type="text"
                                value={value}
                                onChange={(e) => setValue(e.target.value)}
                                required
                                placeholder={field === 'amount' ? '1000' : 'category_name'}
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Decision</label>
                            <select value={decision} onChange={(e) => setDecision(e.target.value as 'APPROVE' | 'REJECT' | 'REVIEW')}>
                                <option value="APPROVE">APPROVE</option>
                                <option value="REJECT">REJECT</option>
                                <option value="REVIEW">REVIEW</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Priority</label>
                            <input
                                type="number"
                                value={priority}
                                onChange={(e) => setPriority(e.target.value)}
                                required
                                min="0"
                                placeholder="0 = highest"
                            />
                        </div>

                        <div className="form-group">
                            <label>&nbsp;</label>
                            <button type="submit" className="submit-button">Create Rule</button>
                        </div>
                    </div>
                </form>
            )}

            {rules.length === 0 ? (
                <p className="no-rules">No rules defined. Add a rule to get started.</p>
            ) : (
                <div className="rules-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Priority</th>
                                <th>Condition</th>
                                <th>Decision</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rules.map((rule) => (
                                <tr key={rule.id}>
                                    <td className="priority-cell">{rule.priority}</td>
                                    <td className="condition-cell">
                                        <code>{rule.field} {rule.operator} {rule.value}</code>
                                    </td>
                                    <td className={`decision-cell decision-${rule.decision.toLowerCase()}`}>
                                        {rule.decision}
                                    </td>
                                    <td className="actions-cell">
                                        <button onClick={() => handleDelete(rule.id!)} className="delete-button">
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
