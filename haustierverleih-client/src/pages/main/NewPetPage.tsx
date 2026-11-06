import { useEffect, useState } from "react";
import { useApi } from "../../contexts/ApiProvider";
import type { AnimalType, NewPet, Pet } from "../../Schemas";
import { Form } from "react-bootstrap";

export default function NewPetPage(){
    const api = useApi();
    const [animalTypes, setAnimalTypes] = useState<AnimalType[] | null | undefined>();

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
        const formData = new FormData(event.target);
        await api.post<FormData, Pet>("/pets", formData,
        {
          'Content-Type': 'multipart/form-data',
        });
    }

    return(
        <>
        <h1>Neues Haustier anlegen</h1>
        <div className="detail shadow">
            <Form onSubmit={onSubmit} encType="multipart/form-data">
                <label htmlFor="name">Name</label>
                <input type="text" name="name" id="name" required />
                <label htmlFor="description">Beschreibung</label>
                <input type="text" name="description" id="description" required />
                <label htmlFor="animalType">Tierart</label>
                <select name="animalType" id="animalType">
                    {animalTypes?.map(animalType => (<option key={animalType.animalTypeId} value={animalType.animalTypeId}>{animalType.animalType}</option>))}
                </select>
                <label htmlFor="image">Foto-Upload</label>
                <input name="image" id="image" type="file" />
                <input className="button" type="submit" value="Tier anlegen" />
            </Form>
        </div>
        </>
    );
};