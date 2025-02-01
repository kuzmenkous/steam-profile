import { Route, Routes } from "react-router-dom";
import Main from "../Main";
import Create from "../components/Create";
import Editor from "../components/Editor";

const profilesFields = [
    {
        label: "Название шаблона",
        name: "template_username",
        placeholder: "Шаблон №1",
    },
    {
        label: "Аватарка",
        name: "avatar_url",
        placeholder: "https://avatar.com/...",
    },
    {
        label: "Рамка",
        name: "avatar_frame_url",
        placeholder: "https://frame.com/...",
    },
    {
        label: "Steam ID пользователя",
        name: "steam_id",
        placeholder: "1111111111111",
    },
    { label: "Никнейм", name: "username", placeholder: "CSKiller336" },
    { label: "Описание", name: "description", placeholder: "Описание" },
    {
        label: "Местоположение",
        name: "location",
        placeholder: "Romania, Bucharest",
    },
    {
        label: "Флаг",
        name: "location_flag_url",
        placeholder: "Символы: en, us, de...",
    },
    {
        label: "Уровень в профиле",
        name: "player_level",
        placeholder: "10",
    },
    {
        label: "Тип ссылки",
        name: "link_type",
    },
    {
        label: "Активная страница",
        name: "is_active",
    },
    {
        label: "Ссылка",
        name: "slug",
        locked: true,
    },
];

const profilesCreateFields = [
    {
        label: "Название шаблона",
        name: "template_username",
        placeholder: "Шаблон №1",
        required: true,
    },
    {
        label: "Steam ID пользователя",
        name: "steam_id",
        placeholder: "1111111111111",
        required: true,
    },
    {
        label: "Ссылка на профиль Steam",
        name: "steam_link",
        placeholder: "https://steam...",
        required: true,
    },
    {
        label: "Тип ссылки",
        name: "link_type",
        required: true,
    },
];

const profileDefaultValues = {
    template_username: "",
    avatar_url: "",
    avatar_frame_url: "",
    steam_id: "",
    username: "",
    description: "",
    location: "",
    location_flag_url: "",
    player_level: 0,
    link_type: "",
    is_active: true,
    slug: "",
};

const userFields = [
    {
        label: "Email",
        name: "email",
        placeholder: "example@gmail.com",
    },
    {
        label: "Пароль",
        name: "password",
        placeholder: "123456789",
    },
    {
        label: "Активный пользователь",
        name: "is_active",
    },
];

const userCreateFields = [
    {
        label: "Email",
        name: "email",
        placeholder: "example@gmail.com",
        required: true,
    },
    {
        label: "Пароль",
        name: "password",
        placeholder: "123456789",
        required: true,
    },
];

const userDefaultValues = {
    email: "",
    password: "",
    is_active: true,
};

const Router = () => {
    return (
        <Routes>
            <Route path="*" element={<Main />} />
            <Route
                path="/profiles/:id"
                element={
                    <Editor
                        endpoints={{
                            getUrl: "profile/get/by_id",
                            changeUrl: "profile/update",
                            deleteUrl: "profile/delete",
                        }}
                        fields={profilesFields}
                        defaultValues={profileDefaultValues}
                        returnLink="/"
                    />
                }
            />
            <Route
                path="/users/:id"
                element={
                    <Editor
                        endpoints={{
                            getUrl: "user/get",
                            changeUrl: "user/update",
                            deleteUrl: "user/delete",
                        }}
                        fields={userFields}
                        defaultValues={userDefaultValues}
                        returnLink="/users"
                    />
                }
            />
            <Route
                path="/users/create"
                element={
                    <Create
                        createUrl="user/create"
                        fields={userCreateFields}
                        returnLink="/users"
                    />
                }
            />
            <Route
                path="/profiles/create"
                element={
                    <Create
                        createUrl="profile/create"
                        fields={profilesCreateFields}
                        returnLink="/"
                    />
                }
            />
        </Routes>
    );
};

export default Router;
