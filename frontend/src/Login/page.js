import { Link } from "react-router-dom";
import './styles.css';

export default function Login() {
    return (
        <main>
            <h2>Sign into your Bookfinder account</h2>
            <form className="login-form">
                <div className="email">
                    <label for="email-text-input" className="form-label">Email Address</label>
                    <input required type="text" id="email-text-input" name="username" placeholder="Username" className="form-input" />
                </div>
                <div className="password">
                    <label for="password-input" className="form-label">Password</label>
                    <input required type="password" id="password-input" name="password" placeholder="Password" className="form-input" />
                </div>
                <input className="login-button" type="submit" value="Login" />
            </form>
            <div style={{textAlign: "center"}}>
                <div className="redirect-to-login">
                    <p style={{display: "inline"}}>Don't Have An Account, </p>
                    <Link to="/signup" className="inline-link">Sign Up</Link>
                </div>
            </div>
        </main>
    );
}