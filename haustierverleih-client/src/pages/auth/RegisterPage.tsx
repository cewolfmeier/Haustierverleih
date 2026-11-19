import React, { useRef } from "react";
import { Form } from "react-bootstrap";
import type { NewUser, User } from "../../Schemas";
import { useNavigate } from "react-router-dom";


export default function RegisterPage(){
    const navigate = useNavigate()
    const usernameField = useRef<HTMLInputElement>(null);
    const passwordField = useRef<HTMLInputElement>(null);
    const passwordRepeatField = useRef<HTMLInputElement>(null);

    const onSubmit = async (event: React.SubmitEvent) => {
        event.preventDefault(); //Note: prevents a reload of the page so Formdata doesn't get lost
        if (passwordField.current?.value !== passwordRepeatField.current?.value) return;
        /*
        const response = await api.post<NewUser, User>("/users", 
            {
                username: usernameField.current ? usernameField.current.value : "",
                password: passwordField.current ? passwordField.current.value : "",
            }
        );
        if (response.status == 201) {
            navigate("/login")
        };
        */
    }

    return(  
        <>
        <h1>Registrieren</h1>
        <Form onSubmit={onSubmit}>
            <label htmlFor="username">Benutzername</label>
            <input type="text" name="Username" id="username" required ref={usernameField}/>
            <label htmlFor="password">Passwort</label>
            <input type="password" name="Password" id="password" required ref={passwordField}/>
            <label htmlFor="password-repeat">Passwort wiederholen</label>
            <input type="password" name="Password-Repeat" id="password-repeat" required ref={passwordRepeatField}/>
            <input className="button-form" type="submit" value="Registrieren" />
        </Form>
        </>
    );
};