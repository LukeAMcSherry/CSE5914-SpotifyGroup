import React, { useEffect } from "react"
import { useLocation } from "react-router-dom"

function useQuery() {
    return new URLSearchParams(useLocation().search)
}

export default function Callback() {
    const query = useQuery()
    useEffect(() => {
        // check if the code parameter is in the URI
        const code = query.get("code")
        if (code) {
            fetch("/callback", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code })
            }).then(async response => {
                const data = await response.json()
                // handle the data here
            }).catch(error => {
                // handle error here
            })
        }
    }, [query])

    return <div>Logging in...</div>
}