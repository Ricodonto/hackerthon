import { MyButton } from "../Home/page";
import './styles.css';

export default function Settings() {
    return (
        <div className="settings-page">
            {/* Heading */}
            <h2 className="settings-h2">Manage your account</h2>
            {/* Username */}
            <div style={{backgroundColor: "#D9D9D9"}}>
                <section>
                    <form className="settings-form">
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
                                required
                            />
                        </div>
                    </form>
                </section>
                {/* Password */}
                <section>
                    <form className="settings-form">
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
                                required
                            />
                        </div>
                        <div className="settings-input-block">
                            <label for="confirm-password">Confirm Password</label>
                            <input
                                id="confirm-password"
                                placeholder="Confirm Password"
                                type="password"
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