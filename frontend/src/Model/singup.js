import { url } from "./constants";

export async function signup(username, password) {
    try {   
        let formdata = new FormData();
        formdata.append('username', username);
        formdata.append('password', password);
        let response = await fetch(
            `${url}/signup`,
            {
                method: 'POST',
                body: formdata
            }
        );
        console.log("Fetch Completed!")
        let json = await response.json();
        if (response.status !== 200) {
            console.log(json);
            throw new Error("Could Not Register Account")
        }

        sessionStorage.setItem('username', username)
    } catch(err) {
        console.log(err);
        throw new Error("Could Not Register Account");
    }
}