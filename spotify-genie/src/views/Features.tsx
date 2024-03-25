import '../styles/Home.css';
import '../styles/Features.css';
import MusicNoteGraphic from '../assets/listening-to-music-svgrepo-com.svg';

export default function Features() {

    return(
        <div className="vh-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: '#E1F0DA' }}>
            <div className="container text-black d-flex justify-content-between align-items-center">
                <div>
                    <img className='title-pulse' src={MusicNoteGraphic} alt="Music Note" style={{ maxWidth: '400px', maxHeight: '400px' }} />
                </div>
                <div>
                    <h1 className="display-1 fw-bold mb-4">Features</h1>
                    <ul>
                        <li>Login to Spotify, though Spotify</li>
                        <li>Automatically read through song data to identify listening trends</li>
                        <li>Use a multitude of music data to curate a brand new playlist for any occasion</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
