import { Box } from "@chakra-ui/react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useColorMode, useMediaQuery } from "@chakra-ui/react";
import { Footer, Navbar, Sidebar } from "./components";
import { HomePage, AutoPredictPage } from "./pages";
import "./assets/fpl-bg.jpg";


function App() {
  const [isNotPhoneScreen] = useMediaQuery("(min-width: 500px)");
  const { colorMode, toggleColorMode } = useColorMode();
  const isDark = colorMode === "dark";
  return (
    <Router>
      <Box
        bgGradient={
          isDark
            ? "linear(to-r, gray.900, cyan.900,gray.800, blue.900, green.900, gray.900)"
            : "linear(to-r, cyan.400, blue.500, green.600, green.800)"
        }
        h="100vh"
        w={"100%"}
        position={"relative"}
        overflowY={"auto"}
        overflowX={"revert"}
      >
        <Navbar />
        <Sidebar />
        <main style={{ position: "relative" }}>
          <Routes>
            <Route element={<HomePage isDark={isDark}/>} path="/" exact />
            <Route element={<AutoPredictPage isDark={isDark} />} path="/auto_predict" />
          </Routes>
        </main>
        <Footer />
      </Box>
    </Router>
  );
}

export default App;
