import type { animalType } from "../Schemas";

interface EditPetPageProps{
    animalTypes:animalType[],
    pet: {
        petId: number,
        name:string,
        description: string,
        image: string,
        animalTypeId: number,
        ownerId: number,
        borrowerId: number|null,
    },
}

export default function EditPetPage({animalTypes, pet}:EditPetPageProps){
    return(
        <>
        <h1>Haustier { pet.name } bearbeiten</h1>
        <div className="detail shadow">
            <form action="{{url_for('main.post_edit_pet', pet_id=pet.pet_id)}}" method="put" encType="multipart/form-data">
                <label htmlFor="name">Name</label>
                <input type="text" name="Name" id="name" required value={pet.name}/>
                <label htmlFor="pet_description">Beschreibung</label>
                <input type="text" name="Beschreibung" id="pet_description" value={pet.description} required />
                <label htmlFor="animal_type">Tierart</label>
                <select name="Tierart" id="animal_type">
                    {animalTypes.map(animalType => (<option value={animalType.animalTypeId} selected={pet.animalTypeId == animalType.animalTypeId ? true: false}>{animalType.animalType}</option>))}
                </select>
                <label htmlFor="image">Foto-Upload</label>
                <input name="image" id="image" type="file" />
                <input className="button" type="submit" value="Speichern" />
            </form>
        </div>
        </>
    );
};