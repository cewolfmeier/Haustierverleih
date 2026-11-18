import { createContext, useContext } from 'react';
import { type User } from '../Schemas';

export type UserContextType = {
	currentUser: User | null ;
	login: (username: string, password: string) => Promise<void>;
	logout: () => Promise<void>;
}

export const UserContext = createContext<UserContextType | null>(null);

export function useUser() {
  	return useContext(UserContext) as UserContextType;
}