import { useEffect, useState } from "react";
import { useMeApiCall } from "../hooks/ApiHooks";
import type { Me } from "../Schemas";

export default function Header(){
    const [user, setUser] = useState<Me|undefined>();
    const userCall = useMeApiCall();

    useEffect(()=>{
        setUser(userCall);
    },[userCall]);

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
                                <a className="button" href="/">Profil bearbeiten</a>
                            </li>
                            <li>
                                <a className="button" href="/">Meine Tiere</a>
                            </li>
                            <li>
                                <a className="button" href="/">Admin Bereich</a>
                            </li>
                        </>
                    : 
                        <>
                            <li>
                                <a className="button" href="/">Registrieren</a> {/* href="{{ url_for('auth.register') }}"*/}
                            </li>
                            <li>
                                <a className="button" href="/">Einloggen</a>  {/*href="{{ url_for('auth.login') }}" */}
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