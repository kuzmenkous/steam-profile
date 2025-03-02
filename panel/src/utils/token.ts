import axios from "axios";
import { generateUrl } from "./generateUrl";

const token = "STEAM_FAKER_DS2XG102O_TOKEN";
const refreshToken = "STEAM_FAKER_DS2XG102O_REFRESH_TOKEN";

export const getToken = () => {
    const storageToken = localStorage.getItem(token);
    return storageToken ? `Bearer ${storageToken}` : false;
};

export const getRefreshToken = () => {
    const storageRefreshToken = localStorage.getItem(refreshToken);
    return storageRefreshToken ? `Bearer ${storageRefreshToken}` : false;
};

export const setToken = (newToken: string) => {
    localStorage.setItem(token, newToken);
    return `Bearer ${newToken}`;
};

export const setRefreshToken = (newRefreshToken: string) => {
    localStorage.setItem(refreshToken, newRefreshToken);
    return `Bearer ${newRefreshToken}`;
};

export const validateToken = async (success?: () => any, fail?: () => any) => {
    const token = getToken();

    const isValid = async (token: string, refresh?: boolean) => {
        return await axios
            .post(
                generateUrl(`user/token/is_valid?refresh=${refresh || false}`),
                {
                    token,
                    user_role: "user",
                }
            )
            .then((res) => res.data || false)
            .catch(() => false);
    };

    const getNewToken = async () => {
        const refreshToken = getRefreshToken();

        if (!refreshToken) {
            if (fail) {
                fail();
            }
            return false;
        }

        const refreshTokenValid = await isValid(refreshToken, true);

        if (!refreshTokenValid) {
            if (fail) {
                fail();
            }

            return false;
        }

        return await axios
            .post(generateUrl("user/token/access_from_refresh"), {
                token: refreshToken,
                user_role: "user",
            })
            .then((res) => {
                setToken(res.data.access_token);

                if (success) {
                    success();
                }
                return true;
            })
            .catch(() => {
                if (fail) {
                    fail();
                }

                return false;
            });
    };

    if (!token) return await getNewToken();

    const isTokenValid = await isValid(token);

    if (!isTokenValid) return await getNewToken();

    if (success) {
        success();
    }

    return true;
};
