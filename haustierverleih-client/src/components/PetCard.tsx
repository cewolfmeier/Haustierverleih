interface PetCardProps {
    props: {
        petId: number,
        name:string,
        description: string,
        image: string,
        animalTypeId: number,
        ownerId: number,
        borrowerId: number|null,
    };
};

export default function PetCard({props}:PetCardProps){
    return (
        <a href="/"> {/* {{url_for('main.pet', pet_id=pet.pet_id)}}*/}
        <li className="shadow">
            <img className="thumbnail" src={props.image ?props.image:"/logo-thumbnail.png"} />
            <div>
                <h2>{ props.name } { props.animalTypeId }</h2> {/* pet.animal_type.animal_type */}
                {props.borrowerId === null ?
                    <div className="badge success shadow">Aktuell verfügbar</div>
                    :
                    <div className="badge dark shadow">Nicht verfügbar</div>
                }
            </div>
            <div>
                <div className="description">{ props.description }</div>
                <div>{ props.name } gehört { props.ownerId }</div> {/* pet.owned*/}
            </div>
        </li>
        </a>      
    );
};