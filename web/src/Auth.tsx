import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "react-toastify";
import { SetAuth } from "./redux/auth/authActions";
import { LoginData, loginUser } from "./utils/user";

const Auth = () => {
    const dispatch = useDispatch();
    const [sentData, setSentData] = useState<any>({});
    const buttonRef = useRef<any>();

    const initialValues = {
        email: "",
        password: "",
    };

    const { register, handleSubmit } = useForm({ values: initialValues });

    const fields = [
        {
            label: "Email",
            name: "email",
        },
        {
            label: "Пароль",
            name: "password",
        },
    ];

    const handleData = (data: LoginData) => {
        const isDataValid =
            data.email &&
            data.password &&
            JSON.stringify(sentData || {}) !== JSON.stringify(data);
        setSentData(data);

        if (!isDataValid) return toast.error("Введите корректные данные");

        buttonRef.current.disabled = true;
        loginUser(data, {
            success: () => dispatch(SetAuth(true)),

            fail: (err) =>
                toast.error(
                    err?.response?.data?.error || "Что-то пошло не так"
                ),
            final: () => (buttonRef.current.disabled = false),
        });
    };

    return (
        <div className="auth-modal">
            {fields &&
                fields.length > 0 &&
                fields.map((field: any) => (
                    <input
                        {...register(field.name)}
                        placeholder={field.label}
                    />
                ))}
            <button
                className="button"
                ref={buttonRef}
                onClick={handleSubmit(handleData)}
            >
                Войти
            </button>
        </div>
    );
};

export default Auth;
