export default function RegisterPage(){
    return(
        <>
        <h1>Registrieren</h1>
        <form action="{{url_for('auth.register')}}" method="post">
            <label htmlFor="username">Benutzername</label>
            <input type="text" name="Username" id="username" required />
            <label htmlFor="password">Passwort</label>
            <input type="password" name="Password" id="password" required />
            <label htmlFor="password-repeat">Passwort wiederholen</label>
            <input type="password" name="Password-Repeat" id="password-repeat" required />
            <input className="button-form" type="submit" value="Registrieren" />
        </form>
        </>
    );
};