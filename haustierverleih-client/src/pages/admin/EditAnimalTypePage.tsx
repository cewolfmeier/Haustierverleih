import type { AnimalType } from "../../Schemas";

interface EditAnimalTypePageProps{
    animalType:AnimalType,
}

export default function EditAnimalTypePage({animalType}:EditAnimalTypePageProps){
    return(
        <>
            <h1>Tierart {animalType.animalType} bearbeiten</h1>
            <form action="{{url_for('admin.post_edit_animal_type', animal_type_id=animal_type['animal_type_id'])}}" method="put">
                <label htmlFor="animal_type">Bezeichnung</label>
                <input type="text" name="name" id="animal_type" value="{{ animal_type['animal_type']}}" required />
                <input className="button-form" type="submit" value="Speichern" />
            </form>
        </>
    );
};