import { useEffect, type PropsWithChildren } from 'react';
import { useUser } from '../contexts/UserContext';
import { useNavigate } from 'react-router-dom';

export default function ProtectedRoute({ children }: PropsWithChildren<{}>) {
  const { user } = useUser();
  const navigate = useNavigate();

  useEffect(()=>{
    if (!user?.isAdmin) navigate("/")
  });

  if (!user || !user.isAdmin) {
    return null;
  } else {
    return <>{children}</>;
  }
}