export type Link = {
    name: string;
    href:string;
}

export type Me = {
    userId: number;
    username: string;
    links: Link[];
}

export type AnimalType ={
    animalTypeId: number;
    animalType: string;
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

export type User ={
    userId: number;
    username: string;
    roleId:Number;
}

export type NewUser = {
    username: string;
    password: string;
}

export type Role = {
    roleId: number;
    role: string;
}