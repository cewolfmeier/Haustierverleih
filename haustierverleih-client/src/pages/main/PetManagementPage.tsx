import PetRow from "../../components/PetRow";
import type { Pet } from "../../Schemas";

interface PetManagementPage{
    ownedPets:Pet[],
    borrowedPets:Pet[],
}

export default function PetManagementPage({ownedPets, borrowedPets}:PetManagementPage){
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
                    <strong>Deine eigenen Haustiere ({ownedPets.length})</strong>
                    <a className="button" href="{{ url_for('main.get_new_pet') }}">+ Neues Haustier anlegen</a>
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
                        {ownedPets.map(pet=><PetRow key={pet.petId} pet={pet} isOwner={true}/>)}
                    </tbody>
                </table>
                </div>
                <div className="main-content">
                <p>
                    <strong>
                        Deine ausgeliehenen Haustiere ({borrowedPets.length})
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
                        {borrowedPets.map(pet=><PetRow key={pet.petId} pet={pet} isOwner={false}/>)}
                    </tbody>
                </table>
            </div>
        </>
    );
};