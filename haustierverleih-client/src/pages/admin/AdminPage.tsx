import { useState } from "react";
import AnimalTypeRow from "../../components/admin/AnimalTypeRow";
import UserRow from "../../components/admin/UserRow";
import type { AnimalType, User } from "../../Schemas";


export default function AdminPage(){
    const [animalTypes, setAnimalTypes] = useState<AnimalType[] | null | undefined>();
    const [users, setUsers] = useState<User[] | null | undefined>();

    return(
        <>
            <h1>Verwaltung</h1>
            <div className="main-content">
                    <p>
                        <strong>Benutzer</strong>
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>Benutzername</th>
                                <th>Rolle</th>
                                <th>Aktionen</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users === undefined?
                                <tr><td>Benutzer konnten nicht geladen werden.</td></tr>
                                :
                                <>
                                {users === null?
                                    <tr><td>Es gibt noch keine Benutzer.</td></tr>
                                    :
                                    users.map(user=><UserRow key={user.userId} user={user}/>)
                                }
                                </>
                            }
                        </tbody>
                    </table>
                    </div>
                    <div className="main-content">
                    <p>
                        <strong>Tierarten</strong>
                        <a className="button" href="/admin/animaltypes/new">+ Neue Tierart anlegen</a>
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>Tierart</th>
                                <th>Aktionen</th>
                            </tr>
                        </thead>
                        <tbody>
                            {animalTypes === undefined?
                                <tr><td>Tierarten konnten nicht geladen werden.</td></tr>
                                :
                                <>
                                {animalTypes === null?
                                    <tr><td>Es gibt noch keine Tierarten.</td></tr>
                                    :
                                    animalTypes.map(animalType=><AnimalTypeRow key={animalType.animalTypeId} animalType={animalType}/>)
                                }
                                </>
                            }
                        </tbody>
                    </table>
            </div>
        </>
    );
};