import { Link } from "react-router-dom";
import '../Login/styles.css';
import { useState } from "react";
import { signup } from "../Model/singup";

export default function SignUp() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();
        try {
            console.log(1)
            await signup(username, password);
            console.log(2)
        } catch (err) {
            console.log(3)
            console.log(err)
            setError(true);
            console.log(err.message);
            setErrorMessage(err.message);
        }
    }

    return (
        <div>
            <h2>Register to your Bookfinder account</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <div className="email">

                    {error === true
                        ?
                        <>
                            <label for="email-text-input" className="form-label-error">Username</label>
                            <input
                                required
                                type="text"
                                id="email-text-input"
                                placeholder="Username"
                                className="form-input-error"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </>
                        : <>
                            <label for="email-text-input" className="form-label">Username</label>
                            <input
                                required
                                type="text"
                                id="email-text-input"
                                placeholder="Username"
                                className="form-input"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </>
                    }
                </div>
                <div className="password">
                    {error === true
                        ? <>
                            <label for="password-input" className="form-label-error">Password</label>
                            <input
                                required
                                type="password"
                                id="password-input"
                                placeholder="Password"
                                className="form-input-error"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </>
                        : <>
                            <label for="password-input" className="form-label">Password</label>
                            <input
                                required
                                type="password"
                                id="password-input"
                                placeholder="Password"
                                className="form-input"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </>
                    }
                </div>
                <input className="login-button" type="submit" value="Register" />
                {
                    error === true
                    ? <p className="error-message">{errorMessage}</p>
                    : <></>
                }
            </form>
            <div style={{textAlign: "center"}}>
                <div className="redirect-to-login">
                    <p style={{display: "inline"}}>Already Have An Account, </p>
                    <Link to="/login" class="inline-link">Log In</Link>
                </div>
            </div>
        </div>
    );
}