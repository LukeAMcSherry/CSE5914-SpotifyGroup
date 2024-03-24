import { useEffect, useState } from "react"
export default function Playlist() {
    const [playlists, setPlaylists] = useState([])
    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const res = await fetch('/playlist', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                if (!res.ok) {
                    throw new Error(`Error: ${res.status}`)
                }
                const data = await res.json();
                console.log(data)
                setPlaylists(data)
                console.log(playlists)
            } catch (error) {
                console.error(error)
            }
        };
        fetchPlaylists()
    }, [])
    return <div>Hello </div>
}