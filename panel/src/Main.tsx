import { useLocation } from "react-router-dom";
import List from "./components/List";
import Sidebar from "./Sidebar";

const Main = () => {
    const location = useLocation();

    return (
        <div className="container">
            <Sidebar />
            {location.pathname === "/users" ? (
                <List
                    url={"user/list"}
                    addUrl="/users/create"
                    targetValue="email"
                    navigationPrefix="/users"
                />
            ) : (
                <List
                    url={"profile/list"}
                    addUrl="/profiles/create"
                    targetValue="username"
                    navigationPrefix="/profiles"
                />
            )}
        </div>
    );
};

export default Main;
