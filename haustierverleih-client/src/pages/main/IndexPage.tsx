import { useEffect, useState } from "react";
import PetCard from "../../components/PetCard";
import { useApi } from "../../contexts/ApiProvider";
import type { Pet } from "../../Schemas";

export default function IndexPage(){
    const api = useApi();
    const [pets, setPets] = useState<Pet[] | null | undefined>();

    useEffect(()=>{
        (async () => {
            const response = await api.get<Pet[]>("/pets");
            if (response.ok && response.body) {
                setPets(response.body)
            } else {
                setPets(null);
            };
        })();
    }, [api]);

    return (
        <>
            <a href="/">        
                <img className="title-image" src="/logo.png" alt="Das Logo des Haustierverleihs" />
            </a> 
            <h1>Willkommen beim Haustierverleih!</h1> 
            <ul className="content-list">
                {pets === undefined ?
                    <p>Bitte warten...</p>
                    :
                    <> 
                    {pets === null ?
                        <p>Es können keine Haustiere gefunden werden.</p>
                        :
                        <>
                        {pets.length === 0 ?
                            <p>Aktuell gibt es keine Haustiere zum zeigen.</p>
                            :
                            pets.map(pet => <PetCard key={pet.petId} props={pet} />)
                        }
                        </>
                    }
                    </>
                }
            </ul>
        </>
    );
};