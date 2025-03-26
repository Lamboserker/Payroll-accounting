import React, { Component } from 'react';

class ErrorBoundary extends Component {
    state = {
        hasError: false,
        error: null,
        errorInfo: null,
        errorMessage: 'Etwas ist schief gelaufen. Bitte versuchen Sie es später erneut.'
    };

    // Liefert die Fehlermeldung und aktualisiert den State
    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    // Fängt Fehler und Fehlerinformationen ab
    componentDidCatch(error, errorInfo) {
        this.setState({
            errorInfo
        });
        // Loggen der Fehler für weitere Analyse
        console.error('Fehler in ErrorBoundary:', error, errorInfo);

        // Hier könnte man Fehler an ein externes Monitoring-System senden (z.B. Sentry, LogRocket)
        // sendErrorToMonitoringService(error, errorInfo);
    }

    // Gibt die Benutzeroberfläche der Fehlerseite zurück
    renderErrorContent() {
        const { error, errorMessage, errorInfo } = this.state;

        return (
            <div style={{ padding: '20px', backgroundColor: '#f8d7da', color: '#721c24' }}>
                <h1>Etwas ist schief gelaufen!</h1>
                <p>{errorMessage}</p>
                <details style={{ whiteSpace: 'pre-wrap' }}>
                    <summary>Fehlerdetails anzeigen</summary>
                    {error && <p>{error.toString()}</p>}
                    {errorInfo && <pre>{errorInfo.componentStack}</pre>}
                </details>
                <button
                    onClick={() => window.location.reload()}
                    style={{
                        padding: '10px 20px',
                        marginTop: '20px',
                        backgroundColor: '#155724',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                    }}
                >
                    Seite neu laden
                </button>
            </div>
        );
    }

    render() {
        if (this.state.hasError) {
            return this.renderErrorContent();
        }
        return this.props.children;
    }
}

export default ErrorBoundary;
