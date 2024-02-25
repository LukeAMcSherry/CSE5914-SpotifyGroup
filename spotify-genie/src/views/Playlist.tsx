import { useEffect, useState } from "react"

export default function Playlist() {
    const [artists, setArtists] = useState<any[]>([]); // Use setArtists to match the state variable

    useEffect(() => {
        const fetchArtists = async () => {
            try {
                const res = await fetch('/playlist', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json', // Correct the typo here
                    }
                });
                if (!res.ok) {
                    throw new Error(`Error: ${res.status}`);
                }
                const data = await res.json();
                setArtists(data.artists.items); // Set the artists state to the items from the artists object
            } catch (error) {
                console.error(error); // Use console.error for errors
            }
        };
        fetchArtists();
    }, []);

    return (
        <div>
            <h2>Artists</h2>
            <ul>
                {artists.map(artist => (
                    <li key={artist.id}>{artist.name}</li> // Use artist.id as key for each list item
                ))}
            </ul>
        </div>
    );
}
