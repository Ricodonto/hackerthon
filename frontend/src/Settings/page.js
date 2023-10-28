import { MyButton } from "../Home/page";

export default function Settings() {
    return (
        <>
            {/* Heading */}
            <h2>Manage your account</h2>
            {/* Username */}
            <section>
                <form>
                    <div>
                        <h3>Username</h3>
                        <button type="submit">Change</button>
                    </div>
                    <input 
                        placeholder="New Username"
                        type="text"
                        required
                    />
                </form>
            </section>
            {/* Password */}
            <section>
                <form>
                    <div>
                        <h3>Password</h3>
                        <button type="submit">Change</button>
                    </div>
                    <input 
                        placeholder="Old Password"
                        type="password"
                        required
                    />
                    <input 
                        placeholder="New Password"
                        type="password"
                        required
                    />
                    <input 
                        placeholder="Confirm Password"
                        type="password"
                        required
                    />
                </form>
            </section>
            <MyButton 
                text={"Delete Account"} 
                handleClick={() => console.log("Account Deleted")}
            />
        </>
    );
}