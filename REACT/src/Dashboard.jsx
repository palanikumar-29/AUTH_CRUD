import { useEffect, useState } from "react";

export default function Dashboard() {
    const [profile, setProfile] = useState({});

    useEffect(() => {
        const getProfile = async () => {
            const token = localStorage.getItem("token");

            const res = await fetch("http://127.0.0.1:8000/u1/user/profile", {
                headers: {
                    Authorization: `bearer ${token}`
                },
            }
            );
            const data = await res.json();
            setProfile(data);

        }
        getProfile();
    },[]);

    return (
        <div>
            <h1>Dashboard</h1>
            <br />
            <p>ID :{profile.id}</p>
            <p>Name: {profile.name}</p>
            <p>Role : {profile.role}</p>
        </div>
    );

}