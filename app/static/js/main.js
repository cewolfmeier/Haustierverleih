//import { deletePet } from "./modules/pet.js";

async function deletePet() {
    const petId = this.id;
    console.log(petId);
    /*
    const deleteForm = document.createElement('form');
    const modal = document.getElementById('modal');
    */

    /*
    const contentBox = document.getElementById('anzeigenListe'); 
    const searchInput = document.getElementById('search');
    const searchValue = searchInput.value;
    */
    if (petId !== null){
        try {
            const response = await fetch(`/pet/${petId}/delete`);
            if (!response.ok) {
                throw new Error(`Ein Fehler ist aufgetreten: ${response.status}`); 
            }
            const data = await response.json();
            console.log(data);
            /*
            const cards = [];
            if (data.length > 0){
                
                for (let i=0; i< data.length; i++) {
                    cards.push(createCardElement(data[i]));
                }
                
            } else {
                const notFound = document.createElement('div');
                notFound.textContent = 'Deine Suche hat leider keine Ergebnisse geliefert.';
                cards.push(notFound);
            }
            contentBox.replaceChildren(...cards);
            */
        } catch (error) {
            console.error(error.message); // Wenn ein Fehler aufgetreten ist, wird er auf der Konsole ausgegeben 
        }
    }  
}

function main() {
    const deletePetButtons = document.querySelectorAll('.delete-pet');
    if (deletePetButtons !== null && deletePetButtons.length > 0) {
        for (let i=0; i < deletePetButtons.length; i++){
            deletePetButtons[i].addEventListener('click', this.deletePet);
        }
    }  
}

if (document.readyState === "loading") {
    // Dokument lädt noch
    document.addEventListener("DOMContentLoaded", main);
} else {
    // Dokument wurde schon geladen
    console.log('main!');
    main();
}
