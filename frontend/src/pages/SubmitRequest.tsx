/**
 * SubmitRequest page - main page for submitting requests.
 */
import { RequestForm } from '../components/RequestForm';

export function SubmitRequest() {
    return (
        <div>
            <h1>Submit Request</h1>
            <p className="page-description">
                Submit a request for evaluation. The system will apply rules based on amount and category.
            </p>
            <RequestForm />
        </div>
    );
}
