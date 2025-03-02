"use client";
import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import Sidebar from "../Sidebar";
import { generateUrl } from "../utils/generateUrl";

interface Field {
    label: string;
    name: string;
    placeholder?: string;
    locked?: boolean;
}

type Endpoints = {
    getUrl: string;
    changeUrl: string;
    deleteUrl: string;
};

type EditorProps = {
    endpoints: Endpoints;
    fields: Field[];
    defaultValues: Record<string, any>;
    returnLink: string;
};

const Editor = ({
    endpoints,
    fields,
    defaultValues,
    returnLink,
}: EditorProps) => {
    const navigate = useNavigate();
    const { id } = useParams();
    const sendButton = useRef<HTMLButtonElement>(null);
    const [initialValues, setInitialValues] = useState(defaultValues);
    const [generatingLink, setGeneratingLink] = useState(false);

    useEffect(() => {
        const getInitialValues = async () => {
            const onError = () => {
                navigate("/");
                toast.error(`Не удалось получить данные про объект`);
            };
            if (!id) return onError();

            try {
                const response = await axios.get(
                    generateUrl(`${endpoints.getUrl}/${id}`)
                );

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
    }, [id, endpoints]);

    const { register, handleSubmit, getValues, setValue, watch } = useForm<any>(
        {
            values: initialValues,
        }
    );

    const inviteLinkPath = watch("invite_link_path");
    const slug = watch("slug");

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
            .put(generateUrl(`${endpoints.changeUrl}/${id}`), pushedData)
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

    const deleteItem = (e: any) => {
        if (sendButton.current) sendButton.current.disabled = true;
        e.target.disabled = true;

        const request = axios
            .delete(generateUrl(`${endpoints.deleteUrl}/${id}`))
            .then(() => {
                navigate("/");
            })
            .finally(() => {
                if (sendButton.current) sendButton.current.disabled = false;
                e.target.disabled = false;
            });

        toast.promise(request, {
            pending: "Удаляем объект...",
            success: "Объект удален ✅",
            error: "Не удалось удалить объект 😢",
        });
    };

    const generateFiendInvite = async () => {
        if (generatingLink) return;

        setGeneratingLink(true);

        const request = axios
            .post(generateUrl(`profile/invite_link_path/generate/${id}`))
            .finally(() => setGeneratingLink(false));

        toast.promise(request, {
            pending: "Генерируем ссылку...",
            success: "Ссылка сгенерирована ✅",
            error: "Не удалось сгенерировать ссылку 😢",
        });

        const response = await request;

        if (response.data.invite_link_path)
            setValue("invite_link_path", response.data.invite_link_path);
    };

    useEffect(() => {
        const mainPart =
            process.env.REACT_APP_FRIEND_INVITE_LINK ||
            "http://localhost:3000/p/";
        if (inviteLinkPath && !inviteLinkPath.includes(mainPart))
            setValue("invite_link_path", `${mainPart}${inviteLinkPath}`);
    }, [inviteLinkPath]);

    useEffect(() => {
        const mainPart =
            process.env.REACT_APP_SLUG_LINK || "http://localhost:3000/id/";
        if (slug && !slug.includes(mainPart))
            setValue("slug", `${mainPart}${slug}`);
    }, [slug]);

    return (
        <div className="container">
            <Sidebar />
            <div className="html-editor">
                <div
                    className="leave-button"
                    onClick={() => navigate(`${returnLink}`)}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="none"
                    >
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M15.6666 8L17.75 10.5L15.6666 8Z"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M15.6666 13L17.75 10.5L15.6666 13Z"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                        <path
                            d="M16.5 10.5L10 10.5"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                        />
                        <line
                            x1="4"
                            y1="3.5"
                            x2="13"
                            y2="3.5"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                        />
                        <line
                            x1="4"
                            y1="17.5"
                            x2="13"
                            y2="17.5"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                        />
                        <path
                            d="M13 3.5V7.5"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                        />
                        <path
                            d="M13 13.5V17.5"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                        />
                        <path
                            d="M4 3.5L4 17.5"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                        />
                    </svg>
                </div>
                {fields.map((field) => (
                    <label key={field.name}>
                        <span>
                            {field.label}{" "}
                            {(field.name === "slug" ||
                                field.name === "invite_link_path") && (
                                <svg
                                    style={{ cursor: "pointer" }}
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20px"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    onClick={() => {
                                        navigator.clipboard.writeText(
                                            getValues()[field.name]
                                        );
                                        toast.success(
                                            "Вы скопировали ссылку ✅"
                                        );
                                    }}
                                >
                                    <path
                                        fillRule="evenodd"
                                        clipRule="evenodd"
                                        d="M19.5 16.5L19.5 4.5L18.75 3.75H9L8.25 4.5L8.25 7.5L5.25 7.5L4.5 8.25V20.25L5.25 21H15L15.75 20.25V17.25H18.75L19.5 16.5ZM15.75 15.75L15.75 8.25L15 7.5L9.75 7.5V5.25L18 5.25V15.75H15.75ZM6 9L14.25 9L14.25 19.5L6 19.5L6 9Z"
                                        fill="#fff"
                                    />
                                </svg>
                            )}
                        </span>
                        {field.name === "player_level" ? (
                            <input
                                {...register(field.name)}
                                type="text"
                                onInput={(e) => {
                                    e.currentTarget.value =
                                        e.currentTarget.value.replace(
                                            /\D/g,
                                            ""
                                        );
                                }}
                            />
                        ) : field.name === "is_active" ? (
                            <input {...register(field.name)} type="checkbox" />
                        ) : field.name === "link_type" ? (
                            <select {...register(field.name)}>
                                <option value="with_username">
                                    С никнеймом
                                </option>
                                <option value="with_steam_id">
                                    С Steam ID
                                </option>
                            </select>
                        ) : field.name === "invite_link_path" ? (
                            <>
                                <input
                                    {...register(field.name)}
                                    placeholder={
                                        field.placeholder || field.label
                                    }
                                    readOnly={true}
                                />

                                <button
                                    disabled={generatingLink}
                                    onClick={generateFiendInvite}
                                    className="button"
                                >
                                    Сгенерировать новую ссылку
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="currentColor"
                                        width="15px"
                                        viewBox="0 0 1920 1920"
                                    >
                                        <path
                                            d="M960 0v112.941c467.125 0 847.059 379.934 847.059 847.059 0 467.125-379.934 847.059-847.059 847.059-467.125 0-847.059-379.934-847.059-847.059 0-267.106 126.607-515.915 338.824-675.727v393.374h112.94V112.941H0v112.941h342.89C127.058 407.38 0 674.711 0 960c0 529.355 430.645 960 960 960s960-430.645 960-960S1489.355 0 960 0"
                                            fill-rule="evenodd"
                                        />
                                    </svg>
                                </button>
                            </>
                        ) : (
                            <input
                                {...register(field.name)}
                                placeholder={field.placeholder || field.label}
                                readOnly={field.locked || false}
                            />
                        )}
                    </label>
                ))}

                <div className="buttons-container">
                    <button
                        className="button save"
                        ref={sendButton}
                        onClick={handleSubmit(sendData)}
                    >
                        Сохранить ⬇️
                    </button>
                    <button className="button delete" onClick={deleteItem}>
                        Удалить ❌
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Editor;
