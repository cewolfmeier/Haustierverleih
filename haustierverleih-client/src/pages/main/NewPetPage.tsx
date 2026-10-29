import { useEffect, useRef, useState } from "react";
import { useApi } from "../../contexts/ApiProvider";
import type { AnimalType, NewPet, Pet } from "../../Schemas";
import { Form } from "react-bootstrap";

export default function NewPetPage(){
    const api = useApi();
    const [animalTypes, setAnimalTypes] = useState<AnimalType[] | null | undefined>();
    const nameField = useRef<HTMLInputElement>(null);
    const descriptionField = useRef<HTMLInputElement>(null);
    const animalTypeField = useRef<HTMLInputElement>(null);
    const pictureField = useRef<HTMLInputElement>(null);
    //const formData = new FormData();

    useEffect(()=>{
        (async () => {
            const response = await api.get<AnimalType[]>("/animaltypes");
            if (response.status === 200 && response.data) {
                setAnimalTypes(response.data)
            } else {
                setAnimalTypes(null);
            };
        })();
    }, [api]);

    const onSubmit = async (event: React.SubmitEvent) => {
        event.preventDefault(); //Note: prevents a reload of the page so Formdata doesn't get lost
        await api.post<NewPet, Pet>("/animaltypes", 
            {   
                name: nameField.current ? nameField.current.value : "",
                description: descriptionField.current ? descriptionField.current.value : "",
                animalTypeId: animalTypeField.current ? parseInt(animalTypeField.current.value) : null,
                image: pictureField.current ? pictureField.current.value : null
            }
        );
    }

    return(
        <>
        <h1>Neues Haustier anlegen</h1>
        <div className="detail shadow">
            <Form onSubmit={onSubmit} encType="multipart/form-data">
                <label htmlFor="name">Name</label>
                <input type="text" name="Name" id="name" required />
                <label htmlFor="pet_description">Beschreibung</label>
                <input type="text" name="Beschreibung" id="pet_description" required />
                <label htmlFor="animal_type">Tierart</label>
                <select name="Tierart" id="animal_type">
                    {animalTypes?.map(animalType => (<option value={animalType.animalTypeId}>{animalType.animalType}</option>))}
                </select>
                <label htmlFor="image">Foto-Upload</label>
                <input name="image" id="image" type="file" />
                <input className="button" type="submit" value="Tier anlegen" />
            </Form>
        </div>
        </>
    );
};