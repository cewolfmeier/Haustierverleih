import Header from "./components/Header";
import Footer from "./components/Footer";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import IndexPage from "./pages/IndexPage";

function App() {
  return (
    <div className="content">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<IndexPage />} />
        </Routes>
        <Footer/>
      </BrowserRouter>
    </div>
  )
}

export default App
