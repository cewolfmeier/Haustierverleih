import { Form } from "react-bootstrap";
import { useApi } from "../../contexts/ApiProvider";
import { useNavigate } from "react-router-dom";
import { useUser } from "../../contexts/UserProvider";
import { useRef } from "react";

export default function LoginPage(){
    const api = useApi();
    const user = useUser();
    const navigate = useNavigate()
    const usernameFieldRef = useRef<HTMLInputElement>(null);
    const passwordFieldRef = useRef<HTMLInputElement>(null);

    const onSubmit = async (event: React.SubmitEvent) => {
        if (!usernameFieldRef.current || !passwordFieldRef.current) return;
        event.preventDefault();
        user.login(
            usernameFieldRef.current.value,
            passwordFieldRef.current.value,
        )
        const formData = new FormData(event.target);
        const response = await api.post("/login", formData, {
          'Content-Type': 'multipart/form-data',
        });
        console.log(response)
        if (response.status === 200) {
            navigate("/")
        }
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