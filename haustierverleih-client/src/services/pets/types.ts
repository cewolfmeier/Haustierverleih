export type Pet ={
    petId: number,
    name:string,
    description: string,
    image: string,
    animalTypeId: number,
    ownerId: number,
    borrowerId: number|null,
}