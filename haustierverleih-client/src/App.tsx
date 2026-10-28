import Header from "./components/Header";
import Footer from "./components/Footer";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import IndexPage from "./pages/main/IndexPage";
import FlashProvider from "./contexts/FlashProvider";
import ApiProvider from "./contexts/ApiProvider";

function App() {
  return (
    <div className="content">
      <BrowserRouter>
        <FlashProvider>
          <ApiProvider>
            <Header />
            <Routes>
              <Route path="/" element={<IndexPage />} />
            </Routes>
            <Footer/>
          </ApiProvider>
        </FlashProvider>
      </BrowserRouter>
    </div>
  )
}

export default App
