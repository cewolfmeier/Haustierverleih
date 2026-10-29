import { useEffect, useState } from "react";
import PetRow from "../../components/PetRow";
import { useApi } from "../../contexts/ApiProvider";
import type { Pet } from "../../Schemas";

export default function PetManagementPage(){
    const api = useApi();
    const [ownedPets, setOwnedPets] = useState<Pet[] | null | undefined>();
    const [borrowedPets, setBorrowedPets] = useState<Pet[] | null | undefined>();

    useEffect(()=>{
        (async () => {
            const response = await api.get<Pet[]>("/me/pets");
            if (response.status == 200 && response.data) {
                setOwnedPets(response.data)
            } else {
                setOwnedPets(null);
            };
        })();
        (async () => {
            const response = await api.get<Pet[]>("/me/pets");
            if (response.status == 200 && response.data) {
                setBorrowedPets(response.data)
            } else {
                setBorrowedPets(null);
            };
        })();
    }, [api]);

    return(
        <>
            <div className="modal" tabIndex={-1} id="modal">
                <div className="modal-dialog">
                    <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Modal title</h5>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <p>Modal body text goes here.</p>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" className="btn btn-primary">Save changes</button>
                    </div>
                    </div>
                </div>
            </div>
            <h1>Tierverwaltung</h1>
            <div className="main-content">
                <p>
                    <strong>Deine eigenen Haustiere ({ownedPets?.length})</strong>
                    <a className="button" href="/mypets/new">+ Neues Haustier anlegen</a>
                </p>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Tierart</th>
                            <th>Verfügbarkeit</th>
                            <th>Aktionen</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ownedPets === undefined?
                            <p>Deine Haustiere konnten nicht geladen werden.</p>
                            :
                            <>
                            {ownedPets === null?
                                <p>Du hast noch keine Haustiere.</p>
                                :
                                ownedPets.map(pet=><PetRow key={pet.petId} pet={pet} isOwner={true}/>)
                            }
                            </>
                        }
                    </tbody>
                </table>
                </div>
                <div className="main-content">
                <p>
                    <strong>
                        Deine ausgeliehenen Haustiere ({borrowedPets?.length})
                    </strong>
                </p>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Tierart</th>
                            <th>Besitzer</th>
                            <th>Aktionen</th>
                        </tr>
                    </thead>
                    <tbody>
                        {borrowedPets === undefined?
                            <p>Deine ausgeliehenen Haustiere konnten nicht geladen werden.</p>
                            :
                            <>
                            {borrowedPets === null?
                                <p>Du hast aktuell keine Haustiere ausgeliehen.</p>
                                :
                                borrowedPets.map(pet=><PetRow key={pet.petId} pet={pet} isOwner={false}/>)
                            }
                            </>
                        }
                    </tbody>
                </table>
            </div>
        </>
    );
};