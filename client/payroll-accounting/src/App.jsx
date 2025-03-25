import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Auth/Login/Login";
import Register from "./components/Auth/Register/Register";
import Dashboard from "./components/Dashboard/Dashboard";
import Upload from "./components/Dashboard/Upload";
import NotFound from "./components/404/NotFound";
// import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
// import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
function App() {
  return (
    <div>
      {/* <LocalizationProvider dateAdapter={AdapterDayjs}> */}
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
      {/* </LocalizationProvider> */}
    </div>
  );
}

export default App;
