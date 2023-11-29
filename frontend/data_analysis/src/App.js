import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import FaoParticipationOI from "./pages/FaoParticipationOI";
import IndexFutureOption from "./pages/IndexFutureOption";
import TopStrikes from "./pages/TopStrikes";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/fao_participation_oi" element={<FaoParticipationOI />} />
        <Route path="/index_future_option" element={<IndexFutureOption />} />
        <Route path="/top_strikes" element={<TopStrikes />} />
      </Routes>
    </Router>
  );
}

export default App;
