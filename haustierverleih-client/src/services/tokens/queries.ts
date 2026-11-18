import { mutationOptions } from "@tanstack/react-query";
import { actions } from "../api";
import type { User } from "./types";


export const tokensQueries = {
    all: () => ["accessToken"] as const,
    new: () =>
        mutationOptions({
            mutationFn: actions.login<User>,
            onSuccess: (response)=> localStorage.setItem("currentUser", JSON.stringify(response.data)),
        }),
};