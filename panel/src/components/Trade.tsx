"use client";
import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import Sidebar from "../Sidebar";
import { generateUrl } from "../utils/generateUrl";

type Endpoints = {
    getUrl: string;
    changeUrl: string;
};

type EditorProps = {
    endpoints: Endpoints;
};

const Trade = ({ endpoints }: EditorProps) => {
    const navigate = useNavigate();
    const sendButton = useRef<HTMLButtonElement>(null);
    const [initialValues, setInitialValues] = useState<any>({
        partner: "",
        token: "",
    });

    useEffect(() => {
        const getInitialValues = async () => {
            const onError = () => {
                navigate("/");
                toast.error(`Не удалось получить данные про объект`);
            };

            try {
                const response = await axios.get(generateUrl(endpoints.getUrl));

                const targetValue = response.data;

                Object.keys(targetValue).map((key) => {
                    if (typeof targetValue[key] === "string") {
                        targetValue[key] = targetValue[key]
                            .replace(
                                /[\u180C\u180E\u200B\u200C\u200D\u2060\ufeff\u3000]+/g,
                                " "
                            )
                            .trim();
                    }
                });

                setInitialValues(targetValue);
            } catch {
                onError();
            }
        };

        getInitialValues();
    }, [endpoints]);

    const { register, handleSubmit } = useForm<any>({
        values: initialValues,
    });

    const sendData = (data: any) => {
        const pushedData = { ...data };
        if (pushedData.player_level !== undefined) {
            pushedData.player_level = parseInt(pushedData.player_level || "0");
        }

        Object.keys(initialValues).forEach((key) => {
            if (typeof pushedData[key] === "string") {
                pushedData[key] = pushedData[key].trim();
            }

            if (initialValues[key] === pushedData[key]) {
                delete pushedData[key];
                return;
            }
        });

        if (JSON.stringify(pushedData) === "{}") return;

        if (sendButton.current) sendButton.current.disabled = true;

        const request = axios
            .put(generateUrl(endpoints.changeUrl), pushedData)
            .then((res) => {
                const targetValue = res.data;

                Object.keys(targetValue).forEach((key) => {
                    if (typeof targetValue[key] !== "string") return;
                    targetValue[key] = targetValue[key].trim();
                });

                setInitialValues(targetValue);
            })
            .finally(() => {
                if (sendButton.current) sendButton.current.disabled = false;
            });

        toast.promise(request, {
            pending: "Сохраняем изменения...",
            success: "Изменения сохранены ✅",
            error: "Не удалось сохранить изменения 😢",
        });
    };

    return (
        <div className="container">
            <Sidebar />
            <div className="html-editor">
                <label key={"partner"}>
                    <span>Partner ID</span>

                    <input
                        {...register("partner")}
                        placeholder={"Partner ID"}
                    />
                </label>

                <label key={"token"}>
                    <span>Токен</span>

                    <input {...register("token")} placeholder={"Токен"} />
                </label>

                <div className="buttons-container">
                    <button
                        className="button save"
                        ref={sendButton}
                        onClick={handleSubmit(sendData)}
                    >
                        Сохранить ⬇️
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Trade;
