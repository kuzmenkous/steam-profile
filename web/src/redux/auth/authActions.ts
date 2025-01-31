import { SET_AUTH } from "./authActionTypes";

export const SetAuth = (isAuth: boolean) => {
    return {
        type: SET_AUTH,
        payload: isAuth,
    };
};
