import { Link } from "react-router-dom";
import '../Login/styles.css';

export default function SignUp() {
    return (
        <main>
            <h2>Register to your Bookfinder account</h2>
            <form className="login-form">
                <div className="email">
                    <label for="email-text-input" className="form-label">Email Address</label>
                    <input required type="text" id="email-text-input" name="username" placeholder="Username" className="form-input" />
                </div>
                <div className="password">
                    <label for="password-input" className="form-label">Password</label>
                    <input required type="password" id="password-input" name="password" placeholder="Password" className="form-input" />
                </div>
                <input class="login-button" className="login-button" type="submit" value="Register" />
            </form>
            <div style={{textAlign: "center"}}>
                <div className="redirect-to-login">
                    <p style={{display: "inline"}}>Already Have An Account, </p>
                    <Link to="/login" class="inline-link">Log In</Link>
                </div>
            </div>
        </main>
    );
}