import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "./App.scss";
import Auth from "./Auth";
import { SetAuth } from "./redux/auth/authActions";
import Router from "./router/router";
import { validateToken } from "./utils/token";

const App = () => {
    const dispatch = useDispatch();
    const location = useLocation();
    const isAuth = useSelector((state: any) => state.AuthReducer.isAuth);

    useEffect(() => {
        const checkToken = async () => {
            const isTokenValid = await validateToken();

            dispatch(SetAuth(isTokenValid));
        };

        checkToken();
    }, [location.hash, location.pathname, location.search]);

    return (
        <div className="App">
            {!isAuth ? <Auth /> : <Router />}

            <ToastContainer draggable limit={2} theme="dark" />
        </div>
    );
};

export default App;
