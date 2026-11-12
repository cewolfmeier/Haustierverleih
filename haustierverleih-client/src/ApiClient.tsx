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
  async login(username: string, password: string): Promise<'ok' | 'fail' | 'error'> {
    const response = await this.post<null, Token>('/tokens', null, {
      headers: {
        Authorization:  'Basic ' + btoa(username + ":" + password)
      }
    });
    if (!response.ok || !response.body) {
      return response.status === 401 ? 'fail' : 'error';
    }
    localStorage.setItem('accessToken', response.body.access_token || '');
    return 'ok';
  }

  async logout() {
    await this.delete('/tokens');
    localStorage.removeItem('accessToken');
  }

  isAuthenticated() {
    return localStorage.getItem('accessToken') !== null;
  }*/