import PetCard from "../../components/PetCard";
import { useQuery } from "@tanstack/react-query";
import { petsQueries } from "../../services/pets/queries";


export default function IndexPage(){
    const { data:pets, error, isFetching } = useQuery(petsQueries.list())
    return (
        <>
            <a href="/">        
                <img className="title-image" src="/logo.png" alt="Das Logo des Haustierverleihs" />
            </a> 
            <h1>Willkommen beim Haustierverleih!</h1> 
            <ul className="content-list">
                {isFetching || pets === undefined?
                    <p>Bitte warten...</p>
                    :
                    <> 
                    {pets === null || error?
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