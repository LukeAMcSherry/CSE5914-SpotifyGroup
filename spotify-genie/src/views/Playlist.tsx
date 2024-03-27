import { useEffect, useState } from "react";

export default function Playlist() {
    const [artists, setArtists] = useState<any[]>([]);
    const [fetchedPlaylists, setFetchedPlaylists] = useState<any[]>([]);
    const [selectedPlaylistURI, setSelectedPlaylistURI] = useState<string | null>(null);
    const [loadingRecommendations, setLoadingRecommendations] = useState<boolean>(false);
    const [recommendations, setRecommendations] = useState<string[]>([]);
    const [lyrics, setLyrics] = useState('');

    useEffect(() => {
        const fetchArtists = async () => {
            try {
                const res = await fetch('/follow-artist', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                if (!res.ok) {
                    throw new Error(`Error: ${res.status}`);
                }
                const data = await res.json();
                setArtists(data.artists.items);
            } catch (error) {
                console.error(error);
            }
        };
        fetchArtists();
    }, []);

    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const res = await fetch('/follow-playlists', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                if (!res.ok) {
                    throw new Error(`Error: ${res.status}`);
                }
                const data = await res.json();
                setFetchedPlaylists(data);
            } catch (error) {
                console.error(error);
            }
        };
        fetchPlaylists();
    }, []);

    const handlePlaylistSelection = async (playlistURI: string) => {
        try {
            setLoadingRecommendations(true);
            setSelectedPlaylistURI(playlistURI);
            const response = await fetch('http://localhost:17490/process_playlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ playlist_uri: playlistURI })
            });
            if (!response.ok) {
                throw new Error('Failed to send playlist URI to server');
            }
            const data = await response.json();
            setRecommendations(data);
            setLoadingRecommendations(false);
            console.log(data[0], data[1]);
            if (data.length > 0) {
                const firstRecommendation = data[0]; // This is a string like "Song Name - Artist Name"
                fetchLyrics(firstRecommendation); // Adjust fetchLyrics to handle this format
            }
        } catch (error) {
            console.error('Error:', error);
            setLoadingRecommendations(false);
        }
    };

    const fetchLyrics = async (songWithArtist: string) => {
        const [songName, artistName] = songWithArtist.split(" - "); // Split the string to get song name and artist name
        try {
            const response = await fetch('/lyrics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: songName, artist: artistName }),
            });
            if (!response.ok) {
                throw new Error('Failed to fetch lyrics');
            }
            const data = await response.json();
            setLyrics(data.lyrics);
        } catch (error) {
            console.error('Failed to fetch lyrics:', error);
        }
    };


    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px', padding: '20px' }}>
            {loadingRecommendations ? (
                <div style={{ textAlign: 'center' }}>
                    <h2>Loading Recommendations...</h2>
                </div>
            ) : selectedPlaylistURI ? (
                <div style={{ textAlign: 'center' }}>
                    <h2>Selected Playlist URI:</h2>
                    <p>{selectedPlaylistURI}</p>
                    <h2>Recommendations:</h2>
                    <ul>
                        {recommendations.map((recommendation, index) => (
                            <li key={index}>{recommendation}</li>
                        ))}
                    </ul>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px', padding: '20px' }}>
                        {/* Displaying playlists and recommendations as before */}
                        {lyrics && (
                            <div style={{ gridColumn: '1 / -1', textAlign: 'center' }}>
                                <h2>Lyrics</h2>
                                <p style={{ whiteSpace: 'pre-wrap' }}>{lyrics}</p>
                            </div>
                        )}
                    </div>
                </div>
            ) : (
                fetchedPlaylists.map(playlist => (
                    <div key={playlist.id} style={{ border: '1px solid #ccc', borderRadius: '10px', padding: '10px', textAlign: 'center', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
                        {playlist.images && playlist.images[0] && (
                            <img src={playlist.images[0]?.url} alt={playlist.name} style={{ width: '100%', height: 'auto', borderRadius: '5px' }} />
                        )}
                        <h3>{playlist.name}</h3>
                        <button 
                            onClick={() => handlePlaylistSelection(playlist.uri)} 
                            style={{ display: 'inline-block', marginTop: '10px', textDecoration: 'none', background: '#1DB954', color: 'white', padding: '10px 15px', borderRadius: '20px', border: 'none', cursor: 'pointer' }}
                        >
                            Select Playlist
                        </button>
                    </div>
                ))
            )}
        </div>
    );
}
