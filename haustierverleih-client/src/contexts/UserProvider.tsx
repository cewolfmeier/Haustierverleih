import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useApi } from './ApiProvider';
import { type User } from '../Schemas';

type UserContextType = {
  user: User | null | undefined;
  setUser: (user: User | null | undefined) => void;
  login: (username: string, password: string) => Promise<number|undefined>;
  logout: () => Promise<void>;
}

const UserContext = createContext<UserContextType | null>(null);

export default function UserProvider({ children }: React.PropsWithChildren<{}>) {
  const [user, setUser] = useState<User | null | undefined>();
  const api = useApi();
    /*
  useEffect(() => {
    (async () => {
      if (api.isAuthenticated()) {
        const response = await api.get<User>('/me');
        setUser(response.ok ? response.body : null);
      }
      else {
        setUser(null);
      }
    })();
  }, [api]);
*/
  const login = useCallback(async (username: string, password: string) => {
    const response = await api.login(username, password);
    if (response && response.status === 200) {
      const response = await api.get<User>('/me');
      setUser(response.status === 200 ? response.data : null);
    }
    return response?.status;
  }, [api]);

  const logout = useCallback(async () => {
    //await api.logout();
    setUser(null);
  }, [api]);

  return (
    <UserContext value={{ user, setUser, login, logout }}>
      {children}
    </UserContext>
  );
}

export function useUser() {
  return useContext(UserContext) as UserContextType;
}