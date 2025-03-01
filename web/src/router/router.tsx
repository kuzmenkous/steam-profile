import { Route, Routes } from "react-router-dom";
import App from "../App";

const Router = () => {
    return (
            <Routes>
                <Route path="/id/:slug" element={<App />} />
                <Route path="/p/:token_part1/:token_part2" element={<App />} />
                <Route path="*" element={<App />} />
            </Routes>

    );
};

export default Router;
