import { useEffect, useState } from "react"

export default function Playlist() {
    const [artists, setArtists] = useState<any[]>([]); // Use setArtists to match the state variable

    useEffect(() => {
        const fetchArtists = async () => {
            try {
                const res = await fetch('/follow-artist', {
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
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px', padding: '20px' }}>
            {artists.map(artist => (
                <div key={artist.id} style={{ border: '1px solid #ccc', borderRadius: '10px', padding: '10px', textAlign: 'center', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
                    <img src={artist.images[0]?.url} alt={artist.name} style={{ width: '100%', height: 'auto', borderRadius: '5px' }} />
                    <h3>{artist.name}</h3>
                    <p>{artist.genres.join(', ') || 'No genres listed'}</p>
                    <a href={artist.external_urls.spotify} target="_blank" rel="noopener noreferrer" style={{ display: 'inline-block', marginTop: '10px', textDecoration: 'none', background: '#1DB954', color: 'white', padding: '10px 15px', borderRadius: '20px' }}>Listen on Spotify</a>
                </div>
            ))}
        </div>

    );
}
