import { Form } from "react-bootstrap";
import { useApi } from "../../contexts/ApiProvider";
import { useRef } from "react";
import type { AnimalType, NewAnimalType } from "../../Schemas";

export default function NewAnimalTypePage(){
    const api = useApi();
    const animalTypeField = useRef<HTMLInputElement>(null);

    const onSubmit = async (event: React.SubmitEvent) => {
        event.preventDefault(); //Note: prevents a reload of the page so Formdata doesn't get lost
        await api.post<NewAnimalType, AnimalType>("/animaltypes", 
            {
                animalType: animalTypeField.current ? animalTypeField.current.value : "",
            }
        );
    }

    return(
        <Form onSubmit={onSubmit}>
            <h1>Neue Tierart anlegen</h1>
            <label htmlFor="name">Bezeichnung</label>
            <input type="text" name="name" id="name" required ref={animalTypeField}/>
            <input className="button-form" type="submit" value="Tierart anlegen" />
        </Form>
    );
};