import React, { useState } from "react";
import { useNavigate} from "react-router-dom";


export default function Login() {
  const [Username, setUsername] = useState("");
  const [Password, setPassword] = useState("");

  const navigate = useNavigate();

  async function handlelogin(e) {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", Username);
    formData.append("password", Password);

    try {
      const res = await fetch("http://127.0.0.1:8000/u1/user/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("token", data.access_token);

        const token = localStorage.getItem("token");
        console.log("Token from localStorage:",token);
        const profile =await fetch("http://127.0.0.1:8000/u1/user/profile",{
            method:"GET",
            headers:{
                Authorization:`Bearer ${token}`
            },
        });
        const profileData = await profile.json();
        console.log("Profile Data:", profileData);

        alert("Login Successful");

        // navigate("/Dashboard");
         navigate("/Crud");
        
        console.log("Bearer Token:");
        console.log(data.access_token);
      } else {
        alert(data.detail);
      }
    } catch (error) {
      console.log(error);
      alert("Server Error");
    }
  }

  return (
    <>
      <h2>Login</h2>

      <form onSubmit={handlelogin}>
        <input
          type="text"
          placeholder="Username"
          value={Username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={Password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br />
        <br />

        <button type="submit">Login</button>
      </form>
    </>
  );
}