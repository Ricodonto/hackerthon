import { url } from "./constants";

export async function changeUsername(old_username, new_username) {
    try {   
        let formdata = new FormData();
        // let username = sessionStorage.getItem('username');
        formdata.append('old_username', old_username);
        formdata.append('new_username', new_username);
        let response = await fetch(
            `${url}/profile/changeusr`,
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
                throw new Error("Could Not Change Username")
            }
        }

        // return json;
    } catch(err) {
        console.log(err);
        throw(err);
    }
}