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