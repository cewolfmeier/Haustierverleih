import axios from "axios";

export default class ApiClient{
    client = axios.create({
        baseURL: "http://localhost:5000/api/v0",
        timeout: 1000,
    });
    constructor(){
        
    }

    async get(path:string){
        this.client.get(path)
        .then((response) => {
            console.log(response.data);
        })
        .catch((error) => {
            console.error(error);
        });
    };
};

