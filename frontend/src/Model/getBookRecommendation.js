import UserProfile from "./userSession";
import { url } from "./constants";

export async function getBookRecommendation(prompt) {
    try {   
        let username = UserProfile.getName();
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
        if (response.status !== 200) {
            console.log(json);
            throw new Error("Could Not Get Recommendation")
        }

        return json;
    } catch(err) {
        console.log(err);
        throw new Error("Could Not Get Recommendation");
    }
}