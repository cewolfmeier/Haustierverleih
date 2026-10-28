export const useMeApiCall = () => {
    // /me
    return {
        userId: 1,
        username: "Testuser",
        links : [
            {
                name:"Admin-Bereich",
                href:"/", // /admin
            },
            {
                name:"Meine Tiere",
                href:"/", // me/pets
            },
        ]
    };
};

export const usePetsApiCall = () => {
    return [
        {petId: 1, name: "Hektor", description:"Mein Wauzi", image:"/logo.png", animalTypeId: 1, ownerId: 1, borrowerId:2},
        {petId: 1, name: "Bello", description:"Der bellt nicht, der beißt nur.", image:"/logo.png", animalTypeId: 1, ownerId: 1, borrowerId:null},
        {petId: 1, name: "Mietzekatze", description:"Etwas Katze muss sein.", image:"/logo.png", animalTypeId: 1, ownerId: 1, borrowerId:null},
    ];
};