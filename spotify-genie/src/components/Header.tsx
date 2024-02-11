import { Link } from 'react-router-dom';
import logo from '../assets/music-svgrepo-com.svg'
export default function Header() {
    return (
        <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: "#D4E7C5" }}>
            <div className="container-fluid mx-5">
                <Link to="/">
                    <a className="navbar-brand">
                        <img src={logo} alt="Logo" height="70px" />
                    </a>
                </Link>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div className="navbar-nav ms-auto">
                        <a className="nav-link" href="#features">Features</a>
                        <a className="nav-link" href="#pricing">Pricing</a>
                        <a className="nav-link" href="#about">About</a>
                    </div>
                </div>
            </div>
        </nav>
    );
}
