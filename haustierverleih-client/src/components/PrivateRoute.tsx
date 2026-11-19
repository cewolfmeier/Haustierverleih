import type { PropsWithChildren } from 'react';
import { useUser } from '../contexts/UserContext';

export default function PrivateRoute({ children }: PropsWithChildren) {
	const { currentUser } = useUser();

	if (currentUser === undefined) {
		return null;
	} else if (currentUser) {
		return <>{children}</>;
	};
};
