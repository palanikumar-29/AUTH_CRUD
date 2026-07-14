import {BrowserRouter,Routes,Route} from "react-router-dom";
import Login from "./Login";
import Dashboard  from "./Dashboard";
import Crud from "./Crud";

export default function App(){
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login/>}/>
                <Route path="/Crud" element={<Crud/>}/>
            </Routes>
        </BrowserRouter>
    );
}