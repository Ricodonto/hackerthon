import { Outlet, Link } from "react-router-dom";
import './styles.css'

export default function Root() {
    return (
        <body className="root">
            {/* The Nav Bar At The Top */}
            <div className="navbar">
                <UserImage initial={'R'} name={'Roman Njoroge'} />
                <h1 className="page-title">BookFinder</h1>
            </div>
            <Links />
            {/* all the other elements */}
            <Outlet />
            {/* A footer */}
            <footer>
                <p>© 2023 BookFinder.</p>
            </footer>
        </body>
    );
}

function Links() {
    return (
        <div className="links">
            <Link to={'/'} className="link"><LinkBox text={'Home'} /></Link>
            <Link to={'about'} className="link"><LinkBox text={'About'} /></Link>
            <Link to={'history'} className="link"><LinkBox text={'History'} /></Link>
        </div>
    );
}

function LinkBox(props) {
    return (
        <div className="linkbox">
            <p className="linktext">{props.text}</p>
        </div>
    )
}

function UserImage(props) {
    return (
        <div className="user-portion">
            <div className="user-initial">
                <p>{props.initial}</p>
            </div>
            <p>Hello, {props.name}</p>
        </div>
    )
}