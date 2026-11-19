import { queryOptions } from "@tanstack/react-query";
import { actions } from "../api";

export const usersQueries = {
    all: () => ["users"] as const,
    one: () => ["user"] as const,
    list: () => 
        queryOptions({
            queryKey: [...usersQueries.all(), "list"] as const,
            queryFn: () => actions.getAll("/users")
        }),
    byId: (id: number|string) =>
        queryOptions({
            queryKey: [...usersQueries.one(), "byId", id] as const,
            queryFn: () => actions.getById("/users", id.toString())
        }),
};
