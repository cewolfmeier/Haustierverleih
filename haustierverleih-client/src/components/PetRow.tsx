import type { pet } from "../Schemas";

interface PetRowProps{
    pet: pet
    isOwner: boolean
}

export default function PetRow({pet, isOwner}:PetRowProps){
    return(
        <tr>
            <td>{pet.name}</td>
            <td>{pet.animalTypeId}</td>
            {!isOwner?
                <>
                <td>{pet.ownerId}</td>
                <td>
                    <div>
                        <a className="button" href="{{ url_for('main.pet', pet_id=pet.pet_id) }}">Details</a>
                    </div>
                </td>
                </>
                :
                <>
                    <td>{pet.borrowerId && "nicht"}verfügbar</td>
                    <td>
                        <div>
                            <a className="button" href="{{ url_for('main.get_edit_pet', pet_id=pet.pet_id) }}">Bearbeiten</a> 
                            <button type="button" className="delete-pet btn btn-danger" data-bs-toggle="modal" data-bs-target="#modal" id="{{ pet.pet_id }}">
                                <i className="bi bi-trash-fill"></i>
                            </button>
                            <a className="button" href="{{ url_for('main.pet', pet_id=pet.pet_id) }}">Details</a>
                        </div>
                    </td>
                </>
            }
        </tr>
    );
};