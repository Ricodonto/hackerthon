import { url } from "./constants";

export async function badFeedback(username, prompt_id) {
    try {   
        let formdata = new FormData();
        formdata.append('username', username);
        formdata.append('prompt_id', prompt_id);
        let response = await fetch(
            `${url}/feedback/bad`,
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
                throw new Error("Could Not Give Feedback")
            }
        }

        return json;
    } catch(err) {
        console.log(err);
        throw(err);
    }
}