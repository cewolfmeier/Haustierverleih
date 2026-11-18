import axios from "axios";

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
        return await api.post("/tokens", {},
            {
                headers:{
                    Authorization:  'Basic ' + btoa(credentials.username + ":" + credentials.password)
                },
            });
    },
    logout : async<TRES>(): Promise<Response<TRES>> => {
        return await api.delete("/tokens");
    },
};
