import '../styles/Home.css';
import MusicNoteGraphic from '../assets/listening-to-music-svgrepo-com.svg';

export default function Home() {
    async function handleLogin() {
        const res = await fetch('/login')
        const data = await res.json()
        window.location.href = data.auth_url
    }
    return (
        <div className="vh-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: '#E1F0DA' }}>
            <div className="container text-black d-flex justify-content-between align-items-center">
                <div>
                    <h1 className="display-1 fw-bold mb-4">Spotify Genie</h1>
                    <p className="fs-3 mb-5">Embark on a musical journey tailored to your unique taste and find your next favorite song with Spotify Genie.</p>
                    <button onClick={handleLogin} className="btn btn-dark btn-lg">Login With Spotify</button>
                </div>
                <div>
                    <img className='title-pulse' src={MusicNoteGraphic} alt="Music Note" style={{ maxWidth: '400px', maxHeight: '400px' }} />
                </div>
            </div>
        </div>
    );
}
