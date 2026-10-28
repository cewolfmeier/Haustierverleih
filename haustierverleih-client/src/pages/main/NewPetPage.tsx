import type { animalType } from "../../Schemas";

interface NewPetPageProps{
    animalTypes:animalType[]
}

export default function NewPetPage({animalTypes}:NewPetPageProps){
    return(
        <>
        <h1>Neues Haustier anlegen</h1>
        <div className="detail shadow">
            <form action="{{url_for('main.post_new_pet')}}" method="post" encType="multipart/form-data">
                <label htmlFor="name">Name</label>
                <input type="text" name="Name" id="name" required />
                <label htmlFor="pet_description">Beschreibung</label>
                <input type="text" name="Beschreibung" id="pet_description" required />
                <label htmlFor="animal_type">Tierart</label>
                <select name="Tierart" id="animal_type">
                    {animalTypes.map(animalType => (<option value={animalType.animalTypeId}>{animalType.animalType}</option>))}
                </select>
                <label htmlFor="image">Foto-Upload</label>
                <input name="image" id="image" type="file" />
                <input className="button" type="submit" value="Tier anlegen" />
            </form>
        </div>
        </>
    );
};