import { useState, useEffect } from "react";

export default function Crud() {
  const [users, setUsers] = useState([]);

  const [edit, setEdit] = useState(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    const res = await fetch("http://127.0.0.1:8000/u1/user/");
    const data = await res.json();
    setUsers(data);
  }

  function editUser(user) {
    setEdit(user.name);

    setName(user.name);
    setEmail(user.email);

    // Don't show hashed password
    setPassword("");

    setRole(user.role);
  }

  async function updateUser(e) {
    e.preventDefault();

    const updatedUser = {
      name,
      email,
      password,
      role,
    };

    const res = await fetch(
      `http://127.0.0.1:8000/u1/user/${edit}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedUser),
      }
    );

    if (res.ok) {
      alert("User Updated");
      loadUsers();
      clearForm();
    } else {
      alert("Update Failed");
    }
  }

  async function deleteUser(name) {
    if (!window.confirm("Delete this user?")) return;

    const res = await fetch(
      `http://127.0.0.1:8000/u1/user/${name}`,
      {
        method: "DELETE",
      }
    );

    if (res.ok) {
      alert("User Deleted");
      loadUsers();

      if (edit === name) {
        clearForm();
      }
    }
  }

  function clearForm() {
    setEdit(null);
    setName("");
    setEmail("");
    setPassword("");
    setRole("");
  }

  return (
    <>
      <h2>User Management</h2>

      {edit && (
        <form onSubmit={updateUser}>
          <h3>Edit User</h3>

          <input
            type="text"
            value={name}
            readOnly
            placeholder="Name"
          />

          <br />
          <br />

          <input
            type="email"
            value={email}
            readOnly
            placeholder="Email"
          />

          <br />
          <br />

          <input
            type="password"
            placeholder="New Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <br />
          <br />

          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="guest">Guest</option>
            <option value="admin">Admin</option>
          </select>

          <br />
          <br />

          <button type="submit">Update</button>

          <button
            type="button"
            onClick={clearForm}
            style={{ marginLeft: "10px" }}
          >
            Cancel
          </button>
        </form>
      )}

      <br />

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Password</th>
            <th>Email</th>
            <th>Role</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.name}</td>
              <td>{u.password}</td>
              <td>{u.email}</td>
              <td>{u.role}</td>

              <td>
                <button onClick={() => editUser(u)}>
                  Edit
                </button>

                <button
                  onClick={() => deleteUser(u.name)}
                  style={{ marginLeft: "10px" }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}