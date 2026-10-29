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

export default class ApiClient{
    client = axios.create({
        baseURL: import.meta.env.VITE_API_URL,
        headers: {
            'Content-Type': 'application/json',
        },
        timeout: 1000,
    });

    async get<TRES>(path:string): Promise<Response<TRES>> {
        return await this.client.get(path);
    }

    async post<TREQ, TRES>(path:string, body:TREQ): Promise<Response<TRES>> {
        return await this.client.post(path, body);
    }

};
