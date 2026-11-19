import Header from "./components/Header";
import Footer from "./components/Footer";
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import IndexPage from "./pages/main/IndexPage";
import FlashProvider from "./contexts/FlashProvider";
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
import PrivateRoute from "./components/PrivateRoute";
import UserProvider from "./contexts/UserProvider";
import { Container } from "react-bootstrap";
import ProtectedRoute from "./components/ProtectedRoute";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient()

function App() {
  return (
    <Container className="content">
      <BrowserRouter>
        <FlashProvider>
          <QueryClientProvider client={queryClient}>
            <UserProvider>
              <Header />
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/" element={<IndexPage />} />
              <Route path="*" element={
                <PrivateRoute>
                  <Routes>
                    <Route path="/me/edit" element={<EditUserPage />} />
                    <Route path="/mypets" element={<PetManagementPage />} />
                    <Route path="/mypets/:petId/edit" element={<EditPetPage />} />
                    <Route path="/mypets/new" element={<NewPetPage />} />
                    <Route path="/mypets/:petId" element={<PetPage />} />
                    <Route path="*" element={<Navigate to="/"/>}/>
                  </Routes>
                  <ProtectedRoute>
                    <Routes>
                      <Route path="/admin" element={<AdminPage />} />
                      <Route path="/admin/animaltypes/:animalTypeId/edit" element={<EditAnimalTypePage />} />
                      <Route path="/admin/animaltypes/new" element={<NewAnimalTypePage />} />
                      <Route path="/admin/users/:userId/edit" element={<EditUserPage />} />
                    </Routes>
                  </ProtectedRoute>
                </PrivateRoute>
              } />
              </Routes>
              <Footer/>
            </UserProvider>
          </QueryClientProvider>
        </FlashProvider>
      </BrowserRouter>
    </Container>
  )
}

export default App
