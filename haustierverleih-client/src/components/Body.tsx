import type { PropsWithChildren } from "react";

export default function Body({children}: PropsWithChildren) {
    return(
        <div>
            {children}
        </div>
    );
};