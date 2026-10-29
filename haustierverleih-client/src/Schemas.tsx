export type Link = {
    name: string;
    href:string;
}

export type AnimalType ={
    animalTypeId: number;
    animalType: string;
}

export type Me = {
    userId: number;
    username: string;
    links: Link[];
}

export type Pet ={
    petId: number,
    name:string,
    description: string,
    image: string,
    animalTypeId: number,
    ownerId: number,
    borrowerId: number|null,
}

export type Role = {
    roleId: number;
    role: string;
}

export type User ={
    userId: number;
    username: string;
    roleId:Number;
}

export type NewAnimalType = {
    animalType: string;
}

export type NewPet = {
    name:string,
    description: string,
    image: string | null,
    animalTypeId: number | null,
}

export type NewUser = {
    username: string;
    password: string;
}