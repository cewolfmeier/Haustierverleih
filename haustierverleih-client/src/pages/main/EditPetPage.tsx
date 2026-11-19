import { useState } from "react";
import type { AnimalType, Pet } from "../../Schemas";
import { useParams } from "react-router-dom";
import { Form } from "react-bootstrap";

export default function EditPetPage(){
    const { petId } = useParams<{ petId: string }>();
    const [animalTypes, setAnimalTypes] = useState<AnimalType[] | null | undefined>();
    const [pet, setPet] = useState<Pet | null | undefined>();

    const onSubmit = async (event: React.SubmitEvent) => {
        event.preventDefault(); //Note: prevents a reload of the page so Formdata doesn't get lost
        const formData = new FormData(event.target);
        formData.append("petId", petId?petId:"")
        await api.put<FormData, Pet>("/pets", formData,
        {
          'Content-Type': 'multipart/form-data',
        });
    }

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
                        <Form onSubmit={onSubmit} method="put" encType="multipart/form-data">
                            <label htmlFor="name">Name</label>
                            <input type="text" name="name" id="name" required value={pet.name}/>
                            <label htmlFor="description">Beschreibung</label>
                            <input type="text" name="description" id="description" value={pet.description} required />
                            <label htmlFor="animalType">Tierart</label>
                            <select name="Tierart" id="animalType">
                                {animalTypes?.map(animalType => (<option key={animalType.animalTypeId} value={animalType.animalTypeId} selected={pet.animalTypeId == animalType.animalTypeId ? true: false}>{animalType.animalType}</option>))}
                            </select>
                            <label htmlFor="image">Foto-Upload</label>
                            <input name="image" id="image" type="file" />
                            <input className="button" type="submit" value="Speichern" />
                        </Form>
                    </div>
                </>
            }
            </>
        } 
        </>
    );
};