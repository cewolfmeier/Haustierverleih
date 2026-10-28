import axios from "axios";

type Response<TRES> = {
  ok: boolean;
  status: number;
  body: TRES | null;
  errors: {json: any} | null;
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
        const { data } = await this.client.get(path);
        return data;
    }

};
/*
  async get<TRES>(url: string, query?: Query, options?: Options<null>): Promise<Response<TRES>> {
    return this.request<null, TRES>({method: 'GET', url, query, ...options});
  }*/
