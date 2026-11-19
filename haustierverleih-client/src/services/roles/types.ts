import { queryOptions } from "@tanstack/react-query";
import { actions } from "../api";

export const rolesQueries = {
    all: () => ["roles"] as const,
    one: () => ["role"] as const,
    list: () => 
        queryOptions({
            queryKey: [...rolesQueries.all(), "list"] as const,
            queryFn: () => actions.getAll("/roles")
        }),
    byId: (id: number|string) =>
        queryOptions({
            queryKey: [...rolesQueries.one(), "byId", id] as const,
            queryFn: () => actions.getById("/roles", id.toString())
        }),
};
