import { Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useRef } from "react";
import { useUser } from "../../contexts/UserContext";

export default function LoginPage(){
    const user = useUser();
    const navigate = useNavigate()
    const usernameFieldRef = useRef<HTMLInputElement>(null);
    const passwordFieldRef = useRef<HTMLInputElement>(null);

    if (user) navigate("/");

    const onSubmit = async (event: React.SubmitEvent) => {
        if (!usernameFieldRef.current || !passwordFieldRef.current) return;
        event.preventDefault();
        user.login(
            usernameFieldRef.current.value,
            passwordFieldRef.current.value,
        )
    }

    return(
        <>
        <h1>Anmelden</h1>
        <Form onSubmit={onSubmit} method="post">
            <label htmlFor="username">Benutzername</label>
            <input type="text" name="Username" id="username" required ref={usernameFieldRef} />
            <label htmlFor="password">Passwort</label>
            <input type="password" name="Password" id="password" required ref={passwordFieldRef} />
            <input className="button-form" type="submit" value="Anmelden" />
        </Form>
        </>
    );
};