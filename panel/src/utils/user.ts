import axios from "axios";
import { generateUrl } from "./generateUrl";
import { setRefreshToken, setToken } from "./token";

export type LoginData = {
    email: string;
    password: string;
};

type callbacks = {
    success?: (res: any) => any;
    fail?: (error: any) => any;
    final?: () => any;
};

export const loginUser = async (data: LoginData, callbacks?: callbacks) => {
    await axios
        .post(generateUrl("user/login"), data)
        .then((res: any) => {
            setToken(res.data.access_token);
            setRefreshToken(res.data.refresh_token);

            if (callbacks?.success) {
                callbacks.success(res);
            }
        })
        .catch((err: any) => {
            if (callbacks?.fail) {
                callbacks.fail(err);
            }
        })
        .finally(() => {
            if (callbacks?.final) {
                callbacks.final();
            }
        });
};

export const logOut = (success?: () => any) => {
    setToken("");
    setRefreshToken("");

    if (success) {
        success();
    }
};
