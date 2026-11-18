import { useUser } from "../contexts/UserContext";


export default function Header(){
    const {currentUser, logout} = useUser();
    return (
        <header className="shadow">
            <nav>
                <a href="/">
                    <img src="/logo.png" alt="Das Logo des Haustierverleihs" /> 
                </a>
                <ul className="navigation">
                    {currentUser ?
                        <>
                            <li>
                                <div>Moin {currentUser.username} !</div>
                            </li>
                            <li>
                                <a className="button" href="/me/edit">Profil bearbeiten</a>
                            </li>
                            <li>
                                <a className="button" href="/mypets">Meine Tiere</a>
                            </li>
                            { currentUser.isAdmin &&
                            <li>
                                <a className="button" href="/admin">Admin Bereich</a>
                            </li>
                            }
                            <li>
                                <a className="button" onClick={logout}>Ausloggen</a> 
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
                </ul> 
            </nav>
        </header>
    )
}