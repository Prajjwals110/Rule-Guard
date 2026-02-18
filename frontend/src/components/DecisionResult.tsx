/**
 * DecisionResult component - displays decision outcome with color coding.
 */
import { memo } from 'react';
import { Decision } from '../types/Decision';
import './DecisionResult.css';

interface DecisionResultProps {
    decision: Decision;
}

const DECISION_CLASS_MAP: Record<string, string> = {
    'APPROVED': 'decision-approved',
    'REJECTED': 'decision-rejected',
    'NEEDS_REVIEW': 'decision-review',
};

function DecisionResultComponent({ decision }: DecisionResultProps) {
    const decisionClass = DECISION_CLASS_MAP[decision.decision] || '';

    return (
        <div className={`decision-result ${decisionClass}`}>
            <h3 className="decision-title">{decision.decision}</h3>
            <p className="decision-explanation">{decision.explanation}</p>
            {decision.rule_id && (
                <p className="decision-meta">Applied Rule ID: {decision.rule_id}</p>
            )}
        </div>
    );
}

export const DecisionResult = memo(DecisionResultComponent);
