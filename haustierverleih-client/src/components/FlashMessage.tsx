import { useContext } from "react";
import { FlashContext, type FlashContextType } from "../contexts/FlashProvider";

export default function FlashMessage(){
    const { flashMessage, visible, hideFlash } = useContext(FlashContext) as FlashContextType
    return (
        <div>
            <div className="alert alert-{{ category }}">
                { flashMessage.message }
            </div>
        </div>
    );
}