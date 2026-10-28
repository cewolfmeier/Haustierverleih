import AnimalTypeRow from "../../components/admin/AnimalTypeRow";
import UserRow from "../../components/admin/UserRow";
import type { AnimalType, User } from "../../Schemas";

interface AdminPageProps{
    animalTypes:AnimalType[],
    users:User[],
}

export default function AdminPage({animalTypes, users}:AdminPageProps){
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
                            {users.map(user=><UserRow key={user.userId} user={user}/>)}
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
                            {animalTypes.map(animalType=><AnimalTypeRow key={animalType.animalTypeId} animalType={animalType}/>)}
                        </tbody>
                    </table>
            </div>
        </>
    );
};