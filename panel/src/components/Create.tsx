"use client";
import axios from "axios";
import { useRef } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import Sidebar from "../Sidebar";
import { generateUrl } from "../utils/generateUrl";

const Create = ({ createUrl, fields, returnLink }: any) => {
    const navigate = useNavigate();
    const sendButton = useRef<any>(null);
    const { register, handleSubmit } = useForm();

    const sendData = async (data: any) => {
        let isError = false;
        const requiredFields = fields
            .filter((field: any) => field.required)
            .map((field: any) => field.name);

        requiredFields.forEach((name: string) => {
            const input: any = document.querySelector(`input[name="${name}"]`);
            if (!input) return;

            if (data[name]) return (input.style.borderColor = "#fff");

            isError = true;
            input.style.borderColor = "red";
        });

        if (isError) return toast.error("Введите все необходимые данные");

        await axios
            .post(generateUrl(createUrl), data)
            .then(() => {
                navigate(returnLink);
                toast.success("Пользователь был создан успешно ✅");
            })
            .catch(() =>
                toast.error(
                    "Не удалось создать профиль пользователя. Убедитесь, что все введенные данные верны 😢"
                )
            );
    };

    return (
        <div className="container">
            <Sidebar />
            <div className="html-editor">
                {fields.map((field: any) => (
                    <label key={field.name}>
                        <span>{field.label} </span>
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
                            <select
                                defaultValue={"with_username"}
                                {...register(field.name)}
                            >
                                <option value="with_username">
                                    С никнеймом
                                </option>
                                <option value="with_steam_id">
                                    С Steam ID
                                </option>
                            </select>
                        ) : (
                            <input
                                {...register(field.name)}
                                placeholder={field.placeholder || field.label}
                                readOnly={field.locked || false}
                            />
                        )}
                    </label>
                ))}
                <button
                    className="button save"
                    ref={sendButton}
                    onClick={handleSubmit(sendData)}
                >
                    Создать ➕
                </button>
            </div>
        </div>
    );
};

export default Create;
