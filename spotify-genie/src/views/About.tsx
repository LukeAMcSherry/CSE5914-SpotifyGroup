import '../styles/About.css';
import '../styles/Features.css';

export default function About() {

    return(
        <div className="vh-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: '#E1F0DA' }}>
            <div className="container text-black text-align-center">
                <div className="credits text-center"><p style={{ fontSize: '3em' }}><b>Created by Steven Egnaczyk, Alexander Felderean, Michael Grentzer, Luke McSherry, Sam Nguyen, and Naishal Patel.</b></p></div>
                <br></br>
                <div className="github text-center"><a style={{ fontSize: '3em' }} href="https://github.com/LukeAMcSherry/CSE5914-SpotifyGroup">Visit our Source Code!</a></div>
            </div>
        </div>
    );
}
