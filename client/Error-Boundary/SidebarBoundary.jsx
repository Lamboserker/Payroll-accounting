import React, { Component } from 'react';

class ErrorBoundary extends Component {
    state = { hasError: false, error: null };

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error caught by ErrorBoundary:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return <h1>Etwas ist schief gelaufen. Versuche es später noch einmal.</h1>;
        }
        return this.props.children;
    }
}

export default ErrorBoundary;
