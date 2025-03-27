import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Auth/Login/Login";
import Register from "./components/Auth/Register/Register";
import Dashboard from "./components/Dashboard/Dashboard";
import Upload from "./components/Dashboard/Upload";
import NotFound from "./components/404/NotFound";
import ProfileSettings from "./components/ProfileSettings/ProfileSettings";
import Topbar from "./components/Dashboard/TopBar";

function App() {
  return (
    <BrowserRouter>
      {/* Topbar - immer sichtbar */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Topbar />
      </div>

      <div className="pt-16"> {/* Padding, um die Topbar nicht zu überdecken */}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/profilesettings" element={<ProfileSettings />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;