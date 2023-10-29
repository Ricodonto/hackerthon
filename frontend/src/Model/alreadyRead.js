import { url } from "./constants";

export async function alreadyReading(olusr) {
    try {   
        let formdata = new FormData();
        let username = sessionStorage.getItem('username');
        formdata.append('username', username);
        formdata.append('olusr', olusr);
        let response = await fetch(
            `${url}/already_read`,
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
                throw new Error("Could Not Get Already Read Books")
            }
        }

        return json;
    } catch(err) {
        console.log(err);
        throw(err);
    }
}