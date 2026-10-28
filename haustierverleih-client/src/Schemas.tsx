export type Link = {
    name: string;
    href:string;
}

export type Me = {
    userId: number;
    username: string;
    links: Link[];
}

export type animalType ={
    animalTypeId: number;
    animalType: string;
}