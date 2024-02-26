import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function Callback() {
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const query = new URLSearchParams(location.search);
        const code = query.get('code');

        if (code) {
            fetch('/callback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP status ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Store access_token in localStorage or context for use in subsequent API calls
                        localStorage.setItem('access_token', data.access_token);
                        navigate('/playlist');
                    } else {
                        console.error('Token exchange was unsuccessful');
                        // Handle unsuccessful token exchange
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }, [location, navigate]);

    return <div>Logging in...</div>;
}
