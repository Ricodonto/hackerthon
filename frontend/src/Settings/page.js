import { MyButton } from "../Home/page";
import './styles.css';
import { changeUsername } from "../Model/changeUsername";
import { changePassword } from "../Model/changePassword";
import { useState } from "react";
import ErrorWidget from "../Components/errorWidget";
import LoadingScreen from "../Components/loadingScreen";

export default function Settings() {
    const [new_username, setNewUsername] = useState("");
    const [new_password, setNewPassword] = useState("");
    const [old_password, setOldPassword] = useState("");
    const [confirm_new, setConfirmNew] = useState("");
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [loadingMessage, setLoadingMessage] = useState("");

    async function handleChangeUsername(event) {
        event.preventDefault();
        // Call function with arguements
        let old_username = sessionStorage.getItem('username');
        if (old_username.length === 0) {
            // Call not logged in error
            setError(true)
            setErrorMessage("Not Logged In")
        }
        try {
            // Set loading to true
            setLoading(true)
            setLoadingMessage("Changing Username")
            // Call function
            await changeUsername(old_username, new_username);
            sessionStorage.setItem('username', new_username)
            // Set loading to false
            setLoading(false)
            setLoadingMessage("")
        } catch(err) {
            // Update stata
            setError(true)
            setErrorMessage(err.message)
        }
    }

    async function handleChangePassword(event) {
        event.preventDefault();
        // Call function with arguements
        let username = sessionStorage.getItem('username');
        if (username.length === 0) {
            // Call not logged in error
            setError(true)
            setErrorMessage("Not Logged In")
        }
        try {
            // Set loading to true
            setLoading(true)
            setLoadingMessage("Changing Password")
            // Call function
            await changePassword(old_password, new_password, confirm_new, username)
            // Set loading to false
            setLoading(false)
            setLoadingMessage("")
        } catch(err) {
            // Update stata
            setError(true)
            setErrorMessage(err.message)
        }
    }

    if (error === true) {
        return <ErrorWidget message={errorMessage} />
    } else if(loading === true) {
        return <LoadingScreen message={loadingMessage} />
    } else {
        return (
            <div className="settings-page">
                {/* Heading */}
                <h2 className="settings-h2">Manage your account</h2>
                {/* Username */}
                <div style={{backgroundColor: "#D9D9D9"}}>
                    <section>
                        <form className="settings-form" onSubmit={handleChangeUsername}>
                            <div className="settings-form-header">
                                <h3>Username</h3>
                                <button className='linkbox' type="submit">Change</button>
                            </div>
                            <div className="settings-input-block">
                                <label for="new-username">New Username</label>
                                <input
                                    id="new-username"
                                    placeholder="New Username"
                                    type="text"
                                    className="settings-input"
                                    value={new_username}
                                    onChange={(e) => setNewUsername(e.target.value)}
                                    required
                                />
                            </div>
                        </form>
                    </section>
                    {/* Password */}
                    <section>
                        <form className="settings-form" onSubmit={handleChangePassword}>
                            <div className="settings-form-header">
                                <h3>Password</h3>
                                <button className='linkbox' type="submit">Change</button>
                            </div>
                            <div className="settings-input-block">
                                <label for="old-password">Old Password</label>
                                <input
                                    id="old-password"
                                    placeholder="Old Password"
                                    type="password"
                                    className="settings-input"
                                    value={old_password}
                                    onChange={(e) => setOldPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="settings-input-block">
                                <label for="new-password">New Password</label>
                                <input
                                    id="new-password"
                                    placeholder="New Password"
                                    type="password"
                                    className="settings-input"
                                    value={new_password}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="settings-input-block">
                                <label for="confirm-password">Confirm Password</label>
                                <input
                                    id="confirm-password"
                                    placeholder="Confirm Password"
                                    type="password"
                                    value={confirm_new}
                                    onChange={(e) => setConfirmNew(e.target.value)}
                                    className="settings-input"
                                    required
                                />
                            </div>
                        </form>
                    </section>
                </div>
                <MyButton
                    text={"Delete Account"}
                    handleClick={() => console.log("Account Deleted")}
                />
            </div>
        );
    }
}