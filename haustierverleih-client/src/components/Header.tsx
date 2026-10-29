import { useMeApiCall } from "../hooks/ApiHooks";


export default function Header(){
    const user = useMeApiCall();

    return (
        <header className="shadow">
            <nav>
                <a href="/">
                    <img src="/logo.png" alt="Das Logo des Haustierverleihs" /> 
                </a>
                <ul className="navigation">
                    {user ?
                        <>
                            <li>
                                <div>Moin {user.username} !</div>
                            </li>
                            <li>
                                <a className="button" href="/me/edit">Profil bearbeiten</a>
                            </li>
                            <li>
                                <a className="button" href="/mypets">Meine Tiere</a>
                            </li>
                            <li>
                                <a className="button" href="/admin">Admin Bereich</a>
                            </li>
                        </>
                    : 
                        <>
                            <li>
                                <a className="button" href="/register">Registrieren</a>
                            </li>
                            <li>
                                <a className="button" href="/login">Einloggen</a>
                            </li>
                        </>
                    }                    
                    <li>
                        <a className="button" href="{{ url_for('auth.logout') }}">Ausloggen</a> 
                    </li>
                </ul> 
            </nav>
        </header>
    )
}