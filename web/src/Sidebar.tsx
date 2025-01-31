import { useNavigate } from "react-router-dom";

const Sidebar = () => {
    const navigate = useNavigate();
    return (
        <div className="sidebar">
            <button className="button" onClick={() => navigate("/profiles")}>
                Профили
            </button>
            <button className="button" onClick={() => navigate("/users")}>
                Пользователи
            </button>
        </div>
    );
};

export default Sidebar;
