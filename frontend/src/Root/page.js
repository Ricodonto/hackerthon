import { Outlet, Link } from "react-router-dom";
import './styles.css'

export default function Root() {
    return (
        <>
            {/* The Nav Bar At The Top */}
            <nav className="navbar">
                <h1 className="page-title">BookFinder</h1>
                <Links />
            </nav>
            {/* all the other elements */}
            <div id="detail" className="content">
                <Outlet />
            </div>
            {/* A footer */}
            <footer>
                <Links />
                <p>© 2023 BookFinder.</p>
            </footer>
        </>
    );
}

function Links() {
    return (
        <ul className="links">
            <li className="individual-link"><Link to={'home'}>Home</Link></li>
            <li className="individual-link"><Link to={'about'}>About</Link></li>
            <li className="individual-link"><Link to={'history'}>History</Link></li>
        </ul>
    );
}