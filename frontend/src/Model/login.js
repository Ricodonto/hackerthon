import { url } from "./constants";

export async function sendLoginDetails(username, password) {
    try {   
        let formdata = new FormData();
        formdata.append('username', username);
        formdata.append('password', password);
        let response = await fetch(
            `${url}/login`,
            {
                method: 'POST',
                body: formdata
            }
        );
        console.log("Fetch Completed!")
        let json = await response.json();
        if (response.status !== 200) {
            console.log(json);
            throw new Error("Could Not Log In")
        }

        sessionStorage.setItem('username', username)
    } catch(err) {
        console.log(err);
        throw new Error("Could Not Log In");
    }
}