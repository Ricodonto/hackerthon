import { url } from "./constants";

export async function changePassword(old_password, new_password, confirm_new, username) {
    try {   
        let formdata = new FormData();
        // let username = sessionStorage.getItem('username');
        formdata.append('old_password', old_password);
        formdata.append('new_password', new_password);
        formdata.append('confirm_new', confirm_new);
        formdata.append('username', username);
        let response = await fetch(
            `${url}/profile/changepwd`,
            {
                method: 'POST',
                body: formdata
            }
        );
        console.log("Fetch Completed!")
        let json = await response.json();
        console.log("JSON IS: ")
        console.log(json)
        if (response.status !== 200) {
            console.log(json);
            if (json['error'] !== null) {
                console.log(10)
                throw new Error(json['error'])
            } else {
                throw new Error("Could Not Change Password")
            }
        }

        // return json;
    } catch(err) {
        console.log(err);
        throw(err);
    }
}