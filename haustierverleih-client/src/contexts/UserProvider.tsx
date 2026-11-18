import React, { useCallback } from 'react';
import { UserContext } from './UserContext';
import { useMutation } from '@tanstack/react-query';
import { tokensQueries } from '../services/tokens/queries';


export default function UserProvider({ children }: React.PropsWithChildren<{}>) {
	const user = localStorage.getItem("currentUser");
	const currentUser = user? JSON.parse(user): null;
	const newToken = useMutation(tokensQueries.new());
	const deleteToken = useMutation(tokensQueries.delete());

	const login = useCallback(async (username: string, password: string) => {
		newToken.mutate({username:username, password:password});
	}, []);

	const logout = useCallback(async () => {
    	deleteToken.mutate();
  	}, []);

  return (
    <UserContext value={{ currentUser, login, logout }}>
      {children}
    </UserContext>
  );
}
