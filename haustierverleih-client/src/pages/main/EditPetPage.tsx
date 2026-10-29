import { useEffect, useState } from "react";
import { useApi } from "../../contexts/ApiProvider";
import type { AnimalType, Pet } from "../../Schemas";
import { useParams } from "react-router-dom";

export default function EditPetPage(){
    const { petId } = useParams<{ petId: string }>();
    const api = useApi();
    const [animalTypes, setAnimalTypes] = useState<AnimalType[] | null | undefined>();
    const [pet, setPet] = useState<Pet | null | undefined>();

    useEffect(()=>{
        (async () => {
            const response = await api.get<Pet>("/me/pets/"+petId);
            if (response.status == 200 && response.data) {
                setPet(response.data)
            } else {
                setPet(null);
            };
        })();
        (async () => {
            const response = await api.get<AnimalType[]>("/animaltypes");
            if (response.status == 200 && response.data) {
                setAnimalTypes(response.data)
            } else {
                setAnimalTypes(null);
            };
        })();
    }, [api]);

    return(
        <>
        {pet === undefined?
            <p>Haustier lädt...</p>
            :
            <>
            {
                pet === null?
                <p>Haustier nicht gefunden.</p>
                :
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
                                {animalTypes?.map(animalType => (<option value={animalType.animalTypeId} selected={pet.animalTypeId == animalType.animalTypeId ? true: false}>{animalType.animalType}</option>))}
                            </select>
                            <label htmlFor="image">Foto-Upload</label>
                            <input name="image" id="image" type="file" />
                            <input className="button" type="submit" value="Speichern" />
                        </form>
                    </div>
                </>
            }
            </>

        }
        
        </>
    );
};