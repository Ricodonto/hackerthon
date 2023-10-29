import { Link } from "react-router-dom";
import './styles.css';
import { sendLoginDetails } from "../Model/login";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    let navigate = useNavigate();

    async function handleSubmit(event) {
        event.preventDefault();
        try {
            console.log(1)
            await sendLoginDetails(username, password);
            console.log(2)
            navigate('/')
        } catch (err) {
            console.log(3)
            console.log(err)
            setError(true);
            console.log(err.message);
            setErrorMessage(err.message);
        }
    }


    return (
        <div className="content-page">
            <h2>Sign into your Bookfinder account</h2>
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
                <input className="login-button" type="submit" value="Login" />
                {
                    error === true
                    ? <p className="error-message">{errorMessage}</p>
                    : <></>
                }
            </form>
            <div style={{ textAlign: "center" }}>
                <div className="redirect-to-login">
                    <p style={{ display: "inline" }}>Don't Have An Account, </p>
                    <Link to="/signup" className="inline-link">Sign Up</Link>
                </div>
            </div>
        </div>
    );
}