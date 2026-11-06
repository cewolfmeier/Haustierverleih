import React, { createContext, useContext } from 'react';
import ApiClient from '../ApiClient';

const ApiContext = createContext<ApiClient | null>(null);

export default function ApiProvider({ children }: React.PropsWithChildren<{}>) {

  const api = new ApiClient();

  return (
    <ApiContext value={api}>
      {children}
    </ApiContext>
  );
}

export function useApi() {
  return useContext(ApiContext) as ApiClient;
}