import { url } from "./constants";

export async function getBookRecommendation(prompt) {
    try {   
        let username = sessionStorage.getItem('username');
        console.log(username);
        let formdata = new FormData();
        formdata.append('username', username);
        formdata.append('prompt', prompt);
        let response = await fetch(
            `${url}/`,
            {
                method: 'POST',
                body: formdata
            }
        );
        console.log("Fetch Completed!")
        let json = await response.json();
        console.log("JSON IS: ")
        
        if (response.status !== 200) {
            console.log(json);
            if (json['error'] !== null) {
                console.log(10)
                throw new Error(json['error'])
            } else {
                throw new Error("Could Not Get Recommendation")
            }
        }
        return json;
    } catch(err) {
        console.log(err);
        throw(err);
    }
}