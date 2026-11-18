import { queryOptions } from "@tanstack/react-query";
import { actions } from "../api";
import type { Pet } from "./types";

export const petsQueries = {
    all: () => ["pets"] as const,
    list: () => 
        queryOptions({
            queryKey: [...petsQueries.all(), "list"] as const,
            queryFn: () => actions.getAll<Pet[]>("/pets")
        }),
}