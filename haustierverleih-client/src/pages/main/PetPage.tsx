import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useApi } from "../../contexts/ApiProvider";
import type { Pet } from "../../Schemas";

interface PetPageProps {
    currentUser:{
        userId:number
    }
};

export default function PetPage({currentUser}:PetPageProps){
    const { petId } = useParams<{ petId: string }>();
    const api = useApi();
    const [pet, setPet] = useState<Pet | null | undefined>();

    useEffect(()=>{
        (async () => {
            const response = await api.get<Pet>("/pets/"+petId);
            if (response.ok && response.body) {
                setPet(response.body)
            } else {
                setPet(null);
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
                    <a href="/">zurück</a>
                    <h2>{ pet.name }</h2>
                    <div className="detail shadow">
                        <img src={pet.image ?pet.image:"/logo-thumbnail.png"} alt={pet.name} />
                        <div className="detail-info">
                            <div className="description">{ pet.description }</div>
                            <div>Besitzer: {pet.ownerId}</div> {/*{ pet.owned }*/}
                            <div>Tierart: {pet.animalTypeId}</div> {/*{ pet.animal_type }*/}
                            {currentUser.userId === pet.ownerId?
                                <a className="button shadow" href="{{ url_for('main.get_edit_pet', pet_id=pet.pet_id) }}">Tier bearbeiten</a>
                                :
                                <>
                                {pet.borrowerId === null?
                                    <a className="button shadow" href="{{ url_for('main.borrow_pet', pet_id=pet.pet_id) }}">Tier ausleihen</a>
                                    :
                                    <>
                                    {currentUser.userId === pet.borrowerId &&
                                        <a className="button shadow" href="{{ url_for('main.return_pet', pet_id=pet.pet_id) }}">Tier zurückgeben</a>
                                    }
                                    </>
                                }
                                </>
                            }
                        </div>
                    </div>
                </>
            }
            </>

        }
        </>
    );
};
