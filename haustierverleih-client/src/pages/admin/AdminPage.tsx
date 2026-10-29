import { useEffect, useState } from "react";
import AnimalTypeRow from "../../components/admin/AnimalTypeRow";
import UserRow from "../../components/admin/UserRow";
import { useApi } from "../../contexts/ApiProvider";
import type { AnimalType, User } from "../../Schemas";


export default function AdminPage(){
    const api = useApi();
    const [animalTypes, setAnimalTypes] = useState<AnimalType[] | null | undefined>();
    const [users, setUsers] = useState<User[] | null | undefined>();

    useEffect(()=>{
        (async () => {
            const response = await api.get<AnimalType[]>("/animaltypes");
            if (response.ok && response.body) {
                setAnimalTypes(response.body)
            } else {
                setAnimalTypes(null);
            };
        })();
        (async () => {
            const response = await api.get<User[]>("/users");
            if (response.ok && response.body) {
                setUsers(response.body)
            } else {
                setUsers(null);
            };
        })();
    }, [api]);

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
                                <p>Benutzer konnten nicht geladen werden.</p>
                                :
                                <>
                                {users === null?
                                    <p>Es gibt noch keine Benutzer.</p>
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
                        <a className="button" href="{{url_for('admin.get_new_animal_type')}}">+ Neue Tierart anlegen</a>
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
                                <p>Tierarten konnten nicht geladen werden.</p>
                                :
                                <>
                                {animalTypes === null?
                                    <p>Es gibt noch keine Tierarten.</p>
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