import type { AnimalType } from "../../Schemas";

interface AnimalTypeRowProps{
    animalType:AnimalType
}

export default function AnimalTypeRow({animalType}:AnimalTypeRowProps){
    return(
        <tr>
            <td>{animalType.animalType}</td>
            <td>
                <a className="button" href="{{ url_for('admin.get_edit_animal_type', animal_type_id=type['animal_type_id']) }}">Bearbeiten</a>
            </td>
        </tr>
    );
};