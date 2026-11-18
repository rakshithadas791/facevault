import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Recognize from "./pages/Recognize";
import History from "./pages/History";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/recognize" element={<Recognize />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}
