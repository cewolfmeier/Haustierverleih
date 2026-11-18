import React, { useCallback } from 'react';
import { UserContext } from './UserContext';
import { useMutation } from '@tanstack/react-query';
import { tokensQueries } from '../services/tokens/queries';


export default function UserProvider({ children }: React.PropsWithChildren<{}>) {
  	const currentUser = () => {
		const user = localStorage.getItem("currentUser") 
		if (user) return JSON.parse(user);
		return null;
	};
	const newToken = useMutation(tokensQueries.new());

	const login = useCallback(async (username: string, password: string) => {
		newToken.mutate({username:username, password:password});
	}, []);
/*
  const logout = useCallback(async () => {
    setUser(null);
    localStorage.removeItem("currentUser");
  }, [api]);*/

  return (
    <UserContext value={{ currentUser, login }}>
      {children}
    </UserContext>
  );
}

