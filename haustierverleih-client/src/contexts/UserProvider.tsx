import React, { useState, useCallback } from 'react';
import { useApi } from './ApiProvider';
import { type User } from '../Schemas';
import { UserContext } from './UserContext';


export default function UserProvider({ children }: React.PropsWithChildren<{}>) {
  const [user, setUser] = useState<User | null | undefined>();
  const api = useApi();

  const login = useCallback(async (username: string, password: string) => {
    const response = await api.login<User>(username, password);
    if (response && response.status === 200) {
      setUser(response.data);
    }
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

