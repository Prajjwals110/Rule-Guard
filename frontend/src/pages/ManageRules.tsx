/**
 * ManageRules page - page for viewing and managing rules.
 */
import { RuleList } from '../components/RuleList';

export function ManageRules() {
    return (
        <div>
            <h1>Manage Rules</h1>
            <p className="page-description">
                View, add, and delete rules. Rules are evaluated in priority order (lower number = higher priority).
            </p>
            <RuleList />
        </div>
    );
}
