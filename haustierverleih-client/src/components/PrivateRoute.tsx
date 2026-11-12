import type { PropsWithChildren } from 'react';
import { useUser } from '../contexts/UserContext';

export default function PrivateRoute({ children }: PropsWithChildren<{}>) {
  const { user } = useUser();

  if (user === undefined) {
    return null;
  }
  else if (user) {
    return <>{children}</>;
  }
}