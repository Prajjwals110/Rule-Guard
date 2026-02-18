/**
 * Main App component with simple navigation.
 */
import { useState } from 'react';
import { SubmitRequest } from './pages/SubmitRequest';
import { ManageRules } from './pages/ManageRules';
import './App.css';

type Page = 'submit' | 'rules';

function App() {
    const [currentPage, setCurrentPage] = useState<Page>('submit');

    return (
        <div className="app">
            <header className="app-header">
                <h1 className="app-title">RuleGuard</h1>
                <p className="app-subtitle">Rule-Based Request Decision System</p>
            </header>

            <nav className="app-nav">
                <button
                    className={`nav-button ${currentPage === 'submit' ? 'active' : ''}`}
                    onClick={() => setCurrentPage('submit')}
                >
                    Submit Request
                </button>
                <button
                    className={`nav-button ${currentPage === 'rules' ? 'active' : ''}`}
                    onClick={() => setCurrentPage('rules')}
                >
                    Manage Rules
                </button>
            </nav>

            <main className="app-main">
                {currentPage === 'submit' ? <SubmitRequest /> : <ManageRules />}
            </main>

            <footer className="app-footer">
                <p>RuleGuard - A simple, well-structured rule-based decision system</p>
            </footer>
        </div>
    );
}

export default App;
