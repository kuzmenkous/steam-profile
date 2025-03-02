import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Sidebar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [currentWidth, setCurrentWidth] = useState(window.innerWidth);
    const sidebarRef = useRef<any>(null);
    const mobileButtonRef = useRef<any>(null);

    const toggleNavbar = (mode = "toggle") => {
        sidebarRef.current?.classList[mode]("active");
        mobileButtonRef.current?.classList[mode]("active");
    };

    useEffect(() => {
        window.addEventListener("resize", () => {
            setCurrentWidth(window.innerWidth);
        });
    }, []);

    useEffect(() => {
        toggleNavbar("remove");
    }, [location]);

    return (
        <>
            {currentWidth <= 780 && (
                <div
                    className="sidebar-mobile-button"
                    ref={mobileButtonRef}
                    onClick={() => toggleNavbar("toggle")}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                    >
                        <path
                            d="M4 4V20M8 12H20M20 12L16 8M20 12L16 16"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </div>
            )}
            <div className="sidebar" ref={sidebarRef}>
                <button
                    className="button"
                    onClick={() => navigate("/profiles")}
                >
                    Профили
                </button>
                <button className="button" onClick={() => navigate("/users")}>
                    Пользователи
                </button>
                <button className="button" onClick={() => navigate("/trade")}>
                    Страница трейда
                </button>
            </div>
        </>
    );
};

export default Sidebar;
