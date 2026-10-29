import { useEffect, useState } from "react";
import { useApi } from "../../contexts/ApiProvider";
import type { AnimalType } from "../../Schemas";
import { useParams } from "react-router-dom";


export default function EditAnimalTypePage(){
    const { animalTypeId } = useParams<{ animalTypeId: string }>();
    const api = useApi();
    const [animalType, setAnimalType] = useState<AnimalType | null | undefined>();

    useEffect(()=>{
        (async () => {
            const response = await api.get<AnimalType>("/animaltypes/"+animalTypeId);
            if (response.ok && response.body) {
                setAnimalType(response.body)
            } else {
                setAnimalType(null);
            };
        })();
    }, [api]);

    return(
        <>
        {animalType === undefined?
            <p>Tierart lädt...</p>
            :
            <>
            {
                animalType === null?
                <p>Tierart nicht gefunden.</p>
                :
                <>
                    <h1>Tierart {animalType.animalType} bearbeiten</h1>
                    <form action="{{url_for('admin.post_edit_animal_type', animal_type_id=animal_type['animal_type_id'])}}" method="put">
                        <label htmlFor="animal_type">Bezeichnung</label>
                        <input type="text" name="name" id="animal_type" value="{{ animal_type['animal_type']}}" required />
                        <input className="button-form" type="submit" value="Speichern" />
                    </form>
                </>
            }
            </>
        }
        </>
    );
};