import type { PropsWithChildren } from 'react';
import { useUser } from '../contexts/UserContext';

export default function PrivateRoute({ children }: PropsWithChildren<{}>) {
	const { currentUser } = useUser();
	const user = currentUser();

	if (user === undefined) {
		return null;
	} else if (user) {
		return <>{children}</>;
	};
};
