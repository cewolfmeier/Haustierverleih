import { usePetsApiCall } from "../../hooks/ApiHooks";
import Pet from "../../components/Pet";

export default function IndexPage(){
    const pets = usePetsApiCall()
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
                            pets.map(pet => <Pet key={pet.petId} props={pet} />)
                        }
                        </>
                    }
                    </>
                }
            </ul>
        </>
    );
};