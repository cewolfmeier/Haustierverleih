import axios, { type AxiosInstance, type AxiosResponse } from "axios";

type Response<TRES> = {
  statusText: string;
  status: number;
  data: TRES | null;
  errors: {json: any} | null;
}

type Request<TREQ> = {
    data: TREQ | null;
}

type Credentials = {
    username:string;
    password:string;
}

export const api = axios.create({
    withCredentials: true,
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 1000,
});

export const actions = {
    getAll : async<TRES>(path:string): Promise<Response<TRES>> => {
        const {data} = await api.get(path);
        return data
    },
    getById : async (path:string, id:string) => {
        return await api.get(path+"/"+id);
    },
    login : async<TRES>(credentials:Credentials): Promise<Response<TRES>> => {
        return await api.post("/login", {},
            {
                headers:{
                    Authorization:  'Basic ' + btoa(credentials.username + ":" + credentials.password)
                },
            });
    }
}



export default class ApiClient{
    client:AxiosInstance
    constructor(){
        this.client = axios.create({
            withCredentials: true,
            baseURL: import.meta.env.VITE_API_URL,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 1000,
        });

        this.client.interceptors.response.use(
            (response: AxiosResponse<any>) =>{
                console.log("got response")
                const config = response?.config
                if (config.raw) {
                    return response
                }
                if (response.status == 200) {
                    const data = response?.data
                    if (!data) {
                        console.log("No data")
                    //throw new HttpError('API Error. No data!')
                    }
                    return data
                }
                console.log("invalid status code")
                //throw new HttpError('API Error! Invalid status code!')
            },

            (response) =>{
                console.log("got error")
                const config = response?.config
                if (config.raw) {
                    console.log(response)
                    //return response
                }
                //console.log(response)
                // the code of this function was written in above section.
                //return httpErrorHandler(response)
            }

        );
    };
    async get<TRES>(path:string): Promise<Response<TRES>> {
        return await this.client.get(path, {raw:true});
    }

    async post<TREQ, TRES>(path:string, body:TREQ, headers={'Content-Type': 'application/json'}): Promise<Response<TRES>> {
        return await this.client.post(path, body, {headers:headers});
    }

    async put<TREQ, TRES>(path:string, body:TREQ, headers={'Content-Type': 'application/json'}): Promise<Response<TRES>> {
        return await this.client.put(path, body, {headers:headers});
    }

    async login<TRES>(username:string, password:string):Promise<Response<TRES>>{
        return await this.client.post(
            "/login",
            {},
            {
                headers:{
                    Authorization:  'Basic ' + btoa(username + ":" + password)
                },
            }
        );
    }

};
/*
  async logout() {
    await this.delete('/tokens');
    localStorage.removeItem('accessToken');
  }
*/