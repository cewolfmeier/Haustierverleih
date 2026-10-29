import Header from "./components/Header";
import Footer from "./components/Footer";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import IndexPage from "./pages/main/IndexPage";
import FlashProvider from "./contexts/FlashProvider";
import ApiProvider from "./contexts/ApiProvider";
import PetManagementPage from "./pages/main/PetManagementPage";
import EditPetPage from "./pages/main/EditPetPage";
import NewPetPage from "./pages/main/NewPetPage";
import PetPage from "./pages/main/PetPage";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import AdminPage from "./pages/admin/AdminPage";
import EditAnimalTypePage from "./pages/admin/EditAnimalTypePage";
import NewAnimalTypePage from "./pages/admin/NewAnimalTypePage";
import EditUserPage from "./pages/admin/EditUserPage";

function App() {
  return (
    <div className="content">
      <BrowserRouter>
        <FlashProvider>
          <ApiProvider>
            <Header />
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              <Route path="/" element={<IndexPage />} />
              <Route path="/me/edit" element={<EditUserPage />} />
              <Route path="/mypets" element={<PetManagementPage />} />
              <Route path="/mypets/:petId/edit" element={<EditPetPage />} />
              <Route path="/mypets/new" element={<NewPetPage />} />
              <Route path="/mypets/:petId" element={<PetPage />} />
              
              <Route path="/admin" element={<AdminPage />} />
              <Route path="/admin/animaltypes/:animalTypeId/edit" element={<EditAnimalTypePage />} />
              <Route path="/admin/animaltypes/new" element={<NewAnimalTypePage />} />
              <Route path="/admin/users/:userId/edit" element={<EditUserPage />} />
              
            </Routes>
            <Footer/>
          </ApiProvider>
        </FlashProvider>
      </BrowserRouter>
    </div>
  )
}

export default App
